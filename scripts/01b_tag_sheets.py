#!/usr/bin/env python3
"""
01b — ĐỌC MÃ QUẢ TỪ NHÃN GIẤY TRONG KHUNG HÌNH

Mã quả được viết tay trên mảnh giấy dán trong khung hình. Đây chính là
`fruit_id`, thứ khoá toàn bộ việc chia tập không rò rỉ.

Script không đọc chữ viết tay tự động, vì nhận dạng chữ số viết tay xoay
ngược sai khá nhiều, mà một mã sai thì kéo theo rò rỉ dữ liệu. Thay vào đó
nó cắt đúng vùng nhãn của mọi ảnh, xoay lại cho đúng chiều, ghép thành các
trang liên hoàn để đọc và điền hàng loạt.

Vị trí nhãn được DÒ TỰ ĐỘNG trên từng ảnh chứ không dùng một toạ độ cố định,
vì khoảng cách chụp thay đổi giữa các đợt. Ô nào dò không ra sẽ được đánh
viền đỏ trên trang và ghi tag_found=0 trong file — TUYỆT ĐỐI KHÔNG ĐOÁN MÃ
cho các ô đó.

Quy trình:

    # 1. Kiểm tra vùng nhãn có cắt đúng không, trước khi làm cả nghìn ảnh
    python scripts/01b_tag_sheets.py --probe --data data/raw --out data/tags

    # 2. Sinh trang và file điền
    python scripts/01b_tag_sheets.py --data data/raw --out data/tags

    # 3. Mở data/tags/sheet_00.png, điền cột fruit_id trong fruit_ids.csv.
    #    Chỉ cần điền dòng ĐỔI QUẢ, các dòng sau để trống.

    # 4. Điền xuôi rồi gộp vào bảng kê
    python scripts/01b_tag_sheets.py --fill-down data/tags/fruit_ids.csv
    python scripts/01b_tag_sheets.py --merge data/tags/fruit_ids.csv \
           --manifest data/manifest.csv
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import cv2
import numpy as np
import pandas as pd
from PIL import ExifTags, Image, ImageDraw

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from chanhday.cards import crop_tag, detect_tag  # noqa: E402
from chanhday.config import CFG  # noqa: E402
from chanhday.io_utils import (chan_doan_thu_muc,  # noqa: E402
                               imread_unicode, imwrite_unicode,
                               iter_images, read_str_csv)

_read_str = read_str_csv
T = {v: k for k, v in ExifTags.TAGS.items()}


def capture_time(p: Path) -> str:
    try:
        with Image.open(p) as im:
            ex = im.getexif()
            ifd = ex.get_ifd(0x8769)
            return str(ifd.get(T.get("DateTimeOriginal"))
                       or ex.get(T.get("DateTime")) or "")
    except Exception:
        return ""


def ordered_paths(root: Path):
    """Sắp theo thời gian chụp: mã quả chạy liên tục nên rất dễ điền."""
    recs = [(p, capture_time(p)) for p in iter_images(root)
            if p.suffix.lower() in (".jpg", ".jpeg", ".png")]
    recs.sort(key=lambda r: (r[1] or "9999", r[0].name))
    return recs


# ---------------------------------------------------------------------------
# Kiểm tra nhanh trước khi chạy cả bộ
# ---------------------------------------------------------------------------

def probe(args):
    """
    Vẽ khung nhãn dò được lên vài ảnh đầy đủ để xác nhận bằng mắt.

    Chạy cái này TRƯỚC khi sinh trang cho cả nghìn ảnh. Nếu khung không trùm
    mảnh giấy thì sửa chỉ mất một phút, còn phát hiện muộn thì mất cả buổi
    ngồi đọc những trang vô dụng.
    """
    recs = ordered_paths(Path(args.data))
    if not recs:
        raise SystemExit(chan_doan_thu_muc(args.data))

    step = max(1, len(recs) // max(args.probe_n, 1))
    chon = recs[::step][:args.probe_n]
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)

    tiles, n_ok = [], 0
    for p, _ in chon:
        im = imread_unicode(p)
        if im is None:
            continue
        vis = im.copy()
        box = detect_tag(im, CFG.layout)
        if box:
            n_ok += 1
            x, y, w, h = box
            cv2.rectangle(vis, (x, y), (x + w, y + h), (0, 255, 0), 8)
            cv2.putText(vis, "NHAN", (x, max(30, y - 12)),
                        cv2.FONT_HERSHEY_SIMPLEX, 2.0, (0, 255, 0), 5)
        else:
            H, W = im.shape[:2]
            rx, ry, rw, rh = CFG.layout.tag_roi
            cv2.rectangle(vis, (int(rx * W), int(ry * H)),
                          (int((rx + rw) * W), int((ry + rh) * H)), (0, 0, 255), 8)
            cv2.putText(vis, "KHONG DO RA", (int(rx * W), int(ry * H) - 15),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.8, (0, 0, 255), 5)
        s = 800 / vis.shape[1]
        tiles.append(cv2.resize(vis, None, fx=s, fy=s))

    if tiles:
        imwrite_unicode(out / "probe_tag.jpg", np.vstack(tiles))
        print(f"[đã ghi] {out / 'probe_tag.jpg'}")
    print(f"Dò ra nhãn ở {n_ok}/{len(tiles)} ảnh kiểm tra.")
    print("\nMỞ ẢNH NÀY RA XEM. Khung xanh phải trùm mảnh giấy ghi mã quả.")
    if n_ok < len(tiles):
        print("Ô báo đỏ là không dò ra. Nếu đa số báo đỏ, chỉnh card_roi trong")
        print("configs/default.yaml cho trùm hết vùng thẻ rồi chạy lại.")


# ---------------------------------------------------------------------------
# Sinh trang đọc mã
# ---------------------------------------------------------------------------

def nguong_doi_qua(diffs, san: float = 0.05) -> float:
    """
    Ngưỡng phân biệt "đổi quả" với "cùng quả", tính từ chính dữ liệu.

    Đo trên bộ ảnh Canon: khi đổi quả mức khác biệt giữa hai ảnh nhãn liên
    tiếp là 0,088–0,248; khi cùng một quả chỉ 0,012–0,038. Hai nhóm tách
    bạch rõ, nhưng giá trị tuyệt đối phụ thuộc độ nét và cỡ chữ của từng bộ
    ảnh, nên đặt một hằng số cứng sẽ hỏng ở bộ khác.

    Dùng trung vị cộng bội số của độ lệch tuyệt đối trung vị: bền với ngoại
    lai, và ở đây phần lớn cặp ảnh là "cùng quả" nên trung vị đại diện đúng
    cho nền.
    """
    d = np.asarray([x for x in diffs if np.isfinite(x) and x < 5.0], float)
    if len(d) < 5:
        return san
    med = float(np.median(d))
    mad = float(np.median(np.abs(d - med))) or 1e-6
    return max(san, med + 6.0 * mad)


def make_sheets(args):
    root = Path(args.data)
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)

    recs = ordered_paths(root)
    if not recs:
        raise SystemExit(chan_doan_thu_muc(root))

    TW, TH = args.tile, int(args.tile * 0.85)

    # Lượt một: cắt nhãn, nén ô lại giữ trong bộ nhớ, đo mức khác biệt liên
    # tiếp. Nén ảnh ô thay vì giữ ảnh gốc để không phải đọc đĩa hai lần mà
    # vẫn giới hạn được bộ nhớ (khoảng 15 KB mỗi ô).
    tiles, founds, diffs = [], [], []
    prev = None
    print(f"Đang cắt nhãn của {len(recs)} ảnh...")
    for k, (p, _) in enumerate(recs):
        im = imread_unicode(p)
        if im is None:
            tiles.append(None)
            founds.append(False)
            diffs.append(9.9)
            continue

        c, found = crop_tag(im, CFG.layout, auto=not args.no_auto)
        if args.rotate == 180:
            c = cv2.rotate(c, cv2.ROTATE_180)
        elif args.rotate:
            c = np.ascontiguousarray(np.rot90(c, args.rotate // 90))

        g = cv2.cvtColor(c, cv2.COLOR_BGR2GRAY)
        s = cv2.resize(g, (48, 36)).astype(np.float32)
        s = (s - s.mean()) / (s.std() + 1e-6)
        diffs.append(float(np.abs(s - prev).mean()) if prev is not None else 9.9)
        prev = s

        ok, buf = cv2.imencode(".jpg", cv2.resize(c, (TW, TH)),
                               [cv2.IMWRITE_JPEG_QUALITY, 90])
        tiles.append(buf if ok else None)
        founds.append(found)

        if (k + 1) % 200 == 0:
            print(f"  {k + 1}/{len(recs)}")

    nguong = args.doi_qua_nguong if args.doi_qua_nguong > 0 else nguong_doi_qua(diffs)
    print(f"Ngưỡng đổi quả: {nguong:.3f}"
          + ("  (tự tính từ dữ liệu)" if args.doi_qua_nguong <= 0 else "  (do bạn đặt)"))

    # Lượt hai: ghép trang
    per = args.cols * args.rows
    rows_csv, n_auto, n_doi = [], 0, 0

    for s0 in range(0, len(recs), per):
        idx = range(s0, min(s0 + per, len(recs)))
        nrow = (len(list(idx)) - 1) // args.cols + 1
        sheet = Image.new("RGB", (args.cols * TW, nrow * (TH + 30)), (255, 255, 255))
        d = ImageDraw.Draw(sheet)

        for i, k in enumerate(idx):
            p, t = recs[k]
            found = founds[k]
            n_auto += found
            la_moi = bool(diffs[k] > nguong)
            n_doi += la_moi

            if tiles[k] is None:
                tile = Image.new("RGB", (TW, TH), (220, 220, 220))
            else:
                tile = Image.fromarray(cv2.cvtColor(
                    cv2.imdecode(tiles[k], cv2.IMREAD_COLOR), cv2.COLOR_BGR2RGB))

            x, y = (i % args.cols) * TW, (i // args.cols) * (TH + 30)
            sheet.paste(tile, (x, y + 30))

            mau = (0, 150, 0) if found else (210, 0, 0)
            nhan = f"{k + 1}. {p.stem}" + ("" if found else "  [KHONG DO RA]")
            if la_moi and found:
                nhan += "   <== QUA MOI?"
            d.text((x + 5, y + 8), nhan, fill=mau)
            d.rectangle([x, y, x + TW - 1, y + TH + 29], outline=mau,
                        width=1 if found else 4)

            rows_csv.append({
                "stt": k + 1,
                "sheet": f"sheet_{s0 // per:02d}.png",
                "image_path": str(p),
                "stem": p.stem,
                "capture_time": t,
                "tag_found": int(found),
                "khac_biet": round(min(diffs[k], 9.9), 4),
                "de_xuat_qua_moi": int(la_moi),
                "fruit_id": "",
                "label": "",
                "tinh_trang": "",
            })

        sp = out / f"sheet_{s0 // per:02d}.png"
        sheet.save(sp)
        print(f"[đã ghi] {sp}")

    df = pd.DataFrame(rows_csv)
    csvp = out / "fruit_ids.csv"
    df.to_csv(csvp, index=False, encoding="utf-8-sig")

    n = len(df)
    n_fail = int((df.tag_found == 0).sum())
    print(f"\n[đã ghi] {csvp}  ({n} dòng)")
    print(f"Dò ra nhãn: {n_auto}/{n} ảnh ({100 * n_auto / max(n, 1):.1f}%)")

    if n_fail:
        print(f"\n{n_fail} ảnh KHÔNG dò ra nhãn, đã đánh viền đỏ trên trang.")
        print("Các ô đó cắt vào chỗ khác, thường là vỏ quả. ĐỪNG ĐOÁN MÃ cho")
        print("chúng — đoán sai một mã nghĩa là train và val dùng chung một quả,")
        print("và phép đánh giá hỏng mà không có dấu hiệu gì.")
        print("Cứ để trống, bước fill-down sẽ tự dừng ở đó.")
        print("\nNếu số này lớn, chạy chế độ kiểm tra rồi chỉnh card_roi:")
        print(f"  python scripts/01b_tag_sheets.py --probe --data {args.data}")

    print(f"\nĐề xuất {n_doi} chỗ đổi quả (nhãn 'QUA MOI?' trên trang).")
    print("Đây là gợi ý từ mức khác biệt giữa hai ảnh nhãn liên tiếp, không")
    print("phải kết luận. Vẫn phải nhìn mã để xác nhận.")
    print("\nCÁCH ĐIỀN NHANH:")
    print("  1. Mở sheet_00.png, đọc mã trên từng ô.")
    print("  2. Trong fruit_ids.csv chỉ điền dòng ĐẦU TIÊN của mỗi quả mới.")
    print("     Các dòng 'QUA MOI?' là chỗ nhiều khả năng phải điền.")
    print(f"  3. python scripts/01b_tag_sheets.py --fill-down {csvp}")


# ---------------------------------------------------------------------------

def fill_down(path, force: bool = False):
    """
    Chép mã quả xuống các dòng trống phía dưới.

    Mặc định DỪNG ở những dòng không dò ra nhãn thay vì chép qua chúng. Chép
    qua nghĩa là gán mã cho một ảnh mà không ai kiểm chứng được, và nếu đúng
    chỗ đó là ranh giới giữa hai quả thì hai tập sẽ dùng chung một quả.
    """
    df = _read_str(path)
    co_co = "tag_found" in df.columns
    chan = (df["tag_found"].astype(str) == "0") if co_co else None

    for col in ("fruit_id", "label", "tinh_trang"):
        if col not in df.columns:
            continue
        s = df[col].astype(str).str.strip().replace("", None)
        if co_co and not force:
            # mỗi đoạn liên tục các dòng dò được nhãn là một nhóm điền riêng
            s = s.groupby(chan.cumsum()).ffill()
            s = s.mask(chan, None)
        else:
            s = s.ffill()
        df[col] = s.fillna("")

    df.to_csv(path, index=False, encoding="utf-8-sig")

    trong = int((df["fruit_id"].astype(str).str.len() == 0).sum())
    print(f"Đã điền xuôi. Còn {trong} dòng trống cột fruit_id.")

    if co_co and not force:
        n_fail = int(chan.sum())
        if n_fail:
            print(f"\n{n_fail} dòng bị bỏ qua vì không dò ra nhãn. Việc điền")
            print("dừng lại ở mỗi dòng như vậy thay vì chép mã qua. Ba lựa chọn:")
            print("  - Điền tay mã cho các dòng đó nếu bạn xác minh được")
            print("  - Loại các ảnh đó khỏi nghiên cứu")
            print("  - Chạy lại với --force nếu chắc chắn chuỗi không đứt quãng")

    if trong == 0 and len(df):
        u = df["fruit_id"].nunique()
        per = df.groupby("fruit_id").size()
        print(f"\nTổng {len(df)} ảnh / {u} quả riêng biệt "
              f"(trung bình {per.mean():.1f} ảnh mỗi quả, "
              f"ít nhất {per.min()}, nhiều nhất {per.max()}).")
        print(f"=> CỠ MẪU THỰC là {u} quả.")

        if "de_xuat_qua_moi" in df.columns:
            n_dx = int((df["de_xuat_qua_moi"].astype(str) == "1").sum())
            if n_dx and abs(n_dx - u) > max(3, 0.25 * u):
                print(f"\nGHI CHÚ: bạn khai {u} quả nhưng ảnh nhãn thay đổi ở "
                      f"{n_dx} chỗ.")
                print("Chênh lệch lớn có thể do bỏ sót một ranh giới đổi quả.")
                print("Xem lại các dòng đánh dấu 'QUA MOI?' trên trang.")


def merge(tag_csv, manifest):
    t = _read_str(tag_csv)
    m = _read_str(manifest)

    # Gộp theo ĐƯỜNG DẪN ĐẦY ĐỦ, không theo tên file.
    #
    # Máy ảnh đánh số lại sau mỗi lần định dạng thẻ, nên IMG_1689.JPG xuất
    # hiện ở nhiều nguồn là chuyện thường. Gộp theo tên file khi có trùng sẽ
    # tạo tích Descartes: 2 dòng thành 4, và mỗi ảnh nhận thêm nhãn của ảnh
    # cùng tên ở nguồn khác. Nhãn sai gán chéo, không có thông báo lỗi.
    def norm(s):
        return str(Path(str(s)).resolve()).lower() if s else ""

    t["_k"] = t["image_path"].map(norm)
    m["_k"] = m["image_path"].map(norm)

    dup_t = int(t["_k"].duplicated().sum())
    if dup_t:
        print(f"CẢNH BÁO: {dup_t} dòng trùng đường dẫn trong {tag_csv}, giữ dòng đầu.")
        t = t.drop_duplicates("_k", keep="first")

    cols = ["_k", "fruit_id"] + [c for c in ("label", "tinh_trang") if c in t.columns]
    drop = [c for c in cols if c != "_k" and c in m.columns]

    n_truoc = len(m)
    out = m.drop(columns=drop).merge(t[cols], on="_k", how="left",
                                     validate="m:1").drop(columns="_k")
    assert len(out) == n_truoc, (
        f"Số dòng đổi từ {n_truoc} thành {len(out)} sau khi gộp. "
        f"Đây là lỗi, dừng lại thay vì ghi dữ liệu sai.")

    out["fruit_id"] = out["fruit_id"].fillna("")
    out.to_csv(manifest, index=False, encoding="utf-8-sig")
    miss = int((out["fruit_id"].astype(str).str.len() == 0).sum())
    print(f"Đã gộp vào {manifest}. Thiếu fruit_id: {miss} dòng.")
    if miss:
        print("Các dòng thiếu là ảnh chưa có mã quả. Script 03 sẽ chặn chúng lại,")
        print("không để lọt vào tập huấn luyện.")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data")
    ap.add_argument("--out", default="data/tags")
    ap.add_argument("--probe", action="store_true",
                    help="vẽ khung nhãn lên vài ảnh để kiểm tra trước")
    ap.add_argument("--probe-n", type=int, default=6)
    ap.add_argument("--no-auto", action="store_true",
                    help="tắt dò tự động, dùng toạ độ cố định trong cấu hình")
    ap.add_argument("--rotate", type=int, default=180,
                    help="độ xoay vùng nhãn; bộ ảnh hiện tại viết ngược nên để 180")
    ap.add_argument("--tile", type=int, default=260)
    ap.add_argument("--cols", type=int, default=6)
    ap.add_argument("--rows", type=int, default=5)
    ap.add_argument("--doi-qua-nguong", type=float, default=0.0,
                    help="ngưỡng đề xuất đổi quả; để 0 thì tự tính từ dữ liệu")
    ap.add_argument("--fill-down")
    ap.add_argument("--force", action="store_true",
                    help="điền xuôi qua cả những dòng không dò ra nhãn")
    ap.add_argument("--merge")
    ap.add_argument("--manifest", default="data/manifest.csv")
    args = ap.parse_args()

    if args.fill_down:
        fill_down(args.fill_down, args.force)
    elif args.merge:
        merge(args.merge, args.manifest)
    elif args.probe:
        if not args.data:
            ap.error("chế độ --probe cần --data")
        probe(args)
    elif args.data:
        make_sheets(args)
    else:
        ap.error("cần --data, --probe, --fill-down hoặc --merge")


if __name__ == "__main__":
    main()
