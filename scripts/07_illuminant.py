#!/usr/bin/env python3
"""
07 — ƯỚC LƯỢNG NGUỒN SÁNG MÔI TRƯỜNG
     ("tự phán đoán môi trường xung quanh rồi mới đọc màu quả")

Ý tưởng cốt lõi, và là chỗ đề tài tuyên bố đóng góp riêng:

    Bốn ô xám trong khung hình cho ta NHÃN ĐÚNG của nguồn sáng ở từng ảnh.
    Dùng nhãn đó huấn luyện một mô-đun ước lượng nguồn sáng TỪ CẢNH, KHÔNG
    CẦN THẺ. Khi triển khai thực tế, nông hộ chụp ảnh không có thẻ, mô-đun
    tự suy ra nguồn sáng, tự hiệu chỉnh màu quả, rồi mới phân loại độ chín.

Ba chế độ:
    --mode extract   trích nguồn sáng từ thẻ trên toàn bộ ảnh -> nhãn giám sát
    --mode baseline  Gray-World / Shades-of-Gray / Max-RGB / Gray-Edge
    --mode train     CNN chưng cất từ thẻ, so với các đường cơ sở trên

Thí nghiệm chính cho mục 4.4 — chạy toàn bộ quy trình ở BA cấu hình:
    (a) không hiệu chỉnh
    (b) hiệu chỉnh bằng thẻ            -> giới hạn trên, cần thẻ trong khung
    (c) hiệu chỉnh bằng nguồn sáng ước lượng -> điều kiện triển khai thật

    chênh lệch (a) và (b) = phần biến thiên do chiếu sáng
    chênh lệch (b) và (c) = cái giá phải trả khi bỏ thẻ đi
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import cv2
import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from chanhday.cards import (angular_error, illuminant_from_patches,  # noqa: E402
                            illuminant_gray_edge, illuminant_gray_world,
                            mask_card_region, sample_gray_patches,
                            summarize_errors)
from chanhday.config import CFG  # noqa: E402
from chanhday.io_utils import (imread_unicode, read_str_csv,  # noqa: E402
                               save_json, write_csv)


# ---------------------------------------------------------------------------

def mode_extract(args):
    df = read_str_csv(args.manifest)
    rows, n_fail = [], 0

    for _, r in df.iterrows():
        p = Path(str(r["image_path"]))
        bgr = imread_unicode(p)
        if bgr is None:
            n_fail += 1
            continue
        patches = sample_gray_patches(bgr, CFG.layout)
        if np.isfinite(patches).all(axis=1).sum() < 2:
            n_fail += 1
            continue
        ill = illuminant_from_patches(patches)
        rows.append({
            "image_path": str(p),
            "label": r.get("label", ""),
            "fruit_id": r.get("fruit_id", ""),
            "source_id": r.get("source_id", ""),
            "session_id": r.get("session_id", ""),
            "capture_time": r.get("capture_time", ""),
            "ill_b": ill[0], "ill_g": ill[1], "ill_r": ill[2],
        })

    out = pd.DataFrame(rows)
    write_csv(out, args.out)
    print(f"Trích nguồn sáng: {len(out)} ảnh thành công, {n_fail} thất bại.")
    if out.empty:
        print("Không đọc được thẻ ở ảnh nào. Chạy scripts/00_calibrate_layout.py")
        print("để dò lại bố cục thẻ trước.")
        return

    V = out[["ill_b", "ill_g", "ill_r"]].to_numpy(float)
    mean_ill = V.mean(0)
    spread = np.array([angular_error(v, mean_ill) for v in V])

    print(f"\nĐộ phân tán chiếu sáng: trung bình {spread.mean():.2f}°, "
          f"lớn nhất {spread.max():.2f}°")
    if spread.max() < 3:
        print("  => Toàn bộ ảnh chụp ở gần như MỘT điều kiện sáng.")
        print("     Chưa đủ đa dạng để huấn luyện tầng ước lượng môi trường.")
        print("     Cần chụp thêm ở nhiều khung giờ, trong nhà và ngoài trời.")
    elif spread.max() < 8:
        print("  => Đa dạng mức vừa. Nên bổ sung ảnh ngoài trời nhiều khung giờ.")
    else:
        print("  => Đa dạng tốt, đủ để huấn luyện tầng ước lượng môi trường.")

    for key, ten in [("source_id", "nguồn thu mẫu"), ("session_id", "buổi chụp")]:
        sub = out[out[key].astype(str).str.len() > 0]
        if sub.empty or sub[key].nunique() < 2:
            continue
        print(f"\nNguồn sáng trung bình theo {ten}:")
        for s, g in sub.groupby(key):
            m = g[["ill_b", "ill_g", "ill_r"]].to_numpy(float).mean(0)
            print(f"  {s:<14} B={m[0]:.3f} G={m[1]:.3f} R={m[2]:.3f}   "
                  f"lệch {angular_error(m, mean_ill):.2f}° so với trung bình chung")
        print(f"  => Nếu chênh lệch giữa các {ten} lớn, một phần khác biệt giữa")
        print(f"     các nguồn ở mục 4.4 là do CHIẾU SÁNG chứ không do giống.")

    save_json({"phan_tan_trung_binh_do": float(spread.mean()),
               "phan_tan_lon_nhat_do": float(spread.max()),
               "n": int(len(out))}, "outputs/illuminant_spread.json")


# ---------------------------------------------------------------------------

def mode_baseline(args):
    df = read_str_csv(args.illum)
    methods = {
        "Không hiệu chỉnh": lambda im: np.ones(3) / np.sqrt(3),
        "Gray-World (p=1)": lambda im: illuminant_gray_world(im, 1),
        "Shades-of-Gray (p=6)": lambda im: illuminant_gray_world(im, 6),
        "Max-RGB": lambda im: illuminant_gray_world(im, np.inf),
        "Gray-Edge": lambda im: illuminant_gray_edge(im, 1),
    }
    errs = {k: [] for k in methods}

    for _, r in df.iterrows():
        bgr = imread_unicode(r["image_path"])
        if bgr is None:
            continue
        gt = np.array([float(r["ill_b"]), float(r["ill_g"]), float(r["ill_r"])])
        # che thẻ để thuật toán không nhìn trộm đáp án
        masked = mask_card_region(bgr, CFG.layout)
        for k, fn in methods.items():
            try:
                errs[k].append(angular_error(fn(masked), gt))
            except Exception:
                pass

    t = pd.DataFrame([summarize_errors(v, k) for k, v in errs.items()])
    t = t.sort_values("trung_vi")
    print("\nSAI SỐ GÓC so với nguồn sáng suy từ thẻ (độ; thấp hơn là tốt hơn)")
    print(t.to_string(index=False))
    write_csv(t, "outputs/illuminant_baselines.csv")
    print("\nĐây là bảng đối chứng bắt buộc: CNN ở chế độ train phải thắng được")
    print("các phương pháp không học này thì mới đáng đưa vào báo cáo.")


# ---------------------------------------------------------------------------

def mode_train(args):
    import torch
    import torch.nn as nn
    from torch.utils.data import DataLoader, Dataset
    import torchvision.transforms as T
    from torchvision.models import ResNet18_Weights, resnet18

    df = read_str_csv(args.illum)
    if len(df) < 100:
        print(f"CẢNH BÁO: chỉ có {len(df)} ảnh. Cần ít nhất 300 để huấn luyện")
        print("ổn định. Kết quả dưới đây chỉ mang tính thăm dò.")

    key = next((k for k in ("source_id", "fruit_id", "session_id")
                if k in df.columns and df[k].astype(str).str.len().gt(0).any()), None)
    if key:
        groups = sorted(df[key].astype(str).unique())
        np.random.default_rng(0).shuffle(groups)
        val_g = set(groups[:max(1, len(groups) // 5)])
        tr = df[~df[key].astype(str).isin(val_g)]
        va = df[df[key].astype(str).isin(val_g)]
        print(f"Chia theo '{key}': train {len(tr)}, val {len(va)} "
              f"(giữ lại {sorted(val_g)})")
    else:
        idx = np.random.default_rng(0).permutation(len(df))
        cut = int(0.8 * len(df))
        tr, va = df.iloc[idx[:cut]], df.iloc[idx[cut:]]
        print("CẢNH BÁO: thiếu fruit_id/source_id nên phải chia theo ảnh.")
        print("Kết quả sẽ lạc quan hơn thực tế.")

    class DS(Dataset):
        def __init__(self, d, train):
            self.d = d.reset_index(drop=True)
            self.train = train
            self.tf = T.ToTensor()

        def __len__(self):
            return len(self.d)

        def __getitem__(self, i):
            r = self.d.iloc[i]
            bgr = imread_unicode(r["image_path"])
            bgr = mask_card_region(bgr, CFG.layout)
            bgr = cv2.resize(bgr, (args.imgsz, args.imgsz))
            rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB).astype(np.float32) / 255.0
            y = np.array([float(r["ill_r"]), float(r["ill_g"]),
                          float(r["ill_b"])], np.float32)

            if self.train:
                # Tăng cường ĐÚNG VẬT LÝ: nhân ảnh với một nguồn sáng ngẫu nhiên
                # rồi cập nhật nhãn tương ứng. Khác hẳn hsv_s=0.7 vốn phá tín hiệu
                # vì nó đổi màu mà không đổi nhãn.
                g = np.exp(np.random.uniform(-0.3, 0.3, 3)).astype(np.float32)
                rgb = np.clip(rgb * g[None, None, :], 0, 1)
                y = y * g
                if np.random.rand() < 0.5:
                    rgb = rgb[:, ::-1].copy()
            return self.tf(rgb), torch.from_numpy(y / (np.linalg.norm(y) + 1e-8))

    dev = "cuda" if torch.cuda.is_available() else "cpu"
    net = resnet18(weights=ResNet18_Weights.DEFAULT)
    net.fc = nn.Linear(net.fc.in_features, 3)
    net = net.to(dev)

    def ang_loss(pred, tgt):
        pred = pred / (pred.norm(dim=1, keepdim=True) + 1e-8)
        return torch.acos((pred * tgt).sum(1).clamp(-1 + 1e-6, 1 - 1e-6)).mean()

    dl_tr = DataLoader(DS(tr, True), batch_size=args.batch, shuffle=True,
                       num_workers=2, drop_last=len(tr) > args.batch)
    dl_va = DataLoader(DS(va, False), batch_size=args.batch, num_workers=2)

    opt = torch.optim.AdamW(net.parameters(), lr=3e-4, weight_decay=1e-4)
    sched = torch.optim.lr_scheduler.CosineAnnealingLR(opt, args.epochs)

    Path("outputs").mkdir(exist_ok=True)
    best, hist, errs = 1e9, [], []
    for ep in range(args.epochs):
        net.train()
        for x, y in dl_tr:
            opt.zero_grad()
            ang_loss(net(x.to(dev)), y.to(dev)).backward()
            opt.step()
        sched.step()

        net.eval()
        errs = []
        with torch.no_grad():
            for x, y in dl_va:
                for a, b in zip(net(x.to(dev)).cpu().numpy(), y.numpy()):
                    errs.append(angular_error(a, b))
        med = float(np.median(errs)) if errs else float("nan")
        hist.append(med)
        print(f"epoch {ep+1:>3}/{args.epochs}   sai số góc trung vị (val) {med:.3f}°")
        if med < best:
            best = med
            torch.save(net.state_dict(), "outputs/illuminant_net.pt")

    save_json({"lich_su": hist, "tot_nhat_trung_vi": best,
               **summarize_errors(errs, "CNN chưng cất từ thẻ")},
              "outputs/illuminant_cnn.json")
    print(f"\nTốt nhất: {best:.3f}°  ->  outputs/illuminant_net.pt")
    print("So con số này với outputs/illuminant_baselines.csv.")
    print("Nếu KHÔNG thắng Shades-of-Gray thì dùng Shades-of-Gray và báo cáo")
    print("trung thực: một đường cơ sở không học thắng CNN cũng là kết quả có giá trị.")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", choices=["extract", "baseline", "train"], required=True)
    ap.add_argument("--manifest")
    ap.add_argument("--illum", default="outputs/illum.csv")
    ap.add_argument("--out", default="outputs/illum.csv")
    ap.add_argument("--imgsz", type=int, default=224)
    ap.add_argument("--batch", type=int, default=32)
    ap.add_argument("--epochs", type=int, default=40)
    args = ap.parse_args()

    Path("outputs").mkdir(exist_ok=True)
    if args.mode == "extract":
        if not args.manifest:
            ap.error("chế độ extract cần --manifest")
        mode_extract(args)
    elif args.mode == "baseline":
        mode_baseline(args)
    else:
        mode_train(args)


if __name__ == "__main__":
    main()
