# CANNY EDGE DETECTOR

## I. Lý thuyết

### 1. Tìm hiểu về các bước của thuật toán Canny

a) Giải thích chi tiết từng bước:
- **Giảm nhiễu (Noise Reduction):** Vì phát hiện cạnh rất nhạy cảm với nhiễu, bước đầu tiên là làm mịn ảnh bằng cách sử dụng bộ lọc Gaussian (Gaussian filter) để loại bỏ các điểm ảnh nhiễu lẻ tẻ.
- **Tính toán Gradient:** Ảnh sau khi làm mịn sẽ được tính toán đạo hàm theo hai hướng (ngang và dọc) bằng toán tử Sobel. Từ đó tính ra được "độ lớn" (magnitude) và "hướng" (direction) của sự thay đổi màu sắc tại mỗi điểm ảnh.
- **Non-maximum suppression (Triệt tiêu phi cực đại):** Bước này giúp "làm mảnh" các đường cạnh. Thuật toán sẽ quét qua toàn bộ ảnh, kiểm tra xem điểm ảnh hiện tại có phải là điểm đạt giá trị gradient cực đại trong vùng lân cận (theo hướng gradient) hay không. Nếu không, điểm đó bị loại bỏ (đưa về 0).
- **Ngưỡng kép (Double Threshold):** Sử dụng hai ngưỡng: High Threshold (Ngưỡng cao) và Low Threshold (Ngưỡng thấp). Điểm ảnh có gradient > Ngưỡng cao được đánh dấu là "Cạnh mạnh". Điểm < Ngưỡng thấp bị loại bỏ. Điểm nằm giữa hai ngưỡng được gọi là "Cạnh yếu".
- **Theo dõi cạnh (Edge Tracking by Hysteresis):** Thuật toán quyết định giữ hay bỏ các "Cạnh yếu". Một "Cạnh yếu" chỉ được công nhận là cạnh thực sự nếu nó nằm kề cận và kết nối với một "Cạnh mạnh". Nếu đứng trơ trọi, nó sẽ bị loại bỏ.

b) So sánh với các thuật toán khác như:
- **Sobel:** Sobel chỉ đơn thuần tính toán đạo hàm bậc 1 để tìm sự thay đổi độ sáng. Kết quả đường cạnh của Sobel thường rất dày, nhiều nhiễu và đứt đoạn. Canny khắc phục được điều này nhờ bước làm mảnh (Non-maximum suppression) và nối cạnh (Hysteresis), cho ra đường cạnh sắc nét chỉ dày 1 pixel.
- **Laplacian:** Laplacian sử dụng đạo hàm bậc 2 để tìm điểm cắt không (zero-crossing). Dù tìm cạnh chính xác nhưng Laplacian cực kỳ nhạy cảm với nhiễu. Canny ổn định hơn rất nhiều nhờ tích hợp bộ lọc Gaussian ở bước đầu tiên.

---

### 2. Các tham số của thuật toán và ảnh hưởng của chúng

a) **Sigma trong Gaussian filter:** Tham số kiểm soát độ phân tán của hàm Gaussian (mức độ làm mờ). 
- Sigma lớn: Ảnh mờ nhiều, khử nhiễu tốt hơn, bỏ qua các chi tiết nhỏ/cạnh vụn vặt, nhưng có thể làm mờ/lệch vị trí cạnh chính.
- Sigma nhỏ: Ảnh ít mờ, bắt được nhiều chi tiết mảnh, nhưng dễ bị nhiễu đánh lừa.

b) **Ngưỡng thấp (Low threshold) và ngưỡng cao (High threshold):**
- **Ngưỡng cao (High):** Quyết định tính "khắt khe" khi chọn cạnh mạnh. Giá trị càng cao, số lượng cạnh mạnh giữ lại càng ít (chỉ giữ các đường nét cực rõ ràng).
- **Ngưỡng thấp (Low):** Quyết định sự "bao dung" đối với cạnh yếu. Giá trị quá thấp sẽ khiến nhiễu bị nhận diện nhầm thành cạnh (do nối vào cạnh mạnh). Tỷ lệ khuyến nghị giữa Ngưỡng cao : Ngưỡng thấp thường là 2:1 hoặc 3:1.

---

### 3. Ưu điểm và nhược điểm của Canny edge detector  

**Ưu điểm:**
- Phát hiện cạnh với tỷ lệ lỗi rất thấp (ít bỏ sót cạnh thật, ít nhận nhầm nhiễu thành cạnh).
- Định vị cạnh cực kỳ chính xác (đường cạnh mảnh 1 pixel nằm đúng vị trí).
- Các đường nét được kết nối liền mạch.

**Nhược điểm:**
- Tốc độ tính toán chậm hơn nhiều so với Sobel/Prewitt do phải trải qua 5 bước phức tạp.
- Khó cấu hình tự động (phải tinh chỉnh 2 tham số ngưỡng thủ công cho từng loại ảnh khác nhau).

a) So sánh với các thuật toán khác về:
- **Độ chính xác:** Cao nhất trong các thuật toán phát hiện cạnh cổ điển.
- **Tốc độ:** Chậm nhất (thua Sobel, Prewitt, Robert).
- **Khả năng xử lý nhiễu:** Rất xuất sắc nhờ bước lọc Gaussian tích hợp.

b) Trong lĩnh vực nào Canny được sử dụng phổ biến nhất?
Canny thường được dùng làm bước tiền xử lý (preprocessing) trong Computer Vision, chuẩn bị dữ liệu đầu vào sắc nét cho các mô hình cao cấp hơn.

c) Ví dụ cụ thể về các ứng dụng:
- **Xe tự lái:** Nhận diện vạch kẻ đường (Lane Detection) để cảnh báo chệch làn.
- **Y tế:** Phân tách ranh giới của khối u, mạch máu trên ảnh X-Quang/MRI.
- **Xử lý tài liệu:** Phát hiện góc cạnh của trang giấy để scan tài liệu (giống ứng dụng CamScanner).

---

## III. Các câu hỏi mở rộng

**1. Làm thế nào để đánh giá chất lượng của các cạnh được phát hiện bởi Canny?**
Có thể đánh giá bằng mắt thường (Qualitative) hoặc bằng các chỉ số toán học (Quantitative) nếu có dữ liệu gốc (Ground Truth) để so sánh. Các chỉ số thường dùng là Precision (Độ xác đáng), Recall (Độ bao phủ), F1-Score, hoặc các độ đo đặc thù như PSNR, SSIM.

**2. Có những phương pháp nào khác để cải thiện hiệu suất của Canny?**
- **Sử dụng Bilateral Filter thay thế Gaussian Filter:** Bilateral Filter giúp làm mờ ảnh để khử nhiễu nhưng vẫn giữ được độ sắc nét của cạnh, giúp Canny phát hiện chính xác hơn.
- **Auto-Canny:** Sử dụng thuật toán tự động tính toán Ngưỡng cao và Ngưỡng thấp dựa trên giá trị trung vị (Median) của toàn bộ điểm ảnh, giúp không phải cài đặt thông số thủ công.

**3. Canny có thể được sử dụng để phát hiện các cạnh trong ảnh màu không? Nếu có, thì như thế nào?**
Bản thân thuật toán Canny gốc chỉ áp dụng trên ảnh xám (1 kênh màu). Để áp dụng cho ảnh màu, có 2 cách:
- **Cách 1 (Phổ biến nhất):** Chuyển đổi ảnh màu (RGB) sang ảnh xám (Grayscale) trước khi áp dụng Canny.
- **Cách 2:** Tính toán Canny riêng biệt trên cả 3 kênh màu R, G, B, sau đó kết hợp các đường cạnh lại bằng phép toán logic OR.

**4. Làm thế nào để áp dụng Canny cho các video?**
Video thực chất là một chuỗi các khung hình (frames) liên tiếp. Để áp dụng Canny, ta sử dụng vòng lặp để đọc từng khung hình bằng `cv2.VideoCapture()`, chuyển đổi khung hình đó sang ảnh xám, áp dụng hàm `cv2.Canny()` và sau đó hiển thị (hoặc lưu) liên tục các khung hình đã xử lý tạo thành một video dạng viền.