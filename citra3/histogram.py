import cv2
import matplotlib.pyplot as plt
from pathlib import Path

# Daftar gambar yang akan diproses
GAMBAR = [f"gambar{x}.jpeg" for x in range(1, 10)]

# Folder penyimpanan histogram
folder_hasil = Path("hasil_histogram")
folder_hasil.mkdir(parents=True, exist_ok=True)

for nomor, nama_gambar in enumerate(GAMBAR, 1):

    # Membaca citra
    citra = cv2.imread(nama_gambar)

    if citra is None:
        print(f"Gambar {nama_gambar} tidak ditemukan!")
        continue

    # Konversi warna dan grayscale
    rgb = cv2.cvtColor(citra, cv2.COLOR_BGR2RGB)
    gray = cv2.cvtColor(citra, cv2.COLOR_BGR2GRAY)

    # Membuat tampilan histogram
    fig, axes = plt.subplots(2, 1, figsize=(12, 8))

    # Histogram RGB
    channel_warna = {
        "Red": rgb[:, :, 0],
        "Green": rgb[:, :, 1],
        "Blue": rgb[:, :, 2]
    }

    for nama_channel, data_channel in channel_warna.items():
        axes[0].hist(
            data_channel.flatten(),
            bins=256,
            range=(0, 256),
            alpha=0.5,
            label=nama_channel
        )

    axes[0].set_title(f"Histogram Citra Asli - Gambar {nomor}")
    axes[0].set_xlabel("Intensitas Piksel")
    axes[0].set_ylabel("Jumlah Piksel")
    axes[0].set_xlim(0, 255)
    axes[0].legend()

    # Histogram grayscale
    axes[1].hist(
        gray.flatten(),
        bins=256,
        range=(0, 256)
    )

    axes[1].set_title(f"Histogram Grayscale - Gambar {nomor}")
    axes[1].set_xlabel("Intensitas Piksel")
    axes[1].set_ylabel("Jumlah Piksel")
    axes[1].set_xlim(0, 255)

    # Merapikan layout
    fig.tight_layout()

    # Menentukan nama file hasil
    file_hasil = folder_hasil / f"histogram{nomor}.png"

    # Menyimpan histogram
    fig.savefig(file_hasil)

    # Membersihkan figure dari memori
    plt.close(fig)

    print(f"Berhasil membuat: {file_hasil}")

print("\nSemua histogram selesai dibuat!")