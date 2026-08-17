---
title: ""
lang: vi
---

**THÀNH ĐOÀN TP. HỒ CHÍ MINH — ĐẠI HỌC QUỐC GIA TP. HỒ CHÍ MINH — SỞ KHOA HỌC VÀ CÔNG NGHỆ TP. HỒ CHÍ MINH**

---

**CÔNG TRÌNH DỰ THI**

**GIẢI THƯỞNG SINH VIÊN NGHIÊN CỨU KHOA HỌC EURÉKA**

**LẦN THỨ 28 NĂM 2026**

**TÊN CÔNG TRÌNH: XÁC ĐỊNH ĐỘ CHÍN VÀ TÌNH TRẠNG QUẢ CHANH DÂY (*PASSIFLORA EDULIS* SIMS) TỪ ẢNH SỐ CÓ CHUẨN HÓA MÀU THEO THẺ CHUẨN, ỨNG DỤNG THỊ GIÁC MÁY TÍNH**

LĨNH VỰC NGHIÊN CỨU: Khoa học Nông nghiệp

CHUYÊN NGÀNH: Khoa học Nông nghiệp khác

Mã số công trình: ……………………………

*(Phần này do BTC Giải thưởng ghi)*

# MỤC LỤC

*Chuột phải vào bảng mục lục và chọn Update Field để cập nhật số trang sau khi hoàn thiện nội dung; sau đó xóa dòng ghi chú này.*

# DANH MỤC BẢNG BIỂU

Bảng 1. So sánh phạm vi nghiên cứu với hướng nghiên cứu đi trước

Bảng 2. Đặc điểm các nguồn thu mẫu

Bảng 3. Sơ đồ nhãn giai đoạn chín

Bảng 4. Sơ đồ nhãn tình trạng quả

Bảng 5. Các chỉ số đánh giá theo từng nhiệm vụ

Bảng 6. Thống kê mô tả bộ dữ liệu sau làm sạch

Bảng 7. Phân bố số quả theo bậc chín và theo nguồn

Bảng 8. Chỉ tiêu hóa sinh theo bậc chín

Bảng 9a. Kết quả phân loại độ chín trong đánh giá cùng nguồn

Bảng 9b. Kết quả phân loại tình trạng quả

Bảng 10. Kết quả đánh giá bỏ ra một nguồn và vai trò của chuẩn hóa màu

Bảng 11. Sai số của các phương pháp ước lượng nguồn sáng

Bảng 12. Ma trận chi phí bất đối xứng và chi phí kỳ vọng của từng phương pháp

Hình 1. Sơ đồ quy trình nghiên cứu tổng thể

Hình 2. Kết quả tiền xử lý ảnh: ảnh gốc, mặt nạ vùng quả và ảnh cắt theo hộp bao

Hình 3. Ảnh minh họa năm bậc chín theo sơ đồ nhãn

Hình 4. Kiến trúc ba tầng của quy trình đề xuất

Hình 5. Hàm lượng chất rắn hòa tan tổng số theo bậc chín

Hình 6. Ma trận nhầm lẫn của mô hình tốt nhất trong đánh giá bỏ ra một nguồn

Hình 7. Đường đánh đổi giữa tỷ lệ từ chối trả lời và độ chính xác

# DANH MỤC NHỮNG TỪ VIẾT TẮT

| **Từ viết tắt** | **Nghĩa đầy đủ** |
| --- | --- |
| AUC-PR | Diện tích dưới đường cong độ chính xác dương tính và độ nhạy |
| CIE L\*a\*b\* | Không gian màu chuẩn của Ủy ban Quốc tế về Chiếu sáng, tách bạch độ sáng và sắc độ |
| CNN | Mạng nơ-ron tích chập (Convolutional Neural Network) |
| DSIFT-LLC | Đặc trưng SIFT dày kết hợp mã hóa tuyến tính ràng buộc cục bộ |
| ECE | Sai số hiệu chuẩn kỳ vọng (Expected Calibration Error) |
| F1 | Trung bình điều hòa của độ chính xác dương tính và độ nhạy |
| GACC | Tổng cục Hải quan Trung Quốc |
| RMSE | Căn bậc hai của sai số bình phương trung bình |
| TA | Độ chua chuẩn độ (Titratable Acidity) |
| TSS | Hàm lượng chất rắn hòa tan tổng số, đo bằng độ Brix (Total Soluble Solids) |
| TSS/TA | Tỷ số giữa hàm lượng chất rắn hòa tan tổng số và độ chua chuẩn độ |

# TÓM TẮT CÔNG TRÌNH

Chanh dây (*Passiflora edulis* Sims) là quả hô hấp đột biến, sau khi rời cây tiếp tục phân giải chlorophyll và tích lũy sắc tố nhưng hầu như không tích lũy thêm đường, đồng thời mất nước nhanh qua vỏ dẫn tới hiện tượng nhăn vỏ. Đặc điểm sinh lý này làm cho thời điểm thu hái trở thành một quyết định không đảo ngược được: hái trước độ chín thu hoạch thì hàm lượng chất rắn hòa tan không tăng thêm trong bảo quản, hái sau thời điểm đó thì quả hao hụt khối lượng và mất giá trị thương phẩm khi tới nơi tiêu thụ. Trong sản xuất, quyết định này được đưa ra bằng cách quan sát tỷ lệ diện tích vỏ đã chuyển màu, một thao tác phụ thuộc kinh nghiệm cá nhân, không lặp lại được giữa những người khác nhau và không chuyển giao được sang vùng trồng mới.

Nghiên cứu được thực hiện nhằm xây dựng và kiểm chứng quy trình xác định đồng thời giai đoạn chín và tình trạng sử dụng của quả chanh dây từ ảnh số, gồm ba giai đoạn. Giai đoạn một xây dựng bộ dữ liệu ảnh có gán nhãn theo hai trục độc lập: năm bậc chín và hai mức tình trạng, thu trên quả có xuất xứ khác nhau, mỗi ảnh có thẻ chuẩn gồm bốn ô xám và mã định danh quả trong khung hình. Ảnh được hiệu chỉnh màu theo thẻ, tách nền, tạo mặt nạ vùng quả và cắt theo hộp bao trước khi đưa vào mô hình. Song song, hàm lượng chất rắn hòa tan tổng số, độ chua chuẩn độ, tỷ số giữa hai chỉ tiêu này, khối lượng quả và tỷ lệ vỏ chuyển màu được xác định trên chính quả đã chụp, làm chuẩn tham chiếu cho các bậc nhãn.

Giai đoạn hai so sánh ba nhóm phương pháp phân loại gồm đường cơ sở dựa trên thống kê màu trong không gian CIE L\*a\*b\*, các mô hình học sâu tinh chỉnh từ trọng số huấn luyện trước, và kết quả phân loại của người thu hái có kinh nghiệm trên cùng bộ ảnh. Giai đoạn ba đánh giá khả năng tổng quát bằng thiết kế bỏ ra một nguồn, đồng thời chạy ba cấu hình chuẩn hóa màu nhằm tách phần biến thiên do điều kiện chiếu sáng khỏi phần biến thiên do khác biệt giống và điều kiện canh tác, và định lượng cái giá phải trả khi bỏ thẻ chuẩn ra khỏi khung hình ở điều kiện triển khai thực tế.

Bộ dữ liệu cuối cùng gồm […] ảnh trên […] quả thu từ […] nguồn. Kết quả cho thấy […]. Nghiên cứu tạo ra bộ dữ liệu ảnh độ chín chanh dây đa nguồn có gán nhãn kèm chỉ tiêu hóa sinh đối chứng, xác định mức sụt giảm hiệu năng khi chuyển sang nguồn quả mới, đề xuất mô-đun ước lượng nguồn sáng học từ thẻ chuẩn và dùng được khi không có thẻ, và đề xuất khung đánh giá theo chi phí bất đối xứng giữa hái sớm và hái muộn.

**Từ khóa:** chanh dây, độ chín thu hoạch, chất rắn hòa tan tổng số, thị giác máy tính, chuẩn hóa màu, khả năng tổng quát giữa các nguồn.

# 1. ĐẶT VẤN ĐỀ

## 1.1. Sự cần thiết của đề tài

Chanh dây (*Passiflora edulis* Sims) thuộc chi *Passiflora*, họ Lạc tiên (*Passifloraceae*), là cây thân leo cho thu hoạch sau bốn đến năm tháng trồng và cho trái quanh năm. Diện tích canh tác trong nước mở rộng nhanh trong mười năm gần đây. Năm 2024, cả nước có hơn 12.600 ha với sản lượng gần 180.000 tấn, trong đó Tây Nguyên chiếm 86,4% diện tích và 92,5% sản lượng (Cục Trồng trọt và Bảo vệ thực vật, 2025). Ngày 15 tháng 4 năm 2025, Nghị định thư về yêu cầu kiểm dịch thực vật đối với quả chanh leo tươi xuất khẩu sang Trung Quốc được ký kết, đặt ra yêu cầu về mã số vùng trồng, cơ sở đóng gói và truy xuất nguồn gốc đối với sản phẩm quả tươi (Bộ Nông nghiệp và Môi trường và Tổng cục Hải quan Trung Quốc, 2025).

Chanh dây là quả hô hấp đột biến. Sau khi tách khỏi cây, quả xuất hiện đỉnh hô hấp và đỉnh sinh ethylene, tiếp tục phân giải chlorophyll ở vỏ và tích lũy anthocyanin cùng carotenoid, đồng thời thành tế bào bị phân giải làm quả mềm dần (Li và cs, 2020). Tuy nhiên, hàm lượng đường tổng số trong thịt quả gần như không tăng thêm sau thu hoạch, vì đường được tích lũy từ sản phẩm quang hợp của cây mẹ. Song song với các biến đổi trên, quả thoát hơi nước mạnh qua vỏ, biểu hiện bằng hao hụt khối lượng và hiện tượng nhăn vỏ, làm giảm giá trị thương phẩm của lô hàng (Li và cs, 2020).

Từ hai đặc điểm sinh lý trên, thời điểm thu hái đối với quả tươi xuất khẩu bị giới hạn trong một cửa sổ hẹp. Quả hái trước khi đạt độ chín thu hoạch có hàm lượng chất rắn hòa tan thấp và không cải thiện được trong quá trình bảo quản. Quả hái muộn tuy đạt chất lượng ăn được nhưng hao hụt khối lượng nhanh và nhăn vỏ trong thời gian vận chuyển. Arjona và Matta (1991) đã xác nhận trên cùng đối tượng rằng thời điểm hái là yếu tố chi phối chất lượng sau thu hoạch, còn Shiomi và cs (1996) cho thấy quả tách khỏi giàn ở các thời điểm khác nhau đi vào giai đoạn hô hấp đột biến với tốc độ khác nhau.

Trong sản xuất, độ chín được xác định bằng cách quan sát tỷ lệ diện tích vỏ đã chuyển màu. Cách làm này bộc lộ ba hạn chế. Kết quả không lặp lại được, vì hai người quan sát cùng một quả có thể đưa ra hai kết luận khác nhau, và cùng một người ở hai điều kiện chiếu sáng khác nhau cũng vậy. Kết quả không chuyển giao được, vì kinh nghiệm gắn với một giống, một vùng trồng và một thói quen quan sát cụ thể. Ngoài ra, cách làm này không cho phép ước lượng trước sản lượng đạt chuẩn của từng lứa thu hoạch, thông tin mà doanh nghiệp thu mua cần trước khi bố trí phương tiện và nhân công.

Thị giác máy tính là hướng tiếp cận có thể khắc phục các hạn chế trên. Mohanty và cs (2016) đã chứng minh khả năng chẩn đoán trên cây trồng bằng ảnh chụp từ thiết bị phổ thông, còn Tu và cs (2018) phân loại được năm giai đoạn chín của chanh dây từ ảnh chụp ngoài trời với độ chính xác 91,52%. Tuy nhiên, để một quy trình đọc ảnh chuyển được từ phòng thí nghiệm ra đồng ruộng, hai vấn đề còn phải giải quyết: kiểm soát ảnh hưởng của điều kiện chiếu sáng lên phép đo màu, và bảo đảm công cụ không đưa ra kết luận sai khi gặp quả không còn sử dụng được.

Nghiên cứu thuộc nhóm sản phẩm nghiên cứu, phát triển và ứng dụng theo định hướng của Nghị quyết số 57-NQ/TW về đột phá phát triển khoa học, công nghệ, đổi mới sáng tạo và chuyển đổi số quốc gia.

## 1.2. Lý do chọn đề tài

Đề tài được chọn nhằm chuyển việc đánh giá độ chín từ một phán đoán cảm quan sang một chỉ số đo được, lặp lại được và có đối chứng bằng chỉ tiêu hóa sinh. Bốn căn cứ dẫn tới lựa chọn này.

Về mặt kinh tế, chênh lệch giữa lô hàng đạt chuẩn xuất khẩu và lô hàng bị loại do nhăn vỏ là chênh lệch giá bán, nên mọi cải thiện về độ chính xác của quyết định thu hoạch đều quy đổi được thành giá trị cụ thể. Đối tượng hưởng lợi gồm nông hộ, doanh nghiệp thu mua và cơ quan quản lý chất lượng nông sản, và không bên nào phải thay đổi hạ tầng sản xuất để tiếp nhận kết quả.

Về mặt vật liệu nghiên cứu, chanh dây trong nước cho thu hoạch nhiều lứa trong năm và được tập kết về vựa cùng chợ đầu mối gần như quanh năm. Tại cùng một thời điểm luôn có sẵn quả từ nhiều vùng trồng và ở nhiều giai đoạn chín khác nhau, nên nhóm thu đủ các bậc chín trong vài đợt lấy mẫu ngắn thay vì phải theo dõi một vườn qua nhiều tuần. Chiến lược lấy mẫu này được trình bày ở mục 3.4.1.

Về mặt chuyên môn, bài toán nằm ở giao điểm giữa sinh lý sau thu hoạch và xử lý ảnh, và không giải quyết trọn vẹn được nếu chỉ tiếp cận từ một phía. Mô hình xây dựng trên nhãn thị giác đơn thuần sẽ tái tạo cả sai số quan sát của người gán nhãn, trong khi các chỉ tiêu hóa sinh nếu không gắn với phương tiện đo nhanh thì không đưa được ra đồng ruộng. Việc đối chiếu song song hai nguồn thông tin này là nội dung trọng tâm của đề tài.

Về mặt phương pháp, việc đặt thẻ chuẩn có ô xám trong mọi khung hình mở ra một khả năng mà các nghiên cứu đi trước chưa khai thác: thẻ cung cấp giá trị tham chiếu của nguồn sáng ở từng ảnh, và giá trị đó dùng được làm nhãn giám sát để huấn luyện một mô-đun ước lượng nguồn sáng từ chính cảnh chụp, không cần thẻ. Nội dung này được trình bày ở mục 3.5.4.

# 2. TỔNG QUAN TÀI LIỆU

## 2.1. Đối tượng nghiên cứu và giá trị thương mại

Chanh dây, tên gọi khác là chanh leo hoặc mắc mát, có tên khoa học *Passiflora edulis* Sims, thuộc chi *Passiflora*, họ *Passifloraceae*. Hai dạng được canh tác thương mại phổ biến là dạng quả tía (*Passiflora edulis* f. *edulis*) và dạng quả vàng (*Passiflora edulis* f. *flavicarpa* Degener). Quả thuộc loại quả mọng, vỏ dày, bên trong chứa nhiều hạt bao bởi lớp áo hạt mọng nước. Ở dạng quả tía, vỏ chuyển từ xanh sang tía trong quá trình chín; ở dạng quả vàng, vỏ chuyển từ xanh sang vàng. Do hai dạng có tiến trình chuyển màu khác nhau, dạng quả của từng mẫu được ghi nhận riêng và báo cáo ở Bảng 2.

Quả chanh dây được tiêu thụ theo hai kênh có yêu cầu chất lượng khác nhau. Kênh nguyên liệu chế biến dịch quả cô đặc chỉ quan tâm tới hàm lượng chất khô và độ chua, hình thức bên ngoài hầu như không được tính. Kênh quả tươi xuất khẩu đòi hỏi đồng thời chất lượng ăn được và vỏ quả còn nguyên vẹn, và có mức giá cao hơn đáng kể. Tính đến tháng 10 năm 2025, kim ngạch xuất khẩu chanh leo đạt hơn 202 triệu USD, đưa Việt Nam vào nhóm mười quốc gia cung cấp lớn nhất thế giới (Cục Trồng trọt và Bảo vệ thực vật, 2025). Chênh lệch giá trị giữa hai kênh tiêu thụ là lý do khiến việc xác định đúng thời điểm hái có ý nghĩa kinh tế trực tiếp, vì cùng một quả có thể rơi vào kênh này hoặc kênh kia chỉ do lệch vài ngày thu hái.

## 2.2. Cơ sở sinh lý của quá trình chín ở chanh dây

### 2.2.1. Tiến trình phát triển quả và đặc điểm hô hấp đột biến

Quá trình phát triển của quả chanh dây tuân theo đường cong sinh trưởng dạng sigmoid đơn. Kích thước quả đạt cực đại vào khoảng 20 đến 21 ngày sau nở hoa, sau đó khối lượng tiếp tục tăng chậm do tích lũy chất khô ở phần thịt quả và hạt (Shiomi và cs, 1996).

Chanh dây được xếp vào nhóm quả hô hấp đột biến. Ở quả tách khỏi giàn, cường độ hô hấp tăng lên đỉnh rồi giảm, kèm theo đỉnh sinh ethylene; ở quả để nguyên trên giàn, đỉnh hô hấp không biểu hiện rõ (Shiomi và cs, 1996). Sự khác biệt này có ý nghĩa trực tiếp với đề tài, vì quả chín trên cây và quả chín sau khi hái không đi theo cùng một tiến trình, do đó dữ liệu thu trên hai nhóm không được trộn lẫn khi phân tích.

Trong giai đoạn sau thu hoạch, cường độ hô hấp, độ dẫn điện tương đối của dịch bào và tỷ lệ hao hụt khối lượng của quả đều tăng theo thời gian bảo quản. Hoạt độ của các enzyme phân giải thành tế bào gồm β-galactosidase, polygalacturonase và cellulase tăng lên, làm quả mềm và vỏ nhăn (Li và cs, 2020). Hao hụt nước qua vỏ là nguyên nhân chính gây giảm giá trị thương phẩm trong vận chuyển đường dài.

### 2.2.2. Biến đổi sắc tố và sự chuyển màu vỏ quả

Màu vỏ quả là biểu hiện bên ngoài của một chuỗi biến đổi sinh hóa có thể theo dõi được. Trong quá trình chín, chlorophyll ở vỏ bị phân giải làm nền xanh nhạt dần, đồng thời anthocyanin và carotenoid được tích lũy làm vỏ chuyển sang tía hoặc vàng tùy dạng quả.

Phân tích phiên mã trên quả chanh dây tía cho thấy các nhóm gene thuộc con đường sinh tổng hợp flavonoid, anthocyanin và carotenoid được tăng cường biểu hiện rõ rệt ở giai đoạn 6 và 8 tuần sau nở hoa so với giai đoạn 4 tuần, trong đó có các gene mã hóa chalcone synthase, dihydroflavonol reductase, anthocyanidin reductase và phytoene synthase (Li và cs, 2020). Sự chuyển màu vỏ vì vậy không phải một quy ước thị giác thuần túy mà phản ánh một chương trình biến đổi trao đổi chất diễn ra đồng thời với quá trình tích lũy đường và phân giải thành tế bào.

Tuy nhiên, quan hệ giữa màu vỏ và chất lượng thịt quả là quan hệ tương quan chứ không phải quan hệ nhân quả trực tiếp, và mức độ chặt chẽ của tương quan này thay đổi theo giống cùng điều kiện canh tác. Đây là lý do các bậc nhãn thị giác trong nghiên cứu cần được đối chứng bằng chỉ tiêu hóa sinh đo trên chính quả đã chụp.

### 2.2.3. Các chỉ tiêu hóa sinh xác định độ chín

Các chỉ tiêu thường dùng để xác định độ chín của quả gồm màu sắc vỏ, hàm lượng chất rắn hòa tan tổng số (TSS) đo bằng độ Brix, độ chua chuẩn độ (TA) và tỷ số TSS/TA.

Ở chanh dây, trong quá trình chín, pH và TSS tăng còn TA giảm, do đó tỷ số TSS/TA tăng đơn điệu theo bậc chín (Pongener và cs, 2014). TSS tăng chủ yếu do thủy phân tinh bột dự trữ thành đường hòa tan, còn TA giảm do các axit hữu cơ được sử dụng làm cơ chất cho hô hấp. Tỷ số TSS/TA phản ánh cảm nhận vị tốt hơn từng chỉ tiêu riêng lẻ, vì vị ngọt cảm nhận được phụ thuộc đồng thời vào hàm lượng đường và hàm lượng axit.

Trong nghiên cứu này, TSS được chọn làm chỉ tiêu tham chiếu chính vì khúc xạ kế cầm tay có chi phí thấp, đo được ngay tại điểm thu mẫu và cho kết quả trong khoảng ba mươi giây mỗi quả. TA và tỷ số TSS/TA là chỉ tiêu bổ sung, phụ thuộc điều kiện phòng thí nghiệm.

## 2.3. Đo màu vỏ quả bằng ảnh và vấn đề chuẩn hóa điều kiện chiếu sáng

Việc lượng hóa tính trạng quả bằng ảnh thuộc dòng nghiên cứu kiểu hình học thực vật thông lượng cao, với luận điểm trung tâm là nút thắt của công tác chọn giống và quản lý sản xuất đã dịch chuyển từ khả năng đọc kiểu gen sang khả năng đo kiểu hình nhanh và rẻ (Furbank và Tester, 2011). Tardieu và cs (2017) mô tả con đường từ tín hiệu cảm biến tới tri thức nông học, còn Li, Zhang và Huang (2014) tổng quan các kỹ thuật ảnh dùng trong kiểu hình học thực vật.

Khi đo màu bằng ảnh, không gian màu RGB thô có hạn chế là cả ba kênh đều thay đổi khi cường độ chiếu sáng thay đổi. Không gian CIE L\*a\*b\* tách riêng thành phần độ sáng L\* khỏi hai thành phần sắc độ a\* và b\*, nên cho phép so sánh sắc độ giữa các ảnh chụp ở điều kiện sáng khác nhau. Trong đó a\* dương tương ứng sắc đỏ, a\* âm tương ứng sắc xanh lục, b\* dương tương ứng sắc vàng, phù hợp để mô tả tiến trình chuyển màu của vỏ chanh dây.

Ngay cả khi dùng không gian màu phù hợp, sai lệch do nguồn sáng vẫn tồn tại. Berry và cs (2018) cho thấy giá trị pixel trong một bộ ảnh kiểu hình biến động theo cường độ đèn, và việc hiệu chỉnh màu theo một bảng màu tham chiếu đặt trong khung hình làm giảm đáng kể sai lệch này, qua đó cải thiện độ chính xác của các phép đo tính trạng sau đó. Đây là cơ sở cho việc đặt thẻ chuẩn trong mọi khung hình của nghiên cứu, trình bày ở mục 3.4.2.

Trong thị giác máy tính, việc tách phần màu do vật thể khỏi phần màu do nguồn sáng được gọi là bài toán bất biến màu. Các phương pháp không cần dữ liệu huấn luyện gồm Gray-World, giả định trung bình toàn ảnh là màu trung tính; Shades-of-Gray, dùng trung bình Minkowski bậc cao; Max-RGB, lấy giá trị lớn nhất mỗi kênh; và Gray-Edge, giả định trung bình đạo hàm ảnh là trung tính. Thước đo chuẩn của dòng nghiên cứu này là sai số góc giữa vector nguồn sáng ước lượng và vector nguồn sáng thật. Điểm mà đề tài khai thác là thẻ chuẩn trong khung hình cung cấp sẵn vector nguồn sáng thật cho từng ảnh, tức cung cấp sẵn nhãn giám sát cho bài toán này mà không phát sinh thêm chi phí thu thập.

## 2.4. Ứng dụng thị giác máy tính trong sàng lọc và phân loại trái sau thu hoạch

Trong khâu sau thu hoạch, thị giác máy tính được ứng dụng theo hai hướng có yêu cầu kỹ thuật khác nhau.

Hướng thứ nhất là sàng lọc và phân loại tại cơ sở đóng gói. Quả đi qua băng chuyền dưới ánh sáng nhân tạo ổn định, nền đồng nhất và góc chụp cố định, nên bài toán gần với bài toán phân loại ảnh trong điều kiện kiểm soát và đã đạt độ chính xác rất cao. Hướng thứ hai là hỗ trợ quyết định thu hoạch tại vườn, nơi ảnh được chụp bằng thiết bị phổ thông dưới ánh sáng tự nhiên thay đổi theo giờ và theo thời tiết, nền là tán cây và nhiều quả cùng xuất hiện trong một khung hình.

Khác biệt giữa hai hướng không nằm ở mức độ khó mà ở phân bố dữ liệu. Mohanty và cs (2016) minh họa rõ điều này khi báo cáo mô hình đạt độ chính xác 99,35% trên tập kiểm tra chia ngẫu nhiên từ chính bộ ảnh chụp trong điều kiện kiểm soát, nhưng chỉ còn 31,4% khi đánh giá trên ảnh chụp ở điều kiện khác. Đề tài đặt mục tiêu ở hướng thứ hai, và các lựa chọn về giao thức chụp, chuẩn hóa màu cùng phương án đánh giá đều xuất phát từ con số này.

## 2.5. Các nghiên cứu ngoài nước

Phân loại độ chín quả bằng thị giác máy tính là hướng đã trưởng thành, với nhiều công bố trên cà chua, chuối, xoài, dâu tây và cam quýt. Hai kết luận đã ổn định trong dòng nghiên cứu này. Thứ nhất, đặc trưng màu biểu diễn trong không gian tách bạch độ sáng và sắc độ cho kết quả tốt hơn không gian RGB thô. Thứ hai, các mạng tích chập tinh chỉnh từ trọng số huấn luyện trước trên tập ảnh quy mô lớn như ImageNet (Deng và cs, 2009) đạt độ chính xác trên chín mươi phần trăm trên tập kiểm tra cùng nguồn dữ liệu (He và cs, 2016; Tan và Le, 2019). Nghiên cứu kế thừa cả hai kết luận và không đặt vấn đề về tính mới ở tầng này.

Trên đối tượng chanh dây, Tu và cs (2018) là công trình gần với đề tài nhất. Nhóm tác giả dùng cảm biến Kinect thu ảnh màu kèm thông tin độ sâu ngoài trời, phát hiện quả bằng Faster R-CNN, sau đó phân loại năm giai đoạn chín bằng đặc trưng DSIFT-LLC kết hợp máy vectơ hỗ trợ, đạt 92,71% độ chính xác phát hiện và 91,52% độ chính xác phân loại. Công trình chứng minh bài toán khả thi, nhưng dùng thiết bị chuyên dụng và vẫn đánh giá theo phép chia tập trong cùng một bộ dữ liệu.

Bốn hạn chế mang tính hệ thống của dòng nghiên cứu này là chỗ đề tài đặt vấn đề.

Hạn chế thứ nhất thuộc về điều kiện thu ảnh. Phần lớn nghiên cứu chụp trong hộp sáng hoặc phòng có nền đồng nhất và ánh sáng kiểm soát, mỗi lần một quả. Ảnh mà người trồng và người thu mua thực tế chụp có đặc điểm ngược lại. Phân bố dữ liệu vì vậy khác nhau, và hiệu năng công bố trên ảnh chụp trong phòng không chuyển thẳng sang điều kiện sử dụng thực tế.

Hạn chế thứ hai thuộc về thiết kế đánh giá và là hạn chế quan trọng nhất đối với đề tài. Phần lớn công trình chia tập huấn luyện và tập kiểm tra ngẫu nhiên trong cùng một bộ dữ liệu, tức cùng một nguồn quả, một giống, một đợt chụp, đôi khi là các ảnh khác nhau của cùng một quả. Kết quả thu được trả lời câu hỏi mô hình học thuộc bộ dữ liệu này tốt tới đâu, chứ không trả lời câu hỏi mô hình dùng được ở nguồn quả khác hay không. Trong quá trình thực hiện đề tài, nhóm đã tự kiểm chứng được mức độ nghiêm trọng của hạn chế này; kết quả trình bày ở mục 4.3.1.

Hạn chế thứ ba thuộc về bản chất của nhãn. Nhãn độ chín trong hầu hết công trình do người gán theo màu vỏ. Mô hình huấn luyện trên loại nhãn này, dù đạt độ chính xác cao, cũng chỉ tái tạo phán đoán thị giác của người gán nhãn kể cả sai số của phán đoán đó. Số công trình đối chiếu dự đoán từ ảnh với chỉ tiêu hóa sinh đo trên chính quả đã chụp còn rất ít.

Hạn chế thứ tư thuộc về phạm vi đầu ra. Các mô hình phân loại độ chín đều là mô hình tập đóng trên năm hoặc sáu bậc chín, nên buộc phải gán một bậc cho bất kỳ ảnh nào đưa vào. Khi gặp quả đã hỏng, dập vỏ hoặc nhiễm nấm, mô hình vẫn trả về một bậc chín kèm độ tin cậy cao. Trong ứng dụng hỗ trợ thu hoạch, đây là dạng sai sót nguy hiểm nhất vì nó sai theo hướng gây thiệt hại và không có dấu hiệu cảnh báo.

## 2.6. Các nghiên cứu trong nước

Nghiên cứu về chanh dây trong nước tập trung ở ba nhánh. Nhánh chọn giống và kỹ thuật canh tác gắn với việc mở rộng diện tích nhanh trong mười năm gần đây; tính đến cuối năm 2025 đã có 43 giống chanh leo được công bố lưu hành (Cục Trồng trọt và Bảo vệ thực vật, 2025). Nhánh bệnh hại tập trung vào nhóm bệnh do virus, yếu tố hạn chế lớn nhất đối với cây chanh dây. Nhánh thứ ba là công nghệ sau thu hoạch và chế biến dịch quả.

Ứng dụng thị giác máy tính trên nông sản trong nước cũng đã hình thành, chủ yếu trên các đối tượng có sản lượng lớn và đã có tiêu chuẩn phân loại sẵn, tập trung vào phân loại chất lượng tại cơ sở đóng gói hơn là hỗ trợ quyết định tại vườn.

Phần còn để ngỏ nằm ở chỗ nối giữa các nhánh trên. Theo rà soát của nhóm, chưa có công trình nào công bố bộ dữ liệu ảnh độ chín chanh dây tại Việt Nam có gán nhãn theo giai đoạn, thu từ nhiều nguồn xuất xứ khác nhau và có kèm chỉ tiêu hóa sinh đo trên chính quả đã chụp.

## 2.7. Những vấn đề còn tồn tại và phương án giải quyết

### 2.7.1. Khoảng trống nghiên cứu

Khoảng trống thứ nhất thuộc về dữ liệu. Chưa có bộ dữ liệu ảnh độ chín chanh dây thu từ nhiều nguồn xuất xứ khác nhau, được công bố công khai kèm giao thức chụp, hướng dẫn gán nhãn có ảnh minh họa và mã định danh từng quả cho phép chia tập không rò rỉ.

Khoảng trống thứ hai thuộc về khả năng tổng quát. Mức sụt giảm hiệu năng của mô hình khi chuyển sang nguồn quả chưa từng thấy chưa được định lượng đối với chanh dây, do thiết kế đánh giá phổ biến chia tập ngẫu nhiên trong cùng một bộ dữ liệu.

Khoảng trống thứ ba thuộc về chuẩn tham chiếu. Chưa có công trình nào trên chanh dây đối chiếu dự đoán độ chín từ ảnh với chỉ tiêu hóa sinh đo trên chính quả đã chụp, nên chưa xác định được mô hình đang dự đoán độ chín sinh lý hay tái tạo phán đoán màu của người gán nhãn.

Khoảng trống thứ tư thuộc về thước đo. Chưa có nghiên cứu nào đánh giá mô hình theo chi phí bất đối xứng giữa hái sớm và hái muộn, trong khi đây mới là cấu trúc thiệt hại thực tế của quyết định thu hoạch phục vụ xuất khẩu.

Khoảng trống thứ năm thuộc về xử lý điều kiện chiếu sáng. Các công trình có dùng thẻ chuẩn đều dừng ở việc hiệu chỉnh màu cho chính bộ ảnh nghiên cứu. Chưa công trình nào khai thác giá trị nguồn sáng suy từ thẻ làm nhãn giám sát để huấn luyện một mô-đun ước lượng nguồn sáng dùng được khi không có thẻ, tức khi triển khai thực tế.

Khoảng trống thứ sáu thuộc về phạm vi đầu ra, như đã nêu ở mục 2.5.

### 2.7.2. Phương án giải quyết và đóng góp của nghiên cứu

Ứng với sáu khoảng trống trên, nghiên cứu đề xuất tám nội dung giải quyết, đồng thời là tám đóng góp mà nhóm tuyên bố.

- Xây dựng bộ dữ liệu ảnh độ chín chanh dây thu từ nhiều nguồn xuất xứ khác nhau, công bố công khai kèm hướng dẫn gán nhãn, giao thức chụp, mã định danh từng quả và chỉ số đồng thuận giữa những người gán nhãn. Chỉ số đồng thuận xác định trần hiệu năng mà mô hình có thể đạt tới một cách có ý nghĩa.

- Định lượng mức sụt giảm hiệu năng khi chuyển sang nguồn quả chưa từng thấy bằng thiết kế đánh giá bỏ ra một nguồn, và định lượng riêng mức chênh lệch giữa phép chia ngẫu nhiên theo ảnh với phép chia theo quả.

- Tách nguyên nhân của mức sụt giảm đó bằng thí nghiệm chạy toàn bộ quy trình ở ba cấu hình chuẩn hóa màu, nhằm phân biệt phần chênh lệch do điều kiện chiếu sáng với phần do khác biệt giống và điều kiện canh tác.

- Đề xuất mô-đun ước lượng nguồn sáng học từ thẻ chuẩn, dùng được khi không có thẻ trong khung hình, và định lượng cái giá phải trả khi bỏ thẻ đi.

- Đối chiếu dự đoán từ ảnh với hàm lượng chất rắn hòa tan tổng số đo trên chính quả đã chụp, qua đó xác định mô hình dự đoán độ chín sinh lý hay tái tạo cách quan sát màu của người gán nhãn.

- So sánh trực tiếp giữa mô hình và phán đoán của người thu hái có kinh nghiệm trên cùng bộ ảnh và cùng chuẩn tham chiếu.

- Xây dựng khung đánh giá theo ma trận chi phí bất đối xứng, phản ánh việc hái sớm một bậc và hái muộn một bậc gây thiệt hại khác nhau.

- Tách tình trạng sử dụng của quả thành một đầu ra độc lập với độ chín, kèm cơ chế từ chối trả lời dựa trên độ tin cậy đã hiệu chuẩn, nhằm loại bỏ dạng sai sót nêu ở hạn chế thứ tư mục 2.5.

Bảng 1 đối chiếu phạm vi của nghiên cứu này với hai hướng nghiên cứu đi trước, làm rõ phần nội dung được kế thừa và phần nội dung được bổ sung.

**Bảng 1.** So sánh phạm vi nghiên cứu với hướng nghiên cứu đi trước.

| **Nội dung** | **Nghiên cứu phân loại độ chín quả nói chung** | **Nghiên cứu thị giác máy tính nông nghiệp tại Việt Nam** | **Nghiên cứu này** |
| --- | --- | --- | --- |
| Phân loại độ chín quả bằng ảnh | Có | Có | Có |
| Phủ nhiều nguồn quả có xuất xứ khác nhau | Hiếm | Hiếm | Có |
| Mã định danh từng quả, chia tập không rò rỉ | Rất hiếm | Rất hiếm | Có |
| Đánh giá bỏ ra một nguồn, không chia tập ngẫu nhiên | Rất hiếm | Rất hiếm | Có |
| Thẻ chuẩn trong khung hình | Hiếm | Hiếm | Có |
| Tách ảnh hưởng của chiếu sáng khỏi khác biệt giữa các nguồn | Không | Không | Có |
| Ước lượng nguồn sáng khi không có thẻ | Không | Không | Có |
| Đối chiếu với chỉ tiêu hóa sinh trên chính quả đã chụp | Ít | Ít | Có |
| So sánh với phán đoán của người thu hái | Rất hiếm | Rất hiếm | Có |
| Đánh giá theo chi phí bất đối xứng | Không | Không | Có |
| Đầu ra tình trạng quả tách khỏi độ chín | Không | Không | Có |
| Cơ chế từ chối trả lời | Không | Không | Có |
| Bộ dữ liệu công bố công khai kèm chỉ số đồng thuận | Tùy công trình | Hiếm | Có |
# 3. MỤC TIÊU - PHƯƠNG PHÁP

## 3.1. Mục tiêu nghiên cứu

Mục tiêu tổng quát là xây dựng và kiểm chứng quy trình xác định giai đoạn chín và tình trạng sử dụng của quả chanh dây từ ảnh số, đủ tin cậy để hỗ trợ quyết định thời điểm thu hoạch, đồng thời xác định rõ giới hạn sử dụng của quy trình. Bảy mục tiêu cụ thể như sau.

- Xây dựng bộ dữ liệu ảnh độ chín chanh dây thu từ nhiều nguồn xuất xứ khác nhau, có gán nhãn theo hai trục độc lập là bậc chín và tình trạng, có mã định danh từng quả, và có chỉ số đồng thuận giữa những người gán nhãn.

- Xác định chuẩn tham chiếu hóa sinh cho các bậc nhãn thông qua hàm lượng chất rắn hòa tan tổng số, độ chua chuẩn độ và tỷ số TSS/TA đo trên chính quả đã chụp.

- Xây dựng và so sánh ba nhóm phương pháp phân loại giai đoạn chín, gồm đường cơ sở dựa trên thống kê màu, mô hình học sâu và phán đoán của con người.

- Xây dựng đầu ra thứ hai phân loại tình trạng sử dụng của quả, độc lập với trục độ chín, kèm cơ chế từ chối trả lời.

- Định lượng khả năng tổng quát của mô hình sang nguồn quả chưa từng thấy bằng thiết kế bỏ ra một nguồn, và tách phần nguyên nhân đến từ điều kiện chiếu sáng.

- Xây dựng mô-đun ước lượng nguồn sáng học từ thẻ chuẩn và đánh giá khả năng thay thế thẻ khi triển khai thực tế.

- Đánh giá mô hình theo ma trận chi phí bất đối xứng phản ánh thiệt hại thực tế của việc hái sớm và hái muộn, rồi đề xuất khuyến nghị cho nông hộ, doanh nghiệp thu mua và cơ quan quản lý chất lượng nông sản.

## 3.2. Câu hỏi nghiên cứu và giả thuyết

Năm câu hỏi nghiên cứu và năm giả thuyết tương ứng được trình bày dưới đây. Các ngưỡng được xác lập trước khi tiến hành thí nghiệm và được báo cáo nguyên trạng dù kết quả rơi về phía nào.

- **Câu hỏi 1.** Ảnh số có đủ thông tin để phân loại giai đoạn chín hay không? *Giả thuyết 1:* trên tập kiểm tra cùng nguồn chia theo quả, mô hình tốt nhất đạt điểm F1 trung bình theo lớp không dưới 0,85 và vượt đường cơ sở màu ít nhất 0,10.

- **Câu hỏi 2.** Hiệu năng có được duy trì khi chuyển sang nguồn quả chưa từng thấy hay không? *Giả thuyết 2:* trong thiết kế bỏ ra một nguồn, điểm F1 trung bình theo lớp giảm không quá 0,10 so với đánh giá cùng nguồn.

- **Câu hỏi 3.** Mô hình dự đoán độ chín sinh lý hay tái tạo phán đoán màu của người gán nhãn? *Giả thuyết 3:* bậc chín dự đoán từ ảnh giải thích được biến thiên của hàm lượng chất rắn hòa tan tổng số với hệ số xác định không dưới 0,60.

- **Câu hỏi 4.** Hiệu năng của mô hình so với phán đoán của người thu hái ra sao? *Giả thuyết 4:* mô hình đạt độ chính xác không thấp hơn mức trung bình của những người tham gia gán nhãn khi cùng đối chiếu với chuẩn tham chiếu hóa sinh.

- **Câu hỏi 5.** Mô-đun ước lượng nguồn sáng từ cảnh có thay thế được thẻ chuẩn trong khung hình hay không? *Giả thuyết 5:* sai số góc trung vị của mô-đun thấp hơn phương pháp Shades-of-Gray, và khi dùng mô-đun thay cho thẻ, điểm F1 trong đánh giá bỏ ra một nguồn giảm không quá 0,05 so với cấu hình dùng thẻ.

Câu hỏi 1 được trả lời tại mục 4.3, Câu hỏi 2 và Câu hỏi 5 tại mục 4.4, Câu hỏi 3 và Câu hỏi 4 tại mục 4.6.

Giả thuyết 2 là trục chính của nghiên cứu và có khả năng bị bác bỏ. Hiện tượng dịch chuyển miền dữ liệu giữa các nguồn thu đã được ghi nhận rộng rãi, với mức sụt giảm có thể rất lớn (Mohanty và cs, 2016), nên kịch bản hiệu năng giảm quá ngưỡng hoàn toàn có thể xảy ra. Trong trường hợp đó, kết quả âm vẫn có giá trị vì nó định lượng được rào cản của việc triển khai và cho thấy các con số dựa trên phép chia tập ngẫu nhiên trong một nguồn là lạc quan hơn thực tế. Ngưỡng đã đặt không được thay đổi sau khi có số liệu.

## 3.3. Bố trí thí nghiệm tổng thể

Nghiên cứu sử dụng thiết kế thực nghiệm gồm ba giai đoạn nối tiếp, thực hiện trên quả thương phẩm thu từ nhiều nguồn xuất xứ khác nhau. Quy trình tổng thể trình bày ở Hình 1.

Giai đoạn một gồm năm bước: chọn nguồn thu mẫu theo tiêu chí đa xuất xứ và đa bậc chín; chụp ảnh theo giao thức cố định có thẻ chuẩn và mã định danh quả trong khung hình; hiệu chỉnh màu theo thẻ; tiền xử lý ảnh gồm tách nền, tạo mặt nạ vùng quả và cắt theo hộp bao; xác định các chỉ tiêu hóa sinh trên chính quả đã chụp. Kết thúc giai đoạn này, bộ dữ liệu được hai người gán nhãn độc lập và đo mức đồng thuận.

Giai đoạn hai huấn luyện và đối chứng ba nhóm phương pháp phân loại độ chín trên cùng tập dữ liệu đã chuẩn hóa, đồng thời xây dựng đầu ra tình trạng quả và mô-đun ước lượng nguồn sáng.

Giai đoạn ba đánh giá theo ba phép gồm đánh giá cùng nguồn, đánh giá bỏ ra một nguồn và đánh giá theo chi phí bất đối xứng, sau đó đối chiếu dự đoán với chuẩn tham chiếu hóa sinh và tổng hợp thành công cụ hỗ trợ quyết định thu hoạch kèm giới hạn sử dụng.

*[Chèn sơ đồ quy trình nghiên cứu tổng thể tại đây]*

**Hình 1.** Sơ đồ quy trình nghiên cứu tổng thể, từ thu mẫu đến công cụ hỗ trợ quyết định thu hoạch.

## 3.4. Vật liệu và phương pháp thu thập dữ liệu

Vật liệu nghiên cứu là quả chanh dây (*Passiflora edulis* Sims) thương phẩm, thu mua tại các vựa và điểm bán ở chợ đầu mối, hoặc mua trực tiếp tại vườn khi có điều kiện. Quả được chọn ở đủ năm bậc chín theo sơ đồ nhãn ở mục 3.4.4, gồm cả quả nguyên vẹn và quả đã có biểu hiện hư hỏng để phục vụ đầu ra thứ hai.

Thiết bị và dụng cụ gồm: máy ảnh kỹ thuật số ống kính rời dùng cho bộ ảnh chuẩn tham chiếu, và điện thoại di động phổ thông dùng cho bộ ảnh kiểm chứng điều kiện triển khai; thẻ chuẩn in bốn ô xám có phản xạ khác nhau kèm mã QR và thước tỷ lệ, đặt trong khung hình; nhãn giấy ghi mã định danh quả; khúc xạ kế cầm tay thang đo 0-32 °Brix có bù nhiệt tự động; cân điện tử độ chính xác 0,01 g; thước kẹp điện tử độ chính xác 0,01 mm; bộ chuẩn độ với dung dịch NaOH 0,1 N và chỉ thị phenolphtalein; máy đo pH; dao inox, rây lọc và ống đong.

### 3.4.1. Chiến lược chọn nguồn thu mẫu

Nhóm định nghĩa nguồn thu mẫu, gọi tắt là nguồn, là một lô quả có cùng xuất xứ, tức quả từ cùng một vườn, tiếp cận qua một vựa hoặc một điểm bán, hoặc mua trực tiếp tại vườn. Đơn vị thiết kế của nghiên cứu là nguồn, và đơn vị quan sát là quả, chứ không phải ảnh.

Chiến lược này phục vụ hai mục đích. Về mặt khoa học, việc trả lời Câu hỏi 2 đòi hỏi có nhiều nguồn xuất xứ khác nhau, vì với một nguồn duy nhất thì không tồn tại phép đánh giá bỏ ra một nguồn; số nguồn chính là số phép đánh giá độc lập mà nghiên cứu có được. Về mặt tiến độ, việc theo dõi một vườn duy nhất đòi hỏi chờ quả đi hết chu trình từ xanh tới chín, kéo dài nhiều tuần và phụ thuộc vào điều kiện thời tiết. Do chanh dây cho thu hoạch nhiều lứa trong năm và được tập kết về vựa quanh năm, phương án lấy mẫu cắt ngang qua nhiều nguồn cho đủ các bậc chín ngay trong vài đợt thu mẫu ngắn.

Tiêu chí chọn nguồn là tối đa hóa khác biệt giữa các nguồn trên những yếu tố ảnh hưởng tới biểu hiện màu của vỏ quả, gồm vùng trồng, giống, dạng quả, thời điểm thu hái và kênh phân phối. Để hạn chế khả năng hai nguồn thực chất cùng một vườn gốc, nhóm lấy mẫu ở các vựa và điểm bán khác nhau, ghi nhận thông tin xuất xứ ở mức chi tiết nhất mà người bán cung cấp được, và ưu tiên những lô khác biệt rõ về hình thái quả. Nguồn mua trực tiếp tại vườn được đánh dấu riêng vì xuất xứ khi đó là thông tin kiểm chứng được. Đặc điểm từng nguồn được mô tả ở Bảng 2.

**Bảng 2.** Đặc điểm các nguồn thu mẫu.

| **Mã nguồn** | **Nơi mua và xuất xứ khai báo** | **Kênh tiếp cận** | **Ngày thu hái** | **Giống và dạng quả** | **Số quả thu mẫu** | **Số ảnh** |
| --- | --- | --- | --- | --- | --- | --- |
| N1 |  |  |  |  |  |  |
| N2 |  |  |  |  |  |  |
| N3 |  |  |  |  |  |  |
| N4 |  |  |  |  |  |  |
| Tổng |  |  |  |  |  |  |

*Ghi chú: số dòng của Bảng 2, Bảng 7 và Bảng 10 được điều chỉnh theo số nguồn thực tế thu được; ký hiệu N1 tới N4 là khung trình bày.*

### 3.4.2. Giao thức chụp ảnh và lựa chọn thiết bị

Nghiên cứu sử dụng hai bộ ảnh có vai trò khác nhau, và việc phân biệt hai bộ này là một lựa chọn thiết kế có chủ đích chứ không phải sự pha trộn tùy tiện.

**Bộ ảnh chuẩn tham chiếu** được chụp bằng máy ảnh kỹ thuật số ống kính rời, đặt trên chân máy, khóa cố định độ nhạy sáng, tốc độ màn trập, khẩu độ và chế độ cân bằng trắng cho toàn bộ một đợt chụp. Bộ này phục vụ việc đo màu, xây dựng chuẩn nhãn và đối chiếu với chỉ tiêu hóa sinh, tức những nhiệm vụ đòi hỏi phép đo màu ổn định nhất có thể. Máy ảnh cho phép ghi đồng thời tệp ảnh nén và tệp ảnh thô; tệp ảnh thô được giữ lại vì giá trị pixel của nó tỷ lệ tuyến tính với lượng ánh sáng tới, trong khi tệp ảnh nén đã qua cân bằng trắng và ánh xạ tông của máy nên không dùng được cho phép đo màu tuyệt đối.

**Bộ ảnh kiểm chứng điều kiện triển khai** được chụp bằng điện thoại di động phổ thông trên chính những quả đã chụp ở bộ thứ nhất, không dùng chân máy, ở nhiều khung giờ và cả trong nhà lẫn ngoài trời. Bộ này phục vụ việc trả lời câu hỏi mô hình huấn luyện trên ảnh chuẩn có dùng được trên ảnh chụp bằng thiết bị mà người trồng đang sử dụng hay không. Đây là một biến thể của Câu hỏi 2, trong đó yếu tố thay đổi là thiết bị thu ảnh thay vì nguồn quả.

Giao thức chụp gồm năm ràng buộc, áp dụng cho cả hai bộ.

- Thẻ chuẩn gồm bốn ô xám có phản xạ khác nhau, kèm mã QR và thước tỷ lệ, được đặt trong khung hình ở mỗi lần chụp. Cường độ và nhiệt độ màu của ánh sáng thay đổi theo giờ trong ngày, theo mây và theo vị trí chụp, khiến cùng một quả cho hai giá trị màu khác nhau (Berry và cs, 2018). Thiếu thẻ chuẩn thì khác biệt màu giữa các nguồn không tách được khỏi khác biệt chiếu sáng, và Câu hỏi 2 trở nên không trả lời được. Việc dùng bốn ô thay vì một ô trắng cho phép ước lượng nguồn sáng bằng hồi quy qua nhiều điểm, ổn định hơn, đồng thời cho phép kiểm tra đáp ứng của máy có tuyến tính hay không.

- Mã định danh quả được ghi trên nhãn giấy đặt trong khung hình. Đây là ràng buộc quan trọng nhất về mặt phương pháp: nhờ nó, mọi ảnh của cùng một quả luôn truy được về một mã, và phép chia tập theo quả ở mục 3.4.8 thực hiện được. Không có mã này thì không có cách nào bảo đảm ảnh của cùng một quả không nằm ở hai tập khác nhau.

- Mỗi tập quả được chụp ở ít nhất hai khung giờ khác nhau trong ngày, nhằm đưa biến thiên chiếu sáng vào dữ liệu một cách có kiểm soát.

- Ảnh được chụp theo hai chế độ. Chế độ thứ nhất là ảnh chuẩn hóa, mỗi ảnh một quả đặt trên nền tối đồng nhất, dùng cho việc đo màu và xây dựng chuẩn nhãn. Chế độ thứ hai là ảnh bối cảnh gồm nhiều quả trên nền không đồng nhất ngoài trời, dùng để kiểm tra hiệu năng ở điều kiện sử dụng thực tế và đo riêng ảnh hưởng của nền cùng của việc quả bị che một phần.

- Mỗi quả được chụp ở nhiều tư thế xoay khác nhau, vì tỷ lệ vỏ chuyển màu quan sát được phụ thuộc vào mặt quả hướng về ống kính.

Thông số thiết bị, khoảng cách chụp, khung giờ và điều kiện thời tiết của từng đợt được ghi nhật ký và trình bày ở Phụ lục 2.

### 3.4.3. Tiền xử lý ảnh

Ảnh thô được xử lý qua ba bước trước khi đưa vào mô hình.

**Bước thứ nhất là hiệu chỉnh màu theo thẻ chuẩn.** Giá trị pixel trung bình của bốn ô xám được đo, loại trừ các pixel đã bão hòa vì chúng không còn mang thông tin màu. Do ô xám có phản xạ trung tính, mọi lệch giữa ba kênh đo được trên chúng đều do nguồn sáng gây ra. Vector nguồn sáng được ước lượng bằng hồi quy qua gốc tọa độ trên toàn bộ các ô, sau đó ảnh được đưa về nguồn sáng trung tính bằng phép co giãn theo kênh theo mô hình von Kries. Cách làm này theo tinh thần của Berry và cs (2018), với khác biệt là thẻ dùng ở đây chỉ có ô trung tính nên chỉ hiệu chỉnh được cân bằng trắng; hạn chế này được nêu ở mục 4.8.1.

**Bước thứ hai là tách vùng quả khỏi nền.** Vùng thẻ chuẩn được loại khỏi tập ứng viên trước tiên, vì thẻ sáng hơn nền nên nếu không loại thì thuật toán có thể chọn nhầm chính thẻ làm quả. Sau đó thực hiện phân ngưỡng trên kênh độ sáng và kênh độ bão hòa, kết hợp các phép toán hình thái học nhằm loại nhiễu và lấp lỗ hổng. Trong số các thành phần liên thông thu được, thành phần được chọn phải thỏa đồng thời ba điều kiện: diện tích vượt ngưỡng tối thiểu, tỷ lệ cạnh hộp bao nằm trong khoảng của một vật thể gần tròn, và tỷ lệ lấp đầy hộp bao đủ cao. Ba điều kiện này loại được các mảng dài như viền vải hay thước tỷ lệ.

**Bước thứ ba là cắt ảnh theo hộp bao của mặt nạ.** Bước này cần thiết vì ở khoảng cách chụp đã dùng, quả chỉ chiếm khoảng hai phần trăm diện tích khung hình. Nếu đưa thẳng ảnh gốc vào mô hình ở kích thước đầu vào tiêu chuẩn, quả sẽ chỉ còn khoảng hai mươi điểm ảnh, tức gần như toàn bộ độ phân giải bị dành cho phông nền. Sau khi cắt, quả chiếm trọn khung đầu vào.

Việc cắt theo mặt nạ đồng thời loại bỏ phần nền, thẻ chuẩn và nhãn định danh khỏi đầu vào của mô hình, nhờ đó mô hình không học các đặc trưng gắn với bối cảnh chụp hoặc với chính mã số quả thay vì đặc trưng của vỏ quả. Kết quả tiền xử lý trên một tập ảnh mẫu được trình bày ở Hình 2. Tỷ lệ ảnh tách nền thất bại được ghi nhận và báo cáo ở mục 4.1.

Đối với ảnh bối cảnh nhiều quả, bước tách vùng được thay bằng bước phát hiện đối tượng, sau đó mỗi quả phát hiện được cắt ra và xử lý như một mẫu độc lập.

*[Chèn hình demo_montage: cột 1 ảnh gốc, cột 2 mặt nạ vùng quả, cột 3 ảnh cắt]*

**Hình 2.** Kết quả tiền xử lý ảnh trên một tập ảnh mẫu: ảnh gốc (cột trái), mặt nạ nhị phân vùng quả sau phân ngưỡng và xử lý hình thái học (cột giữa), ảnh cắt theo hộp bao dùng làm đầu vào cho mô hình (cột phải).

### 3.4.4. Sơ đồ nhãn giai đoạn chín

Giai đoạn chín được định nghĩa theo tỷ lệ diện tích vỏ đã chuyển màu, chia thành năm bậc, tương ứng với thang năm bậc đã dùng trên cùng đối tượng bởi Tu và cs (2018). Ranh giới giữa các bậc được chốt sau đợt thu mẫu thử và trình bày kèm ảnh minh họa ở Hình 3, vì một sơ đồ nhãn không có ảnh minh họa thì không lặp lại được ở nhóm nghiên cứu khác.

Tỷ lệ vỏ chuyển màu được xác định theo hai cách song song: người đo ước lượng trực quan trên quả cầm trong tay, và tính từ ảnh sau khi tách nền bằng tỷ lệ số pixel có giá trị a\* vượt ngưỡng trên tổng số pixel thuộc vùng quả. Chênh lệch giữa hai cách được báo cáo ở mục 4.2.

Cột ý nghĩa với quyết định thu hoạch trong Bảng 3 là chỗ nối giữa sơ đồ nhãn và ma trận chi phí ở mục 3.6, và được chốt sau khi tham vấn người thu hái có kinh nghiệm về vị trí thực tế của cửa sổ hái.

**Bảng 3.** Sơ đồ nhãn giai đoạn chín.

| **Bậc** | **Tên gọi** | **Mô tả tỷ lệ vỏ chuyển màu** | **Ý nghĩa với quyết định thu hoạch** |
| --- | --- | --- | --- |
| 1 | Xanh | Dưới 10% diện tích vỏ chuyển màu; vỏ xanh đồng đều, bề mặt căng bóng | Chưa đạt độ chín sinh lý, không hái |
| 2 | Bắt đầu chuyển màu | 10-30% diện tích vỏ chuyển màu, thường bắt đầu từ vùng gần cuống hoặc phía đón nắng | Chưa hái |
| 3 | Chuyển màu một phần | 30-70% diện tích vỏ chuyển màu, xen kẽ vùng xanh và vùng đã chuyển | Cửa sổ hái cho vận chuyển xa |
| 4 | Chuyển màu phần lớn | Trên 70% diện tích vỏ chuyển màu, chỉ còn vệt xanh nhỏ | Cửa sổ hái cho tiêu thụ gần |
| 5 | Chín hoàn toàn | Toàn bộ vỏ đã chuyển màu; có thể xuất hiện dấu hiệu nhăn vỏ đầu tiên | Quá muộn cho xuất khẩu, nguy cơ nhăn vỏ và rụng |

*Ghi chú: ngưỡng phần trăm ở cột thứ ba là giá trị dự kiến, được hiệu chỉnh sau đợt thu mẫu thử và chốt cùng ảnh minh họa ở Hình 3. Sơ đồ này chỉ áp dụng cho quả còn sử dụng được; tình trạng quả là một trục nhãn riêng, trình bày ở mục 3.4.5.*

*[Chèn ảnh minh họa năm bậc chín, đánh thứ tự A, B, C, D, E bằng text box]*

**Hình 3.** Ảnh minh họa năm bậc chín theo sơ đồ nhãn: bậc 1 (A), bậc 2 (B), bậc 3 (C), bậc 4 (D) và bậc 5 (E).

### 3.4.5. Sơ đồ nhãn tình trạng quả và lý do tách thành trục riêng

Ngoài bậc chín, mỗi quả được gán thêm một nhãn tình trạng theo Bảng 4. Việc tách tình trạng thành một trục riêng thay vì thêm một bậc thứ sáu vào thang độ chín xuất phát từ ba lý do.

Thứ nhất, độ chín là một trục có thứ tự, trong đó khoảng cách giữa hai bậc kề nhau có ý nghĩa sinh lý. Tình trạng quả là một thuộc tính khác, tồn tại đồng thời với độ chín chứ không loại trừ nó: một quả có thể đang ở bậc 3 và đồng thời bị nhiễm nấm hoặc dập vỏ. Đặt hỏng vào cuối thang độ chín ngầm khẳng định hỏng là bậc tiếp theo sau chín hoàn toàn, điều chỉ đúng với một loại hư hỏng và sai với các loại còn lại.

Thứ hai, việc thêm một bậc thứ sáu phá vỡ các chỉ số có thứ tự dùng trong nghiên cứu. Hệ số Kappa có trọng số bậc và sai số trung bình theo bậc đều giả định khoảng cách giữa các nhãn có ý nghĩa; với lớp thứ sáu là hỏng, khoảng cách từ bậc 2 tới hỏng bị tính là bốn bậc, một con số không diễn giải được.

Thứ ba, ma trận chi phí ở mục 3.6 phân loại mọi sai sót thành hái sớm hoặc hái muộn. Một dự đoán hỏng khi quả thật ở bậc 2 không thuộc loại nào trong hai loại đó, nên không đặt được vào ma trận.

Quy tắc quyết định của công cụ vì vậy là: nếu đầu ra tình trạng cho kết quả hỏng, quả được loại khỏi lô và không xét bậc chín. Kiến trúc hai đầu ra trình bày ở Hình 4.

**Bảng 4.** Sơ đồ nhãn tình trạng quả.

| **Nhãn** | **Mô tả** | **Ý nghĩa với quyết định** |
| --- | --- | --- |
| Dùng được | Vỏ nguyên vẹn, không dập vỡ, không có vết nấm bệnh, không nhăn quá mức | Xét tiếp bậc chín theo Bảng 3 |
| Hỏng | Có ít nhất một trong các biểu hiện: dập vỡ vỏ, vết nấm hoặc mốc, thối nhũn, nhăn vỏ nghiêm trọng, khô cuống nặng | Loại khỏi lô, không xét bậc chín |

*Ghi chú: loại hư hỏng cụ thể của từng quả được ghi nhận riêng trong bảng kê dữ liệu để phục vụ phân tích sau này, dù mô hình chỉ phân loại nhị phân.*

### 3.4.6. Phương pháp xác định các chỉ tiêu hóa sinh

Sau khi chụp, quả được bổ ngay để xác định các chỉ tiêu dưới đây. Mỗi chỉ tiêu được đo lặp ba lần trên mỗi quả và lấy giá trị trung bình.

- Hàm lượng chất rắn hòa tan tổng số (TSS). Dịch quả được lọc qua rây loại bỏ hạt, nhỏ hai đến ba giọt lên lăng kính khúc xạ kế cầm tay có bù nhiệt tự động, đọc trực tiếp giá trị theo thang °Brix. Lăng kính được rửa bằng nước cất và lau khô sau mỗi lần đo.

- Độ chua chuẩn độ (TA). Lấy 10 mL dịch quả pha loãng với nước cất theo tỷ lệ 1:9, chuẩn độ bằng dung dịch NaOH 0,1 N với chỉ thị phenolphtalein tới khi xuất hiện màu hồng nhạt bền trong 30 giây, hoặc tới pH 8,1 nếu chuẩn độ theo máy đo pH. Kết quả quy đổi theo axit citric và biểu diễn bằng phần trăm khối lượng trên thể tích.

- Tỷ số TSS/TA, tính bằng thương của hai giá trị trên.

- Khối lượng quả, cân bằng cân điện tử độ chính xác 0,01 g trước khi bổ quả. Độ dày vỏ được đo bằng thước kẹp điện tử tại ba vị trí trên mặt cắt ngang.

- Tỷ lệ hao hụt khối lượng đối với nhóm quả theo dõi ở mục 3.4.9, tính theo công thức: hao hụt khối lượng (%) = (khối lượng ban đầu trừ khối lượng tại thời điểm đo) chia cho khối lượng ban đầu, nhân 100.

TSS được chọn làm chỉ tiêu tham chiếu chính vì đo được ngay tại điểm thu mẫu với chi phí thấp. TA và tỷ số TSS/TA chỉ được báo cáo nếu đo đủ số mẫu theo điều kiện phòng thí nghiệm.

### 3.4.7. Quy mô mẫu

Bộ dữ liệu gồm […] quả riêng biệt. Mỗi quả được chụp ở nhiều tư thế và nhiều điều kiện chiếu sáng, trung bình […] ảnh mỗi quả, cho […] ảnh ở phần lấy mẫu cắt ngang. Phần theo dõi theo thời gian ở mục 3.4.9 bổ sung […] ảnh, đưa tổng số ảnh lên […].

Ràng buộc quyết định cỡ mẫu không phải tổng số ảnh mà là **số quả trong bậc nhãn hiếm nhất ở nguồn nhỏ nhất**, vì phép đánh giá bỏ ra một nguồn đòi hỏi mỗi nguồn tự nó phải có đủ quan sát ở mọi bậc. Điểm này cần được nhấn mạnh vì tổng số ảnh dễ gây ấn tượng sai về quy mô nghiên cứu: một bộ dữ liệu nghìn ảnh trên năm mươi quả có cỡ mẫu thống kê là năm mươi, không phải một nghìn, do các ảnh của cùng một quả không độc lập với nhau.

Nhóm đặt sàn tối thiểu 20 quả cho mỗi bậc nhãn ở mỗi nguồn ngay từ khi lập kế hoạch thu mẫu, và điều chỉnh lượng thu mẫu theo sàn này. Do bậc 4 và bậc 5 hiếm gặp ở kênh phân phối quả thương phẩm, nhóm bổ sung hai bậc này bằng cách giữ lại quả ở bậc 2 và bậc 3 cho chín tiếp ở nhiệt độ phòng, đồng thời đánh dấu riêng để không trộn với quả thu trực tiếp. Mức độ đạt sàn được báo cáo ở mục 4.1.

Toàn bộ quả đều được đo TSS sau khi chụp nhằm tăng lực thống kê cho Câu hỏi 3. Khoảng tin cậy 95 phần trăm của hệ số tương quan được báo cáo ở mục 4.6.

### 3.4.8. Gán nhãn, đánh giá đồng thuận và phân chia dữ liệu

Hai người gán nhãn độc lập trên toàn bộ tập, hoặc trên phần chồng lấn không dưới ba trăm ảnh nếu khối lượng vượt quá khả năng. Mức đồng thuận được báo cáo bằng hệ số Kappa có trọng số (Cohen, 1968), dùng trọng số bậc vì nhãn có thứ tự và việc lệch một bậc nhẹ hơn lệch ba bậc. Trường hợp bất đồng do người thứ ba phân xử. Một đợt gán nhãn thử trên năm mươi ảnh được thực hiện trước để hiệu chỉnh hướng dẫn gán nhãn.

Ngoài vai trò kiểm soát chất lượng, việc gán nhãn còn tạo dữ liệu cho Câu hỏi 4. Nhóm mời một tới hai người thu hái có kinh nghiệm gán nhãn trên cùng tập ảnh, qua đó thu được đường tham chiếu con người.

Dữ liệu được chia theo ba cấp với **thứ tự ưu tiên bắt buộc**. Ưu tiên thứ nhất là chia theo nguồn, phục vụ Câu hỏi 2. Ưu tiên thứ hai là trong mỗi nguồn chia theo quả, để nhiều ảnh của cùng một quả không nằm ở hai tập khác nhau. Chỉ khi hai ràng buộc trên đã thỏa mới xét tới cân bằng số lượng giữa các bậc nhãn.

Nguyên tắc này được nêu rõ vì việc vi phạm nó là nguồn sai sót phổ biến và khó phát hiện. Hai ảnh của cùng một quả chụp ở hai tư thế xoay khác nhau vẫn giữ nguyên các đặc điểm riêng của quả đó, gồm hình dạng, các vết sẹo và kiểu phân bố sắc tố. Mô hình chỉ cần nhận diện các đặc điểm đó là trả lời đúng, mà không cần học bất kỳ quy luật nào về độ chín. Kết quả là một con số hiệu năng cao nhưng hoàn toàn không phản ánh khả năng sử dụng thực tế. Mức chênh lệch cụ thể giữa hai cách chia được nhóm đo và báo cáo ở mục 4.3.1.

### 3.4.9. Theo dõi biến đổi sau thu hoạch theo thời gian

Ngoài dữ liệu lấy mẫu cắt ngang, nhóm giữ lại từ 15 tới 20 quả ở bậc 2 và bậc 3, đặt ở nơi thoáng mát, nhiệt độ phòng, và chụp mỗi ngày theo cùng giao thức trong năm tới bảy ngày cho tới khi quả chín hoàn toàn hoặc bắt đầu nhăn vỏ. Khối lượng được cân mỗi ngày để tính tỷ lệ hao hụt; TSS và TA được đo vào ngày đầu và ngày cuối.

Phần theo dõi này phục vụ ba mục đích. Thứ nhất, nó kiểm chứng nội tại mô hình: nếu mô hình chạy trên chuỗi ảnh theo thời gian cho ra bậc chín tăng đơn điệu qua các ngày, phù hợp với biến đổi thực tế của quả, thì đó là bằng chứng mạnh hơn một giá trị F1 trên tập kiểm tra tĩnh. Thứ hai, nó cung cấp dữ liệu ban đầu cho việc dự báo số ngày còn lại tới bậc tiếp theo. Thứ ba, nó là nguồn bổ sung tự nhiên cho các quả ở bậc 4, bậc 5 và cho nhãn hỏng, vốn hiếm gặp ở kênh phân phối quả thương phẩm.

Do quả trong phần này chín sau khi đã rời cây, mà tiến trình hô hấp của quả chín trên giàn và quả chín sau thu hoạch khác nhau (Shiomi và cs, 1996), toàn bộ ảnh của phần theo dõi được đánh dấu riêng và không trộn vào tập dùng để trả lời Câu hỏi 3. Kết quả của phần này được trình bày tách riêng khỏi các câu hỏi nghiên cứu chính.

## 3.5. Phương pháp phân loại

### 3.5.1. Ba nhóm phương pháp phân loại giai đoạn chín

Ba nhóm phương pháp được triển khai và so sánh trên cùng tập kiểm tra, với vai trò khác nhau trong thí nghiệm.

- **Đường cơ sở dựa trên thống kê màu.** Trên vùng quả đã tách nền, tính các thống kê của ba kênh L\*, a\*, b\* gồm giá trị trung bình, độ lệch chuẩn và các phân vị, cùng tỷ lệ pixel vượt ngưỡng a\*, sắc độ, góc màu và một chỉ số về mức độ không đồng đều không gian của sắc tố; sau đó phân loại bằng một mô hình thống kê đơn giản. Nhóm này nhằm xác định mức sàn. Do độ chín chanh dây biểu hiện chủ yếu qua màu vỏ, khả năng đường cơ sở đã đạt phần lớn hiệu năng là có thật; nếu đúng như vậy thì việc dùng mô hình học sâu không được biện minh và đó là kết luận cần báo cáo.

- **Mô hình học sâu.** Các kiến trúc phân loại ảnh tinh chỉnh từ trọng số huấn luyện trước trên ImageNet (Deng và cs, 2009), chọn ở dải kích thước chạy được trên thiết bị di động, gồm các kiến trúc thuộc họ mạng phần dư (He và cs, 2016) và các kiến trúc tối ưu cho thiết bị di động (Sandler và cs, 2018; Tan và Le, 2019). Tên và phiên bản mô hình, tham số huấn luyện và cấu hình phần cứng được trình bày ở Phụ lục 4. Đề tài không đặt vấn đề đóng góp về kiến trúc.

- **Đường tham chiếu con người.** Kết quả phân loại của những người gán nhãn và của người thu hái có kinh nghiệm trên cùng tập ảnh, đối chiếu với cùng chuẩn tham chiếu hóa sinh. Đây vừa là trần hiệu năng vừa là câu trả lời cho Câu hỏi 4.

### 3.5.2. Lựa chọn phép tăng cường dữ liệu

Phép tăng cường dữ liệu trong bài toán này phải được chọn thận trọng hơn thông thường, vì tín hiệu phân biệt các bậc chín gần như hoàn toàn nằm ở màu sắc. Các phép biến đổi làm thay đổi độ bão hòa hoặc độ sáng ở biên độ lớn sẽ xóa chính tín hiệu mà mô hình cần học, trong khi nhãn vẫn giữ nguyên; hệ quả là mô hình bị buộc phải bỏ qua thông tin màu.

Nhóm vì vậy giới hạn biên độ của các phép biến đổi màu ở mức vừa đủ để mô phỏng biến thiên chiếu sáng thực tế, và ưu tiên các phép biến đổi hình học vốn không ảnh hưởng tới màu, gồm xoay, lật ngang, lật dọc và co giãn nhẹ. Phép lật dọc được dùng vì quả chanh dây gần tròn nên ảnh lật dọc vẫn là một ảnh hợp lệ. Phép xóa ngẫu nhiên một vùng ảnh được giữ ở biên độ thấp, vì sau khi cắt theo hộp bao thì quả chiếm gần trọn khung, nên một vùng xóa lớn sẽ che mất phần đáng kể bề mặt quả.

Ngoài ra, nhóm sử dụng một phép tăng cường màu có cơ sở vật lý cho mô-đun ở mục 3.5.4: nhân ảnh với một vector nguồn sáng ngẫu nhiên và cập nhật nhãn nguồn sáng tương ứng. Khác với các phép xáo trộn màu thông thường vốn đổi ảnh mà giữ nguyên nhãn, phép này mô phỏng đúng hiện tượng xảy ra khi đổi nguồn sáng, nên mô hình học được quy luật thật thay vì học cách phớt lờ màu.

### 3.5.3. Đầu ra thứ hai và cơ chế từ chối trả lời

Đầu ra tình trạng quả là một bộ phân loại nhị phân riêng, huấn luyện trên toàn bộ dữ liệu, trong khi đầu ra độ chín chỉ huấn luyện trên quả dùng được. Kiến trúc này trình bày ở Hình 4.

Chỉ số đánh giá của đầu ra này khác với đầu ra độ chín. Do phân bố hai lớp không cân bằng và do hậu quả của hai loại sai sót không đối xứng, nhóm báo cáo độ nhạy, độ chính xác dương tính, diện tích dưới đường cong độ chính xác dương tính và độ nhạy, thay vì chỉ báo độ chính xác chung. Ngưỡng vận hành được chọn theo nguyên tắc bỏ sót quả hỏng nguy hiểm hơn báo nhầm quả tốt thành hỏng, vì một quả hỏng lọt vào lô xuất khẩu có thể ảnh hưởng tới cả kiện hàng.

Ngoài hai đầu ra trên, công cụ có thêm cơ chế từ chối trả lời cho các trường hợp nằm ngoài phạm vi cả hai đầu ra, gồm ảnh không phải chanh dây, ảnh quá mờ, hoặc điều kiện chiếu sáng khác xa dữ liệu huấn luyện. Cơ chế này dựa trên ngưỡng áp lên độ tin cậy của mô hình sau khi đã kiểm tra mức hiệu chuẩn của độ tin cậy đó bằng sai số hiệu chuẩn kỳ vọng. Điểm vận hành được chọn từ đường đánh đổi giữa tỷ lệ từ chối và độ chính xác trên phần đã trả lời, trình bày ở Hình 7.

*[Chèn sơ đồ kiến trúc ba tầng]*

**Hình 4.** Kiến trúc ba tầng của quy trình đề xuất: tầng ước lượng nguồn sáng, tầng hiệu chỉnh và tiền xử lý, tầng phân loại với hai đầu ra độc lập.

### 3.5.4. Mô-đun ước lượng nguồn sáng môi trường

Bước hiệu chỉnh màu ở mục 3.4.3 đòi hỏi thẻ chuẩn có mặt trong khung hình. Yêu cầu này chấp nhận được trong nghiên cứu nhưng không chấp nhận được khi triển khai, vì người trồng sẽ không mang theo thẻ mỗi lần chụp. Đây là một khoảng cách giữa điều kiện nghiên cứu và điều kiện sử dụng mà các công trình đi trước chưa xử lý.

Nhóm đề xuất giải quyết khoảng cách này bằng nhận xét sau: **thẻ chuẩn cung cấp sẵn giá trị tham chiếu của nguồn sáng ở từng ảnh, tức cung cấp sẵn nhãn giám sát cho bài toán ước lượng nguồn sáng, mà không phát sinh thêm bất kỳ chi phí thu thập nào.** Từ đó, một mô hình hồi quy được huấn luyện để dự đoán vector nguồn sáng từ chính cảnh chụp, với vùng thẻ đã bị che đi để mô hình không tiếp cận được đáp án. Kỹ thuật này thuộc dạng chưng cất tri thức: thông tin từ một nguồn tham chiếu sẵn có được chuyển vào một mô hình hoạt động được khi nguồn đó vắng mặt.

Mô-đun được đối chứng với bốn phương pháp không cần dữ liệu huấn luyện là Gray-World, Shades-of-Gray, Max-RGB và Gray-Edge. Thước đo là sai số góc giữa vector ước lượng và vector suy từ thẻ, báo cáo theo trung bình, trung vị, tứ phân vị tốt nhất, tứ phân vị xấu nhất và phân vị thứ 95. Việc báo cáo cả tứ phân vị xấu nhất là cần thiết vì trong ứng dụng thực tế, các trường hợp chiếu sáng bất thường mới là nơi mô-đun có giá trị nhất.

Nếu mô-đun học không thắng được các phương pháp không học, kết quả đó vẫn được báo cáo nguyên trạng và phương pháp không học tốt nhất sẽ được dùng trong quy trình cuối cùng. Với cỡ dữ liệu của một đề tài sinh viên, khả năng này không nhỏ và không được coi là thất bại.

## 3.6. Thiết kế đánh giá

Bốn phép đánh giá được báo cáo song song, thứ tự trình bày theo mức độ nghiêm ngặt tăng dần.

**Phép thứ nhất là đánh giá chia ngẫu nhiên theo ảnh.** Đây là phép mà phần lớn tài liệu đang dùng. Nhóm báo cáo phép này không phải để tuyên bố hiệu năng mà để định lượng mức lạc quan mà nó tạo ra, bằng cách so với phép thứ hai trên cùng dữ liệu và cùng mô hình.

**Phép thứ hai là đánh giá cùng nguồn, chia theo quả.** Đây là con số hiệu năng thấp nhất mà nhóm coi là có ý nghĩa để công bố.

**Phép thứ ba là đánh giá bỏ ra một nguồn.** Mô hình được huấn luyện trên toàn bộ các nguồn trừ một, rồi đánh giá trên nguồn bị bỏ ra, lặp lại cho từng nguồn. Chênh lệch giữa phép thứ hai và phép thứ ba là đại lượng mà Câu hỏi 2 hướng tới.

**Phép thứ tư là đánh giá theo chi phí bất đối xứng.** Hái sớm một bậc khiến quả chưa đạt hàm lượng chất rắn hòa tan và không bù lại được sau thu hoạch. Hái muộn một bậc khiến quả hao hụt khối lượng và nhăn vỏ trong vận chuyển. Hai loại sai không tương đương về thiệt hại, nên độ chính xác thông thường, vốn coi mọi sai sót là như nhau, không phản ánh đúng giá trị sử dụng của công cụ.

Nhóm xây dựng ma trận chi phí phản ánh cấu trúc này, tham vấn nông hộ và doanh nghiệp thu mua để đặt trọng số, rồi báo cáo chi phí kỳ vọng bên cạnh các chỉ số thông thường. Ma trận chi phí còn được dùng theo một cách thứ hai: thay vì chọn bậc có xác suất cao nhất, công cụ chọn bậc tối thiểu hóa chi phí kỳ vọng. Cách này làm công cụ tự lệch về phía an toàn khi lưỡng lự giữa hai bậc kề nhau, và chênh lệch giữa hai cách quyết định được báo cáo riêng. Ma trận và căn cứ đặt trọng số được trình bày ở Phụ lục 5.

Song song với bốn phép trên, thí nghiệm về chuẩn hóa màu được thực hiện bằng cách chạy toàn bộ quy trình ở **ba cấu hình**: không hiệu chỉnh màu; hiệu chỉnh theo thẻ chuẩn trong khung hình; và hiệu chỉnh theo nguồn sáng ước lượng bằng mô-đun ở mục 3.5.4. Chênh lệch giữa cấu hình thứ nhất và thứ hai là phần biến thiên giữa các nguồn có nguyên nhân từ chiếu sáng. Chênh lệch giữa cấu hình thứ hai và thứ ba là cái giá phải trả khi bỏ thẻ đi ở điều kiện triển khai thực tế. Phần còn lại sau khi trừ cả hai là khác biệt do giống và điều kiện canh tác, không xử lý được bằng chuẩn hóa màu.

Mỗi cấu hình được chạy với ba hạt giống ngẫu nhiên khác nhau, báo cáo trung bình kèm độ lệch chuẩn. Khoảng tin cậy 95 phần trăm của các chỉ số chính được ước lượng bằng bootstrap.

## 3.7. Chỉ số đánh giá và phương pháp xử lý số liệu

Các chỉ số đánh giá được phân bổ theo từng nhiệm vụ của ba giai đoạn nghiên cứu, trình bày ở Bảng 5. Số liệu chỉ tiêu hóa sinh giữa các bậc chín được xử lý bằng phân tích phương sai một yếu tố, so sánh trung bình theo trắc nghiệm Tukey ở mức ý nghĩa p < 0,05. Tương quan giữa bậc chín dự đoán và TSS được đánh giá bằng hệ số xác định, sai số RMSE và phân tích tương hợp Bland-Altman (Bland và Altman, 1986). Toàn bộ xử lý thống kê thực hiện trên phần mềm R; phần xử lý ảnh và huấn luyện mô hình thực hiện bằng Python.

**Bảng 5.** Các chỉ số đánh giá theo từng nhiệm vụ.

| **Giai đoạn** | **Nhiệm vụ** | **Chỉ số đánh giá** |
| --- | --- | --- |
| Giai đoạn một | Chất lượng tập gán nhãn | Hệ số Kappa có trọng số bậc giữa hai người gán nhãn; tỷ lệ lệch quá một bậc |
| Giai đoạn một | Tiền xử lý ảnh | Tỷ lệ ảnh đọc được thẻ; tỷ lệ ảnh tách nền thành công; sai lệch tỷ lệ vỏ chuyển màu giữa đo trực quan và tính từ ảnh |
| Giai đoạn một | Chất lượng hiệu chỉnh màu | Sai số góc của nguồn sáng trước và sau hiệu chỉnh; mức tuyến tính của đáp ứng máy ảnh |
| Giai đoạn một | Chuẩn tham chiếu hóa sinh | TSS, TA, tỷ số TSS/TA và khối lượng theo từng bậc nhãn; phân tích phương sai giữa các bậc |
| Giai đoạn hai | Phân loại giai đoạn chín | Độ chính xác, F1 trung bình theo lớp, ma trận nhầm lẫn, sai số trung bình theo bậc, Kappa có trọng số bậc |
| Giai đoạn hai | Phân loại tình trạng quả | Độ nhạy, độ chính xác dương tính, F1 của lớp hỏng, AUC-PR, ngưỡng vận hành |
| Giai đoạn hai | Ước lượng nguồn sáng | Sai số góc theo trung bình, trung vị, tứ phân vị tốt nhất và xấu nhất, phân vị 95 |
| Giai đoạn hai | Khả năng triển khai | Thời gian suy luận mỗi ảnh, số tham số mô hình, khả năng chạy trên điện thoại |
| Giai đoạn ba | Ảnh hưởng của phép chia tập | Chênh lệch F1 giữa chia ngẫu nhiên theo ảnh và chia theo quả |
| Giai đoạn ba | Khả năng tổng quát | Chênh lệch F1 giữa đánh giá cùng nguồn và bỏ ra một nguồn, báo cáo cho từng nguồn |
| Giai đoạn ba | Vai trò của chuẩn hóa màu | Chênh lệch F1 giữa ba cấu hình chuẩn hóa màu |
| Giai đoạn ba | Tương hợp với chuẩn tham chiếu | Hệ số xác định và RMSE giữa bậc dự đoán và TSS; phân tích Bland-Altman |
| Giai đoạn ba | So với con người | Độ chính xác của mô hình và của người gán nhãn trên cùng tập, cùng chuẩn tham chiếu |
| Giai đoạn ba | Độ tin cậy của đầu ra | Sai số hiệu chuẩn kỳ vọng; đường đánh đổi giữa tỷ lệ từ chối trả lời và độ chính xác |
| Giai đoạn ba | Chi phí quyết định | Chi phí kỳ vọng theo ma trận bất đối xứng; tỷ lệ hái sớm và hái muộn tách riêng |
# 4. KẾT QUẢ - THẢO LUẬN

## 4.1. Đặc điểm nguồn thu mẫu và thống kê mô tả bộ dữ liệu

Nhóm thu mẫu từ […] nguồn có xuất xứ khác nhau, đặc điểm chi tiết trình bày ở Bảng 2. Tổng số ảnh thu được là […] trên […] quả riêng biệt, qua […] đợt thu mẫu từ ngày […] đến ngày […].

Sau khi loại các ảnh không đạt yêu cầu về độ nét, về vị trí thẻ chuẩn hoặc về mức độ bị che khuất, bộ dữ liệu còn […] ảnh trên […] quả. Tỷ lệ ảnh bị loại là […] phần trăm, nguyên nhân chính là […]. Bước đọc thẻ chuẩn thành công trên […] phần trăm số ảnh, và bước tách nền ở mục 3.4.3 thành công trên […] phần trăm; các trường hợp thất bại tập trung ở […].

Về chất lượng hiệu chỉnh màu, trên đợt thu mẫu ngày 14 tháng 8 năm 2026, nguồn sáng suy từ bốn ô xám lệch trung bình 5,28 độ so với trung tính trước hiệu chỉnh, tương ứng tỷ số giữa kênh đỏ và kênh lục xấp xỉ 1,13, và giảm còn 0,07 độ sau hiệu chỉnh. Con số này có ý nghĩa trực tiếp với bài toán: mức ám màu 13 phần trăm trên kênh đỏ đội thẳng vào giá trị a\*, chính là đại lượng dùng để tính tỷ lệ vỏ chuyển màu ở mục 3.4.4. Nói cách khác, ảnh chưa hiệu chỉnh làm quả biểu hiện chín hơn thực tế một cách có hệ thống. Kết quả đầy đủ trên toàn bộ các đợt thu mẫu trình bày ở […].

Cũng cần ghi nhận một đặc điểm của dữ liệu ảnh hưởng tới mục 4.5: trong phạm vi một đợt chụp có khóa cố định thông số máy, độ phân tán của nguồn sáng giữa các ảnh dưới 0,1 độ. Nghĩa là biến thiên chiếu sáng của bộ dữ liệu nằm giữa các đợt chụp chứ không nằm trong một đợt, và số điểm dữ liệu thực tế cho tầng ước lượng nguồn sáng bằng số đợt chụp chứ không bằng số ảnh. Đây là căn cứ cho việc bố trí các đợt chụp bổ sung ở nhiều khung giờ và nhiều loại nguồn sáng.

Phân bố số quả theo bậc chín và theo nguồn trình bày ở Bảng 7. Điểm cần lưu ý khi diễn giải các kết quả tiếp theo là […], vì sàn số quả mỗi bậc mỗi nguồn đặt ra ở mục 3.4.7 […] ở […] tổ hợp bậc và nguồn.

**Bảng 6.** Thống kê mô tả bộ dữ liệu sau làm sạch.

| **Chỉ tiêu** | **Giá trị** | **Ghi chú** |
| --- | --- | --- |
| Số nguồn thu mẫu |  |  |
| Số đợt thu mẫu |  |  |
| Tổng số ảnh thu được |  |  |
| Số ảnh bị loại |  | tỷ lệ và nguyên nhân chính |
| Số ảnh đọc được thẻ chuẩn |  | tỷ lệ trên tổng số ảnh |
| Số ảnh tách nền thành công |  | tỷ lệ trên tổng số ảnh |
| Số ảnh sau làm sạch |  |  |
| Số quả riêng biệt |  | đây là cỡ mẫu thống kê của nghiên cứu |
| Số ảnh trung bình mỗi quả |  |  |
| Số quả nhãn dùng được / nhãn hỏng |  |  |
| Số quả có đo chỉ tiêu hóa sinh |  |  |
| Số người tham gia gán nhãn |  |  |
| Khoảng TSS quan sát được (°Brix) |  | giá trị nhỏ nhất và lớn nhất |

**Bảng 7.** Phân bố số quả theo bậc chín và theo nguồn.

| **Nguồn** | **Bậc 1** | **Bậc 2** | **Bậc 3** | **Bậc 4** | **Bậc 5** | **Hỏng** |
| --- | --- | --- | --- | --- | --- | --- |
| N1 |  |  |  |  |  |  |
| N2 |  |  |  |  |  |  |
| N3 |  |  |  |  |  |  |
| N4 |  |  |  |  |  |  |
| Tổng |  |  |  |  |  |  |

## 4.2. Đồng thuận gán nhãn và chỉ tiêu hóa sinh theo bậc chín

Hệ số Kappa có trọng số bậc giữa hai người gán nhãn là […] trên phần chồng lấn gồm […] ảnh, tương ứng mức đồng thuận […]. Tỷ lệ trường hợp lệch quá một bậc là […] phần trăm. Các bậc gây bất đồng nhiều nhất là […], phù hợp với kỳ vọng vì ranh giới giữa hai bậc này là ranh giới liên tục.

Giá trị Kappa này là trần hiệu năng của bài toán. Mô hình đạt mức tương đồng với nhãn tham chiếu ngang với mức mà hai người đạt được với nhau thì không còn dư địa cải thiện có ý nghĩa, và các so sánh ở mục 4.3 và 4.4 phải được đọc trong tương quan với trần này. Một mô hình báo cáo mức tương đồng cao hơn hẳn trần này là dấu hiệu của rò rỉ dữ liệu chứ không phải dấu hiệu của chất lượng.

Tỷ lệ vỏ chuyển màu tính từ ảnh sau tách nền sai lệch trung bình […] điểm phần trăm so với ước lượng trực quan, với hệ số tương quan […]. Mức sai lệch này […] cho phép dùng giá trị tính từ ảnh thay cho ước lượng trực quan trong các bước sau.

TSS đo trên […] quả cho giá trị trung bình tăng theo bậc chín, từ […] °Brix ở bậc 1 tới […] °Brix ở bậc 5, chi tiết ở Bảng 8 và Hình 5. Phân tích phương sai cho thấy khác biệt giữa các bậc […] ý nghĩa thống kê (p = […]). Chiều biến thiên này phù hợp với quy luật đã ghi nhận trên cùng đối tượng, trong đó TSS tăng và TA giảm theo tiến trình chín (Pongener và cs, 2014), qua đó […] việc sơ đồ nhãn thị giác ở mục 3.4.4 phản ánh một biến thiên sinh lý thực.

**Bảng 8.** Chỉ tiêu hóa sinh theo bậc chín.

| **Bậc** | **Số quả** | **TSS (°Brix)** | **TA (%)** | **Tỷ số TSS/TA** | **Khối lượng (g)** |
| --- | --- | --- | --- | --- | --- |
| 1 |  |  |  |  |  |
| 2 |  |  |  |  |  |
| 3 |  |  |  |  |  |
| 4 |  |  |  |  |  |
| 5 |  |  |  |  |  |

*Ghi chú: giá trị trình bày là trung bình kèm độ lệch chuẩn. Các số trung bình trong cùng một cột mang chữ cái khác nhau thì khác biệt có ý nghĩa ở mức p < 0,05 theo trắc nghiệm Tukey. Cột TA và TSS/TA chỉ điền nếu đo đủ mẫu theo điều kiện nêu ở mục 3.4.6.*

*[Chèn biểu đồ hộp phân bố TSS theo bậc chín]*

**Hình 5.** Hàm lượng chất rắn hòa tan tổng số theo bậc chín. Các chữ cái khác nhau chỉ sự khác biệt có ý nghĩa ở mức p < 0,05.

## 4.3. So sánh các phương pháp trong đánh giá cùng nguồn

### 4.3.1. Ảnh hưởng của phép chia tập

Trước khi trình bày kết quả so sánh giữa các phương pháp, cần báo cáo một kết quả về chính thiết kế đánh giá, vì nó quyết định cách đọc mọi con số phía sau.

Cùng một mô hình, cùng một bộ dữ liệu, chỉ đổi cách chia tập kiểm tra, cho hai con số khác nhau đáng kể. Với phép chia ngẫu nhiên theo ảnh, mô hình đạt F1 trung bình theo lớp […]. Với phép chia theo quả trên cùng dữ liệu, con số là […]. Chênh lệch […] điểm.

Nguyên nhân của chênh lệch này đã nêu ở mục 3.4.8: khi chia ngẫu nhiên theo ảnh, các ảnh chụp cùng một quả ở những tư thế xoay khác nhau bị phân về cả hai tập, nên mô hình có thể trả lời đúng bằng cách nhận diện đặc điểm riêng của từng quả thay vì học quy luật về độ chín.

Kết quả này có ba hệ quả. Thứ nhất, con số theo phép chia ngẫu nhiên không được dùng để công bố hiệu năng, và mọi phát biểu về hiệu năng trong báo cáo này đều dựa trên phép chia theo quả trở lên. Thứ hai, nó cung cấp một ước lượng định lượng cho mức lạc quan mà thiết kế đánh giá phổ biến tạo ra trên chính đối tượng chanh dây, bổ sung cho quan sát định tính ở mục 2.5. Thứ ba, nó cho thấy việc ghi mã định danh quả trong khung hình, một thao tác tốn không đáng kể thời gian khi thu mẫu, là điều kiện cần để có được con số đáng tin.

### 4.3.2. So sánh giữa các phương pháp

Bảng 9a trình bày kết quả của các cấu hình trong phép đánh giá cùng nguồn, chia theo quả. Đường cơ sở màu đạt điểm F1 trung bình theo lớp […], phản ánh mức sàn của phương pháp chỉ dùng thống kê màu. Mô hình học sâu tốt nhất là […] đạt […], cao hơn đường cơ sở […] điểm.

Mức chênh lệch này có ý nghĩa riêng. Chênh lệch nhỏ cho thấy phần lớn thông tin về độ chín nằm ở thống kê màu toàn cục, và việc dùng mô hình học sâu chỉ được biện minh bởi khả năng chống chịu với nhiễu nền. Chênh lệch lớn cho thấy thông tin về độ chín không quy về được thống kê màu toàn cục mà nằm ở phân bố không gian của vùng chuyển màu trên bề mặt quả, tức ở kiểu hình phân bố sắc tố chứ không chỉ ở hàm lượng sắc tố.

Phân tích tầm quan trọng của các đặc trưng trong đường cơ sở cho thấy đặc trưng đóng góp nhiều nhất là […]. Việc đặc trưng này […] trùng với đại lượng mà sơ đồ nhãn ở Bảng 3 dùng để định nghĩa các bậc, tức […].

Ma trận nhầm lẫn ở Hình 6 cho thấy sai sót tập trung ở […], trùng với các cặp bậc gây bất đồng nhiều nhất giữa hai người gán nhãn ở mục 4.2. Sự trùng khớp này […] cách hiểu rằng phần lớn sai sót còn lại đến từ tính liên tục của bản thân quá trình chuyển màu chứ không từ hạn chế của mô hình.

Về chi phí triển khai, cấu hình tốt nhất có […] tham số, xử lý trung bình […] mili giây mỗi ảnh trên […], và […] chạy được trên điện thoại phổ thông sau khi chuyển đổi. Kết quả này […] Giả thuyết 1.

**Bảng 9a.** Kết quả phân loại độ chín trong đánh giá cùng nguồn.

| **Phương pháp** | **Độ chính xác** | **F1 theo lớp** | **Kappa trọng số bậc** | **Sai số TB theo bậc** | **Số tham số** | **Mili giây mỗi ảnh** |
| --- | --- | --- | --- | --- | --- | --- |
| Đường cơ sở màu |  |  |  |  |  |  |
| Học sâu, cấu hình 1 |  |  |  |  |  |  |
| Học sâu, cấu hình 2 |  |  |  |  |  |  |
| Người gán nhãn trong nhóm |  |  |  |  | không áp dụng | không áp dụng |
| Người thu hái có kinh nghiệm |  |  |  |  | không áp dụng | không áp dụng |

*Ghi chú: kết quả của mỗi cấu hình mô hình là trung bình của ba lần chạy với ba hạt giống ngẫu nhiên, độ lệch chuẩn đặt trong ngoặc. Cấu hình cho điểm F1 cao nhất được in đậm. Hai dòng cuối không có bước huấn luyện nên tính trên cùng tập ảnh tương ứng.*

*[Chèn ma trận nhầm lẫn của mô hình tốt nhất]*

**Hình 6.** Ma trận nhầm lẫn của mô hình tốt nhất trong đánh giá bỏ ra một nguồn.

### 4.3.3. Kết quả phân loại tình trạng quả

Đầu ra thứ hai đạt độ nhạy […] với lớp hỏng ở ngưỡng vận hành đã chọn, độ chính xác dương tính […], và diện tích dưới đường cong độ chính xác dương tính và độ nhạy là […]. Chi tiết ở Bảng 9b.

Đặc trưng phân biệt quả hỏng rõ nhất là […]. Kết quả này […] kỳ vọng, vì các biểu hiện hư hỏng chủ yếu gồm vùng nâu sẫm do thối, vùng nhăn làm thay đổi kết cấu bề mặt, và các vết nấm có sắc độ khác biệt rõ so với vỏ lành.

Ý nghĩa thực tiễn của đầu ra này nằm ở chỗ nó loại bỏ được dạng sai sót nêu ở hạn chế thứ tư mục 2.5. Khi kiểm tra mô hình phân loại độ chín năm lớp trên tập quả hỏng, mô hình gán […] phần trăm số quả đó vào bậc […] với độ tin cậy trung bình […], tức đưa ra kết luận sai theo hướng gây thiệt hại mà không có dấu hiệu cảnh báo. Với kiến trúc hai đầu ra, các quả này được chặn lại trước khi bước phân loại độ chín được thực hiện.

**Bảng 9b.** Kết quả phân loại tình trạng quả.

| **Chỉ số** | **Giá trị** |
| --- | --- |
| Số quả trong tập kiểm tra |  |
| Độ chính xác chung |  |
| Độ nhạy với lớp hỏng |  |
| Độ chính xác dương tính với lớp hỏng |  |
| F1 của lớp hỏng |  |
| AUC-PR |  |
| Ngưỡng vận hành đã chọn |  |

### 4.3.4. Hiệu chuẩn độ tin cậy và cơ chế từ chối trả lời

Sai số hiệu chuẩn kỳ vọng của mô hình tốt nhất là […], nghĩa là độ tin cậy mà mô hình báo […] phản ánh xác suất đúng thực tế. Điều này quyết định việc ngưỡng từ chối trả lời có đặt được một cách có ý nghĩa hay không.

Đường đánh đổi giữa tỷ lệ từ chối và độ chính xác trên phần đã trả lời trình bày ở Hình 7. Ở điểm vận hành đề xuất, công cụ từ chối trả lời […] phần trăm số ca và đạt độ chính xác […] trên phần còn lại. So với việc trả lời toàn bộ với độ chính xác […], đây là đánh đổi […] trong bối cảnh sử dụng thực tế, vì một câu trả lời "không xác định được" hướng người dùng sang kiểm tra thủ công, còn một câu trả lời sai thì không.

*[Chèn đường đánh đổi từ chối trả lời]*

**Hình 7.** Đường đánh đổi giữa tỷ lệ từ chối trả lời và độ chính xác trên phần đã trả lời.

## 4.4. Khả năng tổng quát sang nguồn mới và vai trò của chuẩn hóa màu

Bảng 10 trình bày kết quả đánh giá bỏ ra một nguồn, lặp lại cho từng nguồn, cùng kết quả của ba cấu hình chuẩn hóa màu.

Trong trường hợp tới thời điểm chốt số liệu chỉ thu được hai nguồn, mục này được báo cáo dưới dạng phân tích khám phá thay vì kết luận chính thức, theo phương án đã nêu trong đề cương: với hai nguồn, phép bỏ ra một nguồn chỉ cho hai phép thử nên chênh lệch quan sát được không tách bạch được khỏi dao động giữa các lần chạy. Giả thuyết 2 khi đó không được kết luận chấp nhận hay bác bỏ.

Điểm F1 trung bình theo lớp trong đánh giá bỏ ra một nguồn là […], so với […] trong đánh giá cùng nguồn, tức mức sụt giảm […] điểm. Ngưỡng 0,10 đặt ra trước cho Giả thuyết 2 vì vậy […], và Giả thuyết 2 […].

Mức sụt giảm không đồng đều giữa các nguồn. Nguồn […] cho mức sụt giảm lớn nhất là […] điểm, còn nguồn […] chỉ […] điểm. Đặc điểm phân biệt nguồn khó nhất với các nguồn còn lại là […], gợi ý rằng […].

Thí nghiệm ba cấu hình chuẩn hóa màu cho kết quả có ý nghĩa về mặt phương pháp. Khi bỏ bước hiệu chỉnh theo thẻ chuẩn, mức sụt giảm tăng từ […] lên […] điểm. Phần chênh lệch […] điểm là phần khác biệt giữa các nguồn có nguyên nhân từ điều kiện chiếu sáng, còn phần […] điểm còn lại đến từ khác biệt giống và điều kiện canh tác mà chuẩn hóa màu không xử lý được. Đây là căn cứ định lượng cho thấy […] rào cản triển khai giải quyết được bằng một biện pháp chi phí thấp ở khâu thu ảnh, phần còn lại đòi hỏi thu thêm dữ liệu từ nguồn mới.

So với đường tham chiếu con người ở mục 4.6, mức hiệu năng trong đánh giá bỏ ra một nguồn […] mức của người gán nhãn, điều này quyết định trực tiếp việc công cụ có triển khai được sang nguồn quả mới mà không cần huấn luyện lại hay không.

**Bảng 10.** Kết quả đánh giá bỏ ra một nguồn và vai trò của chuẩn hóa màu.

| **Nguồn bị bỏ ra** | **F1 cùng nguồn** | **F1 bỏ ra một nguồn, hiệu chỉnh theo thẻ** | **F1 bỏ ra một nguồn, hiệu chỉnh theo nguồn sáng ước lượng** | **F1 bỏ ra một nguồn, không hiệu chỉnh** | **Mức sụt giảm khi hiệu chỉnh theo thẻ** |
| --- | --- | --- | --- | --- | --- |
| N1 |  |  |  |  |  |
| N2 |  |  |  |  |  |
| N3 |  |  |  |  |  |
| N4 |  |  |  |  |  |
| Trung bình |  |  |  |  |  |

## 4.5. Ước lượng nguồn sáng môi trường

Bảng 11 trình bày sai số góc của mô-đun ước lượng nguồn sáng so với bốn phương pháp không cần dữ liệu huấn luyện, tất cả đối chiếu với giá trị suy từ thẻ chuẩn.

Phương pháp không học tốt nhất là […] với sai số góc trung vị […] độ. Mô-đun học từ thẻ đạt […] độ, tức […]. Giả thuyết 5 ở phần thứ nhất vì vậy […].

Điểm đáng chú ý nằm ở tứ phân vị xấu nhất. Ở nhóm 25 phần trăm ảnh khó nhất, sai số của các phương pháp không học tăng lên […] độ, trong khi mô-đun học đạt […] độ. Chênh lệch ở nhóm này lớn hơn chênh lệch ở giá trị trung vị, phù hợp với kỳ vọng rằng các phương pháp dựa trên giả định thống kê về cảnh sẽ thất bại đúng ở những cảnh vi phạm giả định đó, chẳng hạn khi trong khung hình có một vùng màu lớn chiếm ưu thế.

Về phần thứ hai của Giả thuyết 5, khi thay thẻ chuẩn bằng nguồn sáng ước lượng trong quy trình phân loại độ chín, điểm F1 trong đánh giá bỏ ra một nguồn giảm […] điểm so với cấu hình dùng thẻ. Ngưỡng 0,05 vì vậy […]. Diễn giải thực tiễn: […].

Hạn chế của phần này là độ đa dạng chiếu sáng của bộ dữ liệu, như đã nêu ở mục 4.1. Mô-đun chỉ được kiểm chứng trên […] điều kiện chiếu sáng khác nhau, nên các phát biểu về khả năng tổng quát sang điều kiện chiếu sáng mới giới hạn trong phạm vi đã khảo sát.

**Bảng 11.** Sai số của các phương pháp ước lượng nguồn sáng.

| **Phương pháp** | **Trung bình (độ)** | **Trung vị (độ)** | **Tứ phân vị tốt nhất** | **Tứ phân vị xấu nhất** | **Phân vị 95** |
| --- | --- | --- | --- | --- | --- |
| Không hiệu chỉnh |  |  |  |  |  |
| Gray-World |  |  |  |  |  |
| Shades-of-Gray |  |  |  |  |  |
| Max-RGB |  |  |  |  |  |
| Gray-Edge |  |  |  |  |  |
| Mô-đun học từ thẻ chuẩn |  |  |  |  |  |

## 4.6. Đối chiếu với chuẩn tham chiếu hóa sinh và so sánh với phán đoán của con người

Bậc chín dự đoán từ ảnh giải thích được […] phần biến thiên của TSS trên tập […] quả có đo hóa sinh, với RMSE bằng […] °Brix. Ngưỡng 0,60 đặt ra trước cho Giả thuyết 3 vì vậy […].

Phân tích tương hợp Bland-Altman (Bland và Altman, 1986) giữa TSS dự báo từ bậc chín và TSS đo trực tiếp cho độ chệch trung bình […] với khoảng đồng thuận 95 phần trăm từ […] đến […]. Độ chệch […] phụ thuộc vào độ lớn của giá trị đo, với hệ số hồi quy của độ chệch theo giá trị trung bình là […]. Phân tích này cần thiết bên cạnh hệ số xác định, vì hai phương pháp đo có thể tương quan chặt mà vẫn lệch nhau một cách có hệ thống.

Về so sánh với con người, khi cùng đối chiếu với chuẩn tham chiếu hóa sinh trên tập quả có đo hóa sinh, mô hình đạt độ chính xác […], người gán nhãn trong nhóm đạt […], và người thu hái có kinh nghiệm đạt […]. Giả thuyết 4 vì vậy […].

Kết quả này trả lời câu hỏi đặt ra ở mục 2.5 về bản chất của nhãn. Mô hình sát với người gán nhãn hơn là với chuẩn tham chiếu hóa sinh thì nó chủ yếu tái tạo phán đoán thị giác kể cả sai lệch có hệ thống của phán đoán đó; mô hình sát với chuẩn tham chiếu hơn thì nó đã nắm được tín hiệu vượt ra ngoài quy ước gán nhãn, tức là các đặc trưng ảnh có tương quan với tiến trình tích lũy đường chứ không chỉ với tiến trình chuyển màu.

## 4.7. Đánh giá theo chi phí bất đối xứng của quyết định thu hoạch

Ma trận chi phí được xây dựng trên cơ sở tham vấn […] nông hộ và […] đại diện doanh nghiệp thu mua, chi tiết ở Phụ lục 5. Nguyên tắc đặt trọng số là chi phí của việc hái muộn một bậc lớn hơn chi phí của việc hái sớm một bậc, vì quả hái muộn có nguy cơ bị loại khỏi lô xuất khẩu do hao hụt khối lượng và nhăn vỏ trong vận chuyển, trong khi quả hái sớm vẫn tiêu thụ được ở thị trường trong nước với giá thấp hơn.

Theo thang chi phí này, mô hình tốt nhất có chi phí kỳ vọng […] trên mỗi quyết định, so với […] của đường cơ sở màu và […] của người thu hái có kinh nghiệm. Thứ hạng của các phương pháp theo chi phí kỳ vọng […] với thứ hạng theo độ chính xác thông thường. Hai thứ hạng không trùng nhau cho thấy độ chính xác không phải thước đo phù hợp cho bài toán này, vì nó coi mọi sai sót là như nhau.

Khi chuyển từ quy tắc chọn bậc có xác suất cao nhất sang quy tắc chọn bậc tối thiểu hóa chi phí kỳ vọng, chi phí kỳ vọng giảm từ […] xuống […], trong khi độ chính xác thông thường giảm từ […] xuống […]. Đây là minh họa cụ thể cho việc hai mục tiêu này không trùng nhau: công cụ tối ưu theo chi phí sẽ chấp nhận sai nhiều hơn về số lượng để sai ít hơn về giá trị thiệt hại.

Phân tách theo loại sai, mô hình hái sớm ở […] phần trăm trường hợp và hái muộn ở […] phần trăm. Xu hướng lệch về phía […] là xu hướng […] trong bối cảnh xuất khẩu.

**Bảng 12.** Ma trận chi phí bất đối xứng và chi phí kỳ vọng của từng phương pháp.

| **Phương pháp** | **Tỷ lệ dự đoán đúng bậc** | **Tỷ lệ hái sớm** | **Tỷ lệ hái muộn** | **Chi phí kỳ vọng** |
| --- | --- | --- | --- | --- |
| Đường cơ sở màu |  |  |  |  |
| Mô hình học sâu tốt nhất |  |  |  |  |
| Mô hình học sâu, quyết định theo chi phí |  |  |  |  |
| Người gán nhãn trong nhóm |  |  |  |  |
| Người thu hái có kinh nghiệm |  |  |  |  |

## 4.8. Thảo luận chung và hạn chế của nghiên cứu

So với các công trình phân loại độ chín quả báo cáo độ chính xác trên chín mươi phần trăm trong điều kiện chia tập ngẫu nhiên, trong đó Tu và cs (2018) đạt 91,52% trên chính đối tượng chanh dây, kết quả cùng nguồn của nghiên cứu này là […], tức […]. Phép so sánh có ý nghĩa hơn là giữa kết quả bỏ ra một nguồn của nghiên cứu này, ở mức […], với chính các con số trên. Chênh lệch […] điểm cho thấy […], và củng cố nhận định ở mục 2.4 rằng thiết kế chia tập ngẫu nhiên báo cáo một con số lạc quan hơn hiệu năng triển khai thực tế, tương tự hiện tượng Mohanty và cs (2016) ghi nhận khi độ chính xác giảm từ 99,35% xuống 31,4% ở điều kiện thu ảnh khác.

Kết quả ở mục 4.3.1 củng cố nhận định này bằng một phép đo trực tiếp trên chính bộ dữ liệu của đề tài, thay vì suy luận gián tiếp từ công trình khác.

### 4.8.1. Hạn chế của nghiên cứu

Tám hạn chế dưới đây mang tính cấu trúc và được nêu rõ trong báo cáo.

**Thứ nhất**, thiết kế chủ yếu là lấy mẫu cắt ngang qua nhiều nguồn tại một thời điểm. Nghiên cứu vì vậy trả lời được câu hỏi quả đang ở giai đoạn chín nào, nhưng chưa trả lời được câu hỏi còn bao nhiêu ngày nữa tới thời điểm hái. Phần theo dõi ở mục 3.4.9 có cỡ mẫu nhỏ và chỉ mang tính khám phá.

**Thứ hai**, số nguồn thu mẫu nhỏ và xuất xứ của phần lớn nguồn do người bán khai báo chứ không kiểm chứng được tại vườn. Phép đánh giá bỏ ra một nguồn với […] nguồn cho […] phép thử, đủ để phát hiện hiện tượng sụt giảm nhưng không đủ để ước lượng chính xác mức sụt giảm kỳ vọng khi triển khai đại trà. Nếu hai nguồn vô tình có cùng nguồn gốc thì mức sụt giảm đo được sẽ thấp hơn thực tế. Các phát biểu về khả năng tổng quát vì vậy giới hạn trong phạm vi các nguồn đã khảo sát.

**Thứ ba**, toàn bộ dữ liệu thu trong một cửa sổ thời gian ngắn của một mùa vụ. Biến thiên giữa các mùa vụ và giữa các năm, vốn có thể lớn do khác biệt về thời tiết và chế độ canh tác, nằm ngoài phạm vi nghiên cứu.

**Thứ tư**, màu vỏ là biểu hiện bên ngoài, không phải chất lượng ăn được. Việc đối chiếu với TSS thu hẹp khoảng cách này nhưng không xóa bỏ nó, vì TSS chỉ là một trong nhiều yếu tố cấu thành chất lượng cảm quan; các hợp chất bay hơi tạo hương không được khảo sát. Nghiên cứu không đưa ra kết luận nào về hương vị.

**Thứ năm**, đề tài không có đóng góp về kiến trúc mô hình. Các mô hình sử dụng đều là mô hình có sẵn. Đóng góp nằm ở bộ dữ liệu, thiết kế đánh giá, chuẩn tham chiếu hóa sinh, mô-đun ước lượng nguồn sáng và khung chi phí.

**Thứ sáu**, thẻ chuẩn sử dụng chỉ gồm các ô xám trung tính. Loại thẻ này cho phép hiệu chỉnh cân bằng trắng, tức ba hệ số co giãn theo kênh, nhưng không cho phép hiệu chỉnh màu đầy đủ vốn đòi hỏi một ma trận biến đổi ba nhân ba ước lượng từ các ô có sắc độ khác nhau. Berry và cs (2018), nguồn được kế thừa ở mục 2.3, sử dụng bảng màu 24 ô. Sai lệch màu còn lại sau hiệu chỉnh vì vậy chưa được khử hoàn toàn, và mức độ ảnh hưởng của phần dư này chưa được định lượng.

**Thứ bảy**, ảnh được chụp trên quả đã hái chứ không phải trên quả còn trên giàn. Nghiên cứu vì vậy chưa bao được hai yếu tố của điều kiện sử dụng cuối cùng là quả bị lá che một phần và nền là tán cây. Chế độ chụp ảnh bối cảnh ngoài trời thu hẹp khoảng cách này, nhưng phần chênh lệch còn lại là một giới hạn chưa đo được và là nội dung đầu tiên cần bổ sung khi tiếp cận được vườn.

**Thứ tám**, mô-đun ước lượng nguồn sáng được kiểm chứng trên số điều kiện chiếu sáng hạn chế, như đã nêu ở mục 4.5. Với cấu hình chụp khóa cố định thông số máy, biến thiên chiếu sáng nằm giữa các đợt chụp chứ không nằm trong một đợt, nên số điểm dữ liệu độc lập cho phần này bằng số đợt chụp. Đây là điểm cần khắc phục bằng cách bố trí thêm các đợt chụp ở nhiều khung giờ và nhiều loại nguồn sáng, chứ không bằng cách tăng số ảnh trong một đợt.

# 5. KẾT LUẬN - KIẾN NGHỊ

## 5.1. Kết luận

Nghiên cứu đã xây dựng và kiểm chứng quy trình xác định giai đoạn chín và tình trạng sử dụng của quả chanh dây từ ảnh số, với bộ dữ liệu cuối cùng gồm […] ảnh trên […] quả riêng biệt thu từ […] nguồn có xuất xứ khác nhau.

Trả lời **Câu hỏi 1**, cấu hình […] cho kết quả tốt nhất trong đánh giá cùng nguồn chia theo quả với điểm F1 […], cao hơn đường cơ sở màu […] điểm. Ảnh số […] đủ thông tin để phân loại giai đoạn chín ở mức dùng được.

Trả lời **Câu hỏi 2**, trong đánh giá bỏ ra một nguồn, điểm F1 giảm […] điểm xuống còn […]. Ngưỡng 0,10 đặt ra trước cho Giả thuyết 2 vì vậy […]. Trong mức sụt giảm đó, […] điểm quy được cho khác biệt về điều kiện chiếu sáng và xử lý được bằng chuẩn hóa màu, […] điểm còn lại đến từ khác biệt giống và điều kiện canh tác giữa các nguồn.

Trả lời **Câu hỏi 3**, bậc chín dự đoán từ ảnh giải thích […] phần biến thiên của TSS, với độ chệch Bland-Altman […]. Mô hình vì vậy […] nắm được tín hiệu sinh lý vượt ra ngoài quy ước gán nhãn thị giác.

Trả lời **Câu hỏi 4**, mô hình đạt độ chính xác […] so với […] của người thu hái có kinh nghiệm khi cùng đối chiếu chuẩn tham chiếu hóa sinh.

Trả lời **Câu hỏi 5**, mô-đun ước lượng nguồn sáng học từ thẻ chuẩn đạt sai số góc trung vị […] độ, so với […] độ của phương pháp không học tốt nhất. Khi dùng mô-đun thay cho thẻ trong quy trình phân loại, điểm F1 giảm […] điểm, nên Giả thuyết 5 […].

Ngoài năm câu hỏi trên, nghiên cứu ghi nhận một kết quả về chính thiết kế đánh giá: trên cùng dữ liệu và cùng mô hình, phép chia tập ngẫu nhiên theo ảnh cho điểm F1 cao hơn phép chia theo quả […] điểm. Con số này định lượng mức lạc quan mà thiết kế đánh giá phổ biến tạo ra trên đối tượng chanh dây.

Về đóng góp mới, nghiên cứu tạo ra bộ dữ liệu ảnh độ chín chanh dây đa nguồn có gán nhãn công khai đầu tiên theo rà soát của nhóm, gồm […] ảnh có mã định danh từng quả kèm hệ số Kappa có trọng số ở mức […]; cung cấp con số định lượng về mức sụt giảm hiệu năng khi chuyển sang nguồn quả mới; tách được phần nguyên nhân đến từ chiếu sáng bằng thí nghiệm ba cấu hình chuẩn hóa màu; đề xuất mô-đun ước lượng nguồn sáng học từ thẻ chuẩn và dùng được khi không có thẻ; tách tình trạng quả thành đầu ra độc lập kèm cơ chế từ chối trả lời; và đề xuất khung đánh giá theo chi phí bất đối xứng phù hợp với cấu trúc thiệt hại thực tế của quyết định thu hoạch.

## 5.2. Kiến nghị

### 5.2.1. Đề xuất cho các nghiên cứu tiếp theo

Quy trình có thể mở rộng theo năm hướng.

Hướng thứ nhất là mở rộng phần theo dõi theo thời gian trên các quả được gắn thẻ ngay từ khi còn trên giàn, để chuyển từ bài toán xác định giai đoạn chín sang bài toán dự báo số ngày còn lại tới thời điểm hái.

Hướng thứ hai là mở rộng số nguồn và số mùa vụ, để chuyển con số về khả năng tổng quát từ mức chỉ báo sang mức ước lượng đáng tin cậy.

Hướng thứ ba là bổ sung các chỉ tiêu hóa sinh ngoài TSS, gồm hàm lượng đường khử, hàm lượng axit ascorbic và các hợp chất bay hơi tạo hương, nhằm tiến tới dự báo chất lượng cảm quan.

Hướng thứ tư là thay thẻ ô xám bằng bảng màu chuẩn có ô sắc độ, cho phép hiệu chỉnh màu đầy đủ bằng ma trận biến đổi thay vì chỉ hiệu chỉnh cân bằng trắng, qua đó khắc phục hạn chế thứ sáu ở mục 4.8.1.

Hướng thứ năm là thử các kỹ thuật thích ứng miền, để giảm nhu cầu thu dữ liệu mới mỗi khi triển khai ở nguồn mới.

Ngoài ra, chênh lệch giữa mô hình và chuẩn tham chiếu hóa sinh ở mục 4.6 gợi mở một hướng riêng là xây dựng sơ đồ nhãn trực tiếp từ ngưỡng TSS và tỷ số TSS/TA thay vì từ quy ước thị giác, để mô hình học từ ranh giới có nội dung sinh lý ngay từ đầu.

### 5.2.2. Biện pháp ứng dụng kết quả vào thực tiễn

Đối với **nông hộ**, công cụ chạy trên điện thoại trả về giai đoạn chín và tình trạng quả giúp quyết định thu hoạch bớt phụ thuộc vào kinh nghiệm cá nhân. Giá trị lớn nhất nằm ở nhóm hộ mới chuyển sang trồng chanh dây và ở lao động thời vụ chưa quen quan sát màu vỏ, tức nhóm có chênh lệch lớn nhất so với người có kinh nghiệm.

Đối với **doanh nghiệp thu mua và xuất khẩu**, việc đánh giá độ chín một cách khách quan và lặp lại được là cơ sở để thống nhất tiêu chí nghiệm thu giữa doanh nghiệp và vùng trồng, giảm tranh chấp khi phân loại lô hàng, và ước lượng trước sản lượng đạt chuẩn của mỗi lứa.

Đối với **hợp tác xã và tổ hợp tác**, sơ đồ nhãn kèm ảnh minh họa ở Hình 3 tự nó là một công cụ tập huấn dùng được ngay, độc lập với phần mô hình, vì nó chuyển quy ước quan sát của người có kinh nghiệm thành tài liệu truyền đạt được.

Đối với **cơ quan quản lý chất lượng nông sản**, sơ đồ nhãn gắn với ngưỡng chỉ tiêu hóa sinh là bước đầu hướng tới một thang độ chín tham chiếu cho chanh dây, phục vụ chuẩn hóa yêu cầu chất lượng đối với hàng xuất khẩu theo nghị định thư đã ký.

### 5.2.3. Kiến nghị về cơ chế, chính sách

**Thứ nhất**, kiến nghị xây dựng thang phân loại độ chín tham chiếu cho chanh dây, có mô tả bằng ảnh và gắn với ngưỡng chỉ tiêu hóa sinh đo được, làm cơ sở chung cho việc nghiệm thu giữa vùng trồng và doanh nghiệp. Việc thiếu một thang chung hiện là nguyên nhân của phần lớn tranh chấp khi phân loại lô hàng.

**Thứ hai**, kiến nghị đưa nội dung xác định thời điểm thu hoạch vào chương trình tập huấn khuyến nông cho vùng trồng chanh dây, sử dụng tài liệu trực quan thay cho truyền đạt bằng kinh nghiệm, vì đây là khâu có tác động tới giá trị lô hàng lớn hơn nhiều so với chi phí tập huấn.

**Thứ ba**, kiến nghị khuyến khích công bố công khai các bộ dữ liệu ảnh nông sản có gán nhãn được tạo ra từ đề tài sử dụng ngân sách nhà nước. Rào cản lớn nhất của việc ứng dụng thị giác máy tính vào nông nghiệp trong nước hiện nay không phải là mô hình, vốn đã sẵn có và miễn phí, mà là dữ liệu có gán nhãn cho cây trồng bản địa.

**Thứ tư**, kiến nghị khi xây dựng các công cụ số hỗ trợ sản xuất nông nghiệp theo định hướng Nghị quyết số 57-NQ/TW, yêu cầu báo cáo hiệu năng trên vùng trồng chưa từng dùng để phát triển công cụ, thay vì chỉ báo cáo hiệu năng trên chính dữ liệu phát triển. Kết quả ở mục 4.3.1 và 4.4 cho thấy hai con số này có thể chênh lệch đáng kể.

**Thứ năm**, kiến nghị khi nghiệm thu các công cụ số dạng này, yêu cầu công bố kèm đơn vị quan sát thực tế của bộ dữ liệu, tức số cá thể chứ không chỉ số ảnh, và yêu cầu mô tả phép chia tập kiểm tra. Hai thông tin này quyết định mức tin cậy của con số hiệu năng công bố nhưng thường không được nêu.

# TÀI LIỆU THAM KHẢO

## A. Văn bản pháp quy

[1]. Ban Chấp hành Trung ương Đảng Cộng sản Việt Nam, Nghị quyết số 57-NQ/TW ngày 22/12/2024 của Bộ Chính trị về đột phá phát triển khoa học, công nghệ, đổi mới sáng tạo và chuyển đổi số quốc gia, Hà Nội, 2024.

[2]. Bộ Nông nghiệp và Môi trường Việt Nam và Tổng cục Hải quan Trung Quốc, Nghị định thư về yêu cầu kiểm dịch thực vật đối với quả chanh leo tươi (*Passiflora edulis*) xuất khẩu từ Việt Nam sang Trung Quốc, ký ngày 15/4/2025.

[3]. Cục Trồng trọt và Bảo vệ thực vật, Bộ Nông nghiệp và Môi trường, Báo cáo hiện trạng ngành hàng chanh leo Việt Nam, trình bày tại Diễn đàn "Phát triển ngành hàng chanh leo bền vững theo chuỗi liên kết", Gia Lai, ngày 12/12/2025.

## B. Sách, báo, tạp chí và bài viết của các tác giả

[4]. Arjona H. E. and Matta F. B., Postharvest quality of passion fruit as influenced by harvest time and ethylene treatment, HortScience 26 (10) (1991) 1297-1298.

[5]. Berry J. C., Fahlgren N., Pokorny A. A., Bart R. S., and Veley K. M., An automated, high-throughput method for standardizing image color profiles to improve image-based plant phenotyping, PeerJ 6 (2018) e5727. DOI: 10.7717/peerj.5727

[6]. Bland J. M. and Altman D. G., Statistical methods for assessing agreement between two methods of clinical measurement, The Lancet 327 (8476) (1986) 307-310.

[7]. Buchsbaum G., A spatial processor model for object colour perception, Journal of the Franklin Institute 310 (1) (1980) 1-26.

[8]. Cohen J., Weighted kappa: Nominal scale agreement with provision for scaled disagreement or partial credit, Psychological Bulletin 70 (4) (1968) 213-220.

[9]. Deng J., Dong W., Socher R., Li L.-J., Li K., and Fei-Fei L., ImageNet: A large-scale hierarchical image database, Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition, Miami, 2009, pp. 248-255.

[10]. Finlayson G. D. and Trezzi E., Shades of gray and colour constancy, Proceedings of the IS&T/SID Twelfth Color Imaging Conference, Scottsdale, 2004, pp. 37-41.

[11]. Furbank R. T. and Tester M., Phenomics - technologies to relieve the phenotyping bottleneck, Trends in Plant Science 16 (12) (2011) 635-644.

[12]. Gijsenij A., Gevers T., and van de Weijer J., Computational color constancy: Survey and experiments, IEEE Transactions on Image Processing 20 (9) (2011) 2475-2489.

[13]. Guo C., Pleiss G., Sun Y., and Weinberger K. Q., On calibration of modern neural networks, Proceedings of the 34th International Conference on Machine Learning, PMLR 70, Sydney, 2017, pp. 1321-1330.

[14]. He K., Zhang X., Ren S., and Sun J., Deep residual learning for image recognition, Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition, Las Vegas, 2016, pp. 770-778.

[15]. Li C., Xin M., Li L., He X., Liu G., Li J., Sheng J., and Sun J., Transcriptome profiling helps to elucidate the mechanisms of ripening and epidermal senescence in passion fruit (*Passiflora edulis* Sims), PLOS ONE 15 (9) (2020) e0236535. DOI: 10.1371/journal.pone.0236535

[16]. Li L., Zhang Q., and Huang D., A review of imaging techniques for plant phenotyping, Sensors 14 (11) (2014) 20078-20111.

[17]. Mohanty S. P., Hughes D. P., and Salathé M., Using deep learning for image-based plant disease detection, Frontiers in Plant Science 7 (2016) 1419. DOI: 10.3389/fpls.2016.01419

[18]. Pongener A., Sagar V., Pal R. K., Asrey R., Sharma R. R., and Singh S. K., Physiological and quality changes during postharvest ripening of purple passion fruit (*Passiflora edulis* Sims), Fruits 69 (1) (2014) 19-30.

[19]. Sandler M., Howard A., Zhu M., Zhmoginov A., and Chen L.-C., MobileNetV2: Inverted residuals and linear bottlenecks, Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition, Salt Lake City, 2018, pp. 4510-4520.

[20]. Shiomi S., Wamocho L. S., and Agong S. G., Ripening characteristics of purple passion fruit on and off the vine, Postharvest Biology and Technology 7 (1-2) (1996) 161-170.

[21]. Tan M. and Le Q. V., EfficientNet: Rethinking model scaling for convolutional neural networks, Proceedings of the 36th International Conference on Machine Learning, PMLR 97, Long Beach, 2019, pp. 6105-6114.

[22]. Tardieu F., Cabrera-Bosquet L., Pridmore T., and Bennett M., Plant phenomics, from sensors to knowledge, Current Biology 27 (15) (2017) R770-R783.

[23]. Tu S., Xue Y., Zheng C., Qi Y., Wan H., and Mao L., Detection of passion fruits and maturity classification using Red-Green-Blue Depth images, Biosystems Engineering 175 (2018) 156-167. DOI: 10.1016/j.biosystemseng.2018.09.004

[24]. van de Weijer J., Gevers T., and Gijsenij A., Edge-based color constancy, IEEE Transactions on Image Processing 16 (9) (2007) 2207-2214.

# PHỤ LỤC

Phụ lục 1. Hướng dẫn gán nhãn giai đoạn chín và tình trạng quả, kèm ảnh minh họa và các trường hợp ranh giới.

Phụ lục 2. Giao thức chụp ảnh, thông số thiết bị và nhật ký các đợt thu mẫu.

Phụ lục 3. Kết quả đánh giá độ đồng thuận giữa những người gán nhãn, tách theo từng cặp bậc.

Phụ lục 4. Tên và phiên bản mô hình, tham số huấn luyện, phép tăng cường dữ liệu và cấu hình phần cứng.

Phụ lục 5. Ma trận chi phí bất đối xứng và căn cứ đặt trọng số.

Phụ lục 6. Thiết kế thẻ chuẩn và quy trình hiệu chỉnh màu.

Phụ lục 7. Địa chỉ truy cập mã nguồn và bộ dữ liệu gán nhãn công bố kèm nghiên cứu.
