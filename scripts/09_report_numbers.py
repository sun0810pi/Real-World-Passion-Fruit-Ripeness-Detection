#!/usr/bin/env python3
"""
09 — GOM TOÀN BỘ SỐ LIỆU ĐỂ ĐIỀN BÁO CÁO

Quét thư mục outputs/, gom mọi kết quả đã có, in ra theo đúng thứ tự các ô
[…] trong báo cáo. Chạy cuối cùng, sau khi mọi script khác đã chạy xong.

    python scripts/09_report_numbers.py

Ô nào chưa có số sẽ hiện "CHƯA CÓ" kèm lệnh cần chạy để có nó.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from chanhday.io_utils import load_json, read_str_csv  # noqa: E402

OUT = Path("outputs")
DATA = Path("data")


def get(path, key=None, fmt="{:.4f}"):
    p = Path(path)
    if not p.exists():
        return None
    try:
        d = load_json(p)
    except Exception:
        return None
    if key is None:
        return d
    v = d
    for k in key.split("."):
        if not isinstance(v, dict) or k not in v:
            return None
        v = v[k]
    return fmt.format(v) if isinstance(v, float) else v


def line(muc, mo_ta, gia_tri, lenh=""):
    if gia_tri is None:
        print(f"  {muc:<14} {mo_ta:<42} CHƯA CÓ")
        if lenh:
            print(f"  {'':<14} {'':<42} -> {lenh}")
    else:
        print(f"  {muc:<14} {mo_ta:<42} {gia_tri}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--manifest", default="data/proc_wb_manifest.csv")
    args = ap.parse_args()

    print("=" * 84)
    print("SỐ LIỆU ĐỂ ĐIỀN VÀO BÁO CÁO")
    print("=" * 84)

    # ---------------- Mục 4.1: bộ dữ liệu ----------------
    print("\n[ MỤC 4.1 + BẢNG 5 — ĐẶC ĐIỂM BỘ DỮ LIỆU ]")
    mf = Path(args.manifest)
    if mf.exists():
        df = read_str_csv(mf)
        line("Bảng 5", "Tổng số ảnh sau làm sạch", len(df))
        line("Bảng 5", "Số quả riêng biệt",
             df.loc[df.fruit_id.astype(str).str.len() > 0, "fruit_id"].nunique())
        line("Bảng 5", "Số nguồn thu mẫu",
             df.loc[df.source_id.astype(str).str.len() > 0, "source_id"].nunique())
        line("Bảng 5", "Số buổi chụp",
             df.loc[df.session_id.astype(str).str.len() > 0, "session_id"].nunique())
        nf = df.loc[df.fruit_id.astype(str).str.len() > 0, "fruit_id"].nunique()
        if nf:
            line("Bảng 5", "Số ảnh trung bình mỗi quả", f"{len(df)/nf:.1f}")
        cams = df.loc[df.camera_model.astype(str).str.len() > 0, "camera_model"]
        if len(cams):
            line("Mục 3.4.2", "Thiết bị chụp", ", ".join(sorted(cams.unique())))
    else:
        line("Bảng 5", "Bảng kê dữ liệu", None,
             "python scripts/01_build_manifest.py --data data/raw")

    st = get(DATA / "proc_wb_stats.json")
    if st:
        line("Mục 4.1", "Tỷ lệ tách nền thành công (%)",
             st.get("ty_le_tach_nen_thanh_cong_pc"))
        line("Mục 4.1", "Tỷ lệ đọc được thẻ (%)", st.get("ty_le_do_the_pc"))
        line("Mục 4.1", "Số ảnh bị loại", st.get("so_anh_that_bai"))
        line("Mục 4.4", "Ám màu trước hiệu chỉnh (độ)",
             st.get("sai_so_goc_truoc_hieu_chinh_do"))
        line("Mục 4.4", "Ám màu sau hiệu chỉnh (độ)",
             st.get("sai_so_goc_sau_hieu_chinh_do"))
    else:
        line("Mục 4.1", "Thống kê tiền xử lý", None,
             "python scripts/02_preprocess.py --manifest data/manifest.csv --out data/proc_wb")

    # ---------------- Mục 4.3: cùng nguồn ----------------
    print("\n[ MỤC 4.3 + BẢNG 8 — ĐÁNH GIÁ CÙNG NGUỒN ]")
    for ten, d in [("Đường cơ sở màu", "baseline_seed0"),
                   ("Học sâu (hạt giống 0)", "cungnguon_s0")]:
        m = get(OUT / d / "metrics.json")
        if m:
            line("Bảng 8", f"{ten} — độ chính xác", f"{m['do_chinh_xac']:.4f}")
            line("Bảng 8", f"{ten} — F1 macro", f"{m['f1_macro']:.4f}")
            line("Bảng 8", f"{ten} — sai số TB theo bậc",
                 f"{m['sai_so_tb_theo_bac']:.4f}")
        else:
            line("Bảng 8", ten, None, f"chạy script 04/05 rồi 06 --out outputs/{d}")

    agg = get(OUT / "aggregate.json")
    if agg:
        print("  --- trung bình 3 hạt giống (mục 3.6) ---")
        for k in ("do_chinh_xac", "f1_macro", "chi_phi_ky_vong"):
            if k in agg:
                line("Bảng 8", k, f"{agg[k]['mean']:.4f} ({agg[k]['std']:.4f})")

    mi = get(OUT / "runs/cungnguon_s0/model_info.json")
    if mi:
        line("Bảng 8", "Số tham số mô hình (triệu)",
             f"{mi['so_tham_so']/1e6:.2f}")

    # ---------------- Mục 4.4: bỏ ra một nguồn ----------------
    print("\n[ MỤC 4.4 + BẢNG 9 — BỎ RA MỘT NGUỒN ]")
    loso = sorted(OUT.glob("loso_*/metrics.json"))
    if loso:
        rows = []
        for f in loso:
            m = load_json(f)
            rows.append({"Nguồn bị bỏ ra": f.parent.name.replace("loso_", ""),
                         "F1 macro": round(m["f1_macro"], 4),
                         "Độ chính xác": round(m["do_chinh_xac"], 4),
                         "Chi phí kỳ vọng": round(m["chi_phi_ky_vong"], 4)})
        t = pd.DataFrame(rows)
        print(t.to_string(index=False))
        base = get(OUT / "cungnguon_s0/metrics.json")
        if base:
            drop = base["f1_macro"] - t["F1 macro"].mean()
            line("Mục 4.4", "Mức sụt giảm F1 (điểm)", f"{drop:.4f}")
            line("Mục 4.4", "Ngưỡng 0,10 của Giả thuyết 2",
                 "ĐẠT" if drop <= 0.10 else "KHÔNG ĐẠT")
    else:
        line("Bảng 9", "Kết quả bỏ ra một nguồn", None,
             "python scripts/03_split.py --mode loso, rồi script 05 và 06")

    # ---------------- Mục 4.4: vai trò chuẩn hóa màu ----------------
    a = get(OUT / "cungnguon_wb_s0/metrics.json")
    b = get(OUT / "cungnguon_nowb_s0/metrics.json")
    if a and b:
        line("Mục 4.4", "F1 CÓ chuẩn hóa màu", f"{a['f1_macro']:.4f}")
        line("Mục 4.4", "F1 KHÔNG chuẩn hóa màu", f"{b['f1_macro']:.4f}")
        line("Mục 4.4", "Phần quy cho chiếu sáng (điểm)",
             f"{a['f1_macro'] - b['f1_macro']:.4f}")

    # ---------------- Mục 4.6: chi phí ----------------
    print("\n[ MỤC 4.6 + BẢNG 10 — CHI PHÍ BẤT ĐỐI XỨNG ]")
    f = OUT / "bang_8_10.csv"
    if f.exists():
        print(pd.read_csv(f).to_string(index=False))
    else:
        line("Bảng 10", "Bảng so sánh chi phí", None,
             'python scripts/06_evaluate.py --compare "A=outputs/..." "B=outputs/..."')

    # ---------------- Đầu ra thứ hai ----------------
    print("\n[ BẢNG 8b — TÌNH TRẠNG QUẢ (dùng được / hỏng) ]")
    m = get(OUT / "tinh_trang/metrics.json")
    if m:
        line("Bảng 8b", "Độ chính xác", f"{m['do_chinh_xac']:.4f}")
        line("Bảng 8b", "F1 lớp 'hỏng'", f"{m['f1_lop_hong']:.4f}")
        if "auc_roc" in m:
            line("Bảng 8b", "AUC-ROC", f"{m['auc_roc']:.4f}")
    else:
        line("Bảng 8b", "Kết quả đầu ra tình trạng", None,
             "python scripts/08_condition_head.py --manifest data/proc_wb_manifest.csv")

    # ---------------- Nguồn sáng ----------------
    print("\n[ MỤC 4.4 — TẦNG ƯỚC LƯỢNG MÔI TRƯỜNG ]")
    f = OUT / "illuminant_baselines.csv"
    if f.exists():
        print(pd.read_csv(f).to_string(index=False))
    else:
        line("Mục 4.4", "Đường cơ sở ước lượng nguồn sáng", None,
             "python scripts/07_illuminant.py --mode extract, rồi --mode baseline")
    cnn = get(OUT / "illuminant_cnn.json")
    if cnn:
        line("Mục 4.4", "CNN — sai số góc trung vị (độ)",
             f"{cnn['tot_nhat_trung_vi']:.3f}")

    # ---------------- Còn thiếu, không script nào sinh được ----------------
    print("\n" + "=" * 84)
    print("NHỮNG Ô PHẢI ĐO NGOÀI ĐỜI, KHÔNG SCRIPT NÀO SINH ĐƯỢC")
    print("=" * 84)
    print("  Bảng 7    TSS, TA, TSS/TA theo từng bậc      -> khúc xạ kế + chuẩn độ")
    print("  Mục 4.2   Kappa giữa hai người gán nhãn      -> cần người thứ hai gán nhãn")
    print("  Mục 4.5   R² và RMSE giữa bậc dự đoán và TSS -> cần số liệu TSS")
    print("  Mục 4.5   Độ chính xác của người thu hái     -> cần mời người gán nhãn")
    print("  Phụ lục 5 Trọng số ma trận chi phí           -> tham vấn nông hộ/doanh nghiệp")
    print("  Bảng 2    Xuất xứ từng nguồn                 -> ghi chép khi thu mẫu")


if __name__ == "__main__":
    main()
