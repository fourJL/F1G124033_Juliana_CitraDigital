import cv2
import pytesseract
import numpy as np
import os

# ==========================================
# PENGATURAN TESSERACT
# ==========================================

pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)

# ==========================================
# FOLDER GAMBAR
# ==========================================

folder = r"D:\citra4"

# ==========================================
# FILE HASIL OCR
# ==========================================

file_hasil = os.path.join(folder, "hasil_ocr.txt")

# ==========================================
# PROSES OCR 9 GAMBAR
# ==========================================

with open(file_hasil, "w", encoding="utf-8") as output:

    print("=" * 70)
    print("HASIL OCR 9 GAMBAR")
    print("=" * 70)

    output.write("=" * 70 + "\n")
    output.write("HASIL OCR 9 GAMBAR\n")
    output.write("=" * 70 + "\n\n")

    for i in range(1, 10):

        print("\n" + "=" * 70)
        print(f"ENHANCEMENT {i}")
        print("=" * 70)

        output.write("\n" + "=" * 70 + "\n")
        output.write(f"ENHANCEMENT {i}\n")
        output.write("=" * 70 + "\n")

        # ======================================
        # MENCARI GAMBAR
        # ======================================

        nama_awal = f"{i:02d}_"

        daftar_file = [
            file for file in os.listdir(folder)
            if file.startswith(nama_awal)
            and file.lower().endswith(".jpg")
        ]

        if len(daftar_file) == 0:

            print(f"Gambar {i} tidak ditemukan!")

            output.write("Gambar tidak ditemukan!\n")

            continue

        # Mengambil file pertama
        nama_file = daftar_file[0]

        path_gambar = os.path.join(
            folder,
            nama_file
        )

        # ======================================
        # MEMBACA GAMBAR
        # ======================================

        gambar = cv2.imread(path_gambar)

        if gambar is None:

            print(f"Gambar {i} gagal dibaca!")

            output.write("Gambar gagal dibaca!\n")

            continue

        # ======================================
        # GRAYSCALE
        # ======================================

        gray = cv2.cvtColor(
            gambar,
            cv2.COLOR_BGR2GRAY
        )

        # ======================================
        # 1. CITRA ASLI
        # ======================================

        original = gray.copy()

        # ======================================
        # 2. BRIGHTNESS ADJUSTMENT
        # Sama seperti enhancement.py
        # ======================================

        brightness = cv2.convertScaleAbs(
            gray,
            alpha=1.0,
            beta=40
        )

        # ======================================
        # 3. CONTRAST STRETCHING
        # Sama seperti enhancement.py
        # ======================================

        min_val = np.min(gray)
        max_val = np.max(gray)

        if max_val > min_val:

            contrast_stretching = (
                (gray.astype(np.float32) - min_val)
                / (max_val - min_val)
                * 255
            ).astype(np.uint8)

        else:

            contrast_stretching = gray.copy()

        # ======================================
        # 4. HISTOGRAM EQUALIZATION
        # Sama seperti enhancement.py
        # ======================================

        histogram_equalization = cv2.equalizeHist(gray)

        # ======================================
        # DAFTAR CITRA
        # ======================================

        daftar_citra = [
            ("Citra Asli", original),
            ("Brightness Adjustment", brightness),
            ("Contrast Stretching", contrast_stretching),
            ("Histogram Equalization", histogram_equalization)
        ]

        # ======================================
        # OCR
        # ======================================

        for nama_metode, citra in daftar_citra:

            # Threshold untuk membantu OCR
            _, threshold = cv2.threshold(
                citra,
                0,
                255,
                cv2.THRESH_BINARY + cv2.THRESH_OTSU
            )

            # OCR
            hasil = pytesseract.image_to_string(
                threshold,
                config="--psm 7"
            )

            # Membersihkan hasil
            hasil = hasil.strip()

            if hasil == "":
                hasil = "(Tidak terbaca)"

            # ==================================
            # TAMPILKAN DI TERMINAL
            # ==================================

            print(f"\n{nama_metode}")
            print("-" * 40)
            print(hasil)

            # ==================================
            # SIMPAN KE TXT
            # ==================================

            output.write(f"\n{nama_metode}\n")
            output.write("-" * 40 + "\n")
            output.write(hasil + "\n")


print("\n" + "=" * 70)
print("SEMUA OCR SELESAI!")
print("=" * 70)

print(f"Hasil OCR disimpan di:")
print(file_hasil)