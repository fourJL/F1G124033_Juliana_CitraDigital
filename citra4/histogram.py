import cv2
import matplotlib.pyplot as plt
import numpy as np
import os

# Folder tempat gambar berada
folder = r"D:\citra4"

# Folder untuk menyimpan hasil histogram
folder_hasil = os.path.join(folder, "hasil_histogram")
os.makedirs(folder_hasil, exist_ok=True)

# Memproses gambar 1 sampai 9
for i in range(1, 10):

    # Mencari file gambar berdasarkan nomor
    nama_awal = f"{i:02d}_"

    daftar_file = [
        file for file in os.listdir(folder)
        if file.startswith(nama_awal)
        and file.lower().endswith((".jpg", ".jpeg", ".png"))
    ]

    if len(daftar_file) == 0:
        print(f"Gambar {i} tidak ditemukan!")
        continue

    # Membaca citra asli
    path_gambar = os.path.join(folder, daftar_file[0])
    gambar = cv2.imread(path_gambar)

    if gambar is None:
        print(f"Gambar {i} gagal dibaca!")
        continue

    # Mengubah citra menjadi grayscale
    gray = cv2.cvtColor(gambar, cv2.COLOR_BGR2GRAY)

    # ==========================================
    # 1. BRIGHTNESS ADJUSTMENT
    # ==========================================
    brightness = cv2.convertScaleAbs(
        gray,
        alpha=1.0,
        beta=40
    )

    # ==========================================
    # 2. CONTRAST STRETCHING
    # ==========================================
    min_val = np.min(gray)
    max_val = np.max(gray)

    if max_val > min_val:
        contrast_stretching = (
            (gray.astype(np.float32) - min_val)
            / (max_val - min_val) * 255
        ).astype(np.uint8)
    else:
        contrast_stretching = gray.copy()

    # ==========================================
    # 3. HISTOGRAM EQUALIZATION
    # ==========================================
    histogram_equalization = cv2.equalizeHist(gray)

    # ==========================================
    # DATA CITRA
    # ==========================================
    citra = [
        gray,
        brightness,
        contrast_stretching,
        histogram_equalization
    ]

    judul = [
        "Histogram Citra Asli",
        "Histogram Brightness Adjustment",
        "Histogram Contrast Stretching",
        "Histogram Equalization"
    ]

    # ==========================================
    # MENAMPILKAN 4 HISTOGRAM
    # ==========================================
    plt.figure(figsize=(14, 8))

    for j in range(4):

        plt.subplot(2, 2, j + 1)

        # Menghitung histogram
        histogram = cv2.calcHist(
            [citra[j]],
            [0],
            None,
            [256],
            [0, 256]
        )

        plt.plot(histogram)

        plt.title(judul[j])
        plt.xlabel("Intensitas Piksel")
        plt.ylabel("Jumlah Piksel")
        plt.xlim([0, 256])
        plt.grid(True, alpha=0.3)

    plt.suptitle(
        f"Perbandingan Histogram Gambar {i}",
        fontsize=16
    )

    plt.tight_layout()

    # Menyimpan hasil histogram
    nama_hasil = os.path.join(
        folder_hasil,
        f"histogram_{i}.png"
    )

    plt.savefig(nama_hasil, dpi=150)

    # Menampilkan histogram
    plt.show()

    plt.close()

    print(f"Histogram gambar {i} berhasil dibuat!")
    print(f"Hasil disimpan: {nama_hasil}")

print("Semua histogram gambar 1 sampai 9 selesai dibuat!")