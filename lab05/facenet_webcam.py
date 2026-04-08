import cv2
from mtcnn import MTCNN
from keras_facenet import FaceNet
import numpy as np

# Khởi tạo detector và embedder
detector = MTCNN()
embedder = FaceNet()

# Giả sử bạn đã có một ảnh "chính chủ" để so sánh (Database)
# Bạn cần trích xuất vector đặc trưng của ảnh này trước
img_target = cv2.imread(f'lab05/my_image.jpeg')
img_target = cv2.cvtColor(img_target, cv2.COLOR_BGR2RGB)
target_face_info = detector.detect_faces(img_target)

if target_face_info:
    x, y, w, h = target_face_info[0]['box']
    # Đảm bảo tọa độ không âm (tránh lỗi cắt ảnh)
    x, y = max(0, x), max(0, y)
    face_crop = img_target[y:y+h, x:x+w]
    
    # Trích xuất embedding
    face_data = embedder.extract(face_crop, threshold=0.7)
    
    if len(face_data) > 0:
        target_embedding = face_data[0]['embedding']
        print("Đã khởi tạo embedding mục tiêu thành công!")
    else:
        print("Lỗi: FaceNet không thể trích xuất đặc trưng từ khuôn mặt trong ảnh mẫu.")
        exit() # Dừng chương trình vì không có dữ liệu mẫu để so sánh
else:
    print("Lỗi: MTCNN không tìm thấy khuôn mặt nào trong ảnh my_face.jpg.")
    exit()


cap = cv2.VideoCapture(0) # Mở webcam mặc định

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Chuyển BGR sang RGB cho MTCNN
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # 1. Phát hiện khuôn mặt bằng MTCNN
    results = detector.detect_faces(rgb_frame)

    for res in results:
        x, y, w, h = res['box']
        # Vẽ khung bao khuôn mặt
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

        # 2. Trích xuất đặc trưng vùng mặt vừa tìm được
        face_crop = rgb_frame[y:y+h, x:x+w]
        if face_crop.size > 0:
            face_data = embedder.extract(face_crop, threshold=0.95)
            
            if face_data:
                current_embedding = face_data[0]['embedding']
                
                # 3. So sánh bằng Cosine Similarity (hoặc Euclidean Distance)
                # FaceNet của keras-facenet thường dùng tính toán khoảng cách
                def compute_similarity(v1, v2):
                    return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))

                similarity = compute_similarity(target_embedding, current_embedding)

                # 4. Điều kiện so sánh theo yêu cầu lab
                label = f"Matched: {similarity:.2f}" if similarity > 0.7 else "Unknown"
                color = (0, 255, 0) if similarity > 0.7 else (0, 0, 255)

                cv2.putText(frame, label, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)

    cv2.imshow("Face Recognition Lab", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()