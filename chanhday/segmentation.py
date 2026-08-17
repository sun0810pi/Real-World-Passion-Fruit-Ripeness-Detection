"""
Tách vùng quả khỏi nền và cắt theo hộp bao (mục 3.4.3, bước 2 và 3).

Vì sao bước này bắt buộc: ảnh gốc 6000x4000 nhưng quả chỉ chiếm khoảng 2%
diện tích. Đưa thẳng vào mô hình ở kích thước 224 thì quả chỉ còn khoảng
20 pixel — gần như toàn bộ độ phân giải bị lãng phí vào phông vải đen.
Sau khi cắt, quả chiếm trọn 224 pixel.
"""
from __future__ import annotations

import cv2
import numpy as np

from .config import CFG
from .cards import roi_mask


def segment_fruit(bgr: np.ndarray, exclude: np.ndarray | None = None,
                  min_area_frac: float | None = None) -> np.ndarray | None:
    """
    Trả mặt nạ nhị phân của quả, hoặc None nếu không tìm được.

    `exclude` là mặt nạ những vùng KHÔNG được coi là quả — bắt buộc truyền
    vùng thẻ vào, vì thẻ sáng hơn phông nên thuật toán có lúc chọn nhầm
    chính cái thẻ làm quả.
    """
    thr = CFG.thresholds
    min_area_frac = min_area_frac or thr.min_fruit_area_frac
    h, w = bgr.shape[:2]

    hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)
    V, S = hsv[:, :, 2], hsv[:, :, 1]

    _, mv = cv2.threshold(V, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    ms = (S > 40).astype(np.uint8) * 255
    m = cv2.bitwise_or(mv, ms)

    if exclude is not None:
        m[exclude.astype(bool)] = 0

    k = np.ones((7, 7), np.uint8)
    m = cv2.morphologyEx(m, cv2.MORPH_OPEN, k, iterations=2)
    m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, k, iterations=3)

    n, lab, stats, _ = cv2.connectedComponentsWithStats((m > 0).astype(np.uint8), 8)
    if n <= 1:
        return None

    for i in 1 + np.argsort(stats[1:, cv2.CC_STAT_AREA])[::-1]:
        area = stats[i, cv2.CC_STAT_AREA]
        if area < min_area_frac * h * w:
            break
        bw, bh = stats[i, cv2.CC_STAT_WIDTH], stats[i, cv2.CC_STAT_HEIGHT]
        # quả chanh dây gần tròn và đặc: loại các mảng dài (viền vải, thước)
        if 0.45 < bw / max(bh, 1) < 2.2 and area / (bw * bh) > 0.5:
            out = (lab == i).astype(np.uint8) * 255
            return cv2.morphologyEx(out, cv2.MORPH_CLOSE, np.ones((15, 15), np.uint8))
    return None


def crop_to_mask(bgr: np.ndarray, mask: np.ndarray,
                 pad: float | None = None, black_bg: bool = True):
    """Cắt theo hộp bao của mặt nạ, tùy chọn bôi đen phần ngoài quả."""
    pad = CFG.thresholds.crop_pad if pad is None else pad
    ys, xs = np.where(mask > 0)
    if len(xs) == 0:
        return None
    x0, x1, y0, y1 = xs.min(), xs.max(), ys.min(), ys.max()
    px, py = int((x1 - x0) * pad), int((y1 - y0) * pad)
    h, w = bgr.shape[:2]
    x0, x1 = max(0, x0 - px), min(w, x1 + px + 1)
    y0, y1 = max(0, y0 - py), min(h, y1 + py + 1)

    img = bgr.copy()
    if black_bg:
        img[mask == 0] = 0
    return img[y0:y1, x0:x1]


def process_one(bgr: np.ndarray, layout=None, black_bg: bool = True):
    """Tách nền + cắt trong một lần gọi. Trả (crop, mask) hoặc (None, None)."""
    layout = layout or CFG.layout
    exclude = roi_mask(bgr.shape, layout.card_roi)
    mask = segment_fruit(bgr, exclude)
    if mask is None:
        return None, None
    return crop_to_mask(bgr, mask, black_bg=black_bg), mask
