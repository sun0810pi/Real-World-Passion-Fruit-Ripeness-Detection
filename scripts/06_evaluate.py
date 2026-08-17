#!/usr/bin/env python3
"""
06 — ĐÁNH GIÁ ĐẦY ĐỦ (sinh số cho Bảng 8, 9, 10 và Hình 5)

    # một cấu hình
    python scripts/06_evaluate.py --pred outputs/runs/cungnguon_s0/predictions.csv \
           --out outputs/cungnguon_s0

    # gộp ba hạt giống -> trung bình kèm độ lệch chuẩn (mục 3.6)
    python scripts/06_evaluate.py --aggregate outputs/cungnguon_s0 \
           outputs/cungnguon_s1 outputs/cungnguon_s2

    # dựng thẳng Bảng 8 và Bảng 10
    python scripts/06_evaluate.py --compare \
        "Đường cơ sở màu=outputs/baseline_seed0" \
        "Học sâu, cùng nguồn=outputs/cungnguon_s0" \
        "Học sâu, bỏ ra một nguồn=outputs/loso_N1"
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score, confusion_matrix, f1_score

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from chanhday.config import CLASS_NAMES, N_CLASSES, build_cost_matrix  # noqa: E402
from chanhday.io_utils import (doc_bat_buoc, load_json,  # noqa: E402
                               save_json, write_csv)
from chanhday.metrics import (bootstrap_ci, calibration_table,  # noqa: E402
                              cost_optimal_prediction, early_late_rates,
                              expected_cost, off_by_more_than_one,
                              quadratic_weighted_kappa, rejection_curve)


def evaluate_one(pred_csv: Path, outdir: Path, cost=None) -> dict:
    df = pd.read_csv(doc_bat_buoc(pred_csv))

    thieu = [c for c in ("y_true", "y_pred") if c not in df.columns]
    if thieu:
        raise SystemExit(f"{pred_csv} thiếu cột {thieu}. "
                         f"File này phải do script 04 hoặc 05 sinh ra.")
    if df.empty:
        raise SystemExit(f"{pred_csv} không có dòng nào. Bước train đã xuất "
                         f"file rỗng — xem lại cảnh báo của script 05.")

    y = df["y_true"].to_numpy(int)
    p = df["y_pred"].to_numpy(int)

    # Chỉ số lớp phải nằm trong 0..4. Vượt ra ngoài thường có nghĩa là đâu đó
    # đã thêm quả hỏng thành lớp thứ sáu, khiến chỉ số các bậc chín dịch
    # chuyển và mọi con số sau đó sai mà không báo lỗi.
    ngoai = sorted(set(np.concatenate([y, p])) - set(range(N_CLASSES)))
    if ngoai:
        raise SystemExit(
            f"Có chỉ số lớp {[int(v) for v in ngoai]} nằm ngoài phạm vi 0..{N_CLASSES-1}.\n"
            f"Nguyên nhân thường gặp: quả hỏng bị đưa vào thang độ chín thành\n"
            f"lớp thứ sáu. Tình trạng quả là trục riêng — chạy\n"
            f"scripts/08_condition_head.py cho phần đó. Xem\n"
            f"docs/thiet_ke_hai_dau_ra.md.")

    outdir.mkdir(parents=True, exist_ok=True)

    res = {
        "n_mau": int(len(y)),
        "do_chinh_xac": float(accuracy_score(y, p)),
        "f1_macro": float(f1_score(y, p, average="macro", zero_division=0)),
        "f1_weighted": float(f1_score(y, p, average="weighted", zero_division=0)),
        "kappa_trong_so_bac": quadratic_weighted_kappa(y, p),
        "ty_le_lech_qua_mot_bac": off_by_more_than_one(y, p),
        "chi_phi_ky_vong": expected_cost(y, p, cost),
    }
    res.update(early_late_rates(y, p))

    f1c = f1_score(y, p, average=None, labels=list(range(N_CLASSES)), zero_division=0)
    res["f1_tung_lop"] = {CLASS_NAMES[i]: round(float(f1c[i]), 4)
                          for i in range(N_CLASSES)}

    for ten, fn in [("do_chinh_xac", accuracy_score),
                    ("f1_macro", lambda a, b: f1_score(a, b, average="macro",
                                                       zero_division=0)),
                    ("chi_phi_ky_vong", lambda a, b: expected_cost(a, b, cost))]:
        lo, hi = bootstrap_ci(fn, y, p)
        res[f"{ten}_ci95"] = [round(lo, 4), round(hi, 4)]

    cm = confusion_matrix(y, p, labels=list(range(N_CLASSES)))
    res["ma_tran_nham_lan"] = cm.tolist()
    write_csv(pd.DataFrame(cm, index=CLASS_NAMES, columns=CLASS_NAMES)
              .reset_index().rename(columns={"index": "that\\du_doan"}),
              outdir / "confusion_matrix.csv")

    pcols = [f"p_{c}" for c in CLASS_NAMES]
    if all(c in df.columns for c in pcols):
        proba = df[pcols].to_numpy()
        rows, ece = calibration_table(proba, y, p)
        write_csv(pd.DataFrame(rows), outdir / "calibration.csv")
        res["ece"] = round(ece, 4)

        write_csv(pd.DataFrame(rejection_curve(proba, y, p)),
                  outdir / "rejection_curve.csv")

        # quyết định tối ưu theo chi phí thay vì theo xác suất cao nhất
        p_cost = cost_optimal_prediction(proba, cost)
        res["chi_phi_ky_vong_khi_toi_uu_theo_chi_phi"] = expected_cost(y, p_cost, cost)
        res["do_chinh_xac_khi_toi_uu_theo_chi_phi"] = float(accuracy_score(y, p_cost))

    save_json(res, outdir / "metrics.json")

    print("\n" + "=" * 64)
    print(f"KẾT QUẢ: {pred_csv}")
    print("=" * 64)
    print(f"n = {res['n_mau']}")
    print(f"Độ chính xác        {res['do_chinh_xac']:.4f}   CI95 {res['do_chinh_xac_ci95']}")
    print(f"F1 macro            {res['f1_macro']:.4f}   CI95 {res['f1_macro_ci95']}")
    print(f"Kappa trọng số bậc  {res['kappa_trong_so_bac']:.4f}")
    print(f"Lệch quá 1 bậc      {res['ty_le_lech_qua_mot_bac']*100:.2f}%")
    print(f"Sai số TB theo bậc  {res['sai_so_tb_theo_bac']:.4f}")
    print("-" * 64)
    print(f"Đúng bậc {res['ty_le_dung_bac']*100:5.2f}%    "
          f"Hái sớm {res['ty_le_hai_som']*100:5.2f}%    "
          f"Hái muộn {res['ty_le_hai_muon']*100:5.2f}%")
    print(f"Chi phí kỳ vọng     {res['chi_phi_ky_vong']:.4f}   "
          f"CI95 {res['chi_phi_ky_vong_ci95']}")
    if "chi_phi_ky_vong_khi_toi_uu_theo_chi_phi" in res:
        print(f"  nếu quyết định theo chi phí thay vì theo xác suất: "
              f"{res['chi_phi_ky_vong_khi_toi_uu_theo_chi_phi']:.4f}")
    print("-" * 64)
    for c, v in res["f1_tung_lop"].items():
        print(f"  F1 {c:<22} {v:.4f}")
    print("-" * 64)
    print("Ma trận nhầm lẫn (hàng = thật, cột = dự đoán):")
    print(pd.DataFrame(cm, index=[c[:12] for c in CLASS_NAMES],
                       columns=[c[:12] for c in CLASS_NAMES]).to_string())

    if res["n_mau"] < 30:
        print("\n" + "!" * 64)
        print(f"CỠ MẪU QUÁ NHỎ: chỉ {res['n_mau']} mẫu trong tập kiểm tra.")
        print("Mọi con số trên đây không kết luận được gì — khoảng tin cậy rộng")
        print("gần bằng toàn bộ thang đo. KHÔNG đưa vào báo cáo.")
        print("Nếu bộ dữ liệu của bạn lớn hơn nhiều con số này, ảnh đã rớt ở")
        print("đâu đó trước bước train. Kiểm tra theo thứ tự:")
        print("  1. data/proc_wb_ledger.csv        (mất ở bước tiền xử lý?)")
        print("  2. python scripts/03_split.py --mode audit   (chia tập lệch?)")
        print("  3. dòng 'Tập val có N ảnh, xuất được M dòng' của script 05")
        print("!" * 64)

    if res["do_chinh_xac"] > 0.97:
        print("\n" + "!" * 64)
        print("CẢNH BÁO: độ chính xác trên 97%.")
        print("Với bài toán này, con số đó gần như luôn nghĩa là rò rỉ dữ liệu.")
        print("Chạy: python scripts/03_split.py --manifest ... --mode audit")
        print("!" * 64)
    return res


def aggregate(dirs):
    rs = [load_json(Path(d) / "metrics.json") for d in dirs
          if (Path(d) / "metrics.json").exists()]
    if not rs:
        raise SystemExit("Không tìm thấy metrics.json nào.")
    keys = ["do_chinh_xac", "f1_macro", "kappa_trong_so_bac",
            "sai_so_tb_theo_bac", "chi_phi_ky_vong",
            "ty_le_hai_som", "ty_le_hai_muon"]
    print("\n" + "=" * 64)
    print(f"TRUNG BÌNH TRÊN {len(rs)} HẠT GIỐNG — dạng 'trung bình (độ lệch chuẩn)'")
    print("=" * 64)
    out = {}
    for k in keys:
        v = np.array([r[k] for r in rs if k in r], float)
        sd = float(v.std(ddof=1)) if len(v) > 1 else 0.0
        out[k] = {"mean": float(v.mean()), "std": sd}
        print(f"  {k:<26} {v.mean():.4f} ({sd:.4f})")
    save_json(out, "outputs/aggregate.json")
    return out


def compare(specs):
    rows = []
    for s in specs:
        name, d = s.split("=", 1)
        f = Path(d) / "metrics.json"
        if not f.exists():
            print(f"(bỏ qua {name}: chưa có {f})")
            continue
        r = load_json(f)
        rows.append({
            "Phương pháp": name,
            "Độ chính xác": round(r["do_chinh_xac"], 4),
            "F1 theo lớp": round(r["f1_macro"], 4),
            "Sai số TB theo bậc": round(r["sai_so_tb_theo_bac"], 4),
            "Kappa": round(r["kappa_trong_so_bac"], 4),
            "Tỷ lệ đúng bậc": round(r["ty_le_dung_bac"], 4),
            "Tỷ lệ hái sớm": round(r["ty_le_hai_som"], 4),
            "Tỷ lệ hái muộn": round(r["ty_le_hai_muon"], 4),
            "Chi phí kỳ vọng": round(r["chi_phi_ky_vong"], 4),
        })
    if not rows:
        return
    t = pd.DataFrame(rows)
    print("\n=== BẢNG 8 (phần chỉ số) ===")
    print(t[["Phương pháp", "Độ chính xác", "F1 theo lớp",
             "Sai số TB theo bậc", "Kappa"]].to_string(index=False))
    print("\n=== BẢNG 10 ===")
    print(t[["Phương pháp", "Tỷ lệ đúng bậc", "Tỷ lệ hái sớm",
             "Tỷ lệ hái muộn", "Chi phí kỳ vọng"]].to_string(index=False))
    write_csv(t, "outputs/bang_8_10.csv")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pred")
    ap.add_argument("--out", default="outputs/eval")
    ap.add_argument("--aggregate", nargs="*")
    ap.add_argument("--compare", nargs="*")
    ap.add_argument("--cost-late", type=float, default=None)
    ap.add_argument("--cost-early", type=float, default=None)
    args = ap.parse_args()

    cost = None
    if args.cost_late is not None or args.cost_early is not None:
        from chanhday.config import COST_EARLY_PER_STEP, COST_LATE_PER_STEP
        cost = build_cost_matrix(args.cost_late or COST_LATE_PER_STEP,
                                 args.cost_early or COST_EARLY_PER_STEP)
        print("Ma trận chi phí đang dùng:\n", cost)

    Path("outputs").mkdir(exist_ok=True)
    if args.compare:
        compare(args.compare)
    elif args.aggregate:
        aggregate(args.aggregate)
    elif args.pred:
        evaluate_one(Path(args.pred), Path(args.out), cost)
    else:
        ap.error("cần --pred, --aggregate hoặc --compare")


if __name__ == "__main__":
    main()
