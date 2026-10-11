import cv2
import numpy as np
import matplotlib.pyplot as plt
import pytesseract
import csv
from pathlib import Path

# ==========================================================
# KONFIGURASI TESSERACT OCR
# ==========================================================
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
CUSTOM_OEM_PSM_CONFIG = r'--oem 3 --psm 6'

# ==========================================================
# GROUND TRUTH (Opsional)
# ==========================================================
GROUND_TRUTH = {}

# ==========================================================
# KONFIGURASI FOLDER
# ==========================================================
folder_input = Path("citra_ijazah")

folder_mean = Path("hasil/mean_filter")
folder_median = Path("hasil/median_filter")
folder_gaussian = Path("hasil/gaussian_filter")
folder_sharpening = Path("hasil/sharpening")
folder_perbandingan = Path("hasil/perbandingan")
folder_laporan = Path("hasil/laporan")

for f in [folder_mean, folder_median, folder_gaussian, folder_sharpening, folder_perbandingan, folder_laporan]:
    f.mkdir(parents=True, exist_ok=True)

# ==========================================================
# FUNGSI FILTERING & SHARPENING
# ==========================================================
def apply_mean_filter(gray, kernel_size=3):
    return cv2.blur(gray, (kernel_size, kernel_size))

def apply_median_filter(gray, kernel_size=3):
    return cv2.medianBlur(gray, kernel_size)

def apply_gaussian_filter(gray, kernel_size=3, sigma=0):
    return cv2.GaussianBlur(gray, (kernel_size, kernel_size), sigma)

def apply_sharpening(gray):
    kernel = np.array([[0, -1, 0],
                       [-1, 5, -1],
                       [0, -1, 0]])
    return cv2.filter2D(gray, -1, kernel)

# ==========================================================
# FUNGSI MEMBUAT BANNER HEADER (Hitam Teks Putih)
# ==========================================================
def tambahkan_banner(img, judul_teks):
    h, w = img.shape[:2]
    banner_height = int(h * 0.25) if int(h * 0.25) > 25 else 25
    
    # Buat banner hitam
    if len(img.shape) == 2:
        banner = np.zeros((banner_height, w), dtype=np.uint8)
    else:
        banner = np.zeros((banner_height, w, 3), dtype=np.uint8)
        
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 0.5
    thickness = 1
    
    # Hitung ukuran teks agar center
    text_size = cv2.getTextSize(judul_teks, font, font_scale, thickness)[0]
    text_x = (w - text_size[0]) // 2
    text_y = (banner_height + text_size[1]) // 2
    
    cv2.putText(banner, judul_teks, (text_x, text_y), font, font_scale, (255, 255, 255), thickness, cv2.LINE_AA)
    
    # Gabungkan banner di atas gambar
    return np.vstack([banner, img])

# ==========================================================
# FUNGSI EVALUASI AKURASI (Abaikan Spasi)
# ==========================================================
def hitung_akurasi_tanpa_spasi(ground_truth, hasil_ocr):
    target = ground_truth.replace(" ", "").strip()
    pred = hasil_ocr.replace(" ", "").strip()
    
    if not target:
        return 0, 0.0
    
    m, n = len(target), len(pred)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m + 1): dp[i][0] = i
    for j in range(n + 1): dp[0][j] = j
    
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if target[i-1] == pred[j-1]:
                dp[i][j] = dp[i-1][j-1]
            else:
                dp[i][j] = 1 + min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1])
                
    karakter_salah = dp[m][n]
    karakter_benar = max(0, len(target) - karakter_salah)
    akurasi = (karakter_benar / len(target)) * 100
    
    return karakter_benar, akurasi

# ==========================================================
# MENCARI SEMUA GAMBAR
# ==========================================================
daftar_gambar = sorted(
    list(folder_input.glob("*.jpg")) + list(folder_input.glob("*.jpeg")) +
    list(folder_input.glob("*.png")) + list(folder_input.glob("*.bmp"))
)

if not daftar_gambar:
    print(f"Tidak ditemukan gambar di folder: {folder_input}")
    exit()

semua_rekap = []

for nomor, file_gambar in enumerate(daftar_gambar, start=1):
    nama = file_gambar.stem
    
    gambar = cv2.imread(str(file_gambar))
    if gambar is None:
        continue

    # Simpan versi RGB untuk Original agar tampil berwarna jika citra aslinya berwarna
    gambar_rgb = cv2.cvtColor(gambar, cv2.COLOR_BGR2RGB)
    gray = cv2.cvtColor(gambar, cv2.COLOR_BGR2GRAY)
    
    # Process Filtering & Sharpening
    hasil_dict = {
        "ORIGINAL": gambar_rgb,
        "MEAN FILTER": apply_mean_filter(gray),
        "MEDIAN FILTER": apply_median_filter(gray),
        "GAUSSIAN FILTER": apply_gaussian_filter(gray),
        "SHARPENING": apply_sharpening(gray)
    }

    # Simpan Gambar Hasil
    cv2.imwrite(str(folder_mean / f"{nama}_mean.jpg"), hasil_dict["MEAN FILTER"])
    cv2.imwrite(str(folder_median / f"{nama}_median.jpg"), hasil_dict["MEDIAN FILTER"])
    cv2.imwrite(str(folder_gaussian / f"{nama}_gaussian.jpg"), hasil_dict["GAUSSIAN FILTER"])
    cv2.imwrite(str(folder_sharpening / f"{nama}_sharpening.jpg"), hasil_dict["SHARPENING"])

    # OCR Processing
    ocr_results = {}
    for metode, img_proc in hasil_dict.items():
        if metode == "ORIGINAL":
            img_ocr = gray
        else:
            img_ocr = img_proc
            
        raw_text = pytesseract.image_to_string(img_ocr, config=CUSTOM_OEM_PSM_CONFIG).strip()
        ocr_results[metode] = raw_text.replace('\n', ' ')

    gt_text = GROUND_TRUTH.get(nama, ocr_results["SHARPENING"] if len(ocr_results["SHARPENING"]) > len(ocr_results["ORIGINAL"]) else ocr_results["ORIGINAL"])

    # TAMPILAN TERMINAL DENGAN GAYA BERBEDA
    print("\n" + "=" * 90)
    print(f" FILE: {nama}.jpg  [{nomor}/{len(daftar_gambar)}]")
    print("=" * 90)
    print(f" Ground Truth Ref : {gt_text}")
    print(" Catatan          : Karakter dihitung tanpa karakter spasi.")
    print("-" * 90)
    
    print(f"{'Metode':<18} | {'Hasil OCR':<40} | {'Char Benar':<12} | {'Akurasi':<10}")
    print("-" * 90)

    for metode, hasil_ocr_bersih in ocr_results.items():
        char_benar, akurasi = hitung_akurasi_tanpa_spasi(gt_text, hasil_ocr_bersih)
        str_benar = f"{char_benar}"
        str_akurasi = f"{akurasi:.2f}%"

        print(f"{metode:<18} | {hasil_ocr_bersih:<40} | {str_benar:<12} | {str_akurasi:<10}")
        
        semua_rekap.append({
            "File": nama,
            "Ground Truth": gt_text,
            "Metode": metode,
            "Hasil OCR": hasil_ocr_bersih,
            "Karakter Benar": str_benar,
            "Akurasi": str_akurasi
        })
        
    print("-" * 90)

    # ==========================================================
    # VISUALISASI MATPLOTLIB (LAYOUT SESUAI DRAFT TEMAN)
    # ==========================================================
    fig = plt.figure(figsize=(10, 6))
    gs = fig.add_gridspec(3, 2, height_ratios=[1, 1, 1])

    # 1. Original (Atas, Tengah/Spanning 2 Kolom)
    ax_orig = fig.add_subplot(gs[0, :])
    img_banner_orig = tambahkan_banner(hasil_dict["ORIGINAL"], "ORIGINAL")
    ax_orig.imshow(img_banner_orig)
    ax_orig.axis("off")

    # 2. Mean Filter (Tengah Kiri)
    ax_mean = fig.add_subplot(gs[1, 0])
    img_banner_mean = tambahkan_banner(hasil_dict["MEAN FILTER"], "MEAN FILTER")
    ax_mean.imshow(img_banner_mean, cmap="gray")
    ax_mean.axis("off")

    # 3. Median Filter (Tengah Kanan)
    ax_median = fig.add_subplot(gs[1, 1])
    img_banner_median = tambahkan_banner(hasil_dict["MEDIAN FILTER"], "MEDIAN FILTER")
    ax_median.imshow(img_banner_median, cmap="gray")
    ax_median.axis("off")

    # 4. Gaussian Filter (Bawah Kiri)
    ax_gauss = fig.add_subplot(gs[2, 0])
    img_banner_gauss = tambahkan_banner(hasil_dict["GAUSSIAN FILTER"], "GAUSSIAN FILTER")
    ax_gauss.imshow(img_banner_gauss, cmap="gray")
    ax_gauss.axis("off")

    # 5. Sharpening (Bawah Kanan)
    ax_sharp = fig.add_subplot(gs[2, 1])
    img_banner_sharp = tambahkan_banner(hasil_dict["SHARPENING"], "SHARPENING")
    ax_sharp.imshow(img_banner_sharp, cmap="gray")
    ax_sharp.axis("off")

    plt.tight_layout()
    plt.savefig(str(folder_perbandingan / f"{nama}_perbandingan.png"), dpi=200, bbox_inches='tight')
    plt.close()

# ==========================================================
# SIMPAN TABEL REKAPITULASI KE CSV
# ==========================================================
path_csv = folder_laporan / "rekapitulasi_ocr.csv"
header = ["File", "Ground Truth", "Metode", "Hasil OCR", "Karakter Benar", "Akurasi"]

with open(path_csv, mode='w', newline='', encoding='utf-8') as file_csv:
    writer = csv.DictWriter(file_csv, fieldnames=header)
    writer.writeheader()
    writer.writerows(semua_rekap)

print("\n" + "=" * 90)
print(f"PROSES SELESAI! Laporan CSV tersimpan di: {path_csv}")
print("=" * 90)