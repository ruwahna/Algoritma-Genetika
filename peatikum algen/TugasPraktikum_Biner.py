import random
import numpy as np
import matplotlib.pyplot as plt

class AlgoritmaGenetika_Biner:
    def __init__(self, pop_size=20, crossover_rate=0.8, mutation_rate=0.1, max_generations=50):
        """Inisialisasi parameter Algoritma Genetika Biner"""
        self.pop_size = pop_size
        self.crossover_rate = crossover_rate
        self.mutation_rate = mutation_rate
        self.max_generations = max_generations
        
        # Jumlah bit per variabel
        self.bits_per_variable = 8  # 8 bit untuk X dan Y (16 bit total)
        self.chromosome_length = 16  # 2 variabel * 8 bit
        
        # Range untuk X dan Y
        self.range_x = (-10, 10)
        self.range_y = (-10, 10)
        
        # Tracking untuk history
        self.fitness_history = []
        self.best_fitness_history = []
        self.worst_fitness_history = []
    
    def desimal_ke_biner(self, desimal):
        """Convert integer to 8-bit binary string"""
        if desimal < 0:
            desimal = 256 + desimal
        biner = bin(desimal)[2:]
        return biner.zfill(8)
    
    def biner_ke_desimal(self, biner_str):
        """Convert 8-bit binary string to integer"""
        desimal = int(biner_str, 2)
        if desimal > 127:
            desimal = desimal - 256
        return desimal
    
    def decode_chromosome(self, chromosome):
        """
        Decode 16-bit chromosome ke real values X dan Y
        Chromosome: 8 bit untuk X + 8 bit untuk Y
        """
        x_biner = chromosome[:8]
        y_biner = chromosome[8:16]
        
        x_desimal = self.biner_ke_desimal(x_biner)
        y_desimal = self.biner_ke_desimal(y_biner)
        
        # Normalisasi ke range [-10, 10]
        x = self.range_x[0] + (x_desimal / 255) * (self.range_x[1] - self.range_x[0])
        y = self.range_y[0] + (y_desimal / 255) * (self.range_y[1] - self.range_y[0])
        
        return x, y
    
    def fungsi_objektif(self, x, y):
        """Fungsi objektif: f(x,y) = x - 2y"""
        return x - 2*y
    
    def hitung_fitness(self, x, y):
        """
        Hitung fitness untuk MINIMASI
        Modifikasi: fitness = C - f(x,y)
        C dipilih agar semua fitness positif
        """
        f_val = self.fungsi_objektif(x, y)
        # Estimasi range f(x,y): max 50 (10 - 2*(-10))
        C = 60
        fitness = C - f_val
        if fitness < 0:
            fitness = 0
        return fitness
    
    def inisialisasi_populasi(self):
        """Inisialisasi populasi awal random (biner)"""
        populasi = []
        for _ in range(self.pop_size):
            chromosome = ''.join(random.choice('01') for _ in range(self.chromosome_length))
            populasi.append(chromosome)
        return populasi
    
    def crossover_uniform(self, parent1, parent2):
        """
        Uniform Crossover: setiap bit 50% dari parent1 atau parent2
        """
        child1 = ''
        child2 = ''
        
        for i in range(self.chromosome_length):
            if random.random() < 0.5:
                child1 += parent1[i]
                child2 += parent2[i]
            else:
                child1 += parent2[i]
                child2 += parent1[i]
        
        return child1, child2
    
    def mutasi(self, chromosome):
        """
        Bit-flip mutation: flip random bit dengan probabilitas mutation_rate
        """
        chromosome_list = list(chromosome)
        
        for i in range(self.chromosome_length):
            if random.random() < self.mutation_rate:
                # Flip bit
                if chromosome_list[i] == '0':
                    chromosome_list[i] = '1'
                else:
                    chromosome_list[i] = '0'
        
        return ''.join(chromosome_list)
    
    def seleksi_roulette_wheel(self, populasi, fitness_scores):
        """Seleksi parent menggunakan Roulette Wheel"""
        total_fitness = sum(fitness_scores)
        if total_fitness == 0:
            return random.choice(populasi)
        
        probabilitas = [f / total_fitness for f in fitness_scores]
        idx = random.choices(range(len(populasi)), weights=probabilitas, k=1)[0]
        return populasi[idx]
    
    def run(self):
        """Jalankan algoritma genetika lengkap"""
        print("="*90)
        print("ALGORITMA GENETIKA (BINER) - MINIMASI")
        print("f(x,y) = x - 2y")
        print("="*90)
        
        # [3] PARAMETER MODEL
        print("\n[3] PARAMETER MODEL ALGORITMA GENETIKA:")
        print(f"    - Ukuran Populasi: {self.pop_size}")
        print(f"    - Bit per Variabel: {self.bits_per_variable}")
        print(f"    - Total Bit Kromosom: {self.chromosome_length}")
        print(f"    - Probabilitas Crossover: {self.crossover_rate} (80%)")
        print(f"    - Probabilitas Mutasi: {self.mutation_rate} (10%)")
        print(f"    - Maksimal Generasi: {self.max_generations}")
        print(f"    - Jumlah Variabel: 2 (x, y)")
        print(f"    - Range X: [{self.range_x[0]}, {self.range_x[1]}]")
        print(f"    - Range Y: [{self.range_y[0]}, {self.range_y[1]}]")
        print(f"    - Tipe Crossover: UNIFORM")
        print(f"    - Tipe Mutasi: BIT-FLIP")
        print(f"    - Seleksi Parent: ROULETTE WHEEL")
        print(f"    - Elitisme: YA")
        
        # [4] POPULASI GENERASI PERTAMA
        populasi = self.inisialisasi_populasi()
        print("\n[4] POPULASI GENERASI PERTAMA (20 INDIVIDU):")
        print("─" * 100)
        print(f"{'No':<5} {'Kromosom Biner':<30} {'X (Desimal)':<12} {'Y (Desimal)':<12} {'f(x,y)':<12} {'Fitness':<12}")
        print("─" * 100)
        
        # [5] NILAI FITNESS GENERASI PERTAMA
        fitness_gen1 = []
        data_gen1 = []
        
        for idx, chromosome in enumerate(populasi, 1):
            x, y = self.decode_chromosome(chromosome)
            f_val = self.fungsi_objektif(x, y)
            fitness = self.hitung_fitness(x, y)
            fitness_gen1.append(fitness)
            data_gen1.append((chromosome, x, y, f_val, fitness))
            
            print(f"{idx:<5} {chromosome:<30} {x:<12.4f} {y:<12.4f} {f_val:<12.4f} {fitness:<12.4f}")
        
        print("─" * 100)
        
        # [5] ANALISIS FITNESS GENERASI 1
        print("\n[5] ANALISIS NILAI FITNESS GENERASI 1:")
        print(f"    - Fitness Minimum: {min(fitness_gen1):.4f}")
        print(f"    - Fitness Maksimum: {max(fitness_gen1):.4f}")
        print(f"    - Fitness Rata-rata: {np.mean(fitness_gen1):.4f}")
        print(f"    - Fitness Standar Deviasi: {np.std(fitness_gen1):.4f}")
        
        # [6] CECK NILAI FITNESS NEGATIF
        print("\n[6] ANALISIS NILAI FITNESS NEGATIF:")
        nilai_negatif = [f for f in fitness_gen1 if f < 0]
        if nilai_negatif:
            print(f"    ⚠ Ditemukan {len(nilai_negatif)} nilai fitness negatif!")
            print(f"    ✓ Modifikasi fungsi fitness diterapkan: fitness = 60 - f(x,y)")
        else:
            print(f"    ✓ Semua nilai fitness POSITIF!")
            print(f"    ✓ Fungsi fitness: fitness = 60 - f(x,y) (untuk minimasi)")
        
        # Loop Generasi
        print("\n[7] PROSES CROSSOVER & MUTASI (GENERASI 1 - 5 SAMPEL):")
        print("─" * 160)
        print(f"{'Ronde':<6} {'Parent 1':<20} {'Parent 2':<20} {'Child 1':<20} {'Child 2':<20} {'X1':<10} {'Y1':<10} {'F1':<10}")
        print("─" * 160)
        
        best_overall = data_gen1[fitness_gen1.index(max(fitness_gen1))]
        
        # Loop Generasi
        for gen in range(1, self.max_generations + 1):
            # Hitung fitness populasi sekarang
            fitness_scores = []
            for chromosome in populasi:
                x, y = self.decode_chromosome(chromosome)
                fitness = self.hitung_fitness(x, y)
                fitness_scores.append(fitness)
            
            # Simpan history
            best_fit = max(fitness_scores)
            worst_fit = min(fitness_scores)
            avg_fit = np.mean(fitness_scores)
            
            self.fitness_history.append(avg_fit)
            self.best_fitness_history.append(best_fit)
            self.worst_fitness_history.append(worst_fit)
            
            # Cari individu terbaik di generasi ini
            best_idx = fitness_scores.index(best_fit)
            best_chromosome = populasi[best_idx]
            x_best, y_best = self.decode_chromosome(best_chromosome)
            f_best = self.fungsi_objektif(x_best, y_best)
            
            if best_fit > best_overall[4]:
                best_overall = (best_chromosome, x_best, y_best, f_best, best_fit)
            
            # Buat populasi baru dengan ELITISME
            new_population = [best_chromosome]  # Elitisme
            
            crossover_round = 0
            while len(new_population) < self.pop_size:
                # Seleksi parent
                parent1 = self.seleksi_roulette_wheel(populasi, fitness_scores)
                parent2 = self.seleksi_roulette_wheel(populasi, fitness_scores)
                
                # Crossover
                if random.random() < self.crossover_rate:
                    child1, child2 = self.crossover_uniform(parent1, parent2)
                else:
                    child1, child2 = parent1, parent2
                
                # Mutasi
                child1 = self.mutasi(child1)
                child2 = self.mutasi(child2)
                
                # Tampilkan detail generasi 1 (5 sampel)
                if gen == 1 and crossover_round < 5:
                    x1, y1 = self.decode_chromosome(child1)
                    f1 = self.fungsi_objektif(x1, y1)
                    print(f"{crossover_round+1:<6} {parent1:<20} {parent2:<20} {child1:<20} {child2:<20} {x1:<10.4f} {y1:<10.4f} {f1:<10.4f}")
                    crossover_round += 1
                
                new_population.append(child1)
                if len(new_population) < self.pop_size:
                    new_population.append(child2)
            
            populasi = new_population[:self.pop_size]
        
        print("─" * 160)
        print(f"(Menampilkan 5 dari ~10 ronde crossover per generasi)\n")
        
        # [8] GRAFIK PERKEMBANGAN FITNESS
        print("[8] GRAFIK PERKEMBANGAN FITNESS PER GENERASI:")
        print("─" * 80)
        
        plt.figure(figsize=(14, 5))
        
        # Plot 1: Fitness per Generasi
        plt.subplot(1, 2, 1)
        generasi = range(1, self.max_generations + 1)
        plt.plot(generasi, self.best_fitness_history, 'g-o', label='Best Fitness', linewidth=2, markersize=4)
        plt.plot(generasi, self.fitness_history, 'b--', label='Average Fitness', linewidth=2)
        plt.plot(generasi, self.worst_fitness_history, 'r--', label='Worst Fitness', linewidth=2)
        plt.xlabel('Generasi', fontsize=12)
        plt.ylabel('Fitness', fontsize=12)
        plt.title('Perkembangan Nilai Fitness per Generasi (Biner)', fontsize=13, fontweight='bold')
        plt.legend(fontsize=10)
        plt.grid(True, alpha=0.3)
        
        # Plot 2: Fitness Distribution
        plt.subplot(1, 2, 2)
        plt.bar(['Best', 'Rata-rata', 'Terburuk'], 
               [self.best_fitness_history[-1], self.fitness_history[-1], self.worst_fitness_history[-1]],
               color=['green', 'blue', 'red'], alpha=0.7, edgecolor='black')
        plt.ylabel('Fitness', fontsize=12)
        plt.title('Fitness pada Generasi Akhir', fontsize=13, fontweight='bold')
        plt.grid(True, alpha=0.3, axis='y')
        
        plt.tight_layout()
        plt.savefig('hasil_genetika_biner.png', dpi=300, bbox_inches='tight')
        print("✓ Grafik tersimpan sebagai 'hasil_genetika_biner.png'")
        plt.show()
        
        # [9] HASIL AKHIR DAN ANALISIS
        print("\n[9] HASIL OPTIMASI AKHIR:")
        print("─" * 80)
        print(f"Solusi Terbaik:")
        print(f"    Kromosom: {best_overall[0]}")
        print(f"    X = {best_overall[1]:.6f}")
        print(f"    Y = {best_overall[2]:.6f}")
        print(f"f(x,y) = {best_overall[3]:.6f} (MINIMAL)")
        print(f"Fitness = {best_overall[4]:.6f}")
        gen_conv = self.best_fitness_history.index(best_overall[4]) + 1
        print(f"Generasi Pencapaian: {gen_conv} (dari {self.max_generations})")
        
        # Hitung improvement
        f_gen1_best = min([d[3] for d in data_gen1])
        improvement = ((f_gen1_best - best_overall[3]) / abs(f_gen1_best)) * 100
        print(f"Improvement dari Gen 1: {improvement:.2f}%")
        
        # [10] ANALISIS RASIO CROSSOVER DAN MUTASI
        print("\n[10] ANALISIS RASIO CROSSOVER DAN MUTASI:")
        print("─" * 80)
        print(f"    Probabilitas Crossover: {self.crossover_rate:.0%}")
        print(f"    - Jenis: UNIFORM (setiap bit 50% dari parent)")
        print(f"    - Interpretasi: {self.crossover_rate:.0%} pasangan melakukan crossover")
        
        print(f"\n    Probabilitas Mutasi: {self.mutation_rate:.0%}")
        print(f"    - Jenis: BIT-FLIP (ubah 0→1 atau 1→0)")
        print(f"    - Interpretasi: Setiap bit {self.mutation_rate:.0%} chance di-flip")
        print(f"    - Expected bits: {self.chromosome_length * self.mutation_rate:.1f} bit per individu")
        
        print(f"\n    Analisis Keseimbangan:")
        if self.crossover_rate >= 0.7:
            print(f"    ✓ Crossover rate TINGGI → Eksplorasi solusi lebih baik")
        if self.mutation_rate <= 0.15:
            print(f"    ✓ Mutation rate RENDAH → Eksploitasi solusi yang baik")
        print(f"    ✓ Kombinasi ini BALANCE untuk konvergensi optimal")
        
        print("\n" + "="*80)
        
        return best_overall

# ========================================
# JALANKAN PROGRAM
# ========================================

if __name__ == "__main__":
    # Buat objek Algoritma Genetika Biner
    ga = AlgoritmaGenetika_Biner(
        pop_size=20,              # Ukuran populasi
        crossover_rate=0.8,       # Probabilitas crossover 80%
        mutation_rate=0.1,        # Probabilitas mutasi 10%
        max_generations=50        # Jumlah generasi
    )
    
    # Jalankan
    hasil = ga.run()
