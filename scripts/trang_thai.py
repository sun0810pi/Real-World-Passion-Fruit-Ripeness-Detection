#!/usr/bin/env python3
"""
TRẠNG THÁI — đang ở bước nào, việc tiếp theo là gì

Chạy bất cứ lúc nào để biết đã làm tới đâu và lệnh kế tiếp là gì:

    python scripts/trang_thai.py

Không sửa gì cả, chỉ đọc và báo cáo.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from chanhday.io_utils import read_str_csv  # noqa: E402

XONG, DANG_DO, CHUA = "[x]", "[~]", "[ ]"


def dem_anh(d: Path) -> int:
    from chanhday.config import IMG_EXTS
    return sum(1 for p in d.rglob("*")
               if p.is_file() and p.suffix.lower() in IMG_EXTS) if d.exists() else 0


def main():
    goc = Path.cwd()
    buoc, tiep = [], []

    # --- 0. dữ liệu thô ---
    raw = goc / "data" / "raw"
    n_raw = dem_anh(raw)
    if n_raw:
        buoc.append((XONG, f"Dữ liệu thô: {n_raw} ảnh trong data/raw/"))
    else:
        buoc.append((CHUA, "Dữ liệu thô: chưa có ảnh trong data/raw/"))
        tiep.append('Chép ảnh vào data/raw/, hoặc trỏ --data thẳng vào nơi ảnh '
                    'đang nằm ở các lệnh dưới đây.')

    # --- 1. bảng kê ---
    mf = goc / "data" / "manifest.csv"
    n_mf = 0
    if mf.exists():
        df = read_str_csv(mf)
        n_mf = len(df)
        co_fruit = int((df.get("fruit_id", "").astype(str).str.len() > 0).sum()) \
            if "fruit_id" in df.columns else 0
        co_src = int((df.get("source_id", "").astype(str).str.len() > 0).sum()) \
            if "source_id" in df.columns else 0
        buoc.append((XONG, f"Bảng kê: {n_mf} dòng"))
        buoc.append((XONG if co_fruit == n_mf else (DANG_DO if co_fruit else CHUA),
                     f"Mã quả: {co_fruit}/{n_mf} dòng có fruit_id"))
        buoc.append((XONG if co_src == n_mf else (DANG_DO if co_src else CHUA),
                     f"Mã nguồn: {co_src}/{n_mf} dòng có source_id"))
        if co_fruit < n_mf:
            tiep.append("python scripts/01b_tag_sheets.py --probe --data <thư mục ảnh> "
                        "--out data/tags     # kiểm tra vùng nhãn trước")
            tiep.append("python scripts/01b_tag_sheets.py --data <thư mục ảnh> "
                        "--out data/tags")
            tiep.append("# điền data/tags/fruit_ids.csv, rồi:")
            tiep.append("python scripts/01b_tag_sheets.py --fill-down "
                        "data/tags/fruit_ids.csv")
            tiep.append("python scripts/01b_tag_sheets.py --merge "
                        "data/tags/fruit_ids.csv --manifest data/manifest.csv")
        elif co_src < n_mf:
            tiep.append("Điền cột source_id trong data/manifest.csv theo sổ thu mẫu.")
    else:
        buoc.append((CHUA, "Bảng kê: chưa có data/manifest.csv"))
        tiep.append("python scripts/01_build_manifest.py --data <thư mục ảnh> "
                    "--out data/manifest.csv")

    # --- 1b. trang đọc mã ---
    tags = goc / "data" / "tags" / "fruit_ids.csv"
    if tags.exists():
        t = read_str_csv(tags)
        da_dien = int((t["fruit_id"].astype(str).str.len() > 0).sum()) \
            if "fruit_id" in t.columns else 0
        n_fail = int((t.get("tag_found", "1").astype(str) == "0").sum()) \
            if "tag_found" in t.columns else 0
        trang = len(list((goc / "data" / "tags").glob("sheet_*.png")))
        buoc.append((XONG if da_dien == len(t) else DANG_DO,
                     f"Trang đọc mã: {trang} trang, đã điền {da_dien}/{len(t)} dòng"
                     + (f", {n_fail} ô không dò ra nhãn" if n_fail else "")))

    # --- 2. tiền xử lý ---
    for ten in ("proc_wb", "proc_nowb"):
        pm = goc / "data" / f"{ten}_manifest.csv"
        if pm.exists():
            buoc.append((XONG, f"Tiền xử lý {ten}: {len(read_str_csv(pm))} ảnh"))
        else:
            buoc.append((CHUA, f"Tiền xử lý {ten}: chưa chạy"))
    if n_mf and not (goc / "data" / "proc_wb_manifest.csv").exists():
        tiep.append("python scripts/02_preprocess.py --manifest data/manifest.csv "
                    "--out data/proc_wb --whitebalance patches")

    # --- 3. chia tập ---
    sp = list((goc / "data" / "splits").glob("fruit_seed*")) \
        if (goc / "data" / "splits").exists() else []
    buoc.append((XONG if sp else CHUA,
                 f"Chia tập: {len(sp)} lần chia theo quả" if sp else "Chia tập: chưa chạy"))
    if (goc / "data" / "proc_wb_manifest.csv").exists() and not sp:
        tiep.append("python scripts/03_split.py --manifest "
                    "data/proc_wb_manifest.csv --mode audit")
        tiep.append("python scripts/03_split.py --manifest "
                    "data/proc_wb_manifest.csv --mode fruit --seed 0")

    # --- 4, 5, 6 ---
    out = goc / "outputs"
    kq = list(out.glob("*/metrics.json")) if out.exists() else []
    buoc.append((XONG if kq else CHUA,
                 f"Kết quả đánh giá: {len(kq)} cấu hình" if kq
                 else "Kết quả đánh giá: chưa có"))
    if sp and not kq:
        tiep.append("python scripts/04_color_baseline.py --split-dir "
                    "data/splits/fruit_seed0 --out outputs/baseline_seed0")
        tiep.append("python scripts/06_evaluate.py --pred "
                    "outputs/baseline_seed0/predictions.csv --out outputs/baseline_seed0")

    # --- in ---
    print("=" * 68)
    print(f"TRẠNG THÁI PIPELINE   ({goc})")
    print("=" * 68)
    for dau, mo_ta in buoc:
        print(f"  {dau} {mo_ta}")

    print("\n" + "-" * 68)
    if tiep:
        print("VIỆC TIẾP THEO")
        print("-" * 68)
        i = 0
        for lenh in tiep:
            if lenh.startswith("#"):
                print(f"     {lenh}")
            else:
                i += 1
                print(f"  {i}. {lenh}")
    else:
        print("Không có bước nào đang chờ. Xem README.md để biết các bước còn lại.")
    print("-" * 68)


if __name__ == "__main__":
    main()
