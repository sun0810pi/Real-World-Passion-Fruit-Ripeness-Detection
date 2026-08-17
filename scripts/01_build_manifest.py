#!/usr/bin/env python3
"""
01 — LẬP BẢNG KÊ DỮ LIỆU

Quét toàn bộ ảnh, đọc EXIF, tìm file RAW đi kèm, đoán nhãn từ tên thư mục,
rồi in báo cáo kiểm toán.

    python scripts/01_build_manifest.py --data data/raw --out data/manifest.csv

Sau bước này, cột fruit_id và source_id thường vẫn trống. Chạy tiếp script
01b để điền nhanh bằng mã viết tay trong khung hình.
"""
from __future__ import annotations

import argparse
import sys
from collections import Counter
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from chanhday.config import (CLASS_NAMES, CLASS_TO_IDX,  # noqa: E402
                             IMG_EXTS, RAW_EXTS,
                             CONDITION_DIR_ALIASES)
from chanhday.io_utils import (chan_doan_thu_muc,  # noqa: E402
                               check_ascii_paths, ensure_columns,
                               find_raw_sibling, guess_fruit_id,
                               guess_source_id, iter_images, read_exif,
                               write_csv)


def infer_label(path: Path, root: Path):
    """
    Trả về (label, tinh_trang) suy từ tên thư mục.

    Thư mục quả hỏng KHÔNG được coi là bậc chín thứ sáu. Nó cho
    tinh_trang='hong' và label rỗng, vì tình trạng là trục riêng.
    """
    parts = [p.strip().lower() for p in path.relative_to(root).parts]

    for part in reversed(parts):
        if part in CONDITION_DIR_ALIASES:
            return "", "hong"

    for part in reversed(path.relative_to(root).parts):
        if part in CLASS_NAMES:
            return part, ""

    for part in reversed(parts):
        for c in CLASS_NAMES:
            if part.startswith(c.split("_")[0] + "_") or part == c.split("_")[0]:
                return c, ""
    return "", ""


def bao_cao_thu_muc(root: Path, df, all_paths):
    """
    Bảng đối chiếu từng thư mục con: có bao nhiêu file, bao nhiêu ảnh được nhận.

    Đây là bảng quan trọng nhất của script. Con số tổng cộng tự nó không cho
    biết ảnh bị bỏ ở đâu, mà nguyên nhân phổ biến nhất là trỏ --data vào một
    thư mục con thay vì thư mục gốc, hoặc một nhánh nào đó chỉ có file RAW.
    """
    import collections

    nhan = collections.Counter()
    for p in all_paths:
        rel = p.relative_to(root)
        nhan[rel.parts[0] if len(rel.parts) > 1 else "(gốc)"] += 1

    tat_ca = collections.Counter()
    duoi_khac = collections.defaultdict(collections.Counter)
    for p in root.rglob("*"):
        if not p.is_file():
            continue
        rel = p.relative_to(root)
        k = rel.parts[0] if len(rel.parts) > 1 else "(gốc)"
        tat_ca[k] += 1
        if p.suffix.lower() not in IMG_EXTS:
            duoi_khac[k][p.suffix.lower() or "(không đuôi)"] += 1

    print("\n" + "-" * 64)
    print("THEO TỪNG THƯ MỤC CON")
    print(f"  {'thư mục':<34}{'ảnh nhận':>10}{'tổng file':>11}")
    for k in sorted(tat_ca):
        co = nhan.get(k, 0)
        canh = "   <-- KHÔNG NHẬN ẢNH NÀO" if co == 0 else ""
        print(f"  {k[:33]:<34}{co:>10}{tat_ca[k]:>11}{canh}")
        if co == 0 and duoi_khac[k]:
            top = ", ".join(f"{e}:{n}" for e, n in duoi_khac[k].most_common(4))
            print(f"  {'':<34}đuôi có trong đó: {top}")


def bao_cao_raw_don_le(root: Path):
    """
    Đếm những lần chụp CHỈ có file RAW, không có JPG đi kèm.

    Script mặc định chỉ quét ảnh thường, nên các lần chụp này biến mất khỏi
    bảng kê mà không có thông báo nào. Trên thư mục mẫu ngày 14/8/2026, tỷ lệ
    này là 4/19, tức hơn hai mươi phần trăm số lần chụp.
    """
    jpg = {p.stem for p in root.rglob("*")
           if p.is_file() and p.suffix.lower() in IMG_EXTS}
    raw = {p.stem for p in root.rglob("*")
           if p.is_file() and p.suffix.lower() in RAW_EXTS}
    thieu = sorted(raw - jpg)
    if not thieu:
        return 0

    print("\n" + "!" * 64)
    print(f"{len(thieu)} lần chụp CHỈ CÓ FILE RAW, không có JPG đi kèm.")
    print("Những lần chụp này KHÔNG nằm trong bảng kê ở trên.")
    print("Ví dụ: " + ", ".join(thieu[:8]) + ("..." if len(thieu) > 8 else ""))
    tong = len(jpg) + len(thieu)
    print(f"Nếu tính cả chúng, tổng số lần chụp là {tong} thay vì {len(jpg)}"
          f"  ({100 * len(thieu) / max(tong, 1):.0f}% đang bị bỏ).")
    print("\nHai cách:")
    print("  - Chạy lại với --include-raw để đưa luôn file RAW vào bảng kê")
    print("    (cần cài rawpy, và bước tiền xử lý sẽ giải mã RAW trực tiếp)")
    print("  - Hoặc xuất JPG cho các lần chụp đó từ phần mềm của máy ảnh")
    print("!" * 64)
    return len(thieu)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", required=True)
    ap.add_argument("--out", default="data/manifest.csv")
    ap.add_argument("--no-exif", action="store_true")
    ap.add_argument("--include-raw", action="store_true",
                    help="đưa cả file RAW không có JPG đi kèm vào bảng kê")
    args = ap.parse_args()

    root = Path(args.data)
    all_paths = list(iter_images(root))

    if args.include_raw:
        co_jpg = {p.stem for p in all_paths}
        them = [p for p in root.rglob("*")
                if p.is_file() and p.suffix.lower() in RAW_EXTS
                and p.stem not in co_jpg]
        if them:
            print(f"Thêm {len(them)} file RAW không có JPG đi kèm.")
            all_paths = sorted(all_paths + them)

    check_ascii_paths(all_paths)

    rows = []
    for p in all_paths:
        rel = p.relative_to(root)
        lab, cond = infer_label(p, root)
        la_raw = p.suffix.lower() in RAW_EXTS
        rows.append({
            "image_path": str(p),
            "label": lab,
            "tinh_trang": cond,
            "old_split": rel.parts[0] if rel.parts[0] in ("train", "val", "test") else "",
            "fruit_id": guess_fruit_id(p.stem),
            "source_id": guess_source_id(p.stem),
            "raw_path": str(p) if la_raw else find_raw_sibling(p),
            "session_id": rel.parts[0] if len(rel.parts) > 1 else "",
            **({} if args.no_exif or la_raw else read_exif(p)),
        })

    if not rows:
        raise SystemExit(chan_doan_thu_muc(root))

    df = ensure_columns(pd.DataFrame(rows))
    df["label_idx"] = df["label"].map(CLASS_TO_IDX).fillna(-1).astype(int)
    if not args.no_exif:
        ct = df["capture_time"].astype(str)
        df.loc[ct.str.len() >= 10, "session_id"] = ct.str.slice(0, 10)
    write_csv(df[[c for c in df.columns]], args.out)

    # ------------------------- kiểm toán -------------------------
    n = len(df)
    print("\n" + "=" * 64)
    print("KIỂM TOÁN DỮ LIỆU")
    print("=" * 64)
    print(f"Tổng số ẢNH:               {n}")
    print("  (mỗi dòng bảng kê là MỘT ẢNH, không phải một quả.")
    print("   Một quả chụp nhiều tư thế sẽ chiếm nhiều dòng.)")
    print(f"Ảnh có file RAW đi kèm:    {(df.raw_path.astype(str).str.len() > 0).sum()}")

    nf = df.loc[df.fruit_id.astype(str).str.len() > 0, "fruit_id"].nunique()
    ns = df.loc[df.source_id.astype(str).str.len() > 0, "source_id"].nunique()
    print(f"Số quả nhận ra:            {nf}" + ("   <-- TRỐNG, chạy script 01b" if not nf else ""))
    print(f"Số nguồn nhận ra:          {ns}" + ("   <-- TRỐNG, phải điền tay" if not ns else ""))

    cams = df.loc[df.camera_model.astype(str).str.len() > 0, "camera_model"].value_counts()
    if len(cams):
        print("\nThiết bị chụp:")
        for k, v in cams.items():
            print(f"  {k:<40} {v}")
        if any(x in " ".join(cams.index).lower()
               for x in ("canon", "nikon", "sony", "fujifilm")):
            print("  LƯU Ý: đây là máy ảnh chuyên dụng, không phải điện thoại.")
            print("  Tên đề tài và mục 3.4.2 phải nói đúng thiết bị đã dùng.")

    print("\nPhân bố theo bậc chín:")
    cnt = Counter(df["label"])
    mx = max([v for k, v in cnt.items() if k] or [1])
    for c in CLASS_NAMES:
        k = cnt.get(c, 0)
        flag = "  <-- QUÁ ÍT" if 0 < k < 60 else ("  <-- TRỐNG" if k == 0 else "")
        print(f"  {c:<22} {k:>5}  {'#' * int(35 * k / mx)}{flag}")
    n_hong = int((df["tinh_trang"] == "hong").sum())
    n_chua = int((df["label"].astype(str).str.len() == 0).sum()) - n_hong
    if n_hong:
        print(f"  {'(hỏng — trục riêng)':<22} {n_hong:>5}")
        print("    Thư mục quả hỏng được đưa sang cột 'tinh_trang', KHÔNG coi là")
        print("    bậc chín thứ sáu. Xem docs/thiet_ke_hai_dau_ra.md để biết vì sao.")
    if n_chua > 0:
        print(f"  {'(chưa gán nhãn)':<22} {n_chua:>5}")

    thieu = [c for c in CLASS_NAMES if cnt.get(c, 0) == 0]
    if thieu:
        print(f"\nCẢNH BÁO: {len(thieu)} bậc KHÔNG có ảnh nào: {', '.join(thieu)}")
        print("Kiểm tra xem thư mục các bậc này có nằm trong --data không.")
        print("Bậc trống sẽ khiến YOLO huấn luyện với số lớp ít hơn 5, và mọi")
        print("chỉ số theo bậc sau đó không so sánh được giữa các lần chạy.")

    if nf:
        per = df[df.fruit_id.astype(str).str.len() > 0].groupby("fruit_id").size()
        print(f"\nSố ảnh mỗi quả: trung bình {per.mean():.1f}, "
              f"ít nhất {per.min()}, nhiều nhất {per.max()}")
        print(f"=> CỠ MẪU THỰC là {nf} quả, không phải {n} ảnh.")

        if df["old_split"].nunique() > 1:
            g = df[df.fruit_id.astype(str).str.len() > 0].groupby("fruit_id")["old_split"].nunique()
            leak = int((g > 1).sum())
            if leak:
                print(f"\nRÒ RỈ: {leak}/{len(g)} quả có ảnh ở cả train lẫn val "
                      f"trong phép chia cũ ({100*leak/len(g):.0f}%).")
                print("Đây là nguyên nhân của độ chính xác cao giả tạo. Chia lại theo quả.")

    bao_cao_thu_muc(root, df, all_paths)
    if not args.include_raw:
        bao_cao_raw_don_le(root)

    print("\n" + "=" * 64)
    print("BƯỚC TIẾP: python scripts/01b_tag_sheets.py --probe --data", args.data,
          "--out data/tags")


if __name__ == "__main__":
    main()
