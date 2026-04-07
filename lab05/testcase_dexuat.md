## III. Một số test case tiêu biểu

### 1. Nhóm test cơ bản

| Test Case        | Mô tả                     | Expected |
|------------------|--------------------------|----------|
| Same person      | Ảnh lưu vs người thật    | Matched  |
| Different person | Ảnh lưu vs người khác    | Unknown  |

---

### 2. Nhóm điều kiện môi trường

| Test Case        | Mô tả             | Expected        |
|------------------|------------------|-----------------|
| Low light        | Ánh sáng yếu     | Có thể sai      |
| Different angle  | Góc mặt khác     | Có thể Matched  |
| Blur image       | Ảnh bị mờ        | Unknown         |

---

### 3. Nhóm vật cản (Occlusion)

| Test Case   | Mô tả               | Expected        |
|-------------|--------------------|-----------------|
| Glasses     | Đeo kính thường    | Matched         |
| Sunglasses  | Kính râm           | Không ổn định   |
| Mask        | Đeo khẩu trang     | Unknown         |

---

### 4. Nhóm khoảng cách & kích thước

| Test Case        | Mô tả                              | Expected        |
|------------------|-----------------------------------|-----------------|
| Close distance   | Mặt gần camera                    | Matched         |
| Far distance     | Mặt nhỏ                           | Unknown         |
| Phone screen     | Ảnh hiển thị trên điện thoại      | Không ổn định   |
| Printed photo    | Ảnh in                            | ⚠️ Có thể bị match sai        |
---
