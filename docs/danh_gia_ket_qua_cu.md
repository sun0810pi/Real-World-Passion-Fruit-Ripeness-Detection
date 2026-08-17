# Đánh giá kết quả train + Kế hoạch hoàn thiện
**Đề tài:** Dự đoán độ chín quả chanh dây từ ảnh điện thoại (Eureka 2026)
**Ngày rà soát:** 15/08/2026

---

## PHẦN 1 — KIỂM TRA KẾT QUẢ TRAIN

### 1.1. Những gì thực sự có trong file kết quả

| Lần chạy | Model | Epoch | Thời gian | Val top-1 | Trạng thái |
|---|---|---|---|---|---|
| `yolo11_cls_5bac_chin` | yolo11m-cls | 5/50 | 0,91 h | 0,681 (đỉnh 0,824) | **Đứt giữa chừng** |
| `yolo11_cls_5bac_chin-2` | yolo11m-cls | 50/50 | 0,03 h | 1,000 | **Hỏng — chỉ 2 ảnh, 1 lớp** |
| `yolo11_cls_5bac_chin-3` | yolo11m-cls | 50/50 | 3,59 h | **0,995** | Chạy trọn |
| `yolo_cls_5bac_chin` | yolov8m-cls | — | — | — | Chỉ có `args.yaml`, không có kết quả |

Suy ra từ chỉ số batch trong log (`train_batch960` ⇒ 24 batch/epoch × 32):

- Tập train ≈ **737–768 ảnh**, tập val = **188 ảnh** ⇒ tổng ≈ **925–955 ảnh**, chia ~80/20.
- Phân bố val (từ confusion matrix): bậc 1 = 39, bậc 2 = 38, bậc 3 = 95, bậc 4 = 10, bậc 5 = 6.
- Suy ra toàn bộ dữ liệu: bậc 3 ≈ 475 ảnh, còn **bậc 4 ≈ 50 ảnh và bậc 5 ≈ 30 ảnh**.

### 1.2. Kết luận: con số 99,5% không dùng được

Đây không phải chê — đây chính xác là cái bẫy mà **mục 2.5, hạn chế thứ hai** trong báo cáo của bạn đã mô tả. Bạn viết đúng lý thuyết rồi tự rơi vào nó khi thực hành. Bằng chứng:

**a) Ma trận nhầm lẫn hoàn hảo tuyệt đối.** 188/188, không một ô lệch nào. Với bài toán mà chính báo cáo nói ranh giới giữa các bậc là "ranh giới liên tục" và hai người gán nhãn còn bất đồng, một mô hình không sai một ảnh nào là dấu hiệu rò rỉ dữ liệu, không phải dấu hiệu mô hình giỏi.

**b) `val/loss` (0,010) thấp hơn `train/loss` (0,104).** Kinh điển. Tập val dễ hơn tập train một cách bất thường — nghĩa là mô hình đã "gặp" nội dung của tập val rồi.

**c) Nguyên nhân gần như chắc chắn: chia tập ngẫu nhiên theo ảnh.** Ảnh trong `val_batch0_labels.jpg` và `train_batch0.jpg` cùng một phông vải đen, cùng khoảng cách, cùng thẻ xám ở góc phải dưới. Mỗi quả được chụp nhiều góc ⇒ ảnh của **cùng một quả** nằm cả ở train lẫn val. Mô hình chỉ cần nhận ra "quả có vết sẹo hình chữ V này" là trả lời đúng. Đây đúng là điều mục **3.4.8** yêu cầu phải tránh: *"Chia ngẫu nhiên theo ảnh sẽ tạo ra kết quả cao một cách giả tạo, vì hai ảnh của cùng một quả gần như là hai bản sao."*

**d) Mất cân bằng lớp nghiêm trọng.** Bậc 5 chỉ có ~30 ảnh trên toàn bộ dữ liệu, bậc 4 ~50, trong khi bậc 3 có ~475. Sàn mà mục **3.4.6** đặt ra (20 quả mỗi bậc mỗi nguồn) chưa đạt ở bậc 4 và bậc 5, kể cả khi tính theo ảnh chứ chưa nói theo quả.

**e) `accuracy_top5` = 1,000 ở mọi epoch.** Với 5 lớp thì top-5 luôn bằng 1. Chỉ số này vô nghĩa, đừng đưa vào báo cáo.

### 1.3. Sai lệch giữa quy trình đã viết và quy trình đã chạy

| Mục trong báo cáo | Đã viết | Đã chạy |
|---|---|---|
| 3.4.3 — Hiệu chỉnh màu theo thẻ chuẩn | Có | **Chưa** — ảnh thô đưa thẳng vào YOLO |
| 3.4.3 — Tách nền, tạo mặt nạ, cắt hộp bao | Có | **Chưa** — còn nguyên phông + thẻ xám trong khung |
| 3.4.8 — Chia theo nguồn, rồi theo quả | Có | **Chưa** — chia ngẫu nhiên theo ảnh |
| 3.5 — Đường cơ sở thống kê màu L\*a\*b\* | Có | **Chưa** |
| 3.5 — Đường tham chiếu con người | Có | **Chưa** |
| 3.5 — Thí nghiệm có/không chuẩn hóa màu | Có | **Chưa** |
| 3.6 — Đánh giá bỏ ra một nguồn | Có | **Chưa** |
| 3.6 — Ma trận chi phí bất đối xứng | Có | **Chưa** |
| 3.6 — Ba hạt giống ngẫu nhiên | Có | **Chưa** — chỉ `seed: 42` |
| 3.4.5 — TSS/TA đo trên chính quả đã chụp | Có | **Chưa thấy dữ liệu** |
| 3.4.8 — Kappa có trọng số giữa 2 người gán nhãn | Có | **Chưa** |

**Đọc bảng này theo hướng tích cực:** phần khó nhất (thiết kế nghiên cứu) bạn đã làm xong và làm tốt hơn phần lớn bài Eureka. Phần còn thiếu là phần thi công, và toàn bộ nằm trong tầm tay.

### 1.4. Vấn đề trong cấu hình huấn luyện

Từ `args.yaml`:

- **`hsv_s: 0.7`, `hsv_v: 0.4`** — tăng cường dữ liệu bằng cách xáo trộn độ bão hòa ±70% và độ sáng ±40%. Với bài toán mà **tín hiệu duy nhất là màu**, đây là tự phá tín hiệu. Bạn đang dạy mô hình bỏ qua đúng thứ cần nhìn. Giảm xuống `hsv_s: 0.2`, `hsv_v: 0.2` — vừa đủ để chống nhiễu chiếu sáng, không đủ để xóa ranh giới bậc chín.
- **`erasing: 0.4`** — xóa ngẫu nhiên 40% ảnh. Nhìn `train_batch0.jpg` thấy nhiều ô đen che gần hết quả, có một ảnh bị hỏng hoàn toàn thành nhiễu màu. Giảm còn `0.1` hoặc tắt.
- **`mosaic: 1.0`** — tham số của bài toán phát hiện, không có tác dụng ở chế độ `classify`. Bỏ.
- **`imgsz: 224`** trong khi quả chỉ chiếm ~5% khung hình ⇒ quả thực tế chỉ còn khoảng 50×50 pixel. Sau khi cắt theo hộp bao thì 224 là hợp lý, còn hiện tại thì đang lãng phí gần hết độ phân giải.
- **`yolo11m-cls`** (~10 M tham số) là quá lớn cho ~750 ảnh. Dùng `yolo11n-cls` hoặc `yolo11s-cls`, vừa hợp cỡ dữ liệu vừa đúng mục tiêu "chạy được trên điện thoại" ở mục 4.3.
- **3,59 giờ cho 50 epoch** với 750 ảnh 224px là quá chậm — gần như chắc chắn đang đọc dữ liệu trực tiếp từ Google Drive. Copy dataset vào `/content/` trước khi train, sẽ nhanh hơn khoảng 10 lần.

---

## PHẦN 2 — Ý TƯỞNG "TỰ PHÁN ĐOÁN MÔI TRƯỜNG" VÀ MỨC KHẢ THI

Ý bạn nêu: mô hình không chỉ đọc độ chín, mà **ước lượng điều kiện chiếu sáng của môi trường xung quanh, tự hiệu chỉnh màu thật của quả trong môi trường đó, rồi mới kết luận độ chín.**

### 2.1. Đánh giá: đây là phần mạnh nhất của đề tài

Trên bình diện học thuật, đây chính là bài toán **color constancy / illuminant estimation** — một nhánh đã có nền tảng vững trong thị giác máy tính. Nhưng gắn nó vào bài toán độ chín nông sản thì hiếm, và nó trả lời trực tiếp Câu hỏi 2 (khả năng tổng quát) mà báo cáo đặt làm trục chính.

Quan trọng hơn: **bạn đã có sẵn dữ liệu để làm việc này mà chưa nhận ra.** Thẻ xám trong mỗi khung hình cho bạn **nhãn đúng của nguồn sáng** ở từng ảnh. Nghĩa là bạn có thể huấn luyện một mô-đun ước lượng nguồn sáng **từ cảnh, không cần thẻ**, lấy giá trị suy từ thẻ làm nhãn giám sát. Đây là kỹ thuật chưng cất (distillation) và nó biến một chi tiết thủ tục thành một đóng góp khoa học riêng.

### 2.2. Kiến trúc đề xuất — ba tầng

```
Ảnh thô từ điện thoại
   │
   ├─ Tầng A: ƯỚC LƯỢNG NGUỒN SÁNG
   │    Đầu vào: ảnh + metadata EXIF (ISO, tốc độ, khẩu, nhiệt độ màu AWB)
   │    Đầu ra:  vector nguồn sáng (r, g, b) chuẩn hóa
   │    Huấn luyện: nhãn lấy từ thẻ xám  ← đây là chỗ mới
   │
   ├─ Tầng B: HIỆU CHỈNH MÀU (von Kries) + TÁCH NỀN + CẮT
   │    Đầu ra: ảnh quả đã đưa về nguồn sáng chuẩn D65
   │
   └─ Tầng C: PHÂN LOẠI ĐỘ CHÍN
        Đầu vào: ảnh đã hiệu chỉnh (+ tùy chọn: vector nguồn sáng làm đặc trưng phụ)
        Đầu ra:  bậc 1–5 + độ tin cậy đã hiệu chuẩn
```

### 2.3. Mức khả thi theo từng tầng

| Thành phần | Khả thi | Ghi chú |
|---|---|---|
| Hiệu chỉnh theo thẻ xám (có thẻ trong ảnh) | **Rất cao** | Toán học đơn giản, dữ liệu đã có. Làm trong 1 ngày. |
| Đường cơ sở không học: Gray-World, Shades-of-Gray, Max-RGB | **Rất cao** | Mỗi thuật toán ~15 dòng code. Bắt buộc phải có để so sánh. |
| Ước lượng nguồn sáng bằng CNN, chưng cất từ thẻ | **Cao** | Cần ~300–500 ảnh phủ nhiều điều kiện sáng. Chụp cùng một mẻ quả ở 5–6 khung giờ là đủ. |
| Dùng EXIF làm đặc trưng phụ | **Cao** | Gần như miễn phí, chỉ cần đọc metadata. Ít người làm, dễ ăn điểm. |
| Sinh dữ liệu bằng cách mô phỏng lại nguồn sáng | **Trung bình–cao** | Từ ảnh đã hiệu chỉnh, nhân lại với nguồn sáng ngẫu nhiên ⇒ tăng dữ liệu **đúng vật lý** thay vì `hsv_s: 0.7` bừa bãi. Kỹ thuật này vừa sửa lỗi ở mục 1.4 vừa là một đóng góp. |
| Suy độ chín dưới nguồn sáng hoàn toàn mới, không thẻ | **Trung bình** | Đây là mục tiêu cuối. Có thể không đạt, nhưng đo được mức sụt giảm là đã có kết quả để báo cáo. |

### 2.4. Rủi ro cần nói thẳng

1. **Thẻ của bạn là thẻ xám bậc thang, không phải bảng ColorChecker 24 ô.** Thẻ xám chỉ cho bạn hiệu chỉnh cân bằng trắng (3 hệ số kênh). Muốn hiệu chỉnh màu đầy đủ (ma trận 3×3 + tuyến tính hóa gamma) thì cần thẻ màu 24 ô. Berry và cs (2018) mà bạn trích ở mục 2.3 dùng bảng 24 ô. **Khuyến nghị: mua một ColorChecker Passport hoặc bản in chuẩn (~200–500 k) trước đợt thu mẫu tiếp theo.** Nếu không kịp, vẫn dùng thẻ xám và ghi rõ trong hạn chế rằng chỉ hiệu chỉnh được cân bằng trắng.
2. **Ảnh JPEG từ điện thoại đã qua xử lý.** Máy đã tự cân bằng trắng, ánh xạ tông, nén. Nguồn sáng suy ra từ ảnh JPEG là "nguồn sáng còn sót lại sau AWB", không phải nguồn sáng vật lý. Không sai, nhưng phải mô tả đúng trong báo cáo. **Nếu điện thoại chụp được RAW/DNG, hãy bật.**
3. **Toàn bộ ảnh hiện tại chụp trên nền vải đen trong nhà.** Muốn nói chuyện "môi trường xung quanh" thì phải có ảnh ngoài trời, nhiều giờ, nhiều thời tiết. Đây là việc phải làm, không có đường tắt.

### 2.5. Kết luận phần 2

Ý tưởng **khả thi và đáng làm**, và nó nâng đề tài từ "phân loại ảnh nông sản, đã có nhiều người làm" lên "định lượng và xử lý được dịch chuyển miền do chiếu sáng trong bài toán độ chín". Nhưng nó chỉ có giá trị **sau khi** phần đánh giá được sửa cho đúng. Một mô-đun ước lượng nguồn sáng gắn lên một phép đánh giá bị rò rỉ vẫn cho ra 99,5% và vẫn vô nghĩa.

**Thứ tự bắt buộc: sửa phép chia tập trước, thêm mô-đun môi trường sau.**

---

## PHẦN 3 — KẾ HOẠCH THI CÔNG

### Giai đoạn 0 — Kiểm toán dữ liệu hiện có (2–3 ngày)

Việc này phải xong trước mọi thứ khác, vì kết quả của nó quyết định các giai đoạn sau.

- [ ] Lập bảng kê từng ảnh với các cột: `image_path`, `fruit_id`, `source_id`, `session_id`, `label`, `capture_time`. Chạy `scripts/01_build_manifest.py`.
- [ ] **Trả lời câu hỏi sống còn: mỗi quả được chụp bao nhiêu ảnh, và có bao nhiêu quả riêng biệt?** Nếu 940 ảnh chỉ từ 60 quả thì cỡ mẫu thực của bạn là 60, không phải 940.
- [ ] Xác định số nguồn thu mẫu. Nếu chỉ có 1 nguồn thì Câu hỏi 2 chưa trả lời được và phải đi thu thêm.
- [ ] Chạy `scripts/03_split.py --audit` để đo mức rò rỉ của phép chia cũ.

### Giai đoạn 1 — Sửa quy trình đánh giá (1 tuần)

- [ ] Tiền xử lý: hiệu chỉnh theo thẻ → tách nền → cắt hộp bao. `scripts/02_preprocess.py`.
- [ ] Chia tập theo nhóm (`StratifiedGroupKFold` trên `fruit_id`). Không bao giờ chia theo ảnh nữa.
- [ ] Train lại với `yolo11s-cls`, `hsv_s: 0.2`, `hsv_v: 0.2`, `erasing: 0.1`, 3 hạt giống (0, 1, 2).
- [ ] Xây đường cơ sở thống kê màu L\*a\*b\*. `scripts/04_color_baseline.py`.
- [ ] Đánh giá đầy đủ: F1 theo lớp, ma trận nhầm lẫn, Kappa, chi phí bất đối xứng, hiệu chuẩn xác suất. `scripts/06_evaluate.py`.

**Dự kiến: độ chính xác sẽ tụt từ 99,5% xuống khoảng 70–85%. Đây là kết quả tốt, không phải kết quả xấu.** Con số 99,5% không dùng được, con số 78% có đối chứng thì dùng được.

### Giai đoạn 2 — Bù dữ liệu còn thiếu (2–3 tuần, chạy song song)

- [ ] **Ưu tiên cao nhất: bậc 4 và bậc 5.** Cần thêm ít nhất 30–40 quả mỗi bậc. Cách nhanh: mua quả bậc 3 rồi để chín ở nhiệt độ phòng 3–5 ngày, chụp mỗi ngày — vừa được bậc 4, 5 vừa đúng luôn phần theo dõi ở mục 3.4.7.
- [ ] **Thu thêm nguồn.** Tối thiểu 3 nguồn, lý tưởng 4–5. Đây là điều kiện cần để làm được đánh giá bỏ ra một nguồn.
- [ ] **Đo TSS.** Khúc xạ kế cầm tay ~300–600 k. Không có TSS thì Câu hỏi 3 và toàn bộ mục 4.5 không viết được. Ưu tiên hơn cả TA vì TA cần phòng thí nghiệm.
- [ ] **Gán nhãn độc lập bởi người thứ hai** trên ít nhất 300 ảnh để tính Kappa. Không có con số này thì mục 4.2 trống.
- [ ] **Ảnh ngoài trời**, nhiều khung giờ, nền tán cây. Đây là dữ liệu cho tầng ước lượng môi trường.

### Giai đoạn 3 — Mô-đun môi trường (1–2 tuần)

- [ ] Trích nguồn sáng từ thẻ trên toàn bộ ảnh ⇒ tạo nhãn. `scripts/07_illuminant.py --extract`.
- [ ] Chạy các đường cơ sở không học (Gray-World, Shades-of-Gray, Max-RGB), báo cáo sai số góc.
- [ ] Huấn luyện bộ ước lượng nguồn sáng bằng CNN, so với các đường cơ sở trên.
- [ ] Thí nghiệm chính: chạy toàn bộ quy trình ở **ba cấu hình** — (a) không hiệu chỉnh, (b) hiệu chỉnh bằng thẻ, (c) hiệu chỉnh bằng nguồn sáng ước lượng không thẻ. Chênh lệch giữa (a) và (b) là phần biến thiên do chiếu sáng; chênh lệch giữa (b) và (c) là cái giá phải trả khi bỏ thẻ đi ở điều kiện triển khai thực tế.

Riêng thí nghiệm ba cấu hình này đủ làm một mục kết quả độc lập và là chỗ đề tài khác biệt rõ nhất so với Tu và cs (2018).

### Giai đoạn 4 — Hoàn thiện báo cáo (1 tuần)

- [ ] Điền số vào 51 chỗ `[…]`. Xem bảng ánh xạ ở `scripts/README.md` — mỗi ô trống ứng với một file kết quả cụ thể do script sinh ra.
- [ ] Vẽ Hình 1 (sơ đồ quy trình), Hình 2 (demo tiền xử lý), Hình 3 (5 bậc chín), Hình 4 (biểu đồ hộp TSS), Hình 5 (ma trận nhầm lẫn).
- [ ] Bổ sung vào mục 4.7.1 hạn chế thứ bảy về giới hạn của thẻ xám so với bảng màu 24 ô.

---

## PHẦN 4 — BA VIỆC LÀM NGAY TRONG TUẦN NÀY

1. **Đếm số quả riêng biệt.** Con số này quyết định mọi thứ. Chạy `01_build_manifest.py`, nhìn cột `fruit_id`.
2. **Train lại một lần với phép chia theo quả**, giữ nguyên mọi thứ khác. Xem độ chính xác thật là bao nhiêu. Đây là con số bạn sẽ mang đi thi.
3. **Mua khúc xạ kế và đặt lịch thu mẫu ở nguồn thứ hai, thứ ba.** Hai việc này có thời gian chờ, khởi động sớm.

---

## Phụ chú — Về việc chấm giải

Ban giám khảo Eureka đọc rất nhiều bài báo cáo độ chính xác trên 95%. Một bài nói *"chúng tôi đạt 99,5% khi chia tập ngẫu nhiên, 76% khi chia theo quả, và 61% khi đánh giá trên nguồn quả chưa từng thấy — và đây là lý do"* sẽ nổi bật hơn hẳn. Báo cáo của bạn đã được viết sẵn theo hướng đó ngay từ đầu (mục 3.2 đã ghi rõ Giả thuyết 2 có thể bị bác bỏ và kết quả âm vẫn có giá trị). Hãy giữ đúng tinh thần đó, đừng đổi ngưỡng sau khi có số liệu.
