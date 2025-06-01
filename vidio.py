import yt_dlp
import os
import ffmpeg

def download_and_convert_to_mpeg2(url):
    try:
        # Membuat folder 'vidio' jika belum ada
        output_folder = "vidio"
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        # Menampilkan format yang tersedia
        ydl_opts = {
            'listformats': True,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            print("\nJudul:", info['title'])
            print("Channel:", info['uploader'])
            print("Durasi (detik):", info['duration'])

        # Meminta input format dari pengguna
        format_id = input("\nMasukkan ID format video yang diinginkan (lihat daftar di atas): ")

        # Opsi unduhan
        ydl_opts = {
            'format': format_id,
            'outtmpl': os.path.join(output_folder, '%(title)s.%(ext)s'),  # Nama file output di folder 'vidio'
        }

        # Mengunduh video
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print("\nSedang mengunduh...")
            info = ydl.extract_info(url, download=True)
            downloaded_file = ydl.prepare_filename(info)
            print("Unduhan selesai!")

        # Nama file hasil unduhan
        input_file = downloaded_file
        output_file = os.path.join(output_folder, os.path.splitext(os.path.basename(downloaded_file))[0] + ".mpg")  # Ubah ekstensi menjadi .mpg

        # Tentukan jalur FFmpeg
        ffmpeg_path = r"C:\ffmpeg\bin\ffmpeg.exe"

        # Konversi ke MPEG-2 menggunakan ffmpeg-python
        print("\nMengonversi ke format MPEG-2 menggunakan ffmpeg-python...")
        (
            ffmpeg
            .input(input_file)
            .output(output_file, vcodec='mpeg2video', acodec='mp2', qscale=2)
            .global_args('-hide_banner', '-loglevel', 'error', f'-ffmpeg_binary={ffmpeg_path}')
            .run(overwrite_output=True)
        )

        print(f"Konversi selesai! File disimpan sebagai: {output_file}")
    
    except Exception as e:
        print("Terjadi kesalahan:", e)

if __name__ == "__main__":
    # Meminta input URL dari pengguna
    video_url = input("Masukkan URL YouTube: ")
    download_and_convert_to_mpeg2(video_url)
