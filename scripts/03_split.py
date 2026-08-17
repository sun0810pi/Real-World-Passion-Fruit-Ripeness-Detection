#!/usr/bin/env python3
"""
03 — CHIA TẬP KHÔNG RÒ RỈ (mục 3.4.8 và 3.6)

Quy tắc bất di bất dịch:
    ưu tiên 1 — chia theo nguồn
    ưu tiên 2 — trong mỗi nguồn, chia theo quả
    ưu tiên 3 — chỉ khi hai điều trên đã thỏa mới xét cân bằng lớp

Ba chế độ tương ứng ba phép đánh giá:
    --mode audit   đo mức rò rỉ của phép chia hiện tại (chạy trước tiên)
    --mode fruit   chia theo quả trong cùng nguồn  -> phép 1, mục 3.6
    --mode loso    bỏ ra một nguồn                 -> phép 2, mục 3.6

    python scripts/03_split.py --manifest data/proc_wb_manifest.csv --mode audit
    python scripts/03_split.py --manifest data/proc_wb_manifest.csv --mode fruit --seed 0
    python scripts/03_split.py --manifest data/proc_wb_manifest.csv --mode loso
"""
from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from chanhday.config import CLASS_NAMES  # noqa: E402
from chanhday.io_utils import (count_files, read_str_csv,  # noqa: E402
                               save_json, unique_stem)

SAN_QUA_MOI_BAC = 20   # sàn đặt ở mục 3.4.6


def audit(df: pd.DataFrame):
    print("=" * 64)
    print("KIỂM TOÁN RÒ RỈ VÀ CỠ MẪU")
    print("=" * 64)

    if df.get("old_split") is not None and df["old_split"].nunique() > 1:
        for key, ten in [("fruit_id", "quả"), ("source_id", "nguồn"),
                         ("session_id", "buổi chụp")]:
            sub = df[df[key].astype(str).str.len() > 0] if key in df else pd.DataFrame()
            if sub.empty:
                continue
            g = sub.groupby(key)["old_split"].nunique()
            leak = int((g > 1).sum())
            print(f"[{ten}] {leak}/{len(g)} đơn vị nằm ở nhiều tập "
                  f"({100*leak/max(len(g),1):.1f}%)")
            if leak and key == "fruit_id":
                print("  => Ảnh của cùng một quả xuất hiện ở cả train lẫn val.")
                print("     Đây là nguyên nhân của độ chính xác cao giả tạo.")
    else:
        print("(manifest chưa có thông tin phép chia cũ)")

    print("\n" + "-" * 64)
    print("CỠ MẪU THỰC")
    for key, ten in [("fruit_id", "quả riêng biệt"), ("source_id", "nguồn"),
                     ("session_id", "buổi chụp")]:
        if key in df:
            print(f"  {ten:<22} {df.loc[df[key].astype(str).str.len() > 0, key].nunique()}")
    print(f"  {'ảnh':<22} {len(df)}")

    ns = df.loc[df.source_id.astype(str).str.len() > 0, "source_id"].nunique() \
        if "source_id" in df else 0
    print("\n" + "-" * 64)
    if ns < 2:
        print("CHƯA ĐỦ ĐIỀU KIỆN cho đánh giá bỏ ra một nguồn (cần ít nhất 2 nguồn).")
        print("Câu hỏi 2 — trục chính của đề tài — hiện chưa trả lời được.")
    elif ns == 2:
        print("Có 2 nguồn: chỉ được 2 phép thử. Theo đúng mục 4.4, phần này phải")
        print("báo cáo dưới dạng PHÂN TÍCH KHÁM PHÁ, không kết luận Giả thuyết 2.")
    else:
        print(f"Có {ns} nguồn -> {ns} phép thử độc lập. Đủ để báo cáo chính thức.")

    if {"source_id", "fruit_id", "label"} <= set(df.columns):
        sub = df[(df.source_id.astype(str).str.len() > 0)
                 & (df.fruit_id.astype(str).str.len() > 0)]
        if not sub.empty:
            t = (sub.groupby(["source_id", "label"])["fruit_id"].nunique()
                 .unstack(fill_value=0).reindex(columns=CLASS_NAMES, fill_value=0))
            print("\n" + "-" * 64)
            print(f"SỐ QUẢ theo nguồn x bậc (sàn mục 3.4.6 là {SAN_QUA_MOI_BAC}):")
            print(t.to_string())
            fail = int((t < SAN_QUA_MOI_BAC).sum().sum())
            print(f"\n{fail}/{t.size} tổ hợp chưa đạt sàn.   <-- điền vào mục 4.1")


def split_by_fruit(df, val_frac, seed):
    """
    Chia theo quả, thực hiện riêng trong từng nguồn VÀ từng bậc chín.

    Phân tầng theo bậc là cần thiết: nếu chỉ bốc quả ngẫu nhiên cho đủ tỷ lệ
    ảnh, tập kiểm tra rất dễ thiếu hẳn một bậc, khiến F1 của bậc đó bằng 0 và
    không diễn giải được. Vẫn giữ nguyên ràng buộc mọi ảnh của một quả nằm
    trọn trong một tập.
    """
    if "fruit_id" not in df or not (df.fruit_id.astype(str).str.len() > 0).all():
        raise SystemExit("Cột fruit_id còn trống. Chạy script 01b trước.")

    out = df.copy()
    out["split"] = "train"
    rng = np.random.default_rng(seed)

    has_src = "source_id" in df and df.source_id.astype(str).str.len().gt(0).any()
    keys = ["source_id", "label"] if has_src else ["label"]

    canh_bao = []
    for key, sub in df.groupby(keys, dropna=False):
        fruits = sorted(sub.fruit_id.unique())
        rng.shuffle(fruits)
        n_val = max(1, int(round(len(fruits) * val_frac)))
        if len(fruits) < 2:
            canh_bao.append((key, len(fruits)))
            continue           # chỉ 1 quả thì để hết ở train
        out.loc[out.fruit_id.isin(fruits[:n_val]), "split"] = "val"

    if canh_bao:
        print("\nCác tổ hợp chỉ có 1 quả, không chia được nên giữ nguyên ở train:")
        for k, n in canh_bao:
            print(f"  {k}: {n} quả")
        print("Bậc tương ứng sẽ vắng mặt ở tập kiểm tra.")

    # Một quả không được nằm ở hai tập. Trường hợp cùng fruit_id xuất hiện ở
    # hai bậc khác nhau (thường là lỗi gán nhãn) sẽ phá ràng buộc này.
    xung_dot = out.groupby("fruit_id")["split"].nunique()
    if (xung_dot > 1).any():
        bad = xung_dot[xung_dot > 1].index.tolist()
        print(f"\nCẢNH BÁO: {len(bad)} quả bị chia về cả hai tập: {bad[:10]}")
        print("Nguyên nhân thường gặp: cùng một fruit_id được gán hai bậc chín")
        print("khác nhau. Sửa nhãn rồi chạy lại, nếu không phép đánh giá vẫn rò rỉ.")
        out.loc[out.fruit_id.isin(bad), "split"] = "train"

    return out


def materialize(df, outdir, path_col):
    for c in ("split", "label"):
        if c not in df.columns:
            raise SystemExit(
                f"Bảng kê thiếu cột '{c}'. Nếu vừa chạy 01b --merge, kiểm tra "
                f"xem cột 'label' đã được điền trong data/tags/fruit_ids.csv chưa.")
    if (df["label"].astype(str).str.len() == 0).any():
        n = int((df["label"].astype(str).str.len() == 0).sum())
        raise SystemExit(f"{n} dòng chưa có nhãn độ chín. Điền cột 'label' "
                         f"trong data/tags/fruit_ids.csv rồi chạy lại 01b --merge.")
    outdir = Path(outdir)
    if outdir.exists():
        shutil.rmtree(outdir)
    n, seen = 0, set()
    for _, r in df.iterrows():
        src = Path(str(r[path_col]))
        if not src.exists():
            continue
        # Tên file phải duy nhất trong toàn tập, không chỉ trong thư mục nguồn
        name = src.name if src.name not in seen else f"{unique_stem(src)}{src.suffix}"
        seen.add(name)
        dst = outdir / str(r["split"]) / str(r["label"]) / name
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
        n += 1

    tren_dia = count_files(outdir)
    if tren_dia != n:
        raise SystemExit(
            f"Copy {n} file nhưng chỉ còn {tren_dia} trên đĩa — có file bị đè. "
            f"Báo lỗi này cho người viết script.")
    return outdir, n


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--manifest", required=True)
    ap.add_argument("--mode", choices=["audit", "fruit", "loso"], default="audit")
    ap.add_argument("--out", default="data/splits")
    ap.add_argument("--val-frac", type=float, default=0.2)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--path-col", default="proc_path")
    args = ap.parse_args()

    df = read_str_csv(args.manifest)
    if args.path_col not in df.columns:
        args.path_col = "image_path"

    if args.mode == "audit":
        audit(df)
        return

    if args.mode == "fruit":
        out = split_by_fruit(df, args.val_frac, args.seed)
        d, n = materialize(out, Path(args.out) / f"fruit_seed{args.seed}", args.path_col)
        info = {"train": int((out.split == "train").sum()),
                "val": int((out.split == "val").sum()),
                "so_qua_train": int(out[out.split == "train"].fruit_id.nunique()),
                "so_qua_val": int(out[out.split == "val"].fruit_id.nunique()),
                "seed": args.seed, "da_copy": n}
        print(f"[cùng nguồn, chia theo quả] {info} -> {d}")
        save_json(info, Path(args.out) / f"fruit_seed{args.seed}_info.json")
        return

    srcs = sorted(s for s in df.get("source_id", pd.Series(dtype=str)).unique() if s)
    if len(srcs) < 2:
        raise SystemExit("Cần ít nhất 2 nguồn để chạy bỏ ra một nguồn.")
    for s in srcs:
        out = df.copy()
        out["split"] = np.where(out.source_id == s, "val", "train")
        d, n = materialize(out, Path(args.out) / f"loso_{s}", args.path_col)
        print(f"[bỏ ra {s}] train={(out.split=='train').sum()} "
              f"val={(out.split=='val').sum()} -> {d}")


if __name__ == "__main__":
    main()
