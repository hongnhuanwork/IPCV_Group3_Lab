import cv2
import pywt
import numpy as np
import os
import matplotlib.pyplot as plt
from itertools import combinations
from sklearn.metrics import accuracy_score, recall_score, precision_score, confusion_matrix, roc_curve, auc

# Lấy đường dẫn thư mục hiện tại (Chống lỗi Not Found)
CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
# Đặt thư mục làm việc hiện tại về CURRENT_DIR để đảm bảo các đường dẫn tương đối hoạt động đúng
os.chdir(CURRENT_DIR)


def imread_unicode(path, flag=cv2.IMREAD_COLOR):
    """Đọc ảnh an toàn với đường dẫn Unicode trên Windows."""
    try:
        data = np.fromfile(path, dtype=np.uint8)
        if data.size == 0:
            return None
        img = cv2.imdecode(data, flag)
        return img
    except Exception:
        return None


def imwrite_unicode(path, img):
    """Ghi ảnh an toàn với đường dẫn Unicode trên Windows."""
    try:
        ext = os.path.splitext(path)[1]
        success, encoded_img = cv2.imencode(ext, img)
        if not success:
            return False
        encoded_img.tofile(path)
        return True
    except Exception:
        return False

# ==========================================
# 0. TỰ ĐỘNG TẠO DỮ LIỆU TEST (DATA AUGMENTATION)
# ==========================================
def generate_test_dataset(base_img_name, prefix):
    """Đọc 1 ảnh gốc và sinh ra 3 phiên bản biến thể để test Wavelet Hash"""
    base_path = os.path.join(CURRENT_DIR, base_img_name)
    img = imread_unicode(base_path, cv2.IMREAD_COLOR)
    
    if img is None:
        print(f"⚠️ Không tìm thấy ảnh gốc: {base_img_name}. Vui lòng chép ảnh vào thư mục!")
        return []

    generated_paths = []
    
    # 1. Ảnh gốc (Lưu lại với tên chuẩn để dễ so sánh)
    path1 = os.path.join(CURRENT_DIR, f"{prefix}_1_original.jpg")
    imwrite_unicode(path1, img)
    generated_paths.append(path1)

    # 2. Ảnh Zoom & Crop (Phóng to phần trung tâm)
    h, w = img.shape[:2]
    zoomed = img[int(h*0.1):int(h*0.9), int(w*0.1):int(w*0.9)] # Cắt bỏ 10% viền
    zoomed = cv2.resize(zoomed, (w, h)) # Phóng to lại bằng kích thước cũ
    path2 = os.path.join(CURRENT_DIR, f"{prefix}_2_zoomed.jpg")
    imwrite_unicode(path2, zoomed)
    generated_paths.append(path2)

    # 3. Ảnh tối đi (Giảm độ sáng 40%)
    darkened = cv2.convertScaleAbs(img, alpha=0.6, beta=0)
    path3 = os.path.join(CURRENT_DIR, f"{prefix}_3_dark.jpg")
    imwrite_unicode(path3, darkened)
    generated_paths.append(path3)

    # 4. Ảnh thêm nhiễu (Noise)
    noise = np.random.randint(0, 50, (h, w, 3), dtype='uint8')
    noisy_img = cv2.add(img, noise) # Cộng ma trận nhiễu vào ảnh
    path4 = os.path.join(CURRENT_DIR, f"{prefix}_4_noise.jpg")
    imwrite_unicode(path4, noisy_img)
    generated_paths.append(path4)

    return generated_paths

# ==========================================
# 1. CÁC HÀM XỬ LÝ LÕI (CORE FUNCTIONS)
# ==========================================

def wavelet_hash(image_path, hash_size=8):
    """
    Trích xuất mã băm wavelet (wHash) từ hình ảnh.
    """
    # 1. Đọc ảnh ở chế độ ảnh xám (Grayscale)
    img = imread_unicode(image_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        print(f"Lỗi: Không thể đọc ảnh {image_path}")
        return None
        
    # 2. Resize ảnh về kích thước cố định (ví dụ: 32x32) để đảm bảo độ dài hash luôn bằng nhau
    img = cv2.resize(img, (hash_size * 4, hash_size * 4))
    
    # 3. Biến đổi Wavelet (Sử dụng 'haar' wavelet, level 2)
    coeffs = pywt.wavedec2(img, 'haar', level=2)
    cA = coeffs[0] # Lấy ma trận hệ số xấp xỉ (Approximation coefficients)
    
    # 4. Lượng tử hóa (Quantization): So sánh với giá trị trung vị
    median_val = np.median(cA)
    binary_matrix = cA > median_val # Trả về ma trận True/False
    
    # 5. Flatten (dàn phẳng) thành mảng 1 chiều chứa các bit 0 và 1
    hash_code = binary_matrix.flatten().astype(int)
    
    return hash_code

def hamming_distance(hash1, hash2):
    """
    Tính khoảng cách Hamming giữa hai mã băm (số bit khác biệt).
    """
    return np.sum(hash1 != hash2)

# ==========================================
# 2. CHUẨN BỊ DỮ LIỆU & TÍNH TOÁN (MAIN PIPELINE)
# ==========================================

# Giả lập danh sách ảnh. 
print("Đang tạo dữ liệu ảnh test...")
# Sinh ra 4 ảnh từ seed_cat và lấy thêm seed_dog làm ảnh "Khác"
cat_images = generate_test_dataset('seed_cat.jpg', 'cat')
dog_path = os.path.join(CURRENT_DIR, 'seed_dog.jpg')

# QUY TẮC MẪU: Các ảnh có cùng tiền tố (ví dụ 'cat') là CÙNG 1 đối tượng (Tương thích).
# image_paths = ['cat_1.jpg', 'cat_2.jpg', 'cat_3.jpg', 'dog_1.jpg', 'dog_2.jpg', 'car_1.jpg']

# Tính hash cho toàn bộ ảnh (Lưu ý: Cần có file ảnh thật trong thư mục để hàm này không lỗi)
# Ở đây dùng try-except để code không bị crash nếu chưa chuẩn bị ảnh
hashes = {}
# Nếu tạo data thành công thì mới chạy tiếp
if len(cat_images) > 0 and os.path.exists(dog_path):
    image_paths = cat_images + [dog_path]

    print("Đang băm hình ảnh (Hasing)...")
    for path in image_paths:
        h = wavelet_hash(path)
        if h is not None:
            hashes[path] = h

# Chỉ chạy đánh giá nếu đã có dữ liệu hash
if len(hashes) >= 2:
    true_labels = []    # Ground truth: 1 nếu tương thích (cùng đối tượng), 0 nếu khác
    predicted_dists = [] # Lưu khoảng cách Hamming
    
    # Lấy tất cả các cặp ảnh có thể có (không trùng lặp)
    pairs = list(combinations(hashes.keys(), 2))
    
    for img1, img2 in pairs:
        # 0. Trích xuất TÊN FILE từ đường dẫn dài
        name1 = os.path.basename(img1) # Ví dụ: Từ 'D:\...\cat_1_original.jpg' lấy ra 'cat_1_original.jpg'
        name2 = os.path.basename(img2) # Ví dụ: Lấy ra 'seed_dog.jpg'

        # 1. Lấy TỪ KHÓA phân loại:
        # Tách tên file bằng dấu '_' và lấy chữ đầu tiên ('cat' hoặc 'seed')
        key1 = name1.split('_')[0] # Ví dụ: 'cat' từ 'cat_1_original.jpg'
        key2 = name2.split('_')[0] # Ví dụ: 'seed' từ 'seed_dog.jpg'

        # Đặc biệt với seed_dog, nếu tên file là seed_dog thì đổi key thành 'dog' để so sánh với 'cat'
        if key1 == 'seed': key1 = name1.split('_')[1].split('.')[0] # Lấy 'cat' từ 'seed_cat.jpg'
        if key2 == 'seed': key2 = name2.split('_')[1].split('.')[0] # Lấy 'dog' từ 'seed_dog.jpg'
        
        # 2. Gán nhãn: Nếu từ khóa giống nhau thì là 1 (Giống), ngược lại là 0 (Khác)
        is_similar = 1 if key1 == key2 else 0
        true_labels.append(is_similar)
        
        # 3. Tính khoảng cách
        dist = hamming_distance(hashes[img1], hashes[img2])
        predicted_dists.append(dist)
        
        print(f"{name1:20} & {name2:20} | Distance: {dist:2} | Thực tế: {'Giống' if is_similar else 'Khác'}")

    # ==========================================
    # 3. ĐÁNH GIÁ (EVALUATION)
    # ==========================================
    
    # Để phân loại, ta cần 1 NGƯỠNG (Threshold). 
    # Nếu khoảng cách Hamming <= THRESHOLD => Dự đoán là Tương thích (1)
    # Hash size 8 -> mã băm dài 64 bit. Khoảng cách < 10 thường được coi là rất giống nhau.
    THRESHOLD = 15 
    
    predictions = [1 if dist <= THRESHOLD else 0 for dist in predicted_dists]
    
    # Tính các chỉ số
    acc = accuracy_score(true_labels, predictions)
    recall = recall_score(true_labels, predictions, zero_division=0) # Độ nhạy
    precision = precision_score(true_labels, predictions, zero_division=0)
    
    # Độ đặc hiệu (Specificity) = TN / (TN + FP)
    tn, fp, fn, tp = confusion_matrix(true_labels, predictions, labels=[0, 1]).ravel()
    specificity = tn / (tn + fp) if (tn + fp) > 0 else 0

    print("\n--- KẾT QUẢ ĐÁNH GIÁ ---")
    print(f"Độ chính xác (Accuracy)  : {acc * 100:.2f}%")
    print(f"Độ nhạy (Sensitivity)    : {recall * 100:.2f}%")
    print(f"Độ đặc hiệu (Specificity): {specificity * 100:.2f}%")
    print(f"Độ chuẩn xác (Precision) : {precision * 100:.2f}%")

    # ==========================================
    # 4. VẼ ĐƯỜNG CONG ROC
    # ==========================================
    # LƯU Ý CHO ROC: ROC cần xác suất (probability) để tính, nhưng ta đang có 'distance'.
    # Khoảng cách càng nhỏ thì xác suất giống nhau càng cao. 
    # Ta nghịch đảo distance để dùng cho ROC curve (ví dụ: -distance)
    scores_for_roc = [-d for d in predicted_dists]
    
    fpr, tpr, thresholds = roc_curve(true_labels, scores_for_roc)
    roc_auc = auc(fpr, tpr)

    plt.figure(figsize=(8, 6))
    plt.plot(fpr, tpr, color='darkorange', lw=2, label=f'ROC curve (AUC = {roc_auc:.2f})')
    plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('Tỷ lệ Dương tính giả (False Positive Rate)')
    plt.ylabel('Độ nhạy (True Positive Rate)')
    plt.title('Đường cong ROC đánh giá Wavelet Hash')
    plt.legend(loc="lower right")
    plt.grid(True)
    plt.show()
else:
    print("Vui lòng đảm bảo có đủ 2 file 'seed_cat.jpg' và 'seed_dog.jpg' trong thư mục code.")