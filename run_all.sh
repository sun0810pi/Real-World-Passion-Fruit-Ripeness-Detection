#!/usr/bin/env bash
# Chạy toàn bộ pipeline một lượt.
# Dừng ngay khi có lỗi, để không âm thầm bỏ qua một bước hỏng.
set -euo pipefail

RAW=${1:-data/raw}
export PYTHONPATH="$(pwd)"

echo "===== 00: dò bố cục thẻ ====="
python scripts/00_calibrate_layout.py --data "$RAW"

echo "===== 01: lập bảng kê ====="
python scripts/01_build_manifest.py --data "$RAW" --out data/manifest.csv

if ! python - <<'PY'
import sys, pandas as pd
d = pd.read_csv("data/manifest.csv", dtype=str, keep_default_na=False)
sys.exit(0 if (d["fruit_id"].str.len() > 0).all() else 1)
PY
then
  echo
  echo "DỪNG: cột fruit_id chưa điền xong."
  echo "  1. python scripts/01b_tag_sheets.py --data $RAW --out data/tags"
  echo "  2. Mở data/tags/sheet_00.png, điền data/tags/fruit_ids.csv"
  echo "  3. python scripts/01b_tag_sheets.py --fill-down data/tags/fruit_ids.csv"
  echo "  4. python scripts/01b_tag_sheets.py --merge data/tags/fruit_ids.csv --manifest data/manifest.csv"
  echo "  5. Chạy lại run_all.sh"
  exit 1
fi

echo "===== 02: tiền xử lý (hai cấu hình) ====="
python scripts/02_preprocess.py --manifest data/manifest.csv --out data/proc_wb   --whitebalance patches
python scripts/02_preprocess.py --manifest data/manifest.csv --out data/proc_nowb --whitebalance none

echo "===== 03: kiểm toán rò rỉ ====="
python scripts/03_split.py --manifest data/proc_wb_manifest.csv --mode audit

echo "===== 03: chia tập theo quả, ba hạt giống ====="
for s in 0 1 2; do
  python scripts/03_split.py --manifest data/proc_wb_manifest.csv --mode fruit --seed "$s"
done

echo "===== 04: đường cơ sở màu ====="
python scripts/04_color_baseline.py --split-dir data/splits/fruit_seed0 --out outputs/baseline_seed0
python scripts/06_evaluate.py --pred outputs/baseline_seed0/predictions.csv --out outputs/baseline_seed0

echo "===== 05 + 06: học sâu, ba hạt giống ====="
for s in 0 1 2; do
  python scripts/05_train_yolo.py --data "data/splits/fruit_seed$s" --name "cungnguon_s$s" --seed "$s"
  python scripts/06_evaluate.py --pred "outputs/runs/cungnguon_s$s/predictions.csv" --out "outputs/cungnguon_s$s"
done
python scripts/06_evaluate.py --aggregate outputs/cungnguon_s0 outputs/cungnguon_s1 outputs/cungnguon_s2

echo "===== 07: tầng ước lượng môi trường ====="
python scripts/07_illuminant.py --mode extract --manifest data/manifest.csv --out outputs/illum.csv
python scripts/07_illuminant.py --mode baseline --illum outputs/illum.csv

echo "===== 08: đầu ra tình trạng quả ====="
python scripts/08_condition_head.py --manifest data/proc_wb_manifest.csv || \
  echo "(bỏ qua: cột tinh_trang chưa điền)"

echo "===== 09: gom số điền báo cáo ====="
python scripts/09_report_numbers.py

echo
echo "XONG. Kết quả nằm trong outputs/"
