# CANNY EDGE DETECTOR

## I. Lý thuyết

### 1. Tìm hiểu về các bước của thuật toán Canny
Canny Edge Detector là một thuật toán phát hiện cạnh (edge detection) phổ biến trong xử lý ảnh. Mục tiêu của thuật toán là xác định các đường biên của vật thể trong ảnh với độ chính xác cao và hạn chế nhiễu.Thuật toán gồm 5 bước chính:

#### 1. Giảm nhiễu (Noise Reduction)

Ảnh số thường chứa nhiễu do ánh sáng, cảm biến hoặc môi trường. Nhiễu có thể làm xuất hiện các cạnh giả, ảnh hưởng đến kết quả phát hiện cạnh.
Canny sử dụng Gaussian Blur để làm mượt ảnh trước khi tìm cạnh:
- Giảm ảnh hưởng của nhiễu
- Làm mượt sự thay đổi cường độ sáng
- Giữ lại cấu trúc chính của vật thể
Kernel Gaussian thường được sử dụng để tính giá trị pixel mới dựa trên các pixel lân cận, trong đó pixel gần trung tâm có trọng số cao hơn.
Ý nghĩa: giảm nhiễu để việc phát hiện cạnh chính xác hơn.

#### 2. Tính toán Gradient (Gradient Calculation)

Sau khi giảm nhiễu, thuật toán xác định vị trí có sự thay đổi mạnh về cường độ sáng vì đó thường là cạnh.
Gradient thể hiện mức độ thay đổi độ sáng giữa các pixel. Thường sử dụng toán tử Sobel để tính gradient theo hai hướng:
- Gx: thay đổi theo chiều ngang
- Gy: thay đổi theo chiều dọc
Độ mạnh cạnh được tính bằng công thức:
G = sqrt(Gx² + Gy²)
Hướng cạnh được xác định bằng:
θ = arctan(Gy / Gx)
Ý nghĩa:
- Gradient lớn → khả năng là cạnh cao
- Gradient nhỏ → vùng phẳng
#### 3. Non-maximum Suppression (Làm mỏng cạnh)

Sau khi tính gradient, các cạnh thường có độ dày lớn. Non-maximum suppression được sử dụng để làm mỏng cạnh.
Nguyên tắc hoạt động:
- So sánh gradient của pixel hiện tại với hai pixel lân cận theo hướng gradient
- Nếu pixel hiện tại không phải giá trị lớn nhất thì bị loại bỏ
Kết quả:
- cạnh trở nên mảnh hơn
- giữ lại các điểm có khả năng là cạnh thực sự
Ý nghĩa: xác định chính xác vị trí cạnh.
#### 4. Ngưỡng kép (Double Threshold)

Không phải tất cả các cạnh đều có độ rõ như nhau. Vì vậy Canny sử dụng hai ngưỡng:
- Ngưỡng cao (High threshold)
- Ngưỡng thấp (Low threshold)
Phân loại pixel:
- Strong edge: gradient ≥ ngưỡng cao
- Weak edge: gradient nằm giữa hai ngưỡng
- Non-edge: gradient < ngưỡng thấp
Ý nghĩa:
- Strong edge chắc chắn là cạnh
- Weak edge có thể là cạnh
- Non-edge bị loại bỏ

#### 5. Theo dõi cạnh (Edge Tracking by Hysteresis)

Ở bước trước, một số pixel được phân loại là weak edge. Tuy nhiên không phải tất cả weak edge đều là cạnh thật.
Thuật toán giữ lại weak edge nếu:
- weak edge nối với strong edge
Ngược lại, weak edge sẽ bị loại bỏ.
Ý nghĩa:
- đảm bảo cạnh liên tục
- loại bỏ cạnh giả do nhiễu

### Tóm tắt quy trình Canny

1. Gaussian Blur để giảm nhiễu
2. Tính gradient để tìm sự thay đổi độ sáng
3. Non-maximum suppression để làm mỏng cạnh
4. Double threshold để phân loại cạnh mạnh và yếu
5. Edge tracking để giữ lại cạnh thật

Canny là một trong những phương pháp phát hiện cạnh hiệu quả nhất vì:
- giảm nhiễu tốt
- xác định cạnh chính xác
- tạo đường biên mảnh và liên tục

Nhược điểm

---

### b) So sánh với các thuật toán khác như:

#### Sobel

Sobel là toán tử phát hiện cạnh dựa trên đạo hàm bậc nhất. Thuật toán sử dụng hai kernel để tính gradient theo chiều ngang (Gx) và chiều dọc (Gy).

Công thức tính độ mạnh cạnh:

G = sqrt(Gx² + Gy²)

Đặc điểm:
- Dễ hiểu và dễ cài đặt
- Tốc độ xử lý nhanh
- Nhạy với nhiễu
- Cạnh thu được thường dày và chưa tối ưu

So với Canny:
- Canny có bước giảm nhiễu nên chính xác hơn
- Canny tạo cạnh mảnh hơn
- Sobel nhanh hơn nhưng kém ổn định hơn

#### Laplacian

Laplacian là toán tử đạo hàm bậc hai, đo sự thay đổi cường độ sáng theo mọi hướng.

Đặc điểm:
- Phát hiện cạnh theo nhiều hướng cùng lúc
- Nhạy với nhiễu hơn Sobel
- Không xác định được hướng cạnh
- Thường cần Gaussian blur trước khi áp dụng

So với Canny:
- Canny ổn định hơn do có bước giảm nhiễu
- Canny kiểm soát cạnh tốt hơn nhờ double threshold
- Laplacian đơn giản nhưng dễ phát hiện cạnh giả


### 2. Các tham số của thuật toán và ảnh hưởng của chúng

#### a) Sigma trong Gaussian filter

Sigma (σ) là tham số điều chỉnh mức độ làm mờ của Gaussian blur.

Vai trò:
- σ nhỏ → ít làm mờ → giữ nhiều chi tiết → dễ nhiễu
- σ lớn → làm mờ mạnh → giảm nhiễu tốt → có thể mất chi tiết cạnh nhỏ

Ảnh hưởng:
- Sigma ảnh hưởng trực tiếp đến số lượng cạnh được phát hiện
- Sigma quá lớn có thể làm mất cạnh quan trọng

Thông thường:
- σ ≈ 1 → 2 được dùng phổ biến

---

#### b) Ngưỡng thấp (Low threshold) và ngưỡng cao (High threshold)

Hai ngưỡng được dùng để phân loại cạnh:
Low threshold:
- Xác định cạnh yếu (weak edge)
- Nếu quá thấp → nhiều cạnh giả

High threshold:
- Xác định cạnh mạnh (strong edge)
- Nếu quá cao → mất cạnh quan trọng
Nguyên tắc chọn:
Low threshold thường bằng khoảng 0.3 đến 0.5 của High threshold.

Ví dụ:
High threshold = 100
Low threshold = 40
Ảnh hưởng:
- Ngưỡng cao → ít cạnh hơn nhưng chính xác hơn
- Ngưỡng thấp → nhiều cạnh hơn nhưng dễ nhiễu


### 3. Ưu điểm và nhược điểm của Canny edge detector  
Các ứng dụng thực tế của Canny edge detector

#### a) So sánh với các thuật toán khác

| Tiêu chí     | Canny | Sobel | Laplacian |
|---------     |------|-------|-----------|
| Độ chính xác | cao | trung bình | trung bình |
| Tốc độ       | chậm hơn | nhanh | nhanh |
| K/n chống nhiễu | tốt | kém | rất nhạy nhiễu |
| Độ mảnh của cạnh| mảnh | dày | không ổn định |
| Độ phức tạp | cao | thấp | thấp |

Kết luận:
Canny cho kết quả tốt nhất nhưng tốn thời gian xử lý hơn.


#### b) Trong lĩnh vực nào Canny được sử dụng phổ biến nhất?

Canny được sử dụng phổ biến trong:

- Computer Vision
- Xử lý ảnh y tế
- Nhận dạng khuôn mặt
- Xe tự lái
- Robot
- Nhận dạng vật thể
- OCR (nhận dạng chữ viết)

Đây là bước tiền xử lý quan trọng trước khi áp dụng các thuật toán AI.

---

#### c) Ví dụ cụ thể về các ứng dụng

1. Nhận dạng khuôn mặt
   Xác định đường viền khuôn mặt và đặc điểm như mắt, mũi, miệng.

2. Xe tự lái
   Phát hiện làn đường và biên của vật thể trên đường.

3. Xử lý ảnh y tế
   Xác định biên của cơ quan trong ảnh X-ray hoặc MRI.

4. OCR
   Xác định đường viền ký tự trước khi nhận dạng chữ.

5. Robot
   Giúp robot xác định vật thể trong môi trường.

---

## III. Các câu hỏi mở rộng

### 1. Làm thế nào để đánh giá chất lượng của các cạnh được phát hiện bởi Canny?

Có thể đánh giá dựa trên:

- Độ liên tục của cạnh
- Độ mảnh của cạnh
- Số lượng cạnh giả
- Khả năng phát hiện đúng vị trí biên của vật thể
- So sánh với ground truth (ảnh có cạnh chuẩn)

Các chỉ số đánh giá phổ biến:
- Precision
- Recall
- F1-score

---

### 2. Có những phương pháp nào khác để cải thiện hiệu suất của Canny?

Một số cách cải thiện:

- Điều chỉnh sigma phù hợp
- Chọn threshold hợp lý
- Sử dụng adaptive threshold
- Kết hợp với thuật toán làm mượt ảnh tốt hơn
- Áp dụng preprocessing để tăng độ tương phản
- Sử dụng GPU để tăng tốc xử lý
- Kết hợp với AI để lọc cạnh tốt hơn

---

### 3. Canny có thể được sử dụng để phát hiện các cạnh trong ảnh màu không? Nếu có, thì như thế nào?

Có thể áp dụng Canny cho ảnh màu bằng cách:

Cách 1:
Chuyển ảnh màu (RGB) sang ảnh xám (grayscale) rồi áp dụng Canny.

Cách 2:
Áp dụng Canny cho từng kênh màu:
- Red
- Green
- Blue

Sau đó kết hợp kết quả lại.

Cách phổ biến nhất là chuyển sang grayscale vì nhanh và hiệu quả.

---

### 4. Làm thế nào để áp dụng Canny cho các video?

Video là chuỗi các frame (khung hình).

Các bước:

1. Tách video thành từng frame
2. Áp dụng Canny cho từng frame
3. Ghép các frame lại thành video mới

Ứng dụng:
- phát hiện chuyển động
- theo dõi vật thể
- xe tự lái
- giám sát an ninh

Ví dụ thư viện Python:
- OpenCV hỗ trợ xử lý Canny cho video theo thời gian thực