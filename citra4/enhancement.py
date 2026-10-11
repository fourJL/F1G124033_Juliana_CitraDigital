import cv2
import matplotlib.pyplot as plt
import numpy as np
import os

# Folder tempat gambar berada
folder = r"D:\citra4"

# Folder untuk menyimpan hasil enhancement
folder_hasil = os.path.join(folder, "hasil_enhancement")
os.makedirs(folder_hasil, exist_ok=True)

# Perulangan untuk memproses gambar 1 sampai 9
for i in range(1, 10):

    # Nama file gambar
    nama_file = f"{i:02d}_"

    # Mencari file JPG yang diawali nomor gambar
    daftar_file = [
        file for file in os.listdir(folder)
        if file.startswith(nama_file) and file.lower().endswith(".jpg")
    ]

    # Mengecek apakah file ditemukan
    if len(daftar_file) == 0:
        print(f"Gambar {i} tidak ditemukan!")
        continue

    # Mengambil nama file gambar
    path_gambar = os.path.join(folder, daftar_file[0])

    # Membaca citra
    gambar = cv2.imread(path_gambar)

    if gambar is None:
        print(f"Gambar {i} gagal dibaca!")
        continue

    # Mengubah BGR menjadi RGB
    gambar_rgb = cv2.cvtColor(gambar, cv2.COLOR_BGR2RGB)

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
    # MENAMPILKAN 4 CITRA
    # ==========================================
    plt.figure(figsize=(16, 5))

    # Citra asli
    plt.subplot(1, 4, 1)
    plt.imshow(gambar_rgb)
    plt.title(f"Citra Asli {i}")
    plt.axis("off")

    # Brightness Adjustment
    plt.subplot(1, 4, 2)
    plt.imshow(brightness, cmap="gray")
    plt.title("Brightness Adjustment")
    plt.axis("off")

    # Contrast Stretching
    plt.subplot(1, 4, 3)
    plt.imshow(contrast_stretching, cmap="gray")
    plt.title("Contrast Stretching")
    plt.axis("off")

    # Histogram Equalization
    plt.subplot(1, 4, 4)
    plt.imshow(histogram_equalization, cmap="gray")
    plt.title("Histogram Equalization")
    plt.axis("off")

    plt.suptitle(f"Hasil Enhancement Gambar {i}", fontsize=14)
    plt.tight_layout()

    # Menyimpan hasil ke folder
    nama_hasil = os.path.join(
        folder_hasil,
        f"hasil_enhancement_{i}.jpg"
    )

    plt.savefig(nama_hasil, dpi=150)

    # Menampilkan hasil
    plt.show()

    print(f"Gambar {i} berhasil diproses!")
    print(f"Hasil disimpan: {nama_hasil}")

print("Semua gambar 1 sampai 9 selesai diproses!")