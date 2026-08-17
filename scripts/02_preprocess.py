#!/usr/bin/env python3
"""
02 — TIỀN XỬ LÝ ẢNH (mục 3.4.3)

Ba bước theo đúng thứ tự báo cáo mô tả:
    1. Hiệu chỉnh màu theo 4 ô xám trên thẻ chuẩn (von Kries)
    2. Tách vùng quả khỏi nền, tạo mặt nạ nhị phân
    3. Cắt theo hộp bao thành phần liên thông lớn nhất

CHẠY HAI LẦN để phục vụ thí nghiệm ở mục 3.5 và 4.4:

    python scripts/02_preprocess.py --manifest data/manifest.csv \
           --out data/proc_wb   --whitebalance patches
    python scripts/02_preprocess.py --manifest data/manifest.csv \
           --out data/proc_nowb --whitebalance none

Chênh lệch hiệu năng giữa hai bộ chính là con số tách "phần biến thiên do
chiếu sáng" khỏi "phần do khác biệt giống và điều kiện canh tác".

Thêm --use-raw nếu có file CR3/NEF: đo màu trên RAW tuyến tính chính xác hơn
JPEG đã qua cân bằng trắng và ánh xạ tông của máy.
"""
from __future__ import annotations

import argparse
import sys
from collections import defaultdict
from pathlib import Path

import cv2
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from chanhday.cards import (angular_error, apply_von_kries,  # noqa: E402
                            illuminant_from_patches, illuminant_gray_world,
                            linearity_check, roi_mask, sample_gray_patches)
from chanhday.config import CFG, RAW_EXTS  # noqa: E402
from chanhday.io_utils import (check_ascii_paths, count_files,  # noqa: E402
                               imread_unicode, imwrite_unicode,
                               read_raw_linear, read_str_csv, save_json,
                               unique_stem, write_csv)
from chanhday.segmentation import crop_to_mask, segment_fruit  # noqa: E402

import pandas as pd  # noqa: E402


def build_montage(demo, path, height=260):
    """Hình 2 của báo cáo: ảnh gốc | mặt nạ | ảnh cắt."""
    def fit(im):
        if im.ndim == 2:
            im = cv2.cvtColor(im, cv2.COLOR_GRAY2BGR)
        s = height / im.shape[0]
        return cv2.resize(im, (int(im.shape[1] * s), height))

    rows = [np.hstack([fit(o), fit(m), fit(c)]) for o, m, c in demo]
    wmax = max(r.shape[1] for r in rows)
    rows = [cv2.copyMakeBorder(r, 0, 4, 0, wmax - r.shape[1],
                               cv2.BORDER_CONSTANT, value=(255, 255, 255))
            for r in rows]
    imwrite_unicode(path, np.vstack(rows))
    print(f"[đã ghi] {path}   (dùng làm Hình 2)")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--manifest", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--whitebalance",
                    choices=["patches", "grayworld", "none"], default="patches")
    ap.add_argument("--use-raw", action="store_true")
    ap.add_argument("--size", type=int, default=None)
    ap.add_argument("--keep-bg", action="store_true")
    ap.add_argument("--limit", type=int, default=0, help="chỉ xử lý N ảnh đầu, để thử")
    args = ap.parse_args()

    size = args.size or CFG.thresholds.output_size
    lay = CFG.layout
    df = read_str_csv(args.manifest)
    if args.limit:
        df = df.head(args.limit)

    check_ascii_paths(df["image_path"].tolist())

    outroot = Path(args.out)
    stats = {"tong": 0, "doc_duoc": 0, "do_the": 0,
             "tach_nen_thanh_cong": 0, "that_bai": []}
    rows, demo, ang_before, ang_after, r2s = [], [], [], [], []

    # Sổ kế toán từng lớp: vào bao nhiêu, rớt ở bước nào, ra bao nhiêu.
    # Bảng này tồn tại để mất ảnh không bao giờ diễn ra âm thầm nữa.
    ledger = defaultdict(lambda: {"vao": 0, "loi_doc": 0, "loi_tach_nen": 0, "ra": 0})

    for _, r in df.iterrows():
        src = Path(str(r["image_path"]))
        lab = str(r.get("label", "") or "(chua_gan_nhan)")
        stats["tong"] += 1
        ledger[lab]["vao"] += 1

        raw_p = str(r.get("raw_path", "") or "")
        la_raw_goc = src.suffix.lower() in RAW_EXTS
        bgr = None

        # Ảnh gốc là file RAW (không có JPG đi kèm) thì buộc phải giải mã RAW,
        # vì cv2 không đọc được CR3/NEF/ARW.
        if la_raw_goc or (args.use_raw and raw_p and Path(raw_p).exists()):
            nguon = str(src) if la_raw_goc else raw_p
            try:
                bgr, _ = read_raw_linear(nguon)
            except ImportError:
                if la_raw_goc:
                    stats["that_bai"].append(f"{src.name}: cần rawpy để đọc RAW")
                    ledger[lab]["loi_doc"] += 1
                    continue
                print(f"  (chưa cài rawpy, dùng JPEG cho {src.name})")
            except Exception as e:
                print(f"  (RAW lỗi {src.name}: {e})")
                if la_raw_goc:
                    stats["that_bai"].append(f"{src.name}: giải mã RAW thất bại")
                    ledger[lab]["loi_doc"] += 1
                    continue
        if bgr is None:
            bgr = imread_unicode(src)
        if bgr is None:
            stats["that_bai"].append(f"{src.name}: không đọc được")
            ledger[lab]["loi_doc"] += 1
            continue
        stats["doc_duoc"] += 1
        orig = bgr.copy()

        ill_used = None
        if args.whitebalance == "patches":
            patches = sample_gray_patches(bgr, lay, CFG.thresholds.saturation_ceiling)
            ok = np.isfinite(patches).all(axis=1).sum()
            if ok >= 2:
                stats["do_the"] += 1
                ill_used = illuminant_from_patches(patches)
                ang_before.append(angular_error(ill_used))
                r2s.append(linearity_check(patches)["r2"])
                bgr = apply_von_kries(bgr, ill_used)
                ang_after.append(angular_error(
                    illuminant_from_patches(sample_gray_patches(bgr, lay))))
        elif args.whitebalance == "grayworld":
            ill_used = illuminant_gray_world(bgr, p=6)
            bgr = apply_von_kries(bgr, ill_used)

        # Loại TOÀN BỘ vùng thẻ khỏi ứng viên: thẻ sáng hơn phông nên thuật
        # toán có lúc chọn nhầm chính cái thẻ làm quả.
        mask = segment_fruit(bgr, roi_mask(bgr.shape, lay.card_roi))
        if mask is None:
            stats["that_bai"].append(f"{src.name}: không tách được nền")
            ledger[lab]["loi_tach_nen"] += 1
            continue
        stats["tach_nen_thanh_cong"] += 1

        crop = crop_to_mask(bgr, mask, black_bg=not args.keep_bg)
        if crop is None or crop.size == 0:
            stats["that_bai"].append(f"{src.name}: hộp bao rỗng")
            ledger[lab]["loi_tach_nen"] += 1
            continue
        crop = cv2.resize(crop, (size, size), interpolation=cv2.INTER_AREA)

        # Quả hỏng đi vào thư mục riêng, không trộn vào các bậc chín
        cond = str(r.get("tinh_trang", "") or "")
        label = "_hong" if cond == "hong" else str(r.get("label", "") or "chua_gan_nhan")
        dst = outroot / label / f"{unique_stem(src)}.jpg"
        if not imwrite_unicode(dst, crop, [cv2.IMWRITE_JPEG_QUALITY, 95]):
            stats["that_bai"].append(f"{src.name}: ghi file thất bại")
            continue
        ledger[lab]["ra"] += 1

        rr = dict(r)
        rr["proc_path"] = str(dst)
        rr["fruit_area_px"] = int((mask > 0).sum())
        if ill_used is not None:
            rr["ill_b"], rr["ill_g"], rr["ill_r"] = [float(v) for v in ill_used]
        rows.append(rr)

        if len(demo) < 4:
            demo.append((orig, mask, crop))

    if demo:
        build_montage(demo, outroot.parent / f"{outroot.name}_hinh2_montage.jpg")

    write_csv(pd.DataFrame(rows), outroot.parent / f"{outroot.name}_manifest.csv")

    n = max(stats["doc_duoc"], 1)
    stats["ty_le_do_the_pc"] = round(100 * stats["do_the"] / n, 2)
    stats["ty_le_tach_nen_thanh_cong_pc"] = round(100 * stats["tach_nen_thanh_cong"] / n, 2)
    if ang_before:
        stats["sai_so_goc_truoc_hieu_chinh_do"] = round(float(np.mean(ang_before)), 3)
        stats["sai_so_goc_sau_hieu_chinh_do"] = round(float(np.mean(ang_after)), 3)
        stats["do_tuyen_tinh_r2_tb"] = round(float(np.nanmean(r2s)), 4)
    stats["so_anh_that_bai"] = len(stats["that_bai"])
    stats["that_bai"] = stats["that_bai"][:50]
    save_json(stats, outroot.parent / f"{outroot.name}_stats.json")

    # ---------------- Sổ kế toán vào / ra ----------------
    led = pd.DataFrame([{"lop": k, **v} for k, v in sorted(ledger.items())])
    if not led.empty:
        led["mat"] = led["vao"] - led["ra"]
        led["ty_le_giu_lai_pc"] = (100 * led["ra"] / led["vao"].clip(lower=1)).round(1)
        write_csv(led, outroot.parent / f"{outroot.name}_ledger.csv")
        print("\n" + "=" * 68)
        print("SỔ KẾ TOÁN ẢNH: VÀO BAO NHIÊU, RA BAO NHIÊU, RỚT Ở ĐÂU")
        print("=" * 68)
        print(led.to_string(index=False))
        tong_vao, tong_ra = int(led["vao"].sum()), int(led["ra"].sum())
        tren_dia = count_files(outroot)
        print("-" * 68)
        print(f"TỔNG: vào {tong_vao} ảnh, ra {tong_ra} ảnh, mất {tong_vao - tong_ra}")
        print(f"Đếm lại file thật trên đĩa: {tren_dia}")

        # Kiểm tra chéo. Sổ kế toán đếm số lần ghi thành công, còn đây đếm
        # số file thực sự tồn tại. Hai số lệch nhau nghĩa là có ảnh đè lên
        # ảnh khác — loại lỗi mà chính sổ kế toán không phát hiện được.
        if tren_dia != tong_ra:
            print("\n" + "!" * 68)
            print(f"XUNG ĐỘT TÊN FILE: ghi {tong_ra} lần nhưng chỉ còn {tren_dia} file.")
            print("Có ảnh đã đè lên ảnh khác. Báo lỗi này cho người viết script.")
            print("!" * 68)

        if tong_ra < tong_vao:
            print("\nĐỌC BẢNG TRÊN TRƯỚC KHI CHẠY TIẾP.")
            print("Ảnh mất ở đây sẽ không bao giờ xuất hiện ở các bước sau, và")
            print("nếu không để ý thì đến bước đánh giá mới phát hiện tập kiểm")
            print("tra chỉ còn vài ảnh.")
            if int(led["loi_doc"].sum()):
                n_raw = sum(1 for t in stats["that_bai"] if "rawpy" in t)
                print(f"  - loi_doc = {int(led['loi_doc'].sum())}: không đọc được file.")
                if n_raw:
                    print(f"    Trong đó {n_raw} file là ảnh RAW mà chưa cài rawpy:")
                    print("        pip install rawpy")
                else:
                    print("    File hỏng hoặc đường dẫn sai. "
                          "Đường dẫn có dấu đã được xử lý.")
            if int(led["loi_tach_nen"].sum()):
                print(f"  - loi_tach_nen = {int(led['loi_tach_nen'].sum())}: "
                      f"không tìm thấy vùng quả. Chạy scripts/00_calibrate_layout.py")
                print("    để kiểm tra card_roi, hoặc giảm min_fruit_area_frac.")
        if tong_ra < 0.9 * tong_vao:
            print("\nMất trên 10% số ảnh. KHÔNG nên chạy tiếp trước khi tìm ra nguyên nhân.")

    print(f"\nTổng ảnh:              {stats['tong']}")
    print(f"Đọc được thẻ:          {stats['ty_le_do_the_pc']}%")
    print(f"Tách nền thành công:   {stats['ty_le_tach_nen_thanh_cong_pc']}%   <-- mục 4.1")
    if ang_before:
        print(f"Ám màu trước hiệu chỉnh: {stats['sai_so_goc_truoc_hieu_chinh_do']}° "
              f"-> sau: {stats['sai_so_goc_sau_hieu_chinh_do']}°")


if __name__ == "__main__":
    main()
