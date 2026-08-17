#!/usr/bin/env python3
"""
00 — DÒ BỐ CỤC THẺ CHUẨN

Chạy script này ĐẦU TIÊN mỗi khi đổi máy ảnh, đổi khoảng cách chụp, hoặc
đổi vị trí đặt thẻ. Nó sinh ảnh kiểm tra để bạn xác nhận bằng mắt rằng
chương trình đang đo đúng chỗ.

    python scripts/00_calibrate_layout.py --data data/raw/Chieu_4
    python scripts/00_calibrate_layout.py --data data/raw/Chieu_4 \
           --patch-x0 0.67 --patch-dx 0.016 --save-layout configs/layout_dienthoai.yaml

Mở outputs/layout_check.jpg: ô đỏ phải trùm đúng 4 ô xám, ô xanh trùm
mảnh giấy ghi mã quả.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import cv2
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from chanhday.cards import (angular_error, illuminant_from_patches,  # noqa: E402
                            linearity_check, sample_gray_patches)
from chanhday.config import CFG, CardLayout  # noqa: E402
from chanhday.io_utils import (chan_doan_thu_muc,  # noqa: E402
                               imread_unicode, imwrite_unicode,
                               iter_images, save_json)


def draw_check(bgr, layout: CardLayout):
    vis = bgr.copy()
    h, w = vis.shape[:2]

    x, y, rw, rh = layout.card_roi
    cv2.rectangle(vis, (int(x * w), int(y * h)),
                  (int((x + rw) * w), int((y + rh) * h)), (0, 255, 255), 6)

    for i, (a, b, c, d) in enumerate(layout.patch_boxes(vis.shape)):
        cv2.rectangle(vis, (a, b), (c, d), (0, 0, 255), 4)
        cv2.putText(vis, str(i + 1), (a, b - 8),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.4, (0, 0, 255), 3)

    x, y, rw, rh = layout.tag_roi
    cv2.rectangle(vis, (int(x * w), int(y * h)),
                  (int((x + rw) * w), int((y + rh) * h)), (0, 255, 0), 6)
    return vis


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", required=True)
    ap.add_argument("--out", default="outputs")
    ap.add_argument("--n", type=int, default=3, help="số ảnh dùng để kiểm tra")
    ap.add_argument("--card-roi", default="")
    ap.add_argument("--tag-roi", default="")
    ap.add_argument("--patch-y", default="")
    ap.add_argument("--patch-x0", type=float, default=None)
    ap.add_argument("--patch-dx", type=float, default=None)
    ap.add_argument("--patch-w", type=float, default=None)
    ap.add_argument("--save-layout", default="")
    args = ap.parse_args()

    lay = CFG.layout
    if args.card_roi:
        lay.card_roi = tuple(float(v) for v in args.card_roi.split(","))
    if args.tag_roi:
        lay.tag_roi = tuple(float(v) for v in args.tag_roi.split(","))
    if args.patch_y:
        lay.patch_y = tuple(float(v) for v in args.patch_y.split(","))
    for k in ("patch_x0", "patch_dx", "patch_w"):
        v = getattr(args, k)
        if v is not None:
            setattr(lay, k, v)

    paths = [p for p in iter_images(args.data)][: args.n]
    if not paths:
        raise SystemExit(chan_doan_thu_muc(args.data))

    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    report = []

    tiles = []
    for p in paths:
        bgr = imread_unicode(p)
        if bgr is None:
            continue
        patches = sample_gray_patches(bgr, lay)
        ill = illuminant_from_patches(patches)
        lin = linearity_check(patches)
        err = angular_error(ill)

        vis = draw_check(bgr, lay)
        s = 900 / vis.shape[1]
        tiles.append(cv2.resize(vis, None, fx=s, fy=s))

        report.append({
            "anh": p.name,
            "gia_tri_4_o_BGR": [[round(float(v), 1) for v in row] for row in patches],
            "nguon_sang_BGR": [round(float(v), 4) for v in ill],
            "sai_so_goc_so_voi_trung_tinh_do": round(err, 2),
            "do_tuyen_tinh_r2": round(lin["r2"], 4),
        })
        print(f"{p.name}: sai số góc {err:.2f}°, tuyến tính R²={lin['r2']:.4f}")

    if tiles:
        imwrite_unicode(out / "layout_check.jpg", np.vstack(tiles))
        print(f"\n[đã ghi] {out/'layout_check.jpg'}")
        print("MỞ ẢNH NÀY RA XEM. Ô đỏ phải trùm đúng 4 ô xám, ô xanh lá trùm")
        print("mảnh giấy ghi mã quả. Sai thì chỉnh --patch-x0 / --patch-dx rồi chạy lại.")

    save_json({"bo_cuc": lay.__dict__, "ket_qua": report}, out / "layout_check.json")

    errs = [r["sai_so_goc_so_voi_trung_tinh_do"] for r in report]
    if errs:
        print(f"\nSai số góc trung bình: {np.mean(errs):.2f}°")
        if np.mean(errs) > 3:
            print("  => Ảnh có ám màu rõ. Bước hiệu chỉnh theo thẻ là bắt buộc,")
            print("     vì ám màu này đội thẳng vào kênh a* dùng để đo độ chín.")
        if np.std(errs) < 0.2 and len(errs) > 1:
            print("  => Chiếu sáng gần như không đổi giữa các ảnh. Tốt cho việc đo màu,")
            print("     nhưng KHÔNG đủ đa dạng để huấn luyện tầng ước lượng môi trường.")

    r2 = [r["do_tuyen_tinh_r2"] for r in report]
    if r2 and np.nanmean(r2) < 0.97:
        print(f"\nĐáp ứng phi tuyến (R²={np.nanmean(r2):.3f}). Ảnh JPEG đã qua ánh xạ")
        print("tông. Nên chuyển sang dùng file RAW để đo màu chính xác.")

    if args.save_layout:
        import yaml
        Path(args.save_layout).parent.mkdir(parents=True, exist_ok=True)
        with open(args.save_layout, "w", encoding="utf-8") as f:
            yaml.safe_dump({"layout": lay.__dict__}, f, allow_unicode=True)
        print(f"[đã ghi] {args.save_layout}")


if __name__ == "__main__":
    main()
