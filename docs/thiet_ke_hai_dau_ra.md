# Vì sao tách "hỏng" thành đầu ra riêng thay vì thêm bậc 6

## Vấn đề

Bộ dữ liệu có 56 quả được đánh dấu hỏng (dải chỉ số 155–210), nhiều hơn tổng số quả ở bậc 4 và bậc 5 cộng lại. Cách xử lý trực giác là thêm một lớp thứ sáu vào mô hình phân loại. Cách đó sai, vì ba lý do.

## Lý do 1 — Hai trục vuông góc, không cùng một trục

Độ chín là một trục **có thứ tự**: bậc 1 → 2 → 3 → 4 → 5 là một tiến trình sinh lý liên tục, và khoảng cách giữa hai bậc kề nhau có ý nghĩa.

Tình trạng quả là một trục **khác**. Một quả có thể đang ở bậc 3 và đồng thời bị nấm, dập vỏ, hoặc sâu đục. Hai thuộc tính này đồng thời tồn tại, không loại trừ nhau.

Nhét "hỏng" vào cuối thang độ chín ngầm khẳng định rằng hỏng là bậc tiếp theo sau chín hoàn toàn. Điều đó chỉ đúng với một loại hỏng (quả để quá lâu), sai với mọi loại còn lại.

## Lý do 2 — Phá vỡ các chỉ số có thứ tự

Hai chỉ số chính của báo cáo đều giả định nhãn có thứ tự:

- **Kappa có trọng số bậc** (mục 3.4.8) phạt lệch một bậc nhẹ hơn lệch ba bậc. Với lớp thứ sáu là "hỏng", khoảng cách từ bậc 2 tới hỏng bị tính là 4 bậc — con số vô nghĩa.
- **Sai số trung bình theo bậc** (Bảng 8) cũng vậy.

Cả hai chỉ số sẽ vẫn ra một con số, chỉ là con số đó không diễn giải được.

## Lý do 3 — Phá vỡ ma trận chi phí

Ma trận chi phí ở mục 3.6 chia mọi sai sót thành hai loại: hái sớm và hái muộn. Báo "hỏng" khi thật ra là bậc 2 không thuộc loại nào. Không đặt được vào ma trận, nên chi phí kỳ vọng ở Bảng 10 mất cơ sở.

---

## Thiết kế thay thế

```
ảnh  ─┬─►  Đầu A: độ chín      → bậc 1..5     (có thứ tự, dùng ma trận chi phí)
      └─►  Đầu B: tình trạng   → dùng được / hỏng   (nhị phân, độc lập)

quy tắc quyết định:
    nếu Đầu B = hỏng  →  loại khỏi lô, KHÔNG xét bậc chín
```

Đầu A huấn luyện chỉ trên quả dùng được. Đầu B huấn luyện trên toàn bộ.

## Lợi ích kèm theo

**Cỡ mẫu tốt hơn.** Đầu B có 56 dương / 154 âm — cân bằng hơn hẳn phần độ chín, nơi bậc 5 chỉ có 5 quả.

**Bịt lỗ hổng nguy hiểm nhất của mô hình 5 lớp.** Softmax buộc phải chọn một trong năm bậc cho bất cứ thứ gì đưa vào. Đưa quả thối vào, mô hình trả về bậc 5 với độ tin cậy 0,99 — tức nói với người dùng "chín hoàn toàn, hái được". Đây là kiểu lỗi tệ nhất trong ứng dụng thật: sai một cách tự tin, theo hướng gây thiệt hại.

**Đóng góp báo cáo được.** Không công trình nào trong phần tổng quan (mục 2.5) tách hai trục này. Đây là một điểm khác biệt nêu được ở mục 2.7.2.

---

## Cần sửa gì trong báo cáo

| Mục | Sửa |
|---|---|
| Bảng 3 | Thêm ghi chú: sơ đồ nhãn này áp dụng cho quả dùng được; tình trạng quả là trục riêng |
| Mục 3.5 | Mô tả đầu ra thứ hai và quy tắc quyết định |
| Mục 3.7 / Bảng 4 | Thêm dòng chỉ số cho đầu B: độ nhạy, độ chính xác dương tính, AUC-PR |
| Bảng 8 | Tách thành 8a (độ chín) và 8b (tình trạng) |
| Mục 4.6 | Nói rõ ma trận chi phí chỉ áp cho đầu A |
| Mục 2.7.2 | Thêm đóng góp thứ bảy |

---

## Mở rộng: cơ chế từ chối trả lời

Vẫn còn một trường hợp cả hai đầu đều không xử lý: ảnh không phải chanh dây, ảnh quá mờ, hoặc ánh sáng quá lạ so với dữ liệu huấn luyện.

Cách rẻ nhất là đặt ngưỡng trên độ tin cậy đã hiệu chuẩn. `chanhday/metrics.py` có sẵn `calibration_table()` và `rejection_curve()` cho việc này.

Ngưỡng chọn theo đánh đổi: công cụ nói "không xác định được" ở 10% số ca khó mà đạt 90% trên 90% còn lại thì dùng được hơn hẳn công cụ đoán bừa mọi ca để đạt 78%. `outputs/*/rejection_curve.csv` cho toàn bộ đường đánh đổi này để chọn điểm vận hành.
