import cv2
import matplotlib.pyplot as plt
import numpy as np
import os

# ==========================================
# FOLDER GAMBAR
# ==========================================

folder = r"D:\citra4"

# ==========================================
# FOLDER HASIL
# ==========================================

folder_hasil = os.path.join(folder, "hasil_enhancement_histogram")
os.makedirs(folder_hasil, exist_ok=True)

# ==========================================
# PROSES GAMBAR 1 SAMPAI 9
# ==========================================

for i in range(1, 10):

    # Nama awal file
    nama_awal = f"{i:02d}_"

    # Mencari file JPG
    daftar_file = [
        file for file in os.listdir(folder)
        if file.startswith(nama_awal)
        and file.lower().endswith(".jpg")
    ]

    # Jika gambar tidak ditemukan
    if len(daftar_file) == 0:
        print(f"Gambar {i} tidak ditemukan!")
        continue

    # Mengambil nama file
    nama_file = daftar_file[0]

    # Lokasi gambar
    path_gambar = os.path.join(folder, nama_file)

    # ==========================================
    # MEMBACA GAMBAR
    # ==========================================

    gambar = cv2.imread(path_gambar)

    if gambar is None:
        print(f"Gambar {i} gagal dibaca!")
        continue

    # ==========================================
    # GRAYSCALE
    # ==========================================

    gray = cv2.cvtColor(
        gambar,
        cv2.COLOR_BGR2GRAY
    )

    # ==========================================
    # 1. CITRA ASLI
    # ==========================================

    original = gray.copy()

    # ==========================================
    # 2. BRIGHTNESS ADJUSTMENT
    # Sesuai enhancement.py sebelumnya
    # ==========================================

    brightness = cv2.convertScaleAbs(
        gray,
        alpha=1.0,
        beta=40
    )

    # ==========================================
    # 3. CONTRAST STRETCHING
    # ==========================================

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

    # ==========================================
    # 4. HISTOGRAM EQUALIZATION
    # ==========================================

    histogram_equalization = cv2.equalizeHist(gray)

    # ==========================================
    # DAFTAR CITRA
    # ==========================================

    daftar_citra = [
        ("Citra Asli (Grayscale)", original),
        ("Brightness Adjustment (beta=40)", brightness),
        ("Contrast Stretching", contrast_stretching),
        ("Histogram Equalization", histogram_equalization)
    ]

    # ==========================================
    # MEMBUAT FIGURE
    # ==========================================

    fig, axes = plt.subplots(
        4, 2,
        figsize=(14, 14)
    )

    fig.suptitle(
        f"Perbandingan Enhancement - {nama_file}",
        fontsize=16
    )

    # ==========================================
    # TAMPILKAN CITRA + HISTOGRAM
    # ==========================================

    for baris, (nama_metode, citra) in enumerate(daftar_citra):

        # ------------------------------
        # CITRA
        # ------------------------------

        axes[baris, 0].imshow(
            citra,
            cmap="gray"
        )

        axes[baris, 0].set_title(
            nama_metode
        )

        axes[baris, 0].axis("off")

        # ------------------------------
        # HISTOGRAM
        # ------------------------------

        histogram = cv2.calcHist(
            [citra],
            [0],
            None,
            [256],
            [0, 256]
        )

        axes[baris, 1].plot(
            histogram
        )

        axes[baris, 1].set_title(
            f"Histogram {nama_metode}"
        )

        axes[baris, 1].set_xlim(
            [0, 256]
        )

        axes[baris, 1].set_xlabel(
            "Intensitas Piksel"
        )

        axes[baris, 1].set_ylabel(
            "Jumlah Piksel"
        )

        axes[baris, 1].grid(
            True,
            alpha=0.2
        )

    # ==========================================
    # MERAPIKAN TAMPILAN
    # ==========================================

    plt.tight_layout(
        rect=[0, 0, 1, 0.97]
    )

    # ==========================================
    # SIMPAN HASIL
    # ==========================================

    nama_hasil = os.path.join(
        folder_hasil,
        f"enhancement_histogram_{i}.png"
    )

    plt.savefig(
        nama_hasil,
        dpi=200,
        bbox_inches="tight"
    )

    plt.show()

    print("=" * 60)
    print(f"Gambar {i} berhasil diproses!")
    print(f"Hasil: {nama_hasil}")

# ==========================================
# SELESAI
# ==========================================

print("\n" + "=" * 60)
print("SEMUA GAMBAR 1 SAMPAI 9 SELESAI!")
print("=" * 60)
print(f"Hasil tersimpan di:")
print(folder_hasil)