# DETEKSI TANDA TANGAN

Program ini merupakan implementasi Pengolahan Citra Digital untuk mendeteksi keberadaan tanda tangan pada citra dokumen.

Program mengolah dua kategori citra, yaitu:

- **Signature Present**: citra yang memiliki tanda tangan.
- **Signature Absent**: citra sampel yang tidak memiliki tanda tangan.

## Metode Pengolahan

Tahapan pengolahan citra yang digunakan dalam program ini meliputi:

1. Membaca citra.
2. Konversi citra ke **grayscale**.
3. **Global Thresholding** untuk melakukan segmentasi foreground dan background.
4. **Otsu Thresholding** untuk melakukan segmentasi secara otomatis berdasarkan nilai threshold.
5. **Morphological Opening** untuk membantu mengurangi noise dan objek kecil.
6. **Morphological Closing** untuk membantu menghubungkan bagian foreground yang terputus.
7. Menghitung karakteristik hasil segmentasi.
8. Menghitung jumlah **foreground pixel**.
9. Menghitung jumlah **background pixel**.
10. Menghitung persentase foreground.
11. Menentukan prediksi **Signature Present** atau **Signature Absent**.
12. Membuat gambar perbandingan seluruh hasil pengolahan.

## Dataset

Dataset terdiri dari 18 citra yang dibagi menjadi dua kategori.

### Signature Present

Folder:

```text
tugasCitra/
```

Berisi 9 citra:

```text
01_HighQuality_Enhanced (2)(1).jpg
02_LowContrast (2).jpg
03_Blurred (2).jpg
04_HighNoise (2).jpg
05_LowResolution_Upsampled (2).jpg
06_Faded_Underexposed (2).jpg
07_ColorShift_WarmTint (2).jpg
08_JPEGCompression_Artifacts (2).jpg
09_CombinedDegradation (2).jpg
```

### Signature Absent

Folder:

```text
hasil_sample/
```

Berisi 9 citra sampel:

```text
sample_01.jpg
sample_02.jpg
sample_03.jpg
sample_04.jpg
sample_05.jpg
sample_06.jpg
sample_07.jpg
sample_08.jpg
sample_09.jpg
```

## Struktur Folder Project

Struktur project yang digunakan:

```text
citra6/
│
├── tugasCitra/
│   ├── 01_HighQuality_Enhanced (2)(1).jpg
│   ├── 02_LowContrast (2).jpg
│   ├── 03_Blurred (2).jpg
│   ├── 04_HighNoise (2).jpg
│   ├── 05_LowResolution_Upsampled (2).jpg
│   ├── 06_Faded_Underexposed (2).jpg
│   ├── 07_ColorShift_WarmTint (2).jpg
│   ├── 08_JPEGCompression_Artifacts (2).jpg
│   └── 09_CombinedDegradation (2).jpg
│
├── hasil_sample/
│   ├── sample_01.jpg
│   ├── sample_02.jpg
│   ├── sample_03.jpg
│   ├── sample_04.jpg
│   ├── sample_05.jpg
│   ├── sample_06.jpg
│   ├── sample_07.jpg
│   ├── sample_08.jpg
│   └── sample_09.jpg
│
├── test.py
└── README.md
```

Setelah program dijalankan, folder hasil akan dibuat secara otomatis.

## Requirements

Program membutuhkan:

- Python 3.x
- OpenCV
- NumPy
- Matplotlib

## Instalasi Library

Buka terminal pada folder project, kemudian jalankan:

```bash
pip install opencv-python numpy matplotlib
```

Untuk memastikan Python sudah terpasang, jalankan:

```bash
python --version
```

Jika perintah `python` tidak tersedia, dapat mencoba:

```bash
py --version
```

## Cara Menjalankan Program

### 1. Buka folder project

Contoh lokasi project:

```text
D:\citra6
```

Pada CMD, jalankan:

```bash
cd /d D:\citra6
```

Jika menggunakan terminal VS Code, buka folder project `citra6`.

### 2. Pastikan dataset tersedia

Sebelum menjalankan program, pastikan folder berikut berada di dalam folder project:

```text
tugasCitra/
hasil_sample/
```

Pastikan masing-masing folder berisi 9 citra.

### 3. Jalankan program

Jalankan:

```bash
python test.py
```

atau:

```bash
py test.py
```

Program kemudian akan memproses seluruh citra dari folder `tugasCitra` dan `hasil_sample`.

## Alur Program

Secara umum, proses program adalah:

```text
Citra Asli
    │
    ▼
Grayscale
    │
    ├───────────────┐
    ▼               ▼
Otsu          Global Threshold
    │               │
    ├──────┐        ├──────┐
    ▼      ▼        ▼      ▼
Opening Closing   Opening Closing
    │      │        │      │
    └──────┴────────┴──────┘
              │
              ▼
   Karakteristik Segmentasi
              │
              ▼
     Foreground Pixel
              │
              ▼
     Foreground (%)
              │
              ▼
          Prediksi
```

## Karakteristik Segmentasi

Untuk setiap hasil segmentasi, program menghitung beberapa karakteristik, yaitu:

- Total pixel
- Foreground pixel
- Background pixel
- Persentase foreground
- Persentase background
- Nilai threshold Global
- Nilai threshold Otsu

Foreground dihitung berdasarkan jumlah pixel bernilai putih pada hasil citra biner.

Persentase foreground dihitung dengan rumus:

```text
Foreground (%) =
(Foreground Pixel / Total Pixel) × 100%
```

## Thresholding

### Global Threshold

Global Threshold menggunakan nilai threshold yang telah ditentukan untuk memisahkan foreground dan background.

Pada program digunakan nilai:

```text
Threshold Global = 127
```

### Otsu Threshold

Otsu digunakan untuk menentukan nilai threshold secara otomatis berdasarkan distribusi intensitas citra.

Nilai threshold Otsu ditampilkan pada terminal untuk setiap citra yang diproses.

## Morphological Operation

Setelah proses thresholding, hasil segmentasi diperbaiki menggunakan dua operasi morfologi.

### Opening

Opening digunakan untuk membantu mengurangi noise atau objek kecil pada hasil segmentasi.

Urutannya adalah:

```text
Erosion → Dilation
```

### Closing

Closing digunakan untuk membantu menghubungkan bagian foreground yang terputus dan mengisi celah kecil pada objek.

Urutannya adalah:

```text
Dilation → Erosion
```

Program menggunakan kernel morfologi berukuran:

```text
3 × 3
```

## Klasifikasi Signature

Prediksi keberadaan tanda tangan dilakukan berdasarkan persentase foreground.

Batas klasifikasi yang digunakan adalah:

```text
Foreground >= 3,00%
        ↓
Signature Present

Foreground < 3,00%
        ↓
Signature Absent
```

## Output Program

Setelah program selesai dijalankan, hasil pengolahan akan tersimpan dalam folder:

```text
hasil_proses/
```

Struktur output:

```text
hasil_proses/
│
├── signature_present/
│   ├── grayscale/
│   ├── otsu/
│   ├── global/
│   ├── otsu_opening/
│   ├── otsu_closing/
│   ├── global_opening/
│   ├── global_closing/
│   └── perbandingan/
│
└── signature_absent/
    ├── grayscale/
    ├── otsu/
    ├── global/
    ├── otsu_opening/
    ├── otsu_closing/
    ├── global_opening/
    ├── global_closing/
    └── perbandingan/
```

## Jenis File Output

Untuk setiap citra akan dihasilkan beberapa file berdasarkan tahapan pengolahan:

```text
Grayscale
Otsu
Global Threshold
Otsu Opening
Otsu Closing
Global Opening
Global Closing
```

Selain itu, program membuat folder `perbandingan/` yang berisi gambar perbandingan dari satu citra. Gambar tersebut menampilkan citra asli, grayscale, Otsu, Global Threshold, Otsu Opening, Otsu Closing, Global Opening, Global Closing, serta catatan hasil perbandingan.

## Output Terminal

Saat program dijalankan, informasi setiap citra akan ditampilkan pada terminal, meliputi:

- Nama citra
- Ukuran citra
- Threshold Global
- Threshold Otsu
- Total pixel
- Foreground pixel
- Background pixel
- Persentase foreground
- Persentase background
- Hasil Opening
- Hasil Closing
- Catatan hasil perbandingan

## Catatan Hasil Perbandingan

Program juga membuat catatan otomatis berdasarkan perubahan jumlah foreground setelah proses opening dan closing.

Catatan digunakan untuk melihat:

- Perubahan foreground setelah Otsu Opening.
- Perubahan foreground setelah Otsu Closing.
- Perubahan foreground setelah Global Opening.
- Perubahan foreground setelah Global Closing.
- Perbandingan area foreground antara Otsu dan Global Threshold.

Catatan tersebut ditampilkan pada terminal dan juga dimasukkan ke dalam gambar hasil perbandingan.

## Tujuan Program

Program ini digunakan untuk melakukan pengujian terhadap proses segmentasi citra pada dua kategori dataset, yaitu **Signature Present** dan **Signature Absent**. Hasil pengolahan dapat digunakan untuk melihat perbedaan karakteristik foreground pada kedua kategori serta mengevaluasi hasil segmentasi menggunakan metode thresholding dan morphological operation.

## Author

**Juliana**  
Program Studi Ilmu Komputer  
Fakultas Matematika dan Ilmu Pengetahuan Alam  
Universitas Halu Oleo  

**Tahun: 2026**
