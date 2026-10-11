import cv2
import os


# ==========================================================
# KONFIGURASI
# ==========================================================

FOLDER_PRESENT = "tugasCitra"
FOLDER_ABSENT = "hasil_sample"

# Batas klasifikasi
BATAS_DETEKSI = 2.00


# ==========================================================
# FUNGSI SEGMENTASI
# ==========================================================

def segmentasi(image):

    # Grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Otsu Threshold
    threshold, binary = cv2.threshold(
        gray,
        0,
        255,
        cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU
    )

    return binary, threshold


# ==========================================================
# MENGAMBIL DATA CITRA
# ==========================================================

def ambil_file(folder):

    if not os.path.exists(folder):
        print(f"Folder tidak ditemukan: {folder}")
        return []

    files = []

    for file in os.listdir(folder):

        if file.lower().endswith(
            (".jpg", ".jpeg", ".png", ".bmp")
        ):
            files.append(file)

    files.sort()

    return files


# ==========================================================
# PROSES SATU CITRA
# ==========================================================

def proses_citra(folder, filename, label):

    path = os.path.join(folder, filename)

    image = cv2.imread(path)

    if image is None:
        return None

    # Segmentasi
    binary, threshold = segmentasi(image)

    # Total pixel
    total_pixel = binary.shape[0] * binary.shape[1]

    # Foreground pixel
    foreground = cv2.countNonZero(binary)

    # Persentase foreground
    fg_persen = (foreground / total_pixel) * 100

    # ------------------------------------------
    # PREDIKSI
    # ------------------------------------------

    if fg_persen >= BATAS_DETEKSI:
        hasil_deteksi = "SIGNATURE PRESENT"
    else:
        hasil_deteksi = "SIGNATURE ABSENT"

    # ------------------------------------------
    # CEK BENAR / SALAH
    # ------------------------------------------

    if label == "PRESENT":
        if hasil_deteksi == "SIGNATURE PRESENT":
            status = "BENAR"
        else:
            status = "SALAH"

    else:
        if hasil_deteksi == "SIGNATURE ABSENT":
            status = "BENAR"
        else:
            status = "SALAH"

    return {
        "filename": filename,
        "label": label,
        "foreground": foreground,
        "total_pixel": total_pixel,
        "fg_persen": fg_persen,
        "hasil_deteksi": hasil_deteksi,
        "status": status
    }


# ==========================================================
# HEADER
# ==========================================================

print()
print("=" * 115)
print("                 HASIL DETEKSI KEBERADAAN TANDA TANGAN")
print("=" * 115)

print()

# Header tabel
print(
    f"{'No':<4}"
    f"{'Nama File':<43}"
    f"{'Label':<10}"
    f"{'Foreground':<13}"
    f"{'Total Pixel':<14}"
    f"{'FG (%)':<10}"
    f"{'Hasil Deteksi':<22}"
    f"{'Status':<8}"
)

print("-" * 115)


# ==========================================================
# AMBIL DATA
# ==========================================================

files_present = ambil_file(FOLDER_PRESENT)
files_absent = ambil_file(FOLDER_ABSENT)

hasil_semua = []


# ==========================================================
# PROSES SIGNATURE PRESENT
# ==========================================================

for filename in files_present:

    hasil = proses_citra(
        FOLDER_PRESENT,
        filename,
        "PRESENT"
    )

    if hasil is not None:
        hasil_semua.append(hasil)


# ==========================================================
# PROSES SIGNATURE ABSENT
# ==========================================================

for filename in files_absent:

    hasil = proses_citra(
        FOLDER_ABSENT,
        filename,
        "ABSENT"
    )

    if hasil is not None:
        hasil_semua.append(hasil)


# ==========================================================
# TAMPILKAN TABEL
# ==========================================================

for no, data in enumerate(hasil_semua, start=1):

    print(
        f"{no:<4}"
        f"{data['filename']:<43}"
        f"{data['label']:<10}"
        f"{data['foreground']:<13}"
        f"{data['total_pixel']:<14}"
        f"{data['fg_persen']:<10.2f}"
        f"{data['hasil_deteksi']:<22}"
        f"{data['status']:<8}"
    )


# ==========================================================
# KETERANGAN
# ==========================================================

print()
print("=" * 115)
print("KETERANGAN")
print("=" * 115)

print()

print("PRESENT = gambar yang memiliki tanda tangan.")
print("ABSENT  = gambar yang tidak memiliki tanda tangan.")
print("Foreground Pixel = jumlah piksel foreground setelah segmentasi.")
print("Foreground (%) = persentase foreground terhadap seluruh piksel.")
print(f"Batas deteksi = {BATAS_DETEKSI:.2f}%.")

print(
    "Jika Foreground (%) >= batas, hasil = SIGNATURE PRESENT."
)

print(
    "Jika Foreground (%) < batas, hasil = SIGNATURE ABSENT."
)


# ==========================================================
# EVALUASI SISTEM
# ==========================================================

total_data = len(hasil_semua)

prediksi_benar = 0
prediksi_salah = 0

for data in hasil_semua:

    if data["status"] == "BENAR":
        prediksi_benar += 1
    else:
        prediksi_salah += 1


# Akurasi
if total_data > 0:
    akurasi = (prediksi_benar / total_data) * 100
else:
    akurasi = 0


# ==========================================================
# TAMPILKAN EVALUASI
# ==========================================================

print()
print("=" * 115)
print("EVALUASI SISTEM")
print("=" * 115)

print()

print(f"{'Total data':<20}: {total_data}")
print(f"{'Prediksi benar':<20}: {prediksi_benar}")
print(f"{'Prediksi salah':<20}: {prediksi_salah}")
print(f"{'Akurasi':<20}: {akurasi:.2f}%")

print()
print("=" * 115)
print("PROGRAM SELESAI")
print("=" * 115)