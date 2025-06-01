import os
from PIL import Image, ImageDraw, ImageFont
import easyocr
from googletrans import Translator

# Inisialisasi EasyOCR
reader = easyocr.Reader(['en'])  # Membaca bahasa Inggris

# Fungsi untuk membaca teks dan bounding box menggunakan EasyOCR
def extract_text_with_boxes(image_path):
    image = Image.open(image_path)
    result = reader.readtext(image)  # Dapatkan hasil deteksi teks beserta bounding box
    return result

# Fungsi untuk menerjemahkan teks
def translate_text(text, src_lang='en', dest_lang='id'):
    translator = Translator()
    translated = translator.translate(text, src=src_lang, dest=dest_lang)
    return translated.text

# Fungsi untuk mengganti teks pada posisi bounding box
def replace_text_with_translation(image_path, translated_text, results, output_path):
    image = Image.open(image_path)
    draw = ImageDraw.Draw(image)
    
    try:
        font = ImageFont.truetype("arial.ttf", 20)  # Gunakan font yang sesuai
    except IOError:
        font = ImageFont.load_default()

    # Memecah terjemahan menjadi beberapa baris
    translated_lines = translated_text.split('. ')  # Pisahkan berdasarkan kalimat atau titik
    translated_index = 0

    for result in results:
        (bbox, text, score) = result  # Bounding box, teks, dan skor kepercayaan
        x1, y1 = bbox[0]
        x2, y2 = bbox[2]

        # Memastikan y1 lebih besar dari y2 jika perlu
        if y1 < y2:
            y1, y2 = y2, y1

        # Menghapus teks asli (menggambar kotak putih)
        draw.rectangle([(x1, y2), (x2, y1)], fill="white")
        
        # Memasukkan terjemahan yang tepat untuk setiap bagian teks
        if translated_index < len(translated_lines):
            text = translated_lines[translated_index]
            translated_index += 1
            # Menyesuaikan posisi agar teks terjemahan tidak saling tumpang tindih
            draw.text((x1, y2), text, font=font, fill="black")

    image.save(output_path)

# Fungsi utama untuk memproses gambar
def process_manga_images(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        if filename.endswith(('.jpg', '.png', '.jpeg')):  # Filter file gambar
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, filename)

            print(f"Memproses {filename}...")
            results = extract_text_with_boxes(input_path)  # Ekstraksi teks dan posisi
            original_text = ' '.join([result[1] for result in results])  # Gabungkan teks asli
            translated_text = translate_text(original_text)  # Terjemahkan teks
            replace_text_with_translation(input_path, translated_text, results, output_path)  # Ganti teks di gambar
            print(f"Selesai memproses {filename}, disimpan ke {output_path}")


input_folder = 'manga/input_images'   
output_folder = 'manga/output_images' 

process_manga_images(input_folder, output_folder)
print("Semua gambar telah diproses.")
