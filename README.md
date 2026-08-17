# Pipeline dự đoán độ chín quả chanh dây

Công trình dự thi Giải thưởng Sinh viên Nghiên cứu khoa học Euréka lần thứ 28, năm 2026.

**Nguyên tắc thiết kế xuyên suốt:** mọi con số đưa vào báo cáo phải đến từ một phép đánh giá không rò rỉ. Chia tập theo nguồn, rồi theo quả — không bao giờ chia ngẫu nhiên theo ảnh.

---

## Cài đặt (5 phút)

```bash
git clone <repo>            # hoặc giải nén file zip
cd chanhday-pipeline

python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS / Linux:
source .venv/bin/activate

pip install -r requirements.txt
pytest tests/ -q            # phải thấy "36 passed"
```

Chỉ chạy các bước 00–04 và 08 thì không cần torch, dùng bản nhẹ:

```bash
pip install -r requirements-minimal.txt
```

Mở thư mục bằng VS Code. Nhấn `F5` để chạy từng bước qua menu Run and Debug — mọi bước đã cấu hình sẵn trong `.vscode/launch.json`.

---

## Đặt dữ liệu

Chép ảnh vào `data/raw/`, hoặc trỏ thẳng `--data` vào nơi ảnh đang nằm — cách nào cũng được.

```
data/
  raw/
    Chieu_4_14-8-2026/
      IMG_1689.JPG
      IMG_1689.CR3        # RAW đi kèm, script tự tìm
      ...
    Sang_5_15-8-2026/
      ...
```

Không cần chia sẵn theo thư mục nhãn. Script sẽ tự lo.

---

## Số ảnh không khớp với con số bạn nhớ?

```bash
python scripts/kiem_ke.py --data "D:\qua_chanh" --so-qua-mong-doi 210
```

Quét toàn bộ cây thư mục, đếm ảnh thường và file RAW riêng, phân bố theo thư mục, và đối chiếu với số quả bạn khai. Bắt được ba nguyên nhân phổ biến nhất: `--data` trỏ vào một nhánh con, lần chụp chỉ có RAW, và nhầm giữa số ảnh với số quả.

---

## Không nhớ đang ở bước nào?

```bash
python scripts/trang_thai.py
```

Liệt kê đã làm tới đâu và in ra đúng lệnh kế tiếp. Chạy được bất cứ lúc nào, không sửa gì cả.

---

## Trình tự chạy

### Bước 0 — Dò bố cục thẻ (chỉ khi đổi máy hoặc đổi cách chụp)

```bash
python scripts/00_calibrate_layout.py --data data/raw/Chieu_4_14-8-2026
```

Mở `outputs/layout_check.jpg`. Ô đỏ phải trùm đúng 4 ô xám, ô xanh lá trùm mảnh giấy ghi mã quả. Sai thì chỉnh `--patch-x0`, `--patch-dx` rồi chạy lại.

### Bước 1 — Lập bảng kê và điền mã quả

```bash
python scripts/01_build_manifest.py --data data/raw --out data/manifest.csv

# Kiểm tra vùng nhãn cắt có đúng không, TRƯỚC khi làm cả nghìn ảnh
python scripts/01b_tag_sheets.py --probe --data data/raw --out data/tags
# -> mở data/tags/probe_tag.jpg, khung xanh phải trùm mảnh giấy ghi mã quả

python scripts/01b_tag_sheets.py --data data/raw --out data/tags
```

Vị trí nhãn được **dò tự động trên từng ảnh**, không dùng toạ độ cố định, vì khoảng cách chụp thay đổi giữa các đợt. Ô nào dò không ra sẽ có viền đỏ trên trang và `tag_found=0` trong file — **đừng đoán mã cho các ô đó**, `--fill-down` sẽ tự dừng ở chúng.

Trang còn đánh dấu `QUA MOI?` ở những chỗ ảnh nhãn thay đổi rõ so với ảnh trước, giúp bạn không bỏ sót ranh giới đổi quả. Ngưỡng tự tính từ dữ liệu.

Mở `data/tags/sheet_00.png`, đọc mã trên từng ô. Trong `data/tags/fruit_ids.csv` **chỉ điền dòng đổi quả** — các dòng sau để trống. Điền luôn cột `label` và `tinh_trang` (`dung_duoc` / `hong`) trong cùng lượt.

```bash
python scripts/01b_tag_sheets.py --fill-down data/tags/fruit_ids.csv
python scripts/01b_tag_sheets.py --merge data/tags/fruit_ids.csv --manifest data/manifest.csv
```

Còn cột `source_id` phải điền tay theo sổ thu mẫu — script không đoán được xuất xứ.

### Bước 2 — Tiền xử lý, chạy hai lần

```bash
python scripts/02_preprocess.py --manifest data/manifest.csv --out data/proc_wb   --whitebalance patches
python scripts/02_preprocess.py --manifest data/manifest.csv --out data/proc_nowb --whitebalance none
```

Có file RAW thì thêm `--use-raw` cho lần thứ nhất: đo màu trên RAW tuyến tính chính xác hơn JPEG đã qua cân bằng trắng của máy.

Chênh lệch hiệu năng giữa hai bộ này chính là con số tách "phần biến thiên do chiếu sáng" khỏi "phần do khác biệt giống" ở mục 4.4.

### Bước 3 — Kiểm toán rồi chia tập

```bash
python scripts/03_split.py --manifest data/proc_wb_manifest.csv --mode audit
```

Đọc kỹ kết quả này trước khi làm tiếp. Nó cho biết cỡ mẫu thực và mức rò rỉ.

```bash
for s in 0 1 2; do
  python scripts/03_split.py --manifest data/proc_wb_manifest.csv --mode fruit --seed $s
done
python scripts/03_split.py --manifest data/proc_wb_manifest.csv --mode loso
```

### Bước 4 — Đường cơ sở màu (chạy trước YOLO)

```bash
python scripts/04_color_baseline.py --split-dir data/splits/fruit_seed0 --out outputs/baseline_seed0
python scripts/06_evaluate.py --pred outputs/baseline_seed0/predictions.csv --out outputs/baseline_seed0
```

Chỉ mất vài giây và cho biết ngay bài toán khó tới đâu.

### Bước 5 — Học sâu

```bash
for s in 0 1 2; do
  python scripts/05_train_yolo.py --data data/splits/fruit_seed$s --name cungnguon_s$s --seed $s
  python scripts/06_evaluate.py --pred outputs/runs/cungnguon_s$s/predictions.csv --out outputs/cungnguon_s$s
done
python scripts/06_evaluate.py --aggregate outputs/cungnguon_s0 outputs/cungnguon_s1 outputs/cungnguon_s2
```

### Bước 6 — Bỏ ra một nguồn

```bash
for n in N1 N2 N3; do
  python scripts/05_train_yolo.py --data data/splits/loso_$n --name loso_$n --seed 0
  python scripts/06_evaluate.py --pred outputs/runs/loso_$n/predictions.csv --out outputs/loso_$n
done
```

### Bước 7 — Đầu ra thứ hai và tầng môi trường

```bash
python scripts/08_condition_head.py --manifest data/proc_wb_manifest.csv

python scripts/07_illuminant.py --mode extract --manifest data/manifest.csv --out outputs/illum.csv
python scripts/07_illuminant.py --mode baseline --illum outputs/illum.csv
python scripts/07_illuminant.py --mode train --illum outputs/illum.csv --epochs 40
```

### Bước 8 — Gom số điền báo cáo

```bash
python scripts/09_report_numbers.py
```

In toàn bộ số theo đúng thứ tự các ô `[…]`, kèm lệnh cần chạy cho ô nào còn thiếu.

Chạy tất cả một lượt: `bash run_all.sh` (macOS/Linux) hoặc `run_all.bat` (Windows).

---

## Cấu trúc

```
chanhday/                 thư viện dùng chung
  config.py               hằng số, bố cục thẻ, ma trận chi phí
  cards.py                thẻ chuẩn, ước lượng và hiệu chỉnh nguồn sáng
  segmentation.py         tách nền, cắt hộp bao
  features.py             đặc trưng CIE L*a*b*
  metrics.py              Kappa, chi phí, hiệu chuẩn, từ chối trả lời
  io_utils.py             bảng kê, EXIF, RAW

scripts/                  chạy theo thứ tự 00 -> 09
configs/default.yaml      bố cục thẻ và ngưỡng
tests/                    pytest, không cần dữ liệu thật
docs/                     ghi chú thiết kế
```

---

## Ánh xạ: ô `[…]` trong báo cáo ⟵ file kết quả

| Mục / Bảng | Lấy từ |
|---|---|
| Bảng 2 — đặc điểm các nguồn | `data/manifest.csv` nhóm theo `source_id` |
| Bảng 5 — thống kê mô tả | `scripts/09_report_numbers.py` |
| Bảng 6 — phân bố quả theo bậc × nguồn | `03_split.py --mode audit` |
| Bảng 7 — chỉ tiêu hóa sinh | **phải đo bằng khúc xạ kế** |
| Bảng 8 — so sánh phương pháp | `outputs/bang_8_10.csv`, `model_info.json` |
| Bảng 8b — tình trạng quả | `outputs/tinh_trang/metrics.json` |
| Bảng 9 — bỏ ra một nguồn | `outputs/loso_*/metrics.json` |
| Bảng 10 — chi phí bất đối xứng | `outputs/bang_8_10.csv` |
| Hình 2 — demo tiền xử lý | `data/proc_wb_hinh2_montage.jpg` |
| Hình 5 — ma trận nhầm lẫn | `outputs/*/confusion_matrix.csv` |
| Mục 4.1 — tỷ lệ tách nền | `data/proc_wb_stats.json` |
| Mục 4.2 — tỷ lệ vỏ chuyển màu từ ảnh | đặc trưng `frac_vo_chuyen_mau` |
| Mục 4.4 — vai trò chuẩn hóa màu | chênh lệch `proc_wb` và `proc_nowb` |
| Mục 4.4 — ước lượng nguồn sáng | `outputs/illuminant_baselines.csv` |
| Mục 4.5 — R² và RMSE với TSS | **cần số liệu TSS** |
| Mục 4.6 — chi phí kỳ vọng | `outputs/*/metrics.json` |

---

## Ba cảnh báo

1. **Ma trận chi phí trong `chanhday/config.py` là giá trị mặc định để chạy thử** (muộn 3,0 / sớm 1,0). Mục 3.6 yêu cầu tham vấn nông hộ và doanh nghiệp thu mua. Phải thay trước khi đưa số vào Bảng 10.
2. **Ngưỡng `a_star_turned` trong `configs/default.yaml` cần hiệu chỉnh** theo bộ ảnh thật, đúng như ghi chú dưới Bảng 3 của báo cáo.
3. **Nếu độ chính xác vẫn trên 97%**, script 06 sẽ tự cảnh báo. Đừng mừng — quay lại `03_split.py --mode audit`.

---

## Xử lý sự cố

| Triệu chứng | Nguyên nhân và cách sửa |
|---|---|
| `ModuleNotFoundError: chanhday` | Chạy script từ thư mục gốc dự án, không phải từ trong `scripts/` |
| Tỷ lệ đọc thẻ = 0% | Bố cục thẻ khác mặc định. Chạy `scripts/00_calibrate_layout.py` |
| Tách nền chọn nhầm cái thẻ | `card_roi` trong `configs/default.yaml` chưa trùm hết thẻ |
| `Cột fruit_id còn trống` | Chưa chạy `01b --fill-down` và `01b --merge` |
| `Cần ít nhất 2 nguồn` | Cột `source_id` chưa điền, hoặc thật sự mới có một nguồn |
| Train chậm bất thường trên Colab | Dữ liệu đang nằm trên Google Drive. Script 05 tự copy về `/content/`; nếu vẫn chậm, copy tay trước |
| `rawpy` cài không được | Bỏ `--use-raw`, script tự dùng JPEG |
| `pip install -r` báo `UnicodeDecodeError: 'charmap'` | Bản cũ có chú thích tiếng Việt trong requirements.txt. Bản này đã thuần ASCII; nếu vẫn gặp, chạy `$env:PYTHONUTF8=1` trước |
| `UnicodeEncodeError` khi script in ra màn hình | Đã tự xử lý trong `chanhday/__init__.py`. Nếu vẫn gặp, chạy `$env:PYTHONUTF8=1` |
| `Không tìm thấy ảnh nào trong data\raw` | Chưa chép ảnh vào. Thông báo lỗi liệt kê thư mục đang có gì và hai cách khắc phục |
| `Không có file: ...fruit_ids.csv` | Chưa chạy bước sinh trang. Thông báo lỗi chỉ đúng lệnh cần chạy, và tự tìm file cùng tên nếu bạn đã ghi ra `--out` khác |
| Không nhớ đang ở bước nào | `python scripts/trang_thai.py` |
| Số ảnh ít hơn nhiều so với dự kiến | `python scripts/kiem_ke.py --data <thư mục gốc> --so-qua-mong-doi <số>` |
| Nhiều lần chụp chỉ có file CR3 | `pip install rawpy` rồi thêm `--include-raw` vào script 01 |

---

## Nhật ký sửa lỗi (v1.1)

Sáu lỗi phát hiện khi chạy thật trên Windows, đã sửa và có test hồi quy đi kèm.

| # | Triệu chứng | Nguyên nhân | Đã sửa ở |
|---|---|---|---|
| 1 | `imread_('Chanh d├óy t├¡m RP9\...'): can't open/read file` — ảnh biến mất âm thầm | `cv2.imread` dùng bảng mã ANSI, thất bại với đường dẫn có dấu, và trả `None` thay vì ném lỗi | `imread_unicode` / `imwrite_unicode` trong `io_utils`, dùng ở mọi script |
| 2 | 200 ảnh vào, 83 ảnh ra, không ai biết mất ở đâu | Không có bước đối chiếu số lượng | Sổ kế toán `*_ledger.csv` in ra cuối script 02 |
| 3 | `FileNotFoundError: runs_fixed\cungnguon_s0\weights\best.pt` sau khi train xong | `project` tương đối bị ultralytics ghép vào `runs_dir`, kết quả rơi vào `C:\Users\<tên>\runs\` | Ép `project` tuyệt đối và đọc `results.save_dir` |
| 4 | Tập val 12 ảnh nhưng `predictions.csv` chỉ 6 dòng | Vòng lặp chỉ duyệt `CLASS_NAMES`, thư mục tên khác bị bỏ qua âm thầm | Script 05 liệt kê rõ mọi thư mục bị bỏ và số ảnh tương ứng |
| 5 | `6_hong` bị nhét thành lớp thứ sáu, chỉ số bậc chín dịch chuyển | Trộn hai trục nhãn vào một | `CONDITION_DIR_ALIASES` đưa thư mục hỏng sang cột `tinh_trang` |
| 6 | `ERROR test: found 13 images in 3 classes (requires 4 classes)` | Thư mục `test/` thiếu lớp so với `train/` | Script 05 kiểm tra trước và chỉ rõ lớp nào thiếu |

## Nhật ký sửa lỗi (v1.2)

Năm lỗi nữa, tìm ra bằng cách tự soi lại code và từ phản hồi khi dùng thật.

| # | Triệu chứng | Nguyên nhân | Đã sửa ở |
|---|---|---|---|
| 7 | Hai ảnh cùng tên `IMG_1689.JPG` từ hai nguồn, ảnh sau đè ảnh trước; sổ kế toán vẫn báo đủ | Ghi ra thư mục phẳng theo lớp, giữ nguyên tên gốc | `unique_stem()` gắn thêm 6 ký tự băm; script 02 đối chiếu lại số file thật trên đĩa |
| 8 | Gộp mã quả làm 2 dòng thành 4, nhãn gán chéo sang ảnh khác | `merge` theo tên file, trùng tên tạo tích Descartes | Gộp theo đường dẫn đầy đủ, `validate="m:1"`, khẳng định số dòng không đổi |
| 9 | Trang đọc mã từ `sheet_12` trở đi hiện vỏ quả thay vì mã | `--tag-roi` là toạ độ cố định, khung hình đổi thì cắt sai chỗ | `detect_tag()` dò tự động từng ảnh, phân biệt mảnh giấy với dải ô xám bằng mật độ biên và tính nhóm |
| 10 | Không biết ô nào cắt trúng nhãn, dễ đoán bừa mã quả | Không có cơ chế báo hiệu | Viền đỏ trên trang, cột `tag_found`, `--fill-down` tự dừng ở dòng không dò ra |
| 11 | Quả nửa xanh nửa đỏ (bậc 3) bị mô tả thành màu vàng | Trung bình số học áp lên đại lượng góc | Thống kê vòng tròn, thêm đặc trưng `H_dong_deu` phân biệt màu đều với màu loang lổ |

## Nhật ký sửa lỗi (v1.3)

| # | Triệu chứng | Nguyên nhân | Đã sửa ở |
|---|---|---|---|
| 12 | `pip install -r requirements.txt` chết ngay: `UnicodeDecodeError: 'charmap' codec can't decode byte 0x8d` | pip trên Windows đọc file bằng cp1252, mà chú thích trong file lại có dấu tiếng Việt | `requirements.txt` thuần ASCII, thêm `requirements-minimal.txt`; test chặn byte ngoài ASCII |
| 13 | Script chết giữa chừng với `UnicodeEncodeError` khi in tiếng Việt trên cửa sổ lệnh Windows | Bảng mã mặc định của console không phải UTF-8 | `chanhday/__init__.py` tự ép `stdout`/`stderr` sang UTF-8 khi được nạp |
| 14 | `Không tìm thấy ảnh nào trong data\raw` — không biết phải làm gì tiếp | Thông báo lỗi không nói gì thêm | `chan_doan_thu_muc()` liệt kê thư mục có tồn tại không, bên trong có gì, các đuôi file tìm thấy, và hai cách khắc phục kèm lệnh cụ thể |

## Nhật ký sửa lỗi (v1.4)

| # | Triệu chứng | Nguyên nhân | Đã sửa ở |
|---|---|---|---|
| 15 | `FileNotFoundError` kèm 20 dòng traceback pandas khi thiếu file đầu vào | Không kiểm tra file trước khi đọc | `doc_bat_buoc()` tra bảng file nào do bước nào sinh ra, in đúng lệnh cần chạy, và tự tìm file cùng tên ở nơi khác trong dự án |
| 16 | Không biết đang ở bước nào trong chuỗi 10 bước | Không có cách kiểm tra | `scripts/trang_thai.py` liệt kê tiến độ và in lệnh kế tiếp |

## Nhật ký sửa lỗi (v1.5)

| # | Triệu chứng | Nguyên nhân | Đã sửa ở |
|---|---|---|---|
| 17 | Nhiều lần chụp biến mất khỏi bảng kê | File chỉ có `.CR3`, không có `.JPG` đi kèm; `iter_images` mặc định bỏ qua RAW. Trên thư mục mẫu là 4/19 lần chụp, tức 21% | Script 01 báo rõ số lần chụp chỉ có RAW, thêm cờ `--include-raw`; script 02 tự giải mã RAW khi ảnh gốc là RAW |
| 18 | Không biết ảnh bị bỏ ở thư mục nào | Chỉ có con số tổng | Script 01 in bảng từng thư mục con: ảnh nhận / tổng file, và liệt kê đuôi file của thư mục không nhận được ảnh nào |
| 19 | Nhầm giữa số ảnh và số quả | Không nói rõ đơn vị | Script 01 ghi rõ mỗi dòng là một ảnh; thêm `scripts/kiem_ke.py` đối chiếu với số quả mong đợi |

Thêm: tập kiểm tra nay được chia phân tầng theo bậc chín nên không còn thiếu hẳn một bậc; script 06 chặn sớm khi chỉ số lớp vượt 0–4 (dấu hiệu quả hỏng bị nhét vào thang độ chín) và khi tập kiểm tra dưới 30 mẫu.

Ngoài ra script 06 nay cảnh báo khi tập kiểm tra dưới 30 mẫu, kèm danh sách ba chỗ cần kiểm tra để tìm ảnh bị mất.
