# Test Cases – Face Recognition (FaceNet + MTCNN)

## 1. Test cơ bản

| Test case | Mô tả | Expected result | Ghi chú kết quả test |
|-----------|------|-----------------|----------------------|
| Same person | Ảnh đã lưu so với đúng người thật | Matched | |
| Different person | Ảnh đã lưu so với người khác | Unknown | |

---

## 2. Điều kiện môi trường

| Test case | Mô tả | Expected result | Ghi chú kết quả test |
|-----------|------|-----------------|----------------------|
| Low light | Ánh sáng yếu | Có thể sai | |
| Different angle | Góc mặt khác so với ảnh mẫu | Có thể Matched | |
| Blur image | Ảnh bị mờ | Unknown | |

---

## 3. Vật cản khuôn mặt (Occlusion)

| Test case | Mô tả | Expected result | Ghi chú kết quả test |
|-----------|------|-----------------|----------------------|
| Glasses | Đeo kính thường | Matched | |
| Sunglasses | Đeo kính râm | Không ổn định | |
| Mask | Đeo khẩu trang | Unknown | |

---

## 4. Khoảng cách & kích thước khuôn mặt

| Test case | Mô tả | Expected result | Ghi chú kết quả test |
|-----------|------|-----------------|----------------------|
| Close distance | Khuôn mặt gần camera | Matched | |
| Far distance | Khuôn mặt nhỏ, đứng xa | Unknown | |
| Phone screen | Khuôn mặt hiển thị qua màn hình điện thoại | Không ổn định | |
| Printed photo | Khuôn mặt từ ảnh in | Có thể match sai | |

---

## Ghi chú chung

- Ngưỡng so sánh: **similarity > 0.7 → Matched**
- **similarity < 0.7 → Unknown**
- Các yếu tố như ánh sáng yếu, góc nghiêng lớn hoặc vật cản có thể làm giảm độ chính xác.
- Cột **Ghi chú kết quả test** dùng để ghi:
  - similarity đo được (ví dụ: 0.82)
  - tốc độ nhận diện
  - nhận xét lỗi hoặc sai lệch