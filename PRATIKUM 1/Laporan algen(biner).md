# Laporan Praktikum Algoritma Genetika (Biner)

## Identitas
- Nama  : [Indah Ruwahna Anugraheni]
- NIM   : [240202866]
- Kelas : [3 IKRB]

---

## Tujuan
Mahasiswa mampu mengimplementasikan Algoritma Genetika dengan representasi biner untuk menyelesaikan masalah optimasi fungsi matematika $f(x) = x^2$ pada rentang nilai $0$ hingga $31$, serta memahami mekanisme seleksi, crossover, dan mutasi.

---

## Dasar Teori
1. Algoritma Genetika: Teknik pencarian heuristik yang didasarkan pada prinsip seleksi alam dan genetika biologi.

2. Representasi Biner: Mengonversi nilai solusi (fenotipe) menjadi untaian bit 0 dan 1 (genotipe) untuk dimanipulasi oleh operator genetik.

3. Fitness Function: Fungsi yang mengukur kualitas atau kelayakan suatu individu untuk bertahan hidup dan bereproduksi.

4. Operator Genetik: Terdiri dari Seleksi (Roulette Wheel), Crossover (One-point), dan Mutasi (Bit-flip) untuk menghasilkan variasi keturunan baru.

---

## Langkah Praktikum
1. Setup: Menyiapkan lingkungan Python dan melakukan import library random

2. Coding: Membuat fungsi encoding biner, perhitungan fitness $x^2$, fungsi seleksi roulette wheel, fungsi crossover satu titik, dan fungsi mutasi bit-flip.

3. Execution: Menjalankan perulangan (loop) sebanyak 15 generasi dengan ukuran populasi 10 individu.

4. Run: Mengamati peningkatan nilai fitness di setiap generasi hingga ditemukan nilai optimal $x=31$.

---

## Kode Program

**1. Inisialisasi Representasi Biner dan Fungsi Fitness**

    Bagian ini adalah pondasi algoritma. Karena batasan nilai $x$ adalah $0$ hingga $31$, kita merepresentasikan setiap angka dalam bentuk untaian 5-bit (genotipe).

```java
def integer_ke_biner(x):
    return bin(x)[2:].zfill(5)

def biner_ke_integer(bin_str):
    return int(bin_str, 2)

def hitung_fitness(x):
    return x * x
```

**Deskripsi**

    Fungsi integer_ke_biner mengubah nilai angka menjadi format string biner. Penggunaan .zfill(5) memastikan bahwa angka kecil seperti $2$ tetap memiliki panjang 5 digit (00010), yang sangat penting agar titik potong saat persilangan gen tetap konsisten. Fungsi hitung_fitness mendefinisikan tujuan algoritma, yaitu mencari nilai $x$ yang menghasilkan $x^2$ terbesar.

**2. Mekanisme Seleksi Roulette Wheel**

Metode seleksi ini mensimulasikan hukum alam di mana individu yang lebih kuat memiliki peluang lebih besar untuk bereproduksi.

```java
def roulette_selection(populasi):
    nilai_fitness = [hitung_fitness(x) for x in populasi]
    total_fitness = sum(nilai_fitness)
    
    prob_kumulatif = []
    kom = 0
    for fit in nilai_fitness:
        kom += (fit / total_fitness)
        prob_kumulatif.append(kom)

    r = random.random()
    for i, batas_atas in enumerate(prob_kumulatif):
        if r <= batas_atas:
            return populasi[i]
```

**Deskripsi**

    Kode ini bekerja dengan menjumlahkan seluruh nilai fitness populasi untuk menentukan total area "roda". Setiap individu diberikan porsi area berdasarkan perbandingan nilai fitness-nya terhadap total. Kemudian, sebuah angka acak r dibangkitkan untuk menentukan individu mana yang terpilih. Semakin tinggi nilai $x^2$, semakin besar rentang probabilitas kumulatifnya, sehingga semakin besar peluang individu tersebut terpilih sebagai orang tua.

**3. Operator Crossover (Pindah Silang)**

Crossover adalah proses pertukaran informasi genetik antara dua orang tua untuk menghasilkan keturunan baru.

```java
def crossover(p1_bin, p2_bin, rate):
    if random.random() < rate:
        titik = random.randint(1, len(p1_bin) - 1)
        child1 = p1_bin[:titik] + p2_bin[titik:]
        child2 = p2_bin[:titik] + p1_bin[titik:]
        return child1, child2
    else:
        return p1_bin, p2_bin
```

**Deskripsi**

    Sesuai instruksi, kita menggunakan One-Point Crossover dengan probabilitas $0.8$. Jika angka acak di bawah $0.8$, program akan memilih satu titik potong secara acak dan menukar bagian ekor biner dari kedua orang tua. Proses ini memungkinkan kombinasi bit-bit yang menghasilkan angka besar (seperti bit di posisi depan) untuk menurun ke generasi berikutnya.

**4. Operasi Mutasi**

Mutasi memberikan variasi genetik baru secara acak untuk mencegah populasi menjadi seragam terlalu cepat (konvergensi dini).

```java
def mutation(individu_bin, rate):
    ind_list = list(individu_bin)
    for i in range(len(ind_list)):
        if random.random() < rate:
            ind_list[i] = '1' if ind_list[i] == '0' else '0'
    return "".join(ind_list)
```

**Deskripsi**

    Dengan probabilitas mutasi yang sangat kecil ($0.003$), setiap bit dalam kromosom berpeluang untuk berubah nilainya (0 menjadi 1 atau sebaliknya). Meskipun jarang terjadi, mutasi sangat penting untuk menjaga agar algoritma tidak terjebak pada angka yang itu-itu saja dan mampu menjelajahi kemungkinan nilai $x$ lainnya.

**5. Loop Generasi (Iterasi Utama)**

Ini adalah bagian yang mengatur jalannya seluruh siklus algoritma dari awal hingga akhir.


```java
for gen in range(1, max_gen + 1):
    new_population = []
    while len(new_population) < pop_size:
        p1_int = roulette_selection(populasi)
        p2_int = roulette_selection(populasi)
        
        c1_bin, c2_bin = crossover(integer_ke_biner(p1_int), integer_ke_biner(p2_int), pc)
        
        new_population.append(biner_ke_integer(mutation(c1_bin, pm)))
        if len(new_population) < pop_size:
            new_population.append(biner_ke_integer(mutation(c2_bin, pm)))
            
    populasi = new_population
```

**Deskripsi**

    Program menjalankan perulangan sebanyak 15 kali sesuai instruksi. Di setiap generasi, populasi baru dibentuk dengan memanggil fungsi seleksi, crossover, dan mutasi secara berulang hingga kuota populasi (10 individu) terpenuhi. Pada akhir setiap generasi, kita bisa melihat bahwa rata-rata nilai fitness dalam populasi cenderung meningkat menuju nilai maksimal, yaitu $x=31$ dengan fitness $961$.

**6. Pengaturan Parameter dan Inisialisasi Populasi**

Sebelum algoritma berjalan, kita harus menentukan aturan main dan menciptakan kelompok individu pertama.

```java
# Parameter sesuai soal
pop_size = 10       # Ukuran populasi
pc = 0.8            # Probabilitas Crossover
pm = 0.003          # Probabilitas Mutasi
max_gen = 15        # Maksimal Generasi

# Inisialisasi Populasi Awal
populasi = [random.randint(0, 31) for _ in range(pop_size)]
```

**Deskripsi**

    Bagian ini menentukan konfigurasi algoritma sesuai dengan instruksi praktikum. Ukuran populasi dibatasi 10 individu untuk menjaga efisiensi komputasi pada fungsi sederhana ini. Probabilitas crossover sebesar 0.8 menunjukkan bahwa peluang terjadinya pertukaran gen cukup tinggi, sedangkan probabilitas mutasi 0.003 dibuat sangat rendah agar solusi yang sudah baik tidak rusak secara drastis. Populasi awal dibangkitkan secara acak menggunakan random.randint(0, 31) sebagai titik awal pencarian solusi.

**7. Hasil Akhir (Terminal Output)**

Bagian paling bawah dari kode berfungsi untuk menampilkan jawaban akhir yang ditemukan oleh algoritma.

```java
solusi_akhir = max(populasi, key=hitung_fitness)
print(f"Nilai x terbaik adalah: {solusi_akhir}")
print(f"Nilai f(x) atau Fitness: {hitung_fitness(solusi_akhir)}")
```

**Deskripsi**
    Setelah melewati 15 generasi, program akan melakukan pencarian individu terakhir yang memiliki nilai fitness tertinggi di dalam populasi. Fungsi max() dengan parameter key=hitung_fitness digunakan untuk mengevaluasi setiap individu dan mengambil nilai $x$ yang paling mendekati atau tepat berada di angka 31.

---

## Hasil Eksekusi
 
![Screenshot hasil](/PRATIKUM%201/screenshot/output%20algen(biner).png)

---

## Analisis
1. Proses Berjalan: Program dimulai dengan 10 individu acak. Melalui seleksi Roulette Wheel, individu dengan nilai $x$ tinggi memiliki peluang lebih besar untuk menjadi orang tua. Keturunan dihasilkan melalui crossover 80% dan mutasi 0.3%.

2. Pendekatan: Minggu ini menggunakan representasi biner (genotipe) untuk melakukan manipulasi data, berbeda dengan pendekatan sebelumnya yang mungkin langsung menggunakan angka integer.

3. Kendala: Typo pada penulisan fungsi zfill dan logika pembagian total fitness nol jika populasi awal buruk. Solusinya adalah memberikan pengecekan kondisi if total_fitness == 0.
---

## Kesimpulan
Algoritma Genetika dengan representasi biner efektif untuk menyelesaikan optimasi fungsi $f(x) = x^2$. Dengan probabilitas crossover yang tinggi dan mutasi yang rendah, populasi dapat berkonvergensi menuju solusi optimal yaitu $x = 31$ (fitness 961) dalam waktu 15 generasi.

---


