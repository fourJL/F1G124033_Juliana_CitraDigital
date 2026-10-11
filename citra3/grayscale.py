import cv2
import matplotlib.pyplot as plt
from pathlib import Path

# Menentukan lokasi penyimpanan hasil
folder_output = Path("hasil")
folder_output.mkdir(parents=True, exist_ok=True)

# Daftar 9 gambar
GAMBAR = [f"gambar{nomor}.jpeg" for nomor in range(1, 10)]

for nomor, file_gambar in enumerate(GAMBAR, start=1):

    # Membuka file gambar
    img = cv2.imread(file_gambar)

    if img is None:
        print(f"Gambar {file_gambar} tidak ditemukan!")
        continue

    # Konversi gambar RGB/BGR menjadi grayscale
    hasil_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Menentukan nama file hasil
    file_output = folder_output / f"grayscale{nomor}.jpeg"

    # Menyimpan gambar grayscale
    cv2.imwrite(str(file_output), hasil_gray)

    # Menampilkan hasil
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.imshow(hasil_gray, cmap="gray")
    ax.set_title(f"Grayscale - Gambar {nomor}")
    ax.set_axis_off()
    plt.show()

    print(f"Berhasil: {file_output}")