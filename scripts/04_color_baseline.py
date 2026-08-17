#!/usr/bin/env python3
"""
04 — ĐƯỜNG CƠ SỞ THỐNG KÊ MÀU CIE L*a*b* (mục 3.5, nhóm phương pháp 1)

Mức sàn bắt buộc. Báo cáo đã viết rõ ở mục 3.5: nếu đường cơ sở đã đạt phần
lớn hiệu năng thì việc dùng mô hình học sâu không được biện minh, và đó là
kết luận cần báo cáo.

Chạy rất nhanh (vài giây cho cả nghìn ảnh) nên hãy chạy trước khi train YOLO.
Nó cho bạn biết ngay bài toán khó tới đâu.

    python scripts/04_color_baseline.py --split-dir data/splits/fruit_seed0 \
           --out outputs/baseline_seed0
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from chanhday.config import CLASS_NAMES, CLASS_TO_IDX, N_CLASSES  # noqa: E402
from chanhday.features import FEATURE_NAMES, extract_from_path  # noqa: E402
from chanhday.io_utils import iter_images, save_json, write_csv  # noqa: E402


def load_split(split_dir: Path, split: str):
    X, y, names = [], [], []
    root = split_dir / split
    if not root.exists():
        raise SystemExit(f"Không có thư mục {root}")
    for cls in CLASS_NAMES:
        d = root / cls
        if not d.exists():
            continue
        for p in iter_images(d):
            f = extract_from_path(p)
            if f is not None:
                X.append(f)
                y.append(CLASS_TO_IDX[cls])
                names.append(p.name)
    if not X:
        raise SystemExit(f"Không đọc được ảnh nào từ {root}")
    return np.vstack(X), np.asarray(y), names


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--split-dir", required=True)
    ap.add_argument("--out", default="outputs/baseline")
    ap.add_argument("--model", choices=["gb", "logreg"], default="gb")
    ap.add_argument("--seed", type=int, default=0)
    args = ap.parse_args()

    sd = Path(args.split_dir)
    Xtr, ytr, _ = load_split(sd, "train")
    Xva, yva, names = load_split(sd, "val")
    print(f"train {Xtr.shape}   val {Xva.shape}   ({len(FEATURE_NAMES)} đặc trưng)")

    clf = (make_pipeline(StandardScaler(),
                         LogisticRegression(max_iter=3000, class_weight="balanced",
                                            random_state=args.seed))
           if args.model == "logreg" else
           HistGradientBoostingClassifier(max_iter=400, learning_rate=0.06,
                                          max_depth=4, l2_regularization=1.0,
                                          random_state=args.seed))
    clf.fit(Xtr, ytr)

    proba = clf.predict_proba(Xva)
    if proba.shape[1] != N_CLASSES:      # tập train thiếu lớp
        full = np.zeros((len(proba), N_CLASSES))
        for j, c in enumerate(clf.classes_):
            full[:, c] = proba[:, j]
        proba = full

    outdir = Path(args.out)
    write_csv(pd.DataFrame({
        "image": names, "y_true": yva, "y_pred": proba.argmax(1),
        **{f"p_{c}": proba[:, i] for i, c in enumerate(CLASS_NAMES)},
    }), outdir / "predictions.csv")

    try:
        from sklearn.inspection import permutation_importance
        imp = permutation_importance(clf, Xva, yva, n_repeats=10,
                                     random_state=args.seed, n_jobs=1)
        order = np.argsort(imp.importances_mean)[::-1][:12]
        top = {FEATURE_NAMES[i]: round(float(imp.importances_mean[i]), 5)
               for i in order}
        save_json(top, outdir / "feature_importance.json")
        print("\nĐặc trưng quan trọng nhất:")
        for k, v in top.items():
            print(f"  {k:<24} {v}")
        print("\n(Nếu frac_vo_chuyen_mau đứng đầu thì mô hình đang dùng đúng")
        print(" đại lượng mà sơ đồ nhãn ở Bảng 3 định nghĩa.)")
    except Exception as e:
        print("(bỏ qua permutation importance:", e, ")")

    print(f"\nBƯỚC TIẾP: python scripts/06_evaluate.py --pred "
          f"{outdir/'predictions.csv'} --out {outdir}")


if __name__ == "__main__":
    main()
