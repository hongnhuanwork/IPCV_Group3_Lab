import cv2
import numpy as np
import os
import pickle
from mtcnn import MTCNN
from keras_facenet import FaceNet

# ==========================================
# 1. CẤU HÌNH VÀ KHỞI TẠO
# ==========================================
detector = MTCNN()
embedder = FaceNet()

THRESHOLD = 0.7            # Ngưỡng nhận diện theo yêu cầu bài tập
DB_FILE = "face_memory.pkl" # File lưu trữ đặc trưng khuôn mặt
BASE_PATH = 'face_image_set'

def get_embedding(face_img):
    """Trích xuất vector đặc trưng từ khuôn mặt."""
    face_img = cv2.cvtColor(face_img, cv2.COLOR_BGR2RGB)
    face_img = cv2.resize(face_img, (160, 160))
    face_img = np.expand_dims(face_img, axis=0)
    embedding = embedder.embeddings(face_img)
    return embedding[0]

# ==========================================
# 2. XỬ LÝ DỮ LIỆU KHUÔN MẶT (DATABASE)
# ==========================================
known_embeddings = []
known_names = []

# Kiểm tra nếu đã có file bộ nhớ thì nạp luôn để tiết kiệm thời gian
if os.path.exists(DB_FILE):
    print(f"--- Đang nạp bộ nhớ từ file {DB_FILE} ---")
    with open(DB_FILE, "rb") as f:
        data = pickle.load(f)
        known_embeddings = data["embeddings"]
        known_names = data["names"]
    print(f"Hoàn tất! Đã nạp {len(known_names)} khuôn mặt.")
else:
    print("--- Không thấy file bộ nhớ. Bắt đầu quét thư mục ảnh mẫu ---")
    if not os.path.exists(BASE_PATH):
        print(f"Lỗi: Thư mục '{BASE_PATH}' không tồn tại!")
        exit()

    for name in os.listdir(BASE_PATH):
        person_path = os.path.join(BASE_PATH, name)
        if os.path.isdir(person_path):
            for img_name in os.listdir(person_path):
                img_path = os.path.join(person_path, img_name)
                img = cv2.imread(img_path)
                if img is None: continue

                # Giới hạn kích thước ảnh để tránh lỗi _ArrayMemoryError (10.4 GiB)
                h, w = img.shape[:2]
                if h > 1000 or w > 1000:
                    scale = 1000 / max(h, w)
                    img = cv2.resize(img, (int(w * scale), int(h * scale)))

                try:
                    results = detector.detect_faces(img)
                    if results:
                        # Lấy khuôn mặt đầu tiên phát hiện được
                        x, y, w_box, h_box = results[0]['box']
                        x, y = max(0, x), max(0, y) # Chống lỗi tọa độ âm
                        face = img[y:y+h_box, x:x+w_box]
                        
                        if face.size > 0:
                            known_embeddings.append(get_embedding(face))
                            known_names.append(name)
                            print(f" Đã học khuôn mặt: {name} từ file {img_name}")
                except Exception as e:
                    print(f" Bỏ qua file {img_name} do lỗi: {e}")

    # Lưu lại để lần sau không cần nạp lại
    if known_embeddings:
        with open(DB_FILE, "wb") as f:
            pickle.dump({"embeddings": known_embeddings, "names": known_names}, f)
        print(f"--- Đã lưu {len(known_names)} dữ liệu vào file {DB_FILE} ---")

# ==========================================
# 3. NHẬN DIỆN THỜI GIAN THỰC QUA WEBCAM
# ==========================================
print("\n--- Đang khởi động Webcam... ---")
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Lỗi: Không thể mở Webcam!")
    exit()

while True:
    ret, frame = cap.read()
    if not ret: break

    # Bước 1: Phát hiện khuôn mặt trong khung hình hiện tại
    results = detector.detect_faces(frame)
    
    for res in results:
        x, y, w, h = res['box']
        x, y = max(0, x), max(0, y)
        face = frame[y:y+h, x:x+w]
        
        if face.size > 0:
            # Bước 2: Trích xuất embedding của mặt đang đứng trước cam
            curr_embedding = get_embedding(face)
            
            # Bước 3: So sánh với cơ sở dữ liệu (Cosine Similarity)
            max_sim = -1
            best_match = "Unknown"
            
            for i, known_emb in enumerate(known_embeddings):
                # Tính độ tương đồng
                sim = np.dot(curr_embedding, known_emb) / (np.linalg.norm(curr_embedding) * np.linalg.norm(known_emb))
                if sim > max_sim:
                    max_sim = sim
                    best_match = known_names[i]
            
            # Bước 4: Hiển thị kết quả dựa trên ngưỡng THRESHOLD
            if max_sim > THRESHOLD:
                label = f"{best_match} (Matched)"
                color = (0, 255, 0) # Xanh lá cho người quen
            else:
                label = "Unknown"
                color = (0, 0, 255) # Đỏ cho người lạ
            
            # Vẽ khung và thông tin lên màn hình
            cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
            cv2.putText(frame, f"{label}: {max_sim:.2f}", (x, y-10), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

    # Hiển thị cửa sổ nhận diện
    cv2.imshow('Face Recognition - Nhan Q de thoat', frame)
    
    # Nhấn phím 'q' trên bàn phím để thoát
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Giải phóng tài nguyên
cap.release()
cv2.destroyAllWindows()