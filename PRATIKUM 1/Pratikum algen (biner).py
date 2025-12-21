import random

# --- 1. FUNGSI DAN PROSEDUR ---

# Representasi kromosom: Mengubah integer ke biner 5-bit
def integer_ke_biner(x):
    return bin(x)[2:].zfill(5)

# Decode: Mengubah biner kembali ke integer
def biner_ke_integer(bin_str):
    return int(bin_str, 2)

# Fitness: f(x) = x^2
def hitung_fitness(x):
    return x * x

# 2.1. Seleksi Roulette Wheel
def roulette_selection(populasi):
    nilai_fitness = [hitung_fitness(x) for x in populasi]
    total_fitness = sum(nilai_fitness)
    
    # Jika total fitness 0 (awal populasi semua 0), beri probabilitas sama
    if total_fitness == 0:
        return random.choice(populasi)

    # Probabilitas kumulatif
    prob_kumulatif = []
    kom = 0
    for fit in nilai_fitness:
        kom += (fit / total_fitness)
        prob_kumulatif.append(kom)

    # Putar roda (ambil angka acak 0-1)
    r = random.random()
    for i, batas_atas in enumerate(prob_kumulatif):
        if r <= batas_atas:
            return populasi[i]

# 2.2. One-Point Crossover
def crossover(p1_bin, p2_bin, rate):
    if random.random() < rate:
        titik = random.randint(1, len(p1_bin) - 1)
        child1 = p1_bin[:titik] + p2_bin[titik:]
        child2 = p2_bin[:titik] + p1_bin[titik:]
        return child1, child2
    else:
        return p1_bin, p2_bin

# 2.3. Mutasi
def mutation(individu_bin, rate):
    ind_list = list(individu_bin)
    for i in range(len(ind_list)):
        if random.random() < rate:
            # Flip bit: jika '0' jadi '1', jika '1' jadi '0'
            ind_list[i] = '1' if ind_list[i] == '0' else '0'
    return "".join(ind_list)

# --- 2. MAIN PROGRAM (EKSEKUSI) ---

# Parameter sesuai instruksi
ps = 10           # Ukuran Populasi
cr = 0.8          # Probabilitas Crossover
mr = 0.003        # Probabilitas Mutasi
max_generasi = 15 # Maksimal Generasi

# Inisialisasi Populasi Awal (Random integer 0-31)
populasi = [random.randint(0, 31) for _ in range(ps)]

print(f"Populasi Awal: {populasi}\n")

# Loop Generasi
for gen in range(1, max_generasi + 1):
    new_population = []
    
    # Proses membuat populasi baru
    while len(new_population) < ps:
        # 1. Seleksi Orang Tua (Individu yang terpilih masih berupa integer)
        parent1_int = roulette_selection(populasi)
        parent2_int = roulette_selection(populasi)
        
        # Konversi ke biner untuk proses genetik
        p1_bin = integer_ke_biner(parent1_int)
        p2_bin = integer_ke_biner(parent2_int)
        
        # 2. Crossover
        c1_bin, c2_bin = crossover(p1_bin, p2_bin, cr)
        
        # 3. Mutasi
        c1_bin = mutation(c1_bin, mr)
        c2_bin = mutation(c2_bin, mr)
        
        # Konversi kembali ke integer dan masukkan ke populasi baru
        new_population.append(biner_ke_integer(c1_bin))
        if len(new_population) < ps:
            new_population.append(biner_ke_integer(c2_bin))
            
    populasi = new_population
    
    # Cari yang terbaik di generasi ini
    best_individu = max(populasi, key=hitung_fitness)
    print(f"Generasi {gen}: Best x = {best_individu}, Fitness = {hitung_fitness(best_individu)}")

print(f"\nHasil Akhir: Solusi terbaik ditemukan adalah x = {max(populasi)}")