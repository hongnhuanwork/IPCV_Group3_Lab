import cv2
import numpy as np
from mtcnn import MTCNN
from keras_facenet import FaceNet
from scipy.spatial.distance import cosine

# 1. KHỞI TẠO MÔ HÌNH VÀ HÀM HỖ TRỢ
detector = MTCNN()    # Mô hình phát hiện khuôn mặt
embedder = FaceNet()  # Mô hình trích xuất đặc trưng khuôn mặt

def extract_face(frame, box, required_size=(160, 160)):
    """Cắt khuôn mặt từ khung hình và resize về chuẩn 160x160 của FaceNet"""
    x, y, w, h = box
    # Xử lý tọa độ âm (Khi mặt nằm quá sát rìa camera)
    x1, y1 = abs(x), abs(y)
    x2, y2 = x1 + w, y1 + h

    # Cắt ảnh
    face = frame[y1:y2, x1:x2]
    # Resize về chuẩn 160x160
    face_resized = cv2.resize(face, required_size)
    return face_resized


# 2. CHUẨN BỊ ẢNH GỐC (ANCHOR) ĐỂ SO SÁNH
print("Đang nạp ảnh gốc (Anchor)...")
anchor_img = cv2.imread('my_face.jpg')
if anchor_img is None:
    print("Không tìm thấy file 'my_face.jpg'. Vui lòng thêm ảnh vào thư mục!")
    exit()

# MTCNN và FaceNet hoạt động chuẩn nhất trên không gian màu RGB
anchor_img_rgb = cv2.cvtColor(anchor_img, cv2.COLOR_BGR2RGB)
anchor_results = detector.detect_faces(anchor_img_rgb)

if len(anchor_results) == 0:
    print("Không tìm thấy khuôn mặt nào trong ảnh gốc!")
    exit()

# Lấy khuôn mặt đầu tiên tìm được và trích xuất vector đặc trưng (Embedding)
anchor_box = anchor_results[0]['box']
anchor_face = extract_face(anchor_img_rgb, anchor_box)
# Embedder trả về mảng 2D, ta lấy phần tử [0] để được vector 1D (512 chiều)
anchor_embedding = embedder.embeddings([anchor_face])[0]


# 3. NHẬN DIỆN THỜI GIAN THỰC (WEBCAM)
print("Đang mở Webcam... Nhấn 'q' để thoát.")
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    # Phát hiện các khuôn mặt trong khung hình hiện tại
    results = detector.detect_faces(frame_rgb)

    for res in results:
        box = res['box']
        confidence = res['confidence']

        # Chỉ xử lý nếu mô hình tự tin > 90% đây là khuôn mặt
        if confidence > 0.90:
            face_crop = extract_face(frame_rgb, box)

            # Trích xuất vector đặc trưng của mặt trong camera
            live_embedding = embedder.embeddings([face_crop])[0]

            # Tính toán độ tương đồng (Cosine Similarity)
            # Hàm cosine() của scipy tính Cosine Distance (từ 0 đến 2).
            # Suy ra Similarity = 1 - Distance (từ -1 đến 1, càng gần 1 càng giống)
            similarity = 1 - cosine(anchor_embedding, live_embedding)

            # Cài đặt điều kiện theo yêu cầu Lab
            if similarity > 0.7:
                label = f"Matched ({similarity:.2f})"
                color = (0, 255, 0) # Xanh lá
            else:
                label = f"Not Matched ({similarity:.2f})"
                color = (0, 0, 255) # Đỏ

            # Vẽ Box và Label lên màn hình
            x, y, w, h = box
            cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
            cv2.putText(frame, label, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

    # Hiển thị
    cv2.imshow('Face Recognition', frame)

    # Bắt sự kiện phím 'q' để thoát
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


# Giải phóng tài nguyên
cap.release()
cv2.destroyAllWindows()