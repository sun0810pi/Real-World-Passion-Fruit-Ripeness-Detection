#!/usr/bin/env python3
"""
KIỂM KÊ — đối chiếu số ảnh thực tế với số bạn nghĩ mình có

Dùng khi con số script báo không khớp với con số bạn nhớ:

    python scripts/kiem_ke.py --data "D:\\qua_chanh"
    python scripts/kiem_ke.py --data "D:\\qua_chanh" --so-qua-mong-doi 210

Chỉ đọc và đếm, không sửa gì. Quét TOÀN BỘ cây thư mục, kể cả những nhánh
mà script 01 bỏ qua, nên phát hiện được ảnh nằm ngoài đường dẫn --data mà
bạn đang dùng.
"""
from __future__ import annotations

import argparse
import collections
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from chanhday.config import (CONDITION_DIR_ALIASES, IMG_EXTS,  # noqa: E402
                             RAW_EXTS)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", required=True)
    ap.add_argument("--so-qua-mong-doi", type=int, default=0,
                    help="số quả bạn nghĩ mình có, để đối chiếu")
    ap.add_argument("--sau", type=int, default=2, help="độ sâu thư mục hiển thị")
    args = ap.parse_args()

    root = Path(args.data)
    if not root.exists():
        raise SystemExit(f"Không có thư mục: {root.resolve()}")

    anh, raw, khac = [], [], collections.Counter()
    for p in root.rglob("*"):
        if not p.is_file():
            continue
        e = p.suffix.lower()
        if e in IMG_EXTS:
            anh.append(p)
        elif e in RAW_EXTS:
            raw.append(p)
        else:
            khac[e or "(không đuôi)"] += 1

    print("=" * 70)
    print(f"KIỂM KÊ: {root.resolve()}")
    print("=" * 70)
    print(f"  Ảnh thường (jpg/png/...):   {len(anh)}")
    print(f"  File RAW (cr3/nef/...):     {len(raw)}")
    if khac:
        print(f"  File khác:                  {sum(khac.values())}  "
              + ", ".join(f"{k}:{v}" for k, v in khac.most_common(5)))

    stem_anh = {p.stem for p in anh}
    stem_raw = {p.stem for p in raw}
    chi_raw = stem_raw - stem_anh
    tong_lan_chup = len(stem_anh | stem_raw)

    print(f"\n  Số LẦN CHỤP riêng biệt:     {tong_lan_chup}")
    print(f"    có ảnh thường:            {len(stem_anh)}")
    print(f"    CHỈ có RAW:               {len(chi_raw)}"
          + ("   <-- script 01 bỏ qua, trừ khi dùng --include-raw"
             if chi_raw else ""))

    # ---------------- theo thư mục ----------------
    print("\n" + "-" * 70)
    print("PHÂN BỐ THEO THƯ MỤC")
    theo = collections.defaultdict(lambda: collections.Counter())
    for p in anh + raw:
        rel = p.relative_to(root)
        k = "/".join(rel.parts[:args.sau - 1]) if len(rel.parts) > 1 else "(gốc)"
        theo[k]["anh" if p.suffix.lower() in IMG_EXTS else "raw"] += 1

    print(f"  {'thư mục':<44}{'ảnh':>8}{'raw':>8}")
    for k in sorted(theo):
        print(f"  {k[:43]:<44}{theo[k]['anh']:>8}{theo[k]['raw']:>8}")

    # ---------------- thư mục quả hỏng ----------------
    hong = [p for p in anh
            if any(x.strip().lower() in CONDITION_DIR_ALIASES
                   for x in p.relative_to(root).parts)]
    if hong:
        print(f"\n  Trong đó nằm ở thư mục quả hỏng: {len(hong)} ảnh")
        print("  (đưa sang cột tinh_trang, KHÔNG tính là bậc chín thứ sáu)")

    # ---------------- đối chiếu ----------------
    print("\n" + "-" * 70)
    print("ĐỐI CHIẾU")
    if args.so_qua_mong_doi:
        q = args.so_qua_mong_doi
        print(f"  Bạn khai có {q} quả.")
        print(f"  Với {tong_lan_chup} lần chụp, trung bình "
              f"{tong_lan_chup / q:.1f} ảnh mỗi quả.")
        if tong_lan_chup < q:
            print(f"\n  BẤT THƯỜNG: số lần chụp ({tong_lan_chup}) ÍT HƠN số quả ({q}).")
            print("  Mỗi quả phải có ít nhất một ảnh, nên khả năng cao là")
            print("  --data đang trỏ vào một phần dữ liệu, không phải toàn bộ.")
            print("  Thử trỏ lên thư mục cha một cấp rồi chạy lại.")
        elif tong_lan_chup < 2 * q:
            print(f"\n  Trung bình dưới 2 ảnh mỗi quả. Nếu bạn chụp mỗi quả")
            print("  nhiều tư thế thì một phần dữ liệu đang nằm ngoài --data.")
    else:
        print("  Thêm --so-qua-mong-doi <số> để đối chiếu với số quả bạn có.")

    print("\n  Nhắc lại đơn vị đếm, vì đây là chỗ hay nhầm:")
    print("    - bảng kê manifest.csv: mỗi dòng là MỘT ẢNH")
    print("    - cỡ mẫu thống kê của nghiên cứu: số QUẢ riêng biệt")
    print("    - một quả chụp 6 tư thế cho 6 dòng bảng kê nhưng vẫn là 1 quả")

    if chi_raw:
        print("\n" + "!" * 70)
        print(f"{len(chi_raw)} lần chụp chỉ có RAW. Muốn dùng chúng:")
        print("    pip install rawpy")
        print(f'    python scripts/01_build_manifest.py --data "{root}" '
              f'--out data/manifest.csv --include-raw')
        print("!" * 70)


if __name__ == "__main__":
    main()
