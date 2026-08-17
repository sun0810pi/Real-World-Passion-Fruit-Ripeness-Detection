#!/usr/bin/env python3
"""
05 — HUẤN LUYỆN YOLO PHÂN LOẠI, CẤU HÌNH ĐÃ SỬA

Đối chiếu với cấu hình cũ (yolo11_cls_5bac_chin-3/args.yaml):

  cũ              mới      lý do
  --------------  -------  ---------------------------------------------------
  yolo11m-cls     11s-cls  ~750 ảnh không nuôi nổi 10M tham số; mục 4.3 lại
                           yêu cầu chạy được trên điện thoại
  hsv_s 0.7       0.15     xáo trộn độ bão hòa ±70% trong bài toán mà MÀU là
  hsv_v 0.4       0.20     tín hiệu duy nhất chính là tự phá tín hiệu
  erasing 0.4     0.10     quả chỉ chiếm phần nhỏ khung, xóa 40% là xóa mất quả
  mosaic 1.0      0.0      tham số của bài toán phát hiện, vô tác dụng ở classify
  seed 42 x1      0,1,2    mục 3.6 yêu cầu ba hạt giống
  dropout 0.0     0.1      chống quá khớp trên dữ liệu nhỏ

    python scripts/05_train_yolo.py --data data/splits/fruit_seed0 \
           --name cungnguon_s0 --seed 0
"""
from __future__ import annotations

import argparse
import shutil
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from chanhday.config import CLASS_NAMES, CLASS_TO_IDX  # noqa: E402
from chanhday.io_utils import save_json, write_csv  # noqa: E402


def stage_locally(src: Path) -> Path:
    """
    Copy dữ liệu về ổ cục bộ trước khi train.

    Lần chạy cũ mất 3,59 giờ cho 50 epoch với chưa tới 1000 ảnh — gần như
    chắc chắn do đọc trực tiếp từ Google Drive. Copy về ổ cục bộ trước
    thường nhanh hơn khoảng mười lần.
    """
    if not Path("/content").exists():
        return src
    if str(src).startswith("/content/") and "drive" not in str(src).lower():
        return src
    dst = Path("/content/_data_local") / src.name
    if dst.exists():
        shutil.rmtree(dst)
    print(f"Copy dữ liệu về ổ cục bộ: {src} -> {dst}")
    shutil.copytree(src, dst)
    return dst


def export_predictions(model, valdir: Path, imgsz: int, out_csv: Path):
    """
    Xuất dự đoán trên tập val.

    Điểm cần chú ý: hàm này chỉ chạy trên các thư mục con có tên nằm trong
    CLASS_NAMES. Thư mục tên khác sẽ bị bỏ qua, và trước đây việc bỏ qua đó
    diễn ra âm thầm — tập val 12 ảnh cho ra file dự đoán 6 dòng mà không có
    thông báo nào, khiến bước đánh giá tính chỉ số trên nửa dữ liệu.

    Nay mọi thư mục bị bỏ qua đều được liệt kê rõ.
    """
    sub = sorted(d.name for d in valdir.iterdir() if d.is_dir()) \
        if valdir.exists() else []
    known = [d for d in sub if d in CLASS_NAMES]
    unknown = [d for d in sub if d not in CLASS_NAMES]

    if unknown:
        n_bo = sum(len([p for p in (valdir / d).iterdir() if p.is_file()])
                   for d in unknown)
        print("\n" + "!" * 68)
        print(f"BỎ QUA {n_bo} ảnh trong {len(unknown)} thư mục không phải bậc chín:")
        for d in unknown:
            print(f"  {d}")
        print("Nếu có thư mục quả hỏng ở đây thì dữ liệu đang bị trộn hai trục.")
        print("Quả hỏng phải nằm ở đầu ra riêng — chạy scripts/08_condition_head.py.")
        print("!" * 68 + "\n")

    thieu = [c for c in CLASS_NAMES if c not in sub]
    if thieu:
        print(f"GHI CHÚ: tập val không có bậc {', '.join(thieu)}. "
              f"F1 của các bậc này sẽ là 0 và không diễn giải được.")

    inv = {v: k for k, v in model.names.items()}
    rows = []
    for cls in known:
        d = valdir / cls
        paths = [p for p in sorted(d.iterdir()) if p.is_file()]
        for i in range(0, len(paths), 64):
            chunk = paths[i:i + 64]
            for p, r in zip(chunk, model.predict([str(x) for x in chunk],
                                                 verbose=False, imgsz=imgsz)):
                pr = r.probs.data.cpu().numpy()
                ordered = np.zeros(len(CLASS_NAMES))
                for c in CLASS_NAMES:
                    if c in inv:
                        ordered[CLASS_TO_IDX[c]] = pr[inv[c]]
                rows.append({"image": p.name, "y_true": CLASS_TO_IDX[cls],
                             "y_pred": int(ordered.argmax()),
                             **{f"p_{c}": ordered[j]
                                for j, c in enumerate(CLASS_NAMES)}})

    n_val = sum(len([p for p in (valdir / d).iterdir() if p.is_file()])
                for d in sub) if sub else 0
    print(f"Tập val có {n_val} ảnh, xuất được {len(rows)} dòng dự đoán.")
    if rows and len(rows) < n_val:
        print(f"  -> {n_val - len(rows)} ảnh bị bỏ, xem cảnh báo phía trên.")
    write_csv(pd.DataFrame(rows), out_csv)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", required=True)
    ap.add_argument("--name", required=True)
    ap.add_argument("--model", default="yolo11s-cls.pt")
    ap.add_argument("--epochs", type=int, default=60)
    ap.add_argument("--imgsz", type=int, default=224)
    ap.add_argument("--batch", type=int, default=32)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--project", default="outputs/runs")
    ap.add_argument("--patience", type=int, default=20)
    ap.add_argument("--no-stage", action="store_true")
    args = ap.parse_args()

    from ultralytics import YOLO

    data = Path(args.data)

    # Kiểm tra trước khi tốn thời gian train
    for split in ("train", "val"):
        d = data / split
        if not d.exists():
            raise SystemExit(f"Không có thư mục {d}. Chạy scripts/03_split.py trước.")
        n = sum(1 for _ in d.rglob("*") if _.is_file())
        ncls = sum(1 for x in d.iterdir() if x.is_dir())
        print(f"{split}: {n} ảnh trong {ncls} thư mục lớp")
        if split == "train" and n < 100:
            print(f"  CẢNH BÁO: chỉ {n} ảnh huấn luyện. Kết quả sẽ dao động rất")
            print(f"  mạnh giữa các hạt giống và không kết luận được gì.")
            print(f"  Nếu bạn nghĩ phải có nhiều ảnh hơn, xem lại sổ kế toán ở")
            print(f"  data/proc_wb_ledger.csv để biết ảnh rớt ở bước nào.")

    # Thư mục test có ít lớp hơn train sẽ làm ultralytics báo ERROR ở cuối
    # mỗi lần validate. Không chặn train nhưng gây nhiễu và dễ hiểu nhầm.
    test_d = data / "test"
    if test_d.exists():
        tr_cls = {x.name for x in (data / "train").iterdir() if x.is_dir()}
        te_cls = {x.name for x in test_d.iterdir() if x.is_dir()}
        if te_cls != tr_cls:
            print(f"\nGHI CHÚ: thư mục test có {len(te_cls)} lớp, train có "
                  f"{len(tr_cls)}. Ultralytics sẽ in ERROR về việc này.")
            print(f"Thiếu: {sorted(tr_cls - te_cls)}")
            print("Tạo thư mục rỗng cho các lớp thiếu, hoặc xóa hẳn thư mục test")
            print("vì pipeline này chỉ dùng train/ và val/.\n")
    if not args.no_stage:
        try:
            data = stage_locally(data)
        except Exception as e:
            print("(không staging được, dùng đường dẫn gốc):", e)

    # Ép đường dẫn tuyệt đối. Với project tương đối, ultralytics ghép nó vào
    # runs_dir trong settings.yaml, nên kết quả rơi vào C:\Users\<tên>\runs\...
    # trong khi script lại đi tìm best.pt ở thư mục làm việc và báo
    # FileNotFoundError sau khi đã train xong hàng chục phút.
    project_abs = str(Path(args.project).resolve())

    t0 = time.time()
    results = YOLO(args.model).train(
        data=str(data.resolve()), epochs=args.epochs, imgsz=args.imgsz, batch=args.batch,
        seed=args.seed, deterministic=True, project=project_abs, name=args.name,
        exist_ok=True, patience=args.patience, cos_lr=True, dropout=0.1,
        # tăng cường dữ liệu: giữ nguyên tín hiệu màu
        hsv_h=0.010, hsv_s=0.15, hsv_v=0.20,
        erasing=0.10, mosaic=0.0, mixup=0.0, auto_augment=None,
        degrees=15.0, translate=0.05, scale=0.20,
        fliplr=0.5, flipud=0.5,      # quả gần tròn nên lật dọc vẫn hợp lệ
        plots=True, val=True,
    )
    mins = (time.time() - t0) / 60
    print(f"Thời gian huấn luyện: {mins:.1f} phút")

    # Lấy thư mục ultralytics THỰC SỰ đã ghi, thay vì tự ghép lại đường dẫn.
    save_dir = Path(getattr(results, "save_dir", Path(project_abs) / args.name))
    best = save_dir / "weights" / "best.pt"
    if not best.exists():
        raise SystemExit(
            f"Không tìm thấy {best}.\n"
            f"Ultralytics đã ghi kết quả vào: {save_dir}\n"
            f"Nếu thư mục này nằm ngoài dự án, chạy lệnh sau để đặt lại:\n"
            f"    yolo settings runs_dir='{Path.cwd() / 'outputs'}'")
    print(f"Kết quả huấn luyện: {save_dir}")

    model = YOLO(str(best))
    export_predictions(model, data / "val", args.imgsz, save_dir / "predictions.csv")

    n_params = sum(p.numel() for p in model.model.parameters())
    save_json({"so_tham_so": int(n_params), "model": args.model,
               "epochs": args.epochs, "seed": args.seed,
               "phut_huan_luyen": round(mins, 1)}, save_dir / "model_info.json")
    print(f"Số tham số: {n_params/1e6:.2f} M   <-- điền vào Bảng 8")
    print(f"BƯỚC TIẾP: python scripts/06_evaluate.py --pred "
          f"{save_dir/'predictions.csv'} --out outputs/{args.name}")


if __name__ == "__main__":
    main()
