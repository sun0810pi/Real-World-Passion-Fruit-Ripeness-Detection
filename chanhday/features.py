"""
Đặc trưng thống kê màu CIE L*a*b* (mục 3.5, nhóm phương pháp 1).

Nhóm đặc trưng này phục vụ hai việc:
  1. Đường cơ sở bắt buộc — nếu nó đã đạt phần lớn hiệu năng thì việc dùng
     mô hình học sâu không được biện minh, và đó là kết luận cần báo cáo.
  2. Tính tỷ lệ vỏ chuyển màu từ ảnh (mục 3.4.4), để so với ước lượng
     trực quan ở mục 4.2.
"""
from __future__ import annotations

from pathlib import Path

import cv2
import numpy as np

from .config import CFG
from .io_utils import imread_unicode

FEATURE_NAMES = (
    [f"{c}_{s}" for c in "Lab" for s in
     ["mean", "std", "p05", "p25", "p50", "p75", "p95"]]
    + ["frac_vo_chuyen_mau", "C_mean", "C_std", "H_mean", "H_std", "H_dong_deu",
       "A_cv", "frac_nau_sam", "do_khong_dong_deu"]
)


def to_cie_lab(bgr: np.ndarray):
    """
    OpenCV lưu L trong 0–255 và a/b lệch 128. Đưa về thang CIE thật:
    L trong 0–100, a/b quanh 0.
    """
    lab = cv2.cvtColor(bgr, cv2.COLOR_BGR2LAB).astype(np.float64)
    return (lab[:, :, 0] * 100.0 / 255.0,
            lab[:, :, 1] - 128.0,
            lab[:, :, 2] - 128.0)


def fruit_mask_from_crop(bgr: np.ndarray) -> np.ndarray:
    """Ảnh cắt có nền bôi đen, nên vùng quả = pixel không đen."""
    m = bgr.sum(axis=2) > 25
    return m if m.sum() >= 200 else np.ones(bgr.shape[:2], bool)


def circular_mean_std(deg: np.ndarray):
    """
    Trung bình và độ phân tán của một tập góc, tính theo thống kê vòng tròn.

    Trung bình số học thông thường sai với đại lượng góc. Một quả nửa đã
    chuyển đỏ (góc màu quanh 0 độ) và nửa còn xanh (góc màu quanh 180 độ)
    sẽ cho trung bình số học bằng 90 độ, tức là "vàng" — một mô tả sai hẳn,
    và sai đúng ở bậc 3 vốn là bậc khó phân biệt nhất.

    Cách đúng là lấy trung bình của vector đơn vị rồi quy ngược ra góc.
    Độ dài vector trung bình còn cho luôn mức phân tán: gần 1 nghĩa là màu
    đồng đều, gần 0 nghĩa là màu loang lổ — thông tin trực tiếp hữu ích cho
    bài toán này.
    """
    rad = np.radians(deg)
    c, s = np.cos(rad).mean(), np.sin(rad).mean()
    # kẹp về [0, 1]: sai số dấu phẩy động có thể cho R nhỉnh hơn 1 khi màu
    # hoàn toàn đồng đều, làm log dương và sqrt nhận số âm -> NaN
    R = float(np.clip(np.hypot(c, s), 0.0, 1.0))
    mean = float(np.degrees(np.arctan2(s, c)))
    # độ lệch chuẩn vòng tròn; R->1 cho 0, R->0 cho giá trị lớn
    std = float(np.degrees(np.sqrt(-2.0 * np.log(max(R, 1e-9)))))
    return mean, std, R


def extract(bgr: np.ndarray) -> np.ndarray:
    """Vector đặc trưng màu trên vùng quả."""
    thr = CFG.thresholds
    mask = fruit_mask_from_crop(bgr)
    L, A, B = to_cie_lab(bgr)
    L, A, B = L[mask], A[mask], B[mask]

    feats = []
    for ch in (L, A, B):
        feats += [ch.mean(), ch.std()]
        feats += list(np.percentile(ch, [5, 25, 50, 75, 95]))

    # tỷ lệ vỏ chuyển màu — chính là đại lượng ở mục 3.4.4
    feats.append(float((A > thr.a_star_turned).mean()))

    # sắc độ và góc màu: mô tả tiến trình xanh -> vàng -> đỏ
    C = np.sqrt(A ** 2 + B ** 2)
    H = np.degrees(np.arctan2(B, A))
    h_mean, h_std, h_R = circular_mean_std(H)
    feats += [C.mean(), C.std(), h_mean, h_std, h_R]
    feats.append(float(A.std() / (abs(A.mean()) + 1e-6)))

    # vùng nâu sẫm: dấu hiệu của quả hỏng, phục vụ đầu ra thứ hai
    feats.append(float(((L < 35) & (C < 20)).mean()))

    # độ không đồng đều không gian: chín loang lổ khác chín đều
    lab_full = cv2.cvtColor(bgr, cv2.COLOR_BGR2LAB)
    a_full = lab_full[:, :, 1].astype(np.float64) - 128.0
    small = cv2.resize(a_full, (32, 32), interpolation=cv2.INTER_AREA)
    feats.append(float(small.std()))

    return np.asarray(feats, float)


def extract_from_path(path: str | Path) -> np.ndarray | None:
    bgr = imread_unicode(path)
    return None if bgr is None else extract(bgr)
