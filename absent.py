import cv2
import os

# ==============================
# FOLDER INPUT DAN OUTPUT
# ==============================

input_folder = "tugasCitra"
output_folder = "hasil_sample"

# Membuat folder output jika belum ada
os.makedirs(output_folder, exist_ok=True)


# ==============================
# DAFTAR FILE
# ==============================

files = [
    "01_HighQuality_Enhanced (2)(1).jpg",
    "02_LowContrast (2).jpg",
    "03_Blurred (2).jpg",
    "04_HighNoise (2).jpg",
    "05_LowResolution_Upsampled (2).jpg",
    "06_Faded_Underexposed (2).jpg",
    "07_ColorShift_WarmTint (2).jpg",
    "08_JPEGCompression_Artifacts (2).jpg",
    "09_CombinedDegradation (2).jpg"
]


# ==============================
# PROSES 9 GAMBAR
# ==============================

for i, filename in enumerate(files, start=1):

    input_path = os.path.join(input_folder, filename)

    # Membaca gambar
    image = cv2.imread(input_path)

    if image is None:
        print(f"Gagal membaca: {filename}")
        continue

    # Ukuran gambar
    height, width = image.shape[:2]

    print(f"{filename}")
    print(f"Ukuran: {width} x {height}")

    # ==========================================
    # AREA SIGNATURE
    # ==========================================
    #
    # CONTOH:
    # x1, y1 = titik kiri atas
    # x2, y2 = titik kanan bawah
    #
    # BAGIAN INI HARUS DISESUAIKAN
    # DENGAN POSISI TANDA TANGAN PADA CITRA
    #

    x1 = int(width * 0.60)
    y1 = int(height * 0.75)

    x2 = int(width * 0.95)
    y2 = int(height * 0.90)

    # Membuat area signature menjadi kosong/putih
    image[y1:y2, x1:x2] = 255

    # Nama output
    output_name = f"sample_{i:02d}.jpg"
    output_path = os.path.join(output_folder, output_name)

    # Menyimpan hasil
    cv2.imwrite(output_path, image)

    print(f"Berhasil: {output_name}")
    print("-" * 40)

print("Semua gambar selesai diproses.")