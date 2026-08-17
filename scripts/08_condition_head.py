#!/usr/bin/env python3
"""
08 — ĐẦU RA THỨ HAI: TÌNH TRẠNG QUẢ (dùng được / hỏng)

Vì sao phải tách khỏi độ chín, không nhét thành "bậc 6":

  1. Độ chín là trục CÓ THỨ TỰ. Tình trạng là trục KHÁC, vuông góc với nó.
     Một quả có thể đang ở bậc 3 và đồng thời bị nấm hoặc dập vỏ.
  2. Nhét hỏng thành lớp 6 phá Kappa có trọng số bậc và "sai số trung bình
     theo bậc" ở Bảng 8, vì khoảng cách từ bậc 2 tới "hỏng" không phải 4 bậc.
  3. Phá luôn ma trận chi phí ở mục 3.6: báo "hỏng" khi thật ra là bậc 2
     không phải hái sớm, cũng không phải hái muộn, nên không đặt vào ma trận được.

Quy tắc quyết định của công cụ:
    nếu tình trạng = hỏng  ->  loại khỏi lô, KHÔNG xét bậc chín

Đồng thời script này giải quyết lỗ hổng nguy hiểm nhất của mô hình 5 lớp:
softmax buộc phải chọn một trong năm bậc cho bất cứ thứ gì đưa vào. Đưa quả
thối vào, nó trả về bậc 5 với độ tin cậy 0,99 — tức bảo người dùng "chín
hoàn toàn, hái được".

    python scripts/08_condition_head.py --manifest data/proc_wb_manifest.csv \
           --out outputs/tinh_trang
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.metrics import (accuracy_score, average_precision_score,
                             confusion_matrix, f1_score, precision_recall_curve,
                             roc_auc_score)

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from chanhday.config import CONDITION_NAMES  # noqa: E402
from chanhday.features import FEATURE_NAMES, extract_from_path  # noqa: E402
from chanhday.io_utils import read_str_csv, save_json, write_csv  # noqa: E402


def build_dataset(df, path_col):
    X, y, groups, names = [], [], [], []
    for _, r in df.iterrows():
        tt = str(r.get("tinh_trang", "")).strip().lower()
        if tt not in CONDITION_NAMES:
            continue
        f = extract_from_path(r[path_col])
        if f is None:
            continue
        X.append(f)
        y.append(CONDITION_NAMES.index(tt))
        groups.append(str(r.get("fruit_id", "")) or str(r.get("image_path")))
        names.append(Path(str(r[path_col])).name)
    if not X:
        raise SystemExit(
            "Không có dòng nào gán cột 'tinh_trang'.\n"
            "Điền cột này trong data/tags/fruit_ids.csv với giá trị "
            "'dung_duoc' hoặc 'hong', rồi chạy script 01b --merge.")
    return np.vstack(X), np.asarray(y), np.asarray(groups), names


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--manifest", required=True)
    ap.add_argument("--out", default="outputs/tinh_trang")
    ap.add_argument("--path-col", default="proc_path")
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--val-frac", type=float, default=0.25)
    args = ap.parse_args()

    df = read_str_csv(args.manifest)
    if args.path_col not in df.columns:
        args.path_col = "image_path"

    X, y, groups, names = build_dataset(df, args.path_col)
    print(f"{len(y)} ảnh   |   dùng được {int((y==0).sum())}   "
          f"hỏng {int((y==1).sum())}   |   {len(set(groups))} quả")

    # Chia theo QUẢ, không theo ảnh — cùng nguyên tắc với mục 3.4.8
    uq = np.array(sorted(set(groups)))
    rng = np.random.default_rng(args.seed)
    rng.shuffle(uq)
    val_q = set(uq[:max(1, int(len(uq) * args.val_frac))])
    m_val = np.array([g in val_q for g in groups])

    if m_val.sum() == 0 or (~m_val).sum() == 0:
        raise SystemExit("Không chia được tập. Cần thêm quả.")
    if len(set(y[~m_val])) < 2:
        raise SystemExit("Tập train chỉ có một lớp. Cần thêm quả hỏng hoặc quả tốt.")

    clf = HistGradientBoostingClassifier(
        max_iter=300, learning_rate=0.06, max_depth=4,
        l2_regularization=1.0, random_state=args.seed)
    clf.fit(X[~m_val], y[~m_val])

    proba = clf.predict_proba(X[m_val])[:, 1]
    pred = (proba >= 0.5).astype(int)
    yv = y[m_val]

    res = {
        "n_val": int(len(yv)),
        "n_qua_val": int(len(val_q)),
        "do_chinh_xac": float(accuracy_score(yv, pred)),
        "f1_lop_hong": float(f1_score(yv, pred, pos_label=1, zero_division=0)),
    }
    if len(set(yv)) == 2:
        res["auc_roc"] = float(roc_auc_score(yv, proba))
        res["auc_pr"] = float(average_precision_score(yv, proba))

        # Ngưỡng vận hành: với công cụ hỗ trợ thu hoạch, BỎ SÓT quả hỏng nguy
        # hiểm hơn báo nhầm quả tốt thành hỏng, vì một quả hỏng lọt vào lô
        # xuất khẩu có thể làm hỏng cả kiện hàng.
        pr, rc, th = precision_recall_curve(yv, proba)
        rows = []
        for target in (0.90, 0.95, 0.99):
            ok = np.where(rc[:-1] >= target)[0]
            if len(ok):
                i = ok[-1]
                rows.append({"do_nhay_muc_tieu": target,
                             "nguong": round(float(th[i]), 4),
                             "do_nhay_dat_duoc": round(float(rc[i]), 4),
                             "do_chinh_xac_duong_tinh": round(float(pr[i]), 4)})
        if rows:
            write_csv(pd.DataFrame(rows), Path(args.out) / "nguong_van_hanh.csv")
            res["nguong_van_hanh"] = rows

    cm = confusion_matrix(yv, pred, labels=[0, 1])
    res["ma_tran_nham_lan"] = cm.tolist()

    write_csv(pd.DataFrame({
        "image": np.asarray(names)[m_val],
        "y_true": yv, "y_pred": pred, "p_hong": proba,
    }), Path(args.out) / "predictions.csv")
    save_json(res, Path(args.out) / "metrics.json")

    print("\n" + "=" * 56)
    print("ĐẦU RA THỨ HAI — TÌNH TRẠNG QUẢ")
    print("=" * 56)
    print(f"Độ chính xác     {res['do_chinh_xac']:.4f}")
    print(f"F1 lớp 'hỏng'    {res['f1_lop_hong']:.4f}")
    if "auc_roc" in res:
        print(f"AUC-ROC          {res['auc_roc']:.4f}")
        print(f"AUC-PR           {res['auc_pr']:.4f}")
    print("\nMa trận nhầm lẫn (hàng = thật, cột = dự đoán):")
    print(pd.DataFrame(cm, index=CONDITION_NAMES,
                       columns=CONDITION_NAMES).to_string())
    print("\n=> Số này điền vào Bảng 8b của báo cáo.")

    try:
        from sklearn.inspection import permutation_importance
        imp = permutation_importance(clf, X[m_val], yv, n_repeats=10,
                                     random_state=args.seed, n_jobs=1)
        order = np.argsort(imp.importances_mean)[::-1][:8]
        print("\nĐặc trưng phân biệt quả hỏng rõ nhất:")
        for i in order:
            print(f"  {FEATURE_NAMES[i]:<24} {imp.importances_mean[i]:.5f}")
    except Exception:
        pass


if __name__ == "__main__":
    main()
