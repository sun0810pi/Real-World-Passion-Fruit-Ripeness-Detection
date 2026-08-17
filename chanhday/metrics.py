"""
Chỉ số đánh giá (mục 3.7, Bảng 4).

Chứa toàn bộ đại lượng mà báo cáo cần: Kappa có trọng số bậc, chi phí kỳ vọng
theo ma trận bất đối xứng, tỷ lệ hái sớm / hái muộn, khoảng tin cậy bootstrap,
và hiệu chuẩn xác suất.
"""
from __future__ import annotations

import numpy as np

from .config import N_CLASSES, build_cost_matrix


# ---------------------------------------------------------------------------
# Kappa có trọng số bậc (Cohen 1968) — mục 3.4.8
# ---------------------------------------------------------------------------

def quadratic_weighted_kappa(a, b, n_classes: int = N_CLASSES) -> float:
    """
    Nhãn độ chín có thứ tự, nên lệch một bậc phải bị phạt nhẹ hơn lệch ba bậc.
    Kappa thường (không trọng số) coi mọi bất đồng như nhau và sẽ báo con số
    thấp hơn thực chất.
    """
    a = np.asarray(a, int)
    b = np.asarray(b, int)
    n = len(a)
    if n == 0:
        return float("nan")

    O = np.zeros((n_classes, n_classes))
    for i, j in zip(a, b):
        O[i, j] += 1

    E = np.outer(np.bincount(a, minlength=n_classes),
                 np.bincount(b, minlength=n_classes)).astype(float) / n

    idx = np.arange(n_classes)
    W = (idx[:, None] - idx[None, :]) ** 2 / (n_classes - 1) ** 2

    denom = (W * E).sum()
    return float("nan") if denom == 0 else float(1.0 - (W * O).sum() / denom)


def off_by_more_than_one(a, b) -> float:
    """Tỷ lệ lệch quá một bậc (mục 4.2)."""
    return float((np.abs(np.asarray(a, int) - np.asarray(b, int)) > 1).mean())


# ---------------------------------------------------------------------------
# Chi phí bất đối xứng (mục 3.6, 4.6)
# ---------------------------------------------------------------------------

def expected_cost(y_true, y_pred, cost: np.ndarray | None = None) -> float:
    cost = build_cost_matrix() if cost is None else cost
    return float(cost[np.asarray(y_true, int), np.asarray(y_pred, int)].mean())


def early_late_rates(y_true, y_pred) -> dict:
    d = np.asarray(y_pred, int) - np.asarray(y_true, int)
    n = len(d)
    return {
        "ty_le_dung_bac": float((d == 0).sum() / n),
        "ty_le_hai_som": float((d > 0).sum() / n),
        "ty_le_hai_muon": float((d < 0).sum() / n),
        "sai_so_tb_theo_bac": float(np.abs(d).mean()),
    }


def cost_optimal_prediction(proba: np.ndarray,
                            cost: np.ndarray | None = None) -> np.ndarray:
    """
    Dự đoán tối thiểu hóa chi phí kỳ vọng thay vì chọn lớp có xác suất cao nhất.

    Đây là chỗ ma trận chi phí thực sự thay đổi hành vi công cụ, không chỉ
    thay đổi cách báo cáo: với chi phí hái muộn cao hơn, mô hình sẽ tự lệch
    về phía báo bậc cao hơn khi lưỡng lự.
    """
    cost = build_cost_matrix() if cost is None else cost
    return np.asarray(proba @ cost).argmin(axis=1)


# ---------------------------------------------------------------------------
# Khoảng tin cậy và hiệu chuẩn
# ---------------------------------------------------------------------------

def bootstrap_ci(fn, y_true, y_pred, n_boot: int = 2000,
                 alpha: float = 0.05, seed: int = 0):
    rng = np.random.default_rng(seed)
    y_true, y_pred = np.asarray(y_true), np.asarray(y_pred)
    n = len(y_true)
    stats = []
    for _ in range(n_boot):
        i = rng.integers(0, n, n)
        try:
            stats.append(fn(y_true[i], y_pred[i]))
        except Exception:
            pass
    if not stats:
        return float("nan"), float("nan")
    return (float(np.percentile(stats, 100 * alpha / 2)),
            float(np.percentile(stats, 100 * (1 - alpha / 2))))


def calibration_table(proba: np.ndarray, y_true, y_pred, n_bins: int = 10):
    """
    Mô hình tự tin 90% thì có đúng 90% số lần không?

    Cần cho cơ chế từ chối trả lời: chỉ đặt được ngưỡng tin cậy có ý nghĩa
    khi xác suất đã được hiệu chuẩn. Trả về (bảng, ECE).
    """
    conf = np.asarray(proba).max(axis=1)
    correct = (np.asarray(y_true) == np.asarray(y_pred)).astype(float)
    edges = np.linspace(0, 1, n_bins + 1)
    idx = np.clip(np.digitize(conf, edges) - 1, 0, n_bins - 1)

    rows, ece = [], 0.0
    for b in range(n_bins):
        m = idx == b
        if not m.any():
            continue
        acc_b, conf_b = correct[m].mean(), conf[m].mean()
        ece += m.sum() / len(conf) * abs(acc_b - conf_b)
        rows.append({"khoang": f"{edges[b]:.1f}-{edges[b+1]:.1f}",
                     "n": int(m.sum()),
                     "do_tin_cay_tb": round(float(conf_b), 4),
                     "do_chinh_xac_tb": round(float(acc_b), 4)})
    return rows, float(ece)


def rejection_curve(proba: np.ndarray, y_true, y_pred, steps: int = 20):
    """
    Đánh đổi giữa tỷ lệ từ chối trả lời và độ chính xác trên phần đã trả lời.

    Công cụ nói "không xác định được" ở 10% số ca khó mà đạt 90% trên 90%
    còn lại thì dùng được hơn hẳn một công cụ đoán bừa mọi ca để đạt 78%.
    """
    conf = np.asarray(proba).max(axis=1)
    correct = (np.asarray(y_true) == np.asarray(y_pred)).astype(float)
    out = []
    for t in np.linspace(0, 0.95, steps):
        keep = conf >= t
        if keep.sum() == 0:
            continue
        out.append({
            "nguong_tin_cay": round(float(t), 3),
            "ty_le_tra_loi": round(float(keep.mean()), 4),
            "do_chinh_xac_phan_tra_loi": round(float(correct[keep].mean()), 4),
        })
    return out
