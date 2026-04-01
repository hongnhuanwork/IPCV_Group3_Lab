# CANNY EDGE DETECTOR

## I. Lý thuyết

### 1. Các bước của thuật toán Canny

Thuật toán Canny gồm 5 bước chính:

---

#### a) Giảm nhiễu (Noise Reduction)

- Ảnh đầu vào thường chứa nhiễu làm sai lệch việc phát hiện cạnh  
- Sử dụng bộ lọc Gaussian để làm mượt ảnh  

Công thức Gaussian:

G(x, y) = (1 / (2πσ²)) * exp(-(x² + y²) / (2σ²))

- σ (sigma) quyết định mức độ làm mượt:
  - σ nhỏ → giữ chi tiết nhưng còn nhiễu  
  - σ lớn → giảm nhiễu tốt nhưng mất chi tiết  

---

#### b) Tính toán Gradient

- Sử dụng toán tử Sobel để tính đạo hàm theo x và y  
- Tính:
  - Độ lớn gradient (magnitude)
  - Hướng gradient (direction)

Công thức:

G = sqrt(Gx² + Gy²)

---

#### c) Non-Maximum Suppression (NMS)

- Làm mỏng cạnh về 1 pixel  
- So sánh mỗi pixel với các pixel lân cận theo hướng gradient  
- Nếu không phải cực đại → loại bỏ  

Kết quả: cạnh sắc nét hơn  

---

#### d) Ngưỡng kép (Double Threshold)

Phân loại pixel thành 3 loại:

- Strong edge: > ngưỡng cao  
- Weak edge: giữa ngưỡng thấp và cao  
- Non-edge: < ngưỡng thấp  

---

#### e) Theo dõi cạnh (Edge Tracking by Hysteresis)

- Giữ lại weak edge nếu nối với strong edge  
- Loại bỏ weak edge không liên kết  

Giúp loại bỏ nhiễu và giữ cạnh thực  

---

#### b) So sánh với các thuật toán khác

| Thuật toán | Đặc điểm |
|------------|---------|
| Sobel | Nhanh, đơn giản, dễ nhiễu |
| Laplacian | Nhạy với nhiễu |
| Canny | Chính xác cao, ít nhiễu |

---

### 2. Các tham số của thuật toán

#### a) Sigma (σ) trong Gaussian filter

- Điều chỉnh độ mượt của ảnh  
- Ảnh hưởng đến:
  - Độ nhiễu  
  - Độ chi tiết  

Giá trị thường dùng:
- σ = 1 → chi tiết cao  
- σ = 2–3 → cân bằng  
- σ > 3 → mượt mạnh  

---

#### b) Ngưỡng thấp và ngưỡng cao

| Tham số | Vai trò |
|--------|--------|
| Low threshold | Xác định cạnh yếu |
| High threshold | Xác định cạnh mạnh |

Quan hệ thường dùng:
- Low ≈ 0.4 × High  

Ảnh hưởng:
- Ngưỡng thấp → nhiều cạnh (có thể nhiễu)  
- Ngưỡng cao → ít cạnh (mất chi tiết)  

---

### 3. Ưu điểm và nhược điểm

#### Ưu điểm

- Độ chính xác cao  
- Ít nhiễu  
- Cạnh mỏng, rõ  
- Tốt hơn Sobel và Laplacian  

#### Nhược điểm

- Tính toán chậm hơn  
- Phụ thuộc tham số  
- Khó tối ưu với ảnh phức tạp  

---

### 4. Ứng dụng thực tế

#### a) So sánh tổng thể

| Tiêu chí | Sobel | Laplacian | Canny |
|----------|------|----------|------|
| Độ chính xác | Trung bình | Thấp | Cao |
| Tốc độ | Nhanh | Nhanh | Chậm |
| Khả năng chống nhiễu | Kém | Rất kém | Tốt |

---

#### b) Lĩnh vực sử dụng

- Computer Vision  
- Xử lý ảnh  
- AI & Deep Learning  
- Robotics  
- Xe tự lái  

---

#### c) Ví dụ ứng dụng

- Nhận diện làn đường  
- Phát hiện vật thể  
- Nhận diện khuôn mặt  
- OCR (nhận dạng chữ)  
- Phân đoạn ảnh  

---

## III. Câu hỏi mở rộng

### 1. Đánh giá chất lượng cạnh

Các phương pháp:

- So sánh với ground truth  
- Precision / Recall  
- F1-score  
- Đánh giá trực quan  

---

### 2. Cải thiện hiệu suất Canny

- Adaptive threshold  
- Multi-scale Gaussian  
- Kết hợp Deep Learning  
- Tối ưu GPU  

---

### 3. Canny với ảnh màu

Có thể thực hiện theo các cách:

- Chuyển sang grayscale rồi áp dụng  
- Áp dụng từng kênh RGB rồi gộp lại  
- Sử dụng không gian màu HSV hoặc LAB  

---

### 4. Áp dụng Canny cho video

Các bước:

1. Tách video thành các frame  
2. Áp dụng Canny cho từng frame  
3. Ghép lại thành video  

Tối ưu:
- Xử lý thời gian thực  
- Kết hợp tracking object  

---

## Tóm tắt

- Canny là thuật toán phát hiện cạnh hiệu quả nhất trong các phương pháp truyền thống  
- Gồm 5 bước:
  1. Gaussian Blur  
  2. Gradient  
  3. Non-Maximum Suppression  
  4. Double Threshold  
  5. Hysteresis  

- Ưu điểm: chính xác, ít nhiễu  
- Nhược điểm: chậm, cần điều chỉnh tham số  