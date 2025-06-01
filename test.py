import cv2

video_path = r'.\vidio\vdio.mp4'
cap = cv2.VideoCapture(video_path)

# Memeriksa apakah video berhasil dibuka
if not cap.isOpened():
    print(f"Gagal membuka video: {video_path}")
else:
    print("Video berhasil dibuka!")
    # Coba membaca beberapa frame pertama untuk memastikan
    ret, frame = cap.read()
    if ret:
        print("Frame pertama berhasil dibaca!")
    else:
        print("Gagal membaca frame pertama.")
