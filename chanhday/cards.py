"""
Thẻ chuẩn: phát hiện, đo ô xám, ước lượng và hiệu chỉnh nguồn sáng.

Bốn ô xám trong khung hình cho ta nhãn đúng của nguồn sáng ở từng ảnh.
Đây là nền tảng của cả bước tiền xử lý (mục 3.4.3) lẫn tầng ước lượng
môi trường (script 07).
"""
from __future__ import annotations

import cv2
import numpy as np

from .config import CFG, CardLayout

NEUTRAL = np.ones(3) / np.sqrt(3)


# ---------------------------------------------------------------------------
# Đo ô xám
# ---------------------------------------------------------------------------

def sample_gray_patches(bgr: np.ndarray, layout: CardLayout | None = None,
                        ceiling: int = 252) -> np.ndarray:
    """
    Giá trị BGR trung bình của từng ô xám. Trả mảng (n_patches, 3);
    ô không đọc được trả về NaN.

    Bỏ pixel có kênh vượt `ceiling` vì pixel cháy sáng đã mất thông tin màu,
    đưa vào sẽ kéo ước lượng nguồn sáng về phía trung tính một cách giả tạo.
    """
    layout = layout or CFG.layout
    out = []
    for x0, y0, x1, y1 in layout.patch_boxes(bgr.shape):
        px = bgr[y0:y1, x0:x1].reshape(-1, 3).astype(np.float64)
        px = px[(px < ceiling).all(axis=1)]
        out.append(px.mean(axis=0) if len(px) >= 10 else np.full(3, np.nan))
    return np.vstack(out)


def illuminant_from_patches(patches: np.ndarray) -> np.ndarray:
    """
    Nguồn sáng (B, G, R) chuẩn hóa, suy từ nhiều ô xám cùng lúc.

    Ô xám phản xạ trung tính nên mọi lệch giữa ba kênh là do nguồn sáng.
    Hồi quy qua gốc tọa độ trên toàn bộ ô ổn định hơn dùng một ô đơn lẻ,
    và tận dụng được cả các ô tối vốn ít bị cháy sáng.
    """
    p = patches[np.isfinite(patches).all(axis=1)]
    if len(p) == 0:
        return NEUTRAL.copy()
    g = p[:, 1]
    ill = np.array([float(np.dot(p[:, c], g) / (np.dot(g, g) + 1e-9)) for c in range(3)])
    ill[1] = 1.0
    n = np.linalg.norm(ill)
    return ill / n if n > 1e-9 else NEUTRAL.copy()


def linearity_check(patches: np.ndarray) -> dict:
    """
    Đáp ứng của máy ảnh có tuyến tính không?

    Nếu ảnh JPEG đã qua ánh xạ tông (gamma), quan hệ giữa các ô xám sẽ cong.
    Khi đó phép hiệu chỉnh von Kries chỉ đúng gần đúng, và nên chuyển sang
    dùng file RAW. Trả về R^2 của hồi quy tuyến tính giữa độ sáng các ô.
    """
    p = patches[np.isfinite(patches).all(axis=1)]
    if len(p) < 3:
        return {"r2": float("nan"), "n_o": int(len(p))}
    y = p.mean(axis=1)
    x = np.arange(len(y), dtype=float)
    A = np.vstack([x, np.ones_like(x)]).T
    coef, *_ = np.linalg.lstsq(A, y, rcond=None)
    resid = y - A @ coef
    ss_tot = ((y - y.mean()) ** 2).sum()
    r2 = 1 - (resid ** 2).sum() / ss_tot if ss_tot > 0 else float("nan")
    return {"r2": float(r2), "n_o": int(len(p))}


# ---------------------------------------------------------------------------
# Đường cơ sở không cần thẻ
# ---------------------------------------------------------------------------

def illuminant_gray_world(bgr: np.ndarray, p: float = 1.0,
                          ceiling: int = 252) -> np.ndarray:
    """
    p = 1   -> Gray-World
    p = 6   -> Shades-of-Gray
    p = inf -> Max-RGB

    Dùng làm đối chứng cho tầng ước lượng môi trường: mô hình CNN phải thắng
    được các phương pháp không học này thì mới đáng đưa vào báo cáo.
    """
    x = bgr.astype(np.float64).reshape(-1, 3)
    x = x[(x < ceiling).all(axis=1)]
    if len(x) == 0:
        return NEUTRAL.copy()
    ill = x.max(axis=0) if np.isinf(p) else np.mean(x ** p, axis=0) ** (1.0 / p)
    n = np.linalg.norm(ill)
    return ill / n if n > 1e-9 else NEUTRAL.copy()


def illuminant_gray_edge(bgr: np.ndarray, p: float = 1.0) -> np.ndarray:
    """Gray-Edge: giả định trung bình đạo hàm ảnh là trung tính."""
    g = cv2.GaussianBlur(bgr.astype(np.float64), (0, 0), 1.0)
    gx = cv2.Sobel(g, cv2.CV_64F, 1, 0, ksize=3)
    gy = cv2.Sobel(g, cv2.CV_64F, 0, 1, ksize=3)
    mag = np.sqrt(gx ** 2 + gy ** 2).reshape(-1, 3)
    ill = np.mean(mag ** p, axis=0) ** (1.0 / p)
    n = np.linalg.norm(ill)
    return ill / n if n > 1e-9 else NEUTRAL.copy()


# ---------------------------------------------------------------------------
# Hiệu chỉnh và đánh giá
# ---------------------------------------------------------------------------

def apply_von_kries(bgr: np.ndarray, ill: np.ndarray) -> np.ndarray:
    """Đưa ảnh về nguồn sáng trung tính bằng phép co giãn theo kênh."""
    ill = np.asarray(ill, float)
    ill = ill / (ill.mean() + 1e-9)     # giữ nguyên độ sáng tổng thể
    out = bgr.astype(np.float64) / ill[None, None, :]
    return np.clip(out, 0, 255).astype(np.uint8)


def angular_error(a, b=NEUTRAL) -> float:
    """Sai số góc giữa hai vector nguồn sáng, tính bằng độ."""
    a = np.asarray(a, float)
    b = np.asarray(b, float)
    na, nb = np.linalg.norm(a), np.linalg.norm(b)
    if na < 1e-9 or nb < 1e-9:
        return float("nan")
    return float(np.degrees(np.arccos(np.clip(a @ b / (na * nb), -1, 1))))


def summarize_errors(errs, ten: str) -> dict:
    """Bộ chỉ số chuẩn của bài toán color constancy."""
    e = np.asarray(errs, float)
    e = e[np.isfinite(e)]
    if len(e) == 0:
        return {"phuong_phap": ten, "n": 0}
    return {
        "phuong_phap": ten,
        "n": int(len(e)),
        "trung_binh": round(float(e.mean()), 3),
        "trung_vi": round(float(np.median(e)), 3),
        "tu_phan_vi_tot": round(float(e[e <= np.percentile(e, 25)].mean()), 3),
        "tu_phan_vi_xau": round(float(e[e >= np.percentile(e, 75)].mean()), 3),
        "p95": round(float(np.percentile(e, 95)), 3),
    }


def _bright_blobs(bgr: np.ndarray, v_pct: float = 88.0, s_max: int = 90,
                  min_area: int = 200):
    """Các mảng sáng, ít bão hòa màu — ứng viên cho ô xám và mảnh giấy."""
    hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)
    V, S = hsv[:, :, 2], hsv[:, :, 1]
    thr = max(int(np.percentile(V, v_pct)), 90)
    m = ((V >= thr) & (S <= s_max)).astype(np.uint8)
    m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8))
    m = cv2.morphologyEx(m, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))

    n, lab, stats, _ = cv2.connectedComponentsWithStats(m, 8)
    out = []
    for i in range(1, n):
        x, y, w, h, a = stats[i]
        if a < min_area:
            continue
        out.append({"x": int(x), "y": int(y), "w": int(w), "h": int(h),
                    "area": int(a), "fill": a / max(w * h, 1)})
    return out


def _edge_density(gray: np.ndarray) -> float:
    """
    Mật độ biên trong một vùng ảnh.

    Đây là tiêu chí phân biệt then chốt giữa dải ô xám và mảnh giấy ghi mã:
    trên dải ô xám luôn có mã QR, mà mã QR gồm rất nhiều ô vuông đen trắng
    nên mật độ biên cao gấp khoảng năm lần chữ viết tay trên giấy trắng.
    Đo trên bộ ảnh Canon: dải ô xám 7,7%, mảnh giấy 1,5%.

    Tiêu chí này bền hơn màu sắc, vì ám màu của nguồn sáng làm mọi vùng
    trong ảnh đều nhuốm màu và độ bão hòa không còn phân biệt được gì.
    """
    if gray.size == 0:
        return 1.0
    return float(cv2.Canny(gray, 60, 160).mean() / 255.0)


def detect_tag(bgr: np.ndarray, layout: CardLayout | None = None,
               max_edge_density: float = 0.08):
    """
    Tự dò vị trí mảnh giấy ghi mã quả. Trả (x, y, w, h) theo pixel, hoặc None.

    Vì sao cần dò tự động thay vì dùng một hình chữ nhật cố định: khoảng cách
    chụp và bố cục thay đổi giữa các đợt, nên một toạ độ cố định sẽ cắt trúng
    quả thay vì trúng mảnh giấy. Khi đó trang đọc mã hiện ra vỏ quả và không
    còn dùng được — nguy hiểm hơn, người điền dễ đoán bừa mã quả, làm hỏng
    phép chia tập mà không ai phát hiện.

    Việc chọn dựa trên mật độ biên THẤP NHẤT trong số các ứng viên, thay vì
    một ngưỡng tuyệt đối, vì mật độ biên phụ thuộc độ nét và độ phân giải của
    từng máy. So sánh tương đối giữa các vùng trong cùng một ảnh thì bền hơn.
    Đo trên bộ ảnh Canon: dải ô xám 10,1%, mảnh giấy 4,8%.
    """
    layout = layout or CFG.layout
    H, W = bgr.shape[:2]

    def _search(region, offset):
        if region.size == 0:
            return None
        gray = cv2.cvtColor(region, cv2.COLOR_BGR2GRAY)
        blobs = _bright_blobs(region, min_area=max(int(0.00002 * W * H), 50))
        if not blobs:
            return None

        cands = []
        for b in blobs:
            ar = b["w"] / max(b["h"], 1)
            # loại mảng quá dẹt hoặc rỗng ruột (viền vải, thước tỷ lệ)
            if not (0.35 < ar < 4.0) or b["fill"] < 0.45:
                continue

            # Tiêu chí 1: mật độ biên. Bắt được trường hợp bốn ô xám dính
            # liền thành một mảng, vì khi đó mã QR nằm trong cùng khung bao.
            sub = gray[b["y"]:b["y"] + b["h"], b["x"]:b["x"] + b["w"]]
            ed = _edge_density(sub)
            if ed > max_edge_density:
                continue

            # Tiêu chí 2: ô xám đi thành nhóm. Bắt được trường hợp bốn ô tách
            # rời nhau — mỗi ô đứng riêng thì cũng phẳng và sáng y hệt mảnh
            # giấy, nên chỉ mật độ biên thôi là không đủ.
            anh_em = sum(
                1 for o in blobs if o is not b
                and abs(o["y"] - b["y"]) < 0.8 * max(b["h"], 1)
                and 0.35 < o["area"] / max(b["area"], 1) < 3.0)
            if anh_em >= 2:
                continue

            cands.append((ed, b))

        if not cands:
            return None
        # mảnh giấy là vùng sáng "phẳng" nhất: ít biên nhất
        _, b = min(cands, key=lambda t: t[0])
        return (b["x"] + offset[0], b["y"] + offset[1], b["w"], b["h"])

    # Giai đoạn 1: tìm trong vùng thẻ, nới rộng cho sai lệch bố cục
    x, y, rw, rh = layout.card_roi
    pad = 0.05
    x0, y0 = int(max(0.0, x - pad) * W), int(max(0.0, y - pad) * H)
    x1, y1 = int(min(1.0, x + rw + pad) * W), int(min(1.0, y + rh + pad) * H)
    if x1 > x0 and y1 > y0:
        got = _search(bgr[y0:y1, x0:x1], (x0, y0))
        if got:
            return got

    # Giai đoạn 2: khung hình đã đổi hẳn, tìm trên toàn ảnh
    return _search(bgr, (0, 0))


def crop_tag(bgr: np.ndarray, layout: CardLayout | None = None,
             pad: float = 0.35, auto: bool = True):
    """
    Cắt vùng nhãn mã quả. Trả (ảnh_cắt, da_do_tu_dong).

    da_do_tu_dong = False nghĩa là phải lùi về toạ độ cố định, tức ảnh cắt ra
    có thể không chứa mã quả. Trang đọc mã sẽ đánh dấu rõ các ô này để người
    điền biết mà bỏ qua thay vì đoán.
    """
    layout = layout or CFG.layout
    H, W = bgr.shape[:2]

    box = detect_tag(bgr, layout) if auto else None
    if box is not None:
        x, y, w, h = box
        px, py = int(w * pad), int(h * pad)
        x0, y0 = max(0, x - px), max(0, y - py)
        x1, y1 = min(W, x + w + px), min(H, y + h + py)
        return bgr[y0:y1, x0:x1], True

    rx, ry, rw, rh = layout.tag_roi
    return bgr[int(ry * H):int((ry + rh) * H),
               int(rx * W):int((rx + rw) * W)], False


def mask_card_region(bgr: np.ndarray, layout: CardLayout | None = None,
                     value: int = 0) -> np.ndarray:
    """
    Che vùng thẻ. Bắt buộc khi chạy các phương pháp ước lượng nguồn sáng
    không dùng thẻ — nếu để lộ thẻ thì thuật toán đang nhìn trộm đáp án.
    """
    layout = layout or CFG.layout
    h, w = bgr.shape[:2]
    x, y, rw, rh = layout.card_roi
    out = bgr.copy()
    out[int(y * h):int((y + rh) * h), int(x * w):int((x + rw) * w)] = value
    return out


def roi_mask(shape, roi) -> np.ndarray:
    """Mặt nạ nhị phân hình chữ nhật từ roi (x, y, w, h) tỷ lệ 0–1."""
    h, w = shape[:2]
    m = np.zeros((h, w), np.uint8)
    x0, y0, rw, rh = roi
    m[int(y0 * h):int((y0 + rh) * h), int(x0 * w):int((x0 + rw) * w)] = 1
    return m
