import cv2
import mediapipe as mp
import time
import numpy as np

# Setup untuk Hand Detection (MediaPipe)
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(False)
mp_draw = mp.solutions.drawing_utils

# Inisialisasi webcam
cap = cv2.VideoCapture(0)

# Inisialisasi untuk menghitung FPS
pTime = 0
cTime = 0


def recognize_gesture(landmarks):
    # Ambil landmark penting
    thumb_tip = landmarks[4]
    index_tip = landmarks[8]
    middle_tip = landmarks[12]
    ring_tip = landmarks[16]
    pinky_tip = landmarks[20]
    wrist = landmarks[0]
    middle_finger_ncp = landmarks[9]
    ring_finger_ncp = landmarks[13]
    

    # 1. Gestur "Aku": Semua jari direntangkan dan miring
    if (
        index_tip.y < wrist.y and middle_tip.y < wrist.y and
        ring_tip.y < wrist.y and pinky_tip.y < wrist.y and
        thumb_tip.y < wrist.y and  # Semua jari di atas pergelangan
        abs(thumb_tip.x - pinky_tip.x) > abs(thumb_tip.y - pinky_tip.y)  # Posisi miring
    ):
        return "Aku"

    # 2. Gestur "Suka": Jempol, telunjuk, dan kelingking diangkat, jari tengah dan manis turun
    if (
        thumb_tip.y < wrist.y and index_tip.y < wrist.y and pinky_tip.y < wrist.y and  # Jempol, telunjuk, kelingking di atas pergelangan
        middle_tip.y > middle_finger_ncp.y and ring_tip.y > ring_finger_ncp.y  # Jari tengah dan manis di bawah pergelangan
    ):
        return "Suka"

    # 3. Gestur "Kamu": Telunjuk menunjuk ke kamera
    if (
        index_tip.z < thumb_tip.z and
        index_tip.z < middle_tip.z and
        index_tip.z < ring_tip.z and
        index_tip.z < pinky_tip.z
    ):
        return "Kamu"

    # Default: Tidak dikenali
    return " "


while True:
    # Baca frame dari webcam
    success, img = cap.read()
    if not success:
        break

    # Convert ke RGB untuk proses MediaPipe
    img = cv2.flip(img, 1)
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Proses Hand detection
    hand_results = hands.process(imgRGB)
    if hand_results.multi_hand_landmarks:
        for hand_landmarks in hand_results.multi_hand_landmarks:
            mp_draw.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Dapatkan koordinat landmark tangan
            landmarks = hand_landmarks.landmark

            # Kenali gestur
            gesture = recognize_gesture(landmarks)
            
            # Menambahkan background untuk teks
            text = f'{gesture}'
            font_scale = 3
            font = cv2.FONT_HERSHEY_PLAIN
            thickness = 3
            text_size = cv2.getTextSize(text, font, font_scale, thickness)[0]
            text_width, text_height = text_size

            # Menambahkan persegi panjang sebagai latar belakang teks
            x, y = 10, 70
            cv2.rectangle(img, (x - 10, y - 10), (x + text_width + 10, y + text_height + 10), (0, 0, 0), -1)

            # Menambahkan teks di atas latar belakang
            cv2.putText(img, text, (x, y + text_height + 5), font, font_scale, (255, 255, 255), thickness)

    # Hitung FPS
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    # Tampilkan frame dengan hasil deteksi tangan
    cv2.imshow("Hand Gesture Recognition", img)

    # Keluar dari loop dengan tombol 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release webcam dan tutup jendela
cap.release()
cv2.destroyAllWindows()