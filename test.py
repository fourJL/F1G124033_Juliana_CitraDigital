import cv2
import os
import numpy as np
import matplotlib.pyplot as plt


# ==========================================================
# KONFIGURASI FOLDER
# ==========================================================

INPUT_FOLDERS = {
    "signature_present": "tugasCitra",
    "signature_absent": "hasil_sample"
}

OUTPUT_FOLDER = "hasil_proses"


# ==========================================================
# MEMBUAT FOLDER OUTPUT
# ==========================================================

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

for kategori in INPUT_FOLDERS:
    os.makedirs(
        os.path.join(OUTPUT_FOLDER, kategori),
        exist_ok=True
    )

    os.makedirs(
        os.path.join(OUTPUT_FOLDER, kategori, "grayscale"),
        exist_ok=True
    )

    os.makedirs(
        os.path.join(OUTPUT_FOLDER, kategori, "otsu"),
        exist_ok=True
    )

    os.makedirs(
        os.path.join(OUTPUT_FOLDER, kategori, "global"),
        exist_ok=True
    )

    os.makedirs(
        os.path.join(OUTPUT_FOLDER, kategori, "otsu_opening"),
        exist_ok=True
    )

    os.makedirs(
        os.path.join(OUTPUT_FOLDER, kategori, "otsu_closing"),
        exist_ok=True
    )

    os.makedirs(
        os.path.join(OUTPUT_FOLDER, kategori, "global_opening"),
        exist_ok=True
    )

    os.makedirs(
        os.path.join(OUTPUT_FOLDER, kategori, "global_closing"),
        exist_ok=True
    )

    os.makedirs(
        os.path.join(OUTPUT_FOLDER, kategori, "perbandingan"),
        exist_ok=True
    )


# ==========================================================
# KERNEL MORFOLOGI
# ==========================================================

kernel = np.ones((3, 3), np.uint8)


# ==========================================================
# FUNGSI MENGHITUNG KARAKTERISTIK SEGMENTASI
# ==========================================================

def hitung_karakteristik(binary):

    total_pixel = binary.shape[0] * binary.shape[1]

    # Karena menggunakan THRESH_BINARY_INV,
    # foreground adalah piksel putih (255)
    foreground = cv2.countNonZero(binary)

    background = total_pixel - foreground

    persentase_foreground = (foreground / total_pixel) * 100
    persentase_background = (background / total_pixel) * 100

    return (
        total_pixel,
        foreground,
        background,
        persentase_foreground,
        persentase_background
    )


# ==========================================================
# FUNGSI MEMBUAT CATATAN HASIL
# ==========================================================

def buat_catatan(
    nama,
    fg_otsu,
    fg_global,
    fg_otsu_open,
    fg_otsu_close,
    fg_global_open,
    fg_global_close
):

    catatan = []

    # ---------------------------------------------
    # Analisis Otsu
    # ---------------------------------------------

    perubahan_open_otsu = fg_otsu_open - fg_otsu
    perubahan_close_otsu = fg_otsu_close - fg_otsu

    if abs(perubahan_open_otsu) < fg_otsu * 0.05:
        catatan.append(
            "Otsu Opening: perubahan foreground relatif kecil."
        )
    elif perubahan_open_otsu < 0:
        catatan.append(
            "Otsu Opening: jumlah foreground berkurang, "
            "menunjukkan sebagian noise atau objek kecil dihilangkan."
        )
    else:
        catatan.append(
            "Otsu Opening: jumlah foreground meningkat."
        )

    if perubahan_close_otsu > 0:
        catatan.append(
            "Otsu Closing: foreground bertambah, "
            "kemungkinan bagian objek yang terputus menjadi lebih terhubung."
        )
    else:
        catatan.append(
            "Otsu Closing: perubahan foreground relatif kecil."
        )

    # ---------------------------------------------
    # Analisis Global
    # ---------------------------------------------

    perubahan_open_global = fg_global_open - fg_global
    perubahan_close_global = fg_global_close - fg_global

    if perubahan_open_global < 0:
        catatan.append(
            "Global Opening: foreground berkurang setelah proses opening."
        )
    else:
        catatan.append(
            "Global Opening: foreground relatif tetap atau meningkat."
        )

    if perubahan_close_global > 0:
        catatan.append(
            "Global Closing: foreground bertambah setelah proses closing."
        )
    else:
        catatan.append(
            "Global Closing: perubahan foreground relatif kecil."
        )

    # ---------------------------------------------
    # Perbandingan Otsu dan Global
    # ---------------------------------------------

    if fg_otsu > fg_global * 1.20:
        catatan.append(
            "Otsu menghasilkan area foreground lebih besar "
            "dibandingkan Global."
        )

    elif fg_global > fg_otsu * 1.20:
        catatan.append(
            "Global menghasilkan area foreground lebih besar "
            "dibandingkan Otsu."
        )

    else:
        catatan.append(
            "Jumlah foreground Otsu dan Global relatif berdekatan."
        )

    return catatan


# ==========================================================
# FUNGSI MEMBUAT GAMBAR PERBANDINGAN
# ==========================================================

def buat_perbandingan(
    original,
    grayscale,
    otsu,
    global_thresh,
    otsu_opening,
    otsu_closing,
    global_opening,
    global_closing,
    nama_file,
    kategori,
    catatan
):

    fig, axes = plt.subplots(3, 3, figsize=(16, 13))

    # ---------------------------------------------
    # Daftar gambar
    # ---------------------------------------------

    gambar = [
        original,
        grayscale,
        otsu,
        global_thresh,
        otsu_opening,
        otsu_closing,
        global_opening,
        global_closing
    ]

    judul = [
        "Citra Asli",
        "Grayscale",
        "Otsu",
        "Global Threshold",
        "Otsu Opening",
        "Otsu Closing",
        "Global Opening",
        "Global Closing"
    ]

    # ---------------------------------------------
    # Menampilkan 8 gambar
    # ---------------------------------------------

    for ax, img, title in zip(axes.flat[:8], gambar, judul):

        if len(img.shape) == 2:
            ax.imshow(img, cmap="gray")
        else:
            ax.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))

        ax.set_title(title)
        ax.axis("off")

    # ---------------------------------------------
    # Kotak catatan di bagian bawah
    # ---------------------------------------------

    axes[2, 2].axis("off")

    teks_catatan = "CATATAN HASIL PERBANDINGAN\n\n"

    for i, teks in enumerate(catatan, start=1):
        teks_catatan += f"{i}. {teks}\n"

    axes[2, 2].text(
        0,
        1,
        teks_catatan,
        fontsize=10,
        verticalalignment="top",
        wrap=True
    )

    fig.suptitle(
        f"Perbandingan Hasil Segmentasi\n"
        f"{kategori} - {nama_file}",
        fontsize=15
    )

    plt.tight_layout()

    # ---------------------------------------------
    # Simpan
    # ---------------------------------------------

    nama_output = os.path.splitext(nama_file)[0] + "_perbandingan.jpg"

    output_path = os.path.join(
        OUTPUT_FOLDER,
        kategori,
        "perbandingan",
        nama_output
    )

    plt.savefig(
        output_path,
        dpi=150,
        bbox_inches="tight"
    )

    plt.close()


# ==========================================================
# PROSES SETIAP KATEGORI
# ==========================================================

for kategori, input_folder in INPUT_FOLDERS.items():

    print("\n")
    print("=" * 80)
    print(f"PROSES DATASET : {kategori.upper()}")
    print("=" * 80)

    files = [
        f for f in os.listdir(input_folder)
        if f.lower().endswith((".jpg", ".jpeg", ".png"))
    ]

    files.sort()

    # ---------------------------------------------
    # PROSES SETIAP CITRA
    # ---------------------------------------------

    for nomor, filename in enumerate(files, start=1):

        print("\n")
        print("-" * 80)
        print(f"CITRA {nomor} : {filename}")
        print("-" * 80)

        input_path = os.path.join(
            input_folder,
            filename
        )

        # -----------------------------------------
        # Membaca citra
        # -----------------------------------------

        original = cv2.imread(input_path)

        if original is None:
            print(f"Gagal membaca: {filename}")
            continue

        # -----------------------------------------
        # GRAYSCALE
        # -----------------------------------------

        grayscale = cv2.cvtColor(
            original,
            cv2.COLOR_BGR2GRAY
        )

        # -----------------------------------------
        # GLOBAL THRESHOLDING
        # -----------------------------------------

        threshold_global = 127

        _, global_thresh = cv2.threshold(
            grayscale,
            threshold_global,
            255,
            cv2.THRESH_BINARY_INV
        )

        # -----------------------------------------
        # OTSU THRESHOLDING
        # -----------------------------------------

        threshold_otsu, otsu = cv2.threshold(
            grayscale,
            0,
            255,
            cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU
        )

        # -----------------------------------------
        # MORPHOLOGICAL OPENING
        # -----------------------------------------

        otsu_opening = cv2.morphologyEx(
            otsu,
            cv2.MORPH_OPEN,
            kernel
        )

        global_opening = cv2.morphologyEx(
            global_thresh,
            cv2.MORPH_OPEN,
            kernel
        )

        # -----------------------------------------
        # MORPHOLOGICAL CLOSING
        # -----------------------------------------

        otsu_closing = cv2.morphologyEx(
            otsu,
            cv2.MORPH_CLOSE,
            kernel
        )

        global_closing = cv2.morphologyEx(
            global_thresh,
            cv2.MORPH_CLOSE,
            kernel
        )

        # ==================================================
        # NAMA DASAR FILE
        # ==================================================

        nama_dasar = os.path.splitext(filename)[0]

        # ==================================================
        # MENYIMPAN SEMUA HASIL
        # ==================================================

        cv2.imwrite(
            os.path.join(
                OUTPUT_FOLDER,
                kategori,
                "grayscale",
                nama_dasar + "_grayscale.jpg"
            ),
            grayscale
        )

        cv2.imwrite(
            os.path.join(
                OUTPUT_FOLDER,
                kategori,
                "otsu",
                nama_dasar + "_otsu.jpg"
            ),
            otsu
        )

        cv2.imwrite(
            os.path.join(
                OUTPUT_FOLDER,
                kategori,
                "global",
                nama_dasar + "_global.jpg"
            ),
            global_thresh
        )

        cv2.imwrite(
            os.path.join(
                OUTPUT_FOLDER,
                kategori,
                "otsu_opening",
                nama_dasar + "_otsu_opening.jpg"
            ),
            otsu_opening
        )

        cv2.imwrite(
            os.path.join(
                OUTPUT_FOLDER,
                kategori,
                "otsu_closing",
                nama_dasar + "_otsu_closing.jpg"
            ),
            otsu_closing
        )

        cv2.imwrite(
            os.path.join(
                OUTPUT_FOLDER,
                kategori,
                "global_opening",
                nama_dasar + "_global_opening.jpg"
            ),
            global_opening
        )

        cv2.imwrite(
            os.path.join(
                OUTPUT_FOLDER,
                kategori,
                "global_closing",
                nama_dasar + "_global_closing.jpg"
            ),
            global_closing
        )

        # ==================================================
        # HITUNG KARAKTERISTIK
        # ==================================================

        data_otsu = hitung_karakteristik(otsu)
        data_global = hitung_karakteristik(global_thresh)
        data_otsu_opening = hitung_karakteristik(otsu_opening)
        data_otsu_closing = hitung_karakteristik(otsu_closing)
        data_global_opening = hitung_karakteristik(global_opening)
        data_global_closing = hitung_karakteristik(global_closing)

        # ==================================================
        # OUTPUT TERMINAL
        # ==================================================

        print(f"Ukuran citra       : {grayscale.shape[1]} x {grayscale.shape[0]}")
        print(f"Threshold Global   : {threshold_global}")
        print(f"Threshold Otsu     : {threshold_otsu:.2f}")

        print("\nKarakteristik hasil segmentasi:")

        print("\n[ OTSU ]")
        print(f"Total piksel       : {data_otsu[0]}")
        print(f"Foreground         : {data_otsu[1]}")
        print(f"Background         : {data_otsu[2]}")
        print(f"% Foreground       : {data_otsu[3]:.2f}%")
        print(f"% Background       : {data_otsu[4]:.2f}%")

        print("\n[ GLOBAL ]")
        print(f"Total piksel       : {data_global[0]}")
        print(f"Foreground         : {data_global[1]}")
        print(f"Background         : {data_global[2]}")
        print(f"% Foreground       : {data_global[3]:.2f}%")
        print(f"% Background       : {data_global[4]:.2f}%")

        print("\n[ OTSU OPENING ]")
        print(f"Foreground         : {data_otsu_opening[1]}")
        print(f"Background         : {data_otsu_opening[2]}")
        print(f"% Foreground       : {data_otsu_opening[3]:.2f}%")

        print("\n[ OTSU CLOSING ]")
        print(f"Foreground         : {data_otsu_closing[1]}")
        print(f"Background         : {data_otsu_closing[2]}")
        print(f"% Foreground       : {data_otsu_closing[3]:.2f}%")

        print("\n[ GLOBAL OPENING ]")
        print(f"Foreground         : {data_global_opening[1]}")
        print(f"Background         : {data_global_opening[2]}")
        print(f"% Foreground       : {data_global_opening[3]:.2f}%")

        print("\n[ GLOBAL CLOSING ]")
        print(f"Foreground         : {data_global_closing[1]}")
        print(f"Background         : {data_global_closing[2]}")
        print(f"% Foreground       : {data_global_closing[3]:.2f}%")

        # ==================================================
        # BUAT CATATAN
        # ==================================================

        catatan = buat_catatan(
            filename,
            data_otsu[1],
            data_global[1],
            data_otsu_opening[1],
            data_otsu_closing[1],
            data_global_opening[1],
            data_global_closing[1]
        )

        # ==================================================
        # BUAT GAMBAR PERBANDINGAN
        # ==================================================

        buat_perbandingan(
            original,
            grayscale,
            otsu,
            global_thresh,
            otsu_opening,
            otsu_closing,
            global_opening,
            global_closing,
            filename,
            kategori,
            catatan
        )

        print("\nCatatan:")
        for teks in catatan:
            print(f"- {teks}")

        print("\nBerhasil diproses.")


# ==========================================================
# SELESAI
# ==========================================================

print("\n")
print("=" * 80)
print("SEMUA CITRA SELESAI DIPROSES")
print("=" * 80)

print(f"Hasil tersimpan di folder: {OUTPUT_FOLDER}")