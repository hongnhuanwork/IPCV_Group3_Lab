import cv2
import numpy as np
from mtcnn import MTCNN
from keras_facenet import FaceNet

detector = MTCNN()
embedder = FaceNet()

def get_similarity(embedding1, embedding2):
    # Normalize vectors
    in_encoder = embedding1 / np.linalg.norm(embedding1)
    out_encoder = embedding2 / np.linalg.norm(embedding2)
    return np.dot(in_encoder, out_encoder)

img_ref = cv2.imread('lab05/face_image_set/Henry Cavill/Henry Cavill_70.jpg')
img_ref_rgb = cv2.cvtColor(img_ref, cv2.COLOR_BGR2RGB)
res = detector.detect_faces(img_ref_rgb)

if res:
    x, y, w, h = res[0]['box']
    face_ref = img_ref_rgb[y:y+h, x:x+w]
    face_ref = cv2.resize(face_ref, (160, 160))
    embedding_ref = embedder.embeddings(np.expand_dims(face_ref, axis=0))[0]
else:
    print("Không tìm thấy mặt trong ảnh mẫu!")
    exit()

cap = cv2.VideoCapture(0)
while True:
    ret, frame = cap.read()
    if not ret: break
    
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    faces = detector.detect_faces(frame_rgb)
    
    for face in faces:
        x, y, w, h = face['box']
        face_img = frame_rgb[y:y+h, x:x+w]
        if face_img.size == 0: continue
        face_img = cv2.resize(face_img, (160, 160))
        
        embedding_curr = embedder.embeddings(np.expand_dims(face_img, axis=0))[0]
        
        similarity = get_similarity(embedding_ref, embedding_curr)
        
        if similarity > 0.6:
            label = f"Matched ({similarity:.2f})"
            color = (0, 255, 0)
        else:
            label = f"Unknown ({similarity:.2f})"
            color = (0, 0, 255)
            
        cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
        cv2.putText(frame, label, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

    cv2.imshow('Face Recognition Lab05', frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()