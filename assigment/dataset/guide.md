# Hướng dẫn tải và thiết lập Dataset

Tài liệu này hướng dẫn cách tải và tổ chức dữ liệu cho hệ thống **Truy xuất và Nhận diện khuôn mặt**. Dự án sử dụng hai bộ dữ liệu chính phục vụ cho việc huấn luyện/thử nghiệm các module Detection, Segmentation và Recognition.

---

## 1. Danh sách Dataset

### A. CelebAMask-HQ (Dành cho Segmentation & Recognition)
* **Mô tả:** Bộ dữ liệu gồm 30,000 ảnh khuôn mặt chất lượng cao, có kèm mask phân vùng chi tiết cho từng bộ phận (mắt, mũi, miệng, da mặt...).
* **Mục đích:** Huấn luyện/Thử nghiệm module **Face Parsing (FastSAM)** và trích xuất đặc trưng khuôn mặt.
* **Link tải:** [Google Drive - CelebAMask-HQ](https://drive.google.com/file/d/1badu11NqxGf6qM3PTTooQDJvQbejgbTv/view)

### B. WIDER Face (Dành cho Detection)
* **Mô tả:** Bộ dữ liệu chuẩn cho bài toán phát hiện khuôn mặt với các tình huống cực đoan: đám đông, che khuất, ánh sáng yếu, mặt siêu nhỏ.
* **Mục đích:** Đánh giá hiệu năng module **Face Localization (RetinaFace)** trong môi trường phức tạp.
* **Link tải:** [Kaggle - WIDER Face Dataset](https://www.kaggle.com/datasets/iamprateek/wider-face-a-face-detection-dataset)

---

## 2. Hướng dẫn cài đặt

### Bước 1: Tải dữ liệu
1.  **CelebAMask-HQ:** Truy cập link Google Drive, tải file `.zip` về máy.
2.  **WIDER Face:**
    * Bạn cần có tài khoản Kaggle.
    * Nhấn nút **Download** trên trang Kaggle.
    * Hoặc sử dụng Kaggle API: `kaggle datasets download -d iamprateek/wider-face-a-face-detection-dataset`

### Bước 2: Giải nén và Cấu trúc thư mục
Để code có thể đọc dữ liệu đồng nhất, hãy giải nén và tổ chức thư mục theo cấu trúc sau:

```text
/project
│
├── /data
│   ├── /CelebAMask-HQ
│   │   ├── /CelebA-HQ-img       # Chứa 30,000 ảnh gốc (.jpg)
│   │   └── /CelebAMask-HQ-mask  # Chứa các ảnh mask (.png)
│   │
│   ├── /WIDER_Face
│   │   ├── /WIDER_train         # Ảnh huấn luyện
│   │   ├── /WIDER_val           # Ảnh kiểm thử
│   │   └── /wider_face_split    # File annotation (txt/xml)
│
├── /models                      # Chứa các file pre-trained (RetinaFace, ArcFace)
└── main.py