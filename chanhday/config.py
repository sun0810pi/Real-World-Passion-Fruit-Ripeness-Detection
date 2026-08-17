"""
Cấu hình trung tâm.

Mọi hằng số của đề tài nằm ở đây, không rải rác trong các script.
Muốn đổi bố cục thẻ, ngưỡng, hay ma trận chi phí thì sửa file này
hoặc ghi đè bằng configs/default.yaml.
"""
from __future__ import annotations

from dataclasses import dataclass, field, asdict
from pathlib import Path

import numpy as np

# ---------------------------------------------------------------------------
# Nhãn độ chín (mục 3.4.4, Bảng 3)
# ---------------------------------------------------------------------------

CLASS_NAMES = [
    "1_xanh",
    "2_bat_dau_chuyen",
    "3_chuyen_mot_phan",
    "4_chuyen_phan_lon",
    "5_chin_hoan_toan",
]
CLASS_TO_IDX = {c: i for i, c in enumerate(CLASS_NAMES)}
N_CLASSES = len(CLASS_NAMES)

CLASS_LABELS_VI = {
    "1_xanh": "Bậc 1 — Xanh (dưới 10% vỏ chuyển màu)",
    "2_bat_dau_chuyen": "Bậc 2 — Bắt đầu chuyển màu (10–30%)",
    "3_chuyen_mot_phan": "Bậc 3 — Chuyển màu một phần (30–70%)",
    "4_chuyen_phan_lon": "Bậc 4 — Chuyển màu phần lớn (trên 70%)",
    "5_chin_hoan_toan": "Bậc 5 — Chín hoàn toàn (toàn bộ vỏ)",
}

# Trục thứ hai, độc lập với độ chín (xem docs/thiet_ke_hai_dau_ra.md)
CONDITION_NAMES = ["dung_duoc", "hong"]
CONDITION_TO_IDX = {c: i for i, c in enumerate(CONDITION_NAMES)}

# Tên thư mục thường gặp cho quả hỏng. Đây KHÔNG phải bậc chín thứ sáu:
# gặp thư mục nào trong danh sách này, script gán tinh_trang='hong' và để
# trống cột label, vì tình trạng là một trục riêng (xem docs/thiet_ke_hai_dau_ra.md).
#
# Bỏ qua điều này là lỗi nghiêm trọng và âm thầm: nếu nhét '6_hong' thành
# lớp thứ sáu rồi đánh số lại, chỉ số lớp của các bậc chín sẽ dịch chuyển
# và mọi con số Kappa, sai số theo bậc, chi phí kỳ vọng đều sai mà không
# có thông báo lỗi nào.
CONDITION_DIR_ALIASES = {
    "6_hong", "hong", "hu", "6_hu", "hong_hoc", "loai_bo", "damaged", "rotten",
}

IMG_EXTS = {".jpg", ".jpeg", ".png", ".bmp", ".webp", ".tif", ".tiff"}
RAW_EXTS = {".cr3", ".cr2", ".nef", ".arw", ".dng", ".raf"}


# ---------------------------------------------------------------------------
# Bố cục thẻ chuẩn
# ---------------------------------------------------------------------------

@dataclass
class CardLayout:
    """
    Vị trí thẻ chuẩn trong khung hình, theo tỷ lệ 0–1 của chiều rộng/cao ảnh.

    Giá trị mặc định đo trên bộ ảnh Canon EOS 200D II (6000x4000), thẻ đặt
    góc phải dưới, 4 ô xám xếp ngang kèm mã QR phía trên, mảnh giấy ghi mã
    quả dán ở phần phải của thẻ.

    Bố cục chụp khác thì chạy `python scripts/00_calibrate_layout.py` để dò lại.
    """
    name: str = "canon_200d_ii"
    card_roi: tuple = (0.65, 0.71, 0.34, 0.18)      # x, y, w, h
    tag_roi: tuple = (0.885, 0.735, 0.090, 0.080)   # mảnh giấy ghi mã quả
    tag_rotate: int = 180                            # chữ viết ngược chiều
    patch_y: tuple = (0.795, 0.822)                  # dải y của 4 ô xám
    patch_x0: float = 0.6695
    patch_dx: float = 0.0163
    patch_w: float = 0.010
    n_patches: int = 4

    def patch_boxes(self, shape):
        """Trả về danh sách (x0, y0, x1, y1) pixel của từng ô xám."""
        h, w = shape[:2]
        y0, y1 = int(self.patch_y[0] * h), int(self.patch_y[1] * h)
        out = []
        for i in range(self.n_patches):
            a = int((self.patch_x0 + self.patch_dx * i) * w)
            out.append((a, y0, a + int(self.patch_w * w), y1))
        return out


CARD_LAYOUTS = {
    "canon_200d_ii": CardLayout(),
    # Thêm bố cục cho bộ ảnh điện thoại tại đây sau khi đo bằng script 00.
}


# ---------------------------------------------------------------------------
# Ma trận chi phí bất đối xứng (mục 3.6, Phụ lục 5)
# ---------------------------------------------------------------------------

COST_LATE_PER_STEP = 3.0    # thiệt hại mỗi bậc HÁI MUỘN
COST_EARLY_PER_STEP = 1.0   # thiệt hại mỗi bậc HÁI SỚM


def build_cost_matrix(late: float = COST_LATE_PER_STEP,
                      early: float = COST_EARLY_PER_STEP) -> np.ndarray:
    """
    COST[y_that, y_du_doan].

    Mô hình báo bậc THẤP hơn thật -> người trồng chờ thêm -> hái muộn.
    Mô hình báo bậc CAO hơn thật  -> người trồng hái ngay -> hái sớm.

    CẢNH BÁO: hai trọng số mặc định chỉ để chạy thử. Mục 3.6 yêu cầu tham vấn
    nông hộ và doanh nghiệp thu mua. Phải thay trước khi đưa số vào Bảng 10.
    """
    cost = np.zeros((N_CLASSES, N_CLASSES), float)
    for t in range(N_CLASSES):
        for p in range(N_CLASSES):
            d = p - t
            cost[t, p] = early * d if d > 0 else late * (-d)
    return cost


# ---------------------------------------------------------------------------
# Ngưỡng xử lý
# ---------------------------------------------------------------------------

@dataclass
class Thresholds:
    a_star_turned: float = 10.0     # a* vượt ngưỡng này = pixel "đã chuyển màu"
    min_fruit_area_frac: float = 0.002
    crop_pad: float = 0.08
    output_size: int = 320
    saturation_ceiling: int = 252   # bỏ pixel cháy sáng khi đo màu


@dataclass
class Config:
    layout: CardLayout = field(default_factory=CardLayout)
    thresholds: Thresholds = field(default_factory=Thresholds)
    seeds: tuple = (0, 1, 2)
    val_frac: float = 0.2

    def to_dict(self):
        return asdict(self)


CFG = Config()


def load_yaml(path: str | Path) -> Config:
    """Nạp cấu hình từ YAML, ghi đè lên giá trị mặc định."""
    import yaml
    with open(path, encoding="utf-8") as f:
        d = yaml.safe_load(f) or {}
    cfg = Config()
    if "layout" in d:
        name = d["layout"].get("name")
        base = CARD_LAYOUTS.get(name, CardLayout())
        cfg.layout = CardLayout(**{**asdict(base), **d["layout"]})
    if "thresholds" in d:
        cfg.thresholds = Thresholds(**{**asdict(Thresholds()), **d["thresholds"]})
    for k in ("seeds", "val_frac"):
        if k in d:
            setattr(cfg, k, d[k])
    return cfg
