import cv2
import cv2.videostab
import mediapipe as mp
import time


mp_pose = mp.solutions.pose
mp_hands = mp.solutions.hands
pose = mp_pose.Pose()
hands = mp_hands.Hands()
mp_drawing = mp.solutions.drawing_utils


# url = "http://192.168.0.100:8080/video"
# cap = cv2.VideoCapture(url)

cap = cv2.VideoCapture(0)


prev_time = 0

while cap.isOpened():
    success, frame = cap.read()
    if not success:
        break


    frame = cv2.flip(frame, 1)

    
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # Deteksi pose
    pose_results = pose.process(image)

    # Deteksi tangan
    hand_results = hands.process(image)

    # Kembalikan gambar menjadi BGR untuk ditampilkan
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    # Gambar titik pose (body tracking)
    if pose_results.pose_landmarks:
        mp_drawing.draw_landmarks(
            image, pose_results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

    # Gambar titik tangan (hand tracking)
    if hand_results.multi_hand_landmarks:
        for hand_landmarks in hand_results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(
                image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    # Menghitung FPS
    curr_time = time.time()
    fps = 1 / (curr_time - prev_time)
    prev_time = curr_time

    # Menampilkan FPS pada video
    cv2.putText(image, f'FPS: {int(fps)}', (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 2)

    # Tampilkan hasilnya
    cv2.imshow('Tracking', image)
    if cv2.waitKey(10) & 0xFF == ord('a'):
        print("kamera Ditutup.........")
        break

cap.release()
cv2.destroyAllWindows()