# Tầng ước lượng môi trường chiếu sáng

## Bài toán

Cùng một quả chanh dây, chụp lúc 8 giờ sáng trời trong và lúc 16 giờ trời râm, cho ra hai giá trị màu khác nhau. Mô hình học trên bộ ảnh chụp ở một điều kiện sẽ sai khi gặp điều kiện khác. Đây là một phần nguyên nhân của hiện tượng sụt giảm hiệu năng giữa các nguồn mà Câu hỏi 2 nhắm tới.

Trong thị giác máy tính, đây là bài toán **color constancy**: tách phần màu do vật thể khỏi phần màu do nguồn sáng.

## Điểm mấu chốt

Bốn ô xám trên thẻ chuẩn có phản xạ trung tính. Mọi lệch màu giữa ba kênh đo được trên chúng đều do nguồn sáng gây ra. Nói cách khác:

> **Thẻ cho ta nhãn đúng của nguồn sáng, miễn phí, ở từng ảnh một.**

Từ đó suy ra thiết kế: dùng nhãn này huấn luyện một mô-đun ước lượng nguồn sáng **từ cảnh, không cần thẻ**. Khi triển khai thật, nông hộ chụp ảnh không có thẻ, mô-đun tự suy ra nguồn sáng và tự hiệu chỉnh.

Đây là kỹ thuật chưng cất (distillation), và nó biến một chi tiết thủ tục của giao thức chụp thành một đóng góp khoa học riêng.

## Kiến trúc

```
Ảnh thô từ thiết bị
   │
   ├─ Tầng A: ƯỚC LƯỢNG NGUỒN SÁNG
   │    vào:  ảnh (đã che vùng thẻ) + tùy chọn EXIF
   │    ra:   vector nguồn sáng (r, g, b) chuẩn hóa
   │    học:  nhãn lấy từ 4 ô xám
   │
   ├─ Tầng B: HIỆU CHỈNH von Kries + TÁCH NỀN + CẮT
   │    ra:   ảnh quả đã đưa về nguồn sáng trung tính
   │
   └─ Tầng C: PHÂN LOẠI ĐỘ CHÍN + TÌNH TRẠNG
```

## Số đo được trên bộ ảnh hiện có

Bộ ảnh Canon EOS 200D II ngày 14/8/2026:

| Đại lượng | Giá trị |
|---|---|
| Ám màu trước hiệu chỉnh | **5,28°** so với trung tính |
| Ám màu sau hiệu chỉnh bằng 4 ô | **0,07°** |
| Tỷ số R/G của nguồn sáng | ≈ 1,13 |
| Độ phân tán chiếu sáng trong một buổi | dưới 0,1° |

Con số 5,28° quan trọng vì kênh đỏ bị đội lên khoảng 13%, mà kênh đỏ chính là a\* — đại lượng dùng để đo tỷ lệ vỏ chuyển màu. **Ảnh thô đang làm quả trông chín hơn thực tế một cách hệ thống.**

Con số dưới 0,1° cũng quan trọng, theo hướng ngược lại: trong một buổi chụp, chiếu sáng gần như không đổi. Nếu có 6 buổi thì bộ dữ liệu chiếu sáng thực chất chỉ có **6 điểm**, không phải 940. Chưa đủ để huấn luyện tầng A.

## Việc cần làm để tầng A có ý nghĩa

Chụp cùng một mẻ quả (khoảng 15–20 quả, phủ đủ 5 bậc) ở nhiều điều kiện sáng:

- 3–4 khung giờ trong ngày: sáng sớm, giữa trưa, chiều, hoàng hôn
- Cả trời trong lẫn trời râm
- Trong nhà dưới đèn huỳnh quang và đèn LED
- Ngoài trời dưới bóng cây (ánh sáng lọc qua lá có ám xanh rất mạnh)

Mục tiêu: độ phân tán chiếu sáng vượt **8°**. Script 07 chế độ `extract` sẽ tự báo con số này.

Ước tính khối lượng: 20 quả × 8 điều kiện × 2 ảnh = 320 ảnh. Làm gọn trong hai ngày.

## Các phương pháp cần so sánh

Script 07 chế độ `baseline` chạy sẵn bốn phương pháp không học:

| Phương pháp | Giả định |
|---|---|
| Gray-World (p=1) | trung bình toàn ảnh là màu trung tính |
| Shades-of-Gray (p=6) | trung bình Minkowski bậc 6 là trung tính |
| Max-RGB | pixel sáng nhất mỗi kênh phản ánh nguồn sáng |
| Gray-Edge | trung bình đạo hàm ảnh là trung tính |

Chế độ `train` huấn luyện ResNet-18 hồi quy vector nguồn sáng, dùng hàm mất mát là sai số góc.

**Nếu CNN không thắng được Shades-of-Gray, hãy dùng Shades-of-Gray và báo cáo trung thực.** Một đường cơ sở không học thắng mô hình học sâu cũng là kết quả có giá trị, và với cỡ dữ liệu hiện tại thì khả năng đó không nhỏ.

## Tăng cường dữ liệu đúng vật lý

Cấu hình cũ dùng `hsv_s: 0.7` — xáo trộn độ bão hòa ±70% mà **không đổi nhãn**. Trong bài toán mà màu là tín hiệu duy nhất, đó là dạy mô hình bỏ qua đúng thứ cần nhìn.

Thay bằng: nhân ảnh với một nguồn sáng ngẫu nhiên, rồi **cập nhật nhãn nguồn sáng tương ứng**.

```python
g = np.exp(np.random.uniform(-0.3, 0.3, 3))   # nguồn sáng ngẫu nhiên
rgb = np.clip(rgb * g, 0, 1)
y = y * g                                      # nhãn đi theo
```

Cách này mô phỏng đúng cái xảy ra ngoài đời khi đổi nguồn sáng, nên mô hình học được quy luật thật thay vì học cách phớt lờ màu. Đã cài trong `scripts/07_illuminant.py`.

## Thí nghiệm chính cho mục 4.4

Chạy toàn bộ quy trình phân loại độ chín ở **ba cấu hình**:

| Cấu hình | Mô tả |
|---|---|
| (a) | không hiệu chỉnh màu |
| (b) | hiệu chỉnh bằng thẻ trong khung hình |
| (c) | hiệu chỉnh bằng nguồn sáng ước lượng, không thẻ |

Diễn giải:

- **(a) so với (b)** = phần biến thiên giữa các nguồn có nguyên nhân từ chiếu sáng. Phần này xử lý được bằng một biện pháp chi phí thấp ở khâu thu ảnh.
- **(b) so với (c)** = cái giá phải trả khi bỏ thẻ đi, tức chênh lệch giữa điều kiện nghiên cứu và điều kiện triển khai thật.
- Phần còn lại sau khi trừ cả hai = khác biệt do giống và điều kiện canh tác, không xử lý được bằng chuẩn hóa màu mà phải thu thêm dữ liệu.

Ba con số này là chỗ đề tài khác biệt rõ nhất so với Tu và cs (2018).

## Rủi ro phải nêu trong hạn chế

1. **Thẻ hiện tại là thẻ xám bậc thang, không phải bảng ColorChecker 24 ô.** Thẻ xám chỉ cho hiệu chỉnh cân bằng trắng (3 hệ số kênh). Hiệu chỉnh màu đầy đủ cần ma trận 3×3 và bước tuyến tính hóa gamma, đòi hỏi bảng có ô màu. Berry và cs (2018) — nguồn được trích ở mục 2.3 — dùng bảng 24 ô. Nên mua một bảng chuẩn trước đợt thu mẫu tiếp theo.

2. **Ảnh JPEG đã qua xử lý của máy.** Máy đã tự cân bằng trắng và ánh xạ tông trước khi ghi file. Nguồn sáng suy ra từ JPEG là "nguồn sáng còn sót lại sau xử lý", không phải nguồn sáng vật lý. Dùng file RAW (`--use-raw` ở script 02) khắc phục được. `chanhday.cards.linearity_check()` báo mức phi tuyến để biết vấn đề nghiêm trọng tới đâu.

3. **Ảnh hiện tại chụp trong nhà trên nền vải đen.** Muốn nói chuyện "môi trường xung quanh" thì phải có ảnh ngoài trời với nền tán cây. Không có đường tắt cho việc này.
