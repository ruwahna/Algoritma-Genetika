import random
import numpy as np
import matplotlib.pyplot as plt

class AlgoritmaGenetika_Real:
    def __init__(self, pop_size=20, crossover_rate=0.8, mutation_rate=0.1, 
                 mutation_sigma=0.5, max_generations=50):
        """Inisialisasi parameter Algoritma Genetika Real-valued"""
        self.pop_size = pop_size
        self.crossover_rate = crossover_rate
        self.mutation_rate = mutation_rate
        self.mutation_sigma = mutation_sigma  # Standar deviasi untuk mutasi Gaussian
        self.max_generations = max_generations
        
        # Range untuk setiap variabel
        self.range_x = (-5, 5)      # x ∈ [-5, 5]
        self.range_y = (-5, 5)      # y ∈ [-5, 5]
        self.range_z = (-3, 3)      # z ∈ [-3, 3]
        
        # Tracking untuk history
        self.fitness_history = []
        self.best_fitness_history = []
        self.worst_fitness_history = []
    
    def fungsi_objektif(self, x, y, z):
        """Fungsi objektif: f(x,y,z) = (x-2)² + (y+1)² + (z-0.5)² + xy"""
        return (x - 2)**2 + (y + 1)**2 + (z - 0.5)**2 + x*y
    
    def hitung_fitness(self, f_value):
        """
        Hitung fitness untuk MINIMASI
        Modifikasi: fitness = C - f(x,y,z)
        C dipilih agar semua fitness positif
        """
        # Estimasi range f(x,y,z): max ~100 (corner)
        C = 150
        fitness = C - f_value
        if fitness < 0:
            fitness = 0
        return fitness
    
    def inisialisasi_populasi(self):
        """Inisialisasi populasi awal random (real-valued)"""
        populasi = []
        for _ in range(self.pop_size):
            x = random.uniform(self.range_x[0], self.range_x[1])
            y = random.uniform(self.range_y[0], self.range_y[1])
            z = random.uniform(self.range_z[0], self.range_z[1])
            populasi.append((x, y, z))
        return populasi
    
    def crossover_arithmetic(self, parent1, parent2):
        """
        Arithmetic Crossover untuk real-valued
        child = alpha * parent1 + (1 - alpha) * parent2
        """
        alpha = random.random()
        
        x1, y1, z1 = parent1
        x2, y2, z2 = parent2
        
        child1_x = alpha * x1 + (1 - alpha) * x2
        child1_y = alpha * y1 + (1 - alpha) * y2
        child1_z = alpha * z1 + (1 - alpha) * z2
        
        child2_x = (1 - alpha) * x1 + alpha * x2
        child2_y = (1 - alpha) * y1 + alpha * y2
        child2_z = (1 - alpha) * z1 + alpha * z2
        
        return (child1_x, child1_y, child1_z), (child2_x, child2_y, child2_z)
    
    def mutasi_gaussian(self, individu):
        """
        Mutasi Gaussian untuk real-valued
        Tambahkan Gaussian noise dengan standar deviasi mutation_sigma
        """
        x, y, z = individu
        
        # Mutasi dengan probabilitas per variabel
        if random.random() < self.mutation_rate:
            x = x + random.gauss(0, self.mutation_sigma)
        if random.random() < self.mutation_rate:
            y = y + random.gauss(0, self.mutation_sigma)
        if random.random() < self.mutation_rate:
            z = z + random.gauss(0, self.mutation_sigma)
        
        # Boundary handling - clip ke range
        x = max(self.range_x[0], min(self.range_x[1], x))
        y = max(self.range_y[0], min(self.range_y[1], y))
        z = max(self.range_z[0], min(self.range_z[1], z))
        
        return (x, y, z)
    
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
        print("ALGORITMA GENETIKA (REAL-VALUED) - MINIMASI")
        print("f(x,y,z) = (x-2)² + (y+1)² + (z-0.5)² + xy")
        print("="*90)
        
        # [3] PARAMETER MODEL
        print("\n[3] PARAMETER MODEL ALGORITMA GENETIKA:")
        print(f"    - Ukuran Populasi: {self.pop_size}")
        print(f"    - Probabilitas Crossover: {self.crossover_rate} (80%)")
        print(f"    - Probabilitas Mutasi: {self.mutation_rate} (10%)")
        print(f"    - Sigma Mutasi Gaussian: {self.mutation_sigma}")
        print(f"    - Maksimal Generasi: {self.max_generations}")
        print(f"    - Jumlah Variabel: 3 (x, y, z)")
        print(f"    - Range X: [{self.range_x[0]}, {self.range_x[1]}]")
        print(f"    - Range Y: [{self.range_y[0]}, {self.range_y[1]}]")
        print(f"    - Range Z: [{self.range_z[0]}, {self.range_z[1]}]")
        print(f"    - Tipe Crossover: ARITHMETIC")
        print(f"    - Tipe Mutasi: GAUSSIAN")
        print(f"    - Seleksi Parent: ROULETTE WHEEL")
        print(f"    - Elitisme: YA")
        
        # [4] POPULASI GENERASI PERTAMA
        populasi = self.inisialisasi_populasi()
        print("\n[4] POPULASI GENERASI PERTAMA (20 INDIVIDU):")
        print("─" * 100)
        print(f"{'No':<5} {'X':<12} {'Y':<12} {'Z':<12} {'f(x,y,z)':<15} {'Fitness':<12}")
        print("─" * 100)
        
        # [5] NILAI FITNESS GENERASI PERTAMA
        fitness_gen1 = []
        data_gen1 = []
        
        for idx, (x, y, z) in enumerate(populasi, 1):
            f_val = self.fungsi_objektif(x, y, z)
            fitness = self.hitung_fitness(f_val)
            fitness_gen1.append(fitness)
            data_gen1.append((x, y, z, f_val, fitness))
            
            print(f"{idx:<5} {x:<12.4f} {y:<12.4f} {z:<12.4f} {f_val:<15.4f} {fitness:<12.4f}")
        
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
            print(f"    ✓ Modifikasi fungsi fitness diterapkan: fitness = 150 - f(x,y,z)")
        else:
            print(f"    ✓ Semua nilai fitness POSITIF!")
            print(f"    ✓ Fungsi fitness: fitness = 150 - f(x,y,z) (untuk minimasi)")
        
        # Loop Generasi
        print("\n[7] PROSES CROSSOVER & MUTASI (GENERASI 1 - 5 SAMPEL):")
        print("─" * 130)
        print(f"{'Ronde':<6} {'Parent 1':<35} {'Parent 2':<35} {'Child 1':<35} {'Child 2':<35} {'F1':<8}")
        print("─" * 130)
        
        best_overall = data_gen1[fitness_gen1.index(max(fitness_gen1))]
        
        # Loop Generasi
        for gen in range(1, self.max_generations + 1):
            # Hitung fitness populasi sekarang
            fitness_scores = []
            for x, y, z in populasi:
                f_val = self.fungsi_objektif(x, y, z)
                fitness = self.hitung_fitness(f_val)
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
            best_x, best_y, best_z = best_chromosome
            
            if best_fit > best_overall[4]:
                best_overall = (best_x, best_y, best_z, 
                               self.fungsi_objektif(best_x, best_y, best_z), best_fit)
            
            # Buat populasi baru dengan ELITISME
            new_population = [best_chromosome]  # Elitisme
            
            crossover_round = 0
            while len(new_population) < self.pop_size:
                # Seleksi parent
                parent1 = self.seleksi_roulette_wheel(populasi, fitness_scores)
                parent2 = self.seleksi_roulette_wheel(populasi, fitness_scores)
                
                # Crossover
                if random.random() < self.crossover_rate:
                    child1, child2 = self.crossover_arithmetic(parent1, parent2)
                else:
                    child1, child2 = parent1, parent2
                
                # Mutasi
                child1 = self.mutasi_gaussian(child1)
                child2 = self.mutasi_gaussian(child2)
                
                # Tampilkan detail generasi 1 (5 sampel)
                if gen == 1 and crossover_round < 5:
                    x1, y1, z1 = child1
                    x2, y2, z2 = child2
                    f1 = self.hitung_fitness(self.fungsi_objektif(x1, y1, z1))
                    p1_str = f"({parent1[0]:.2f}, {parent1[1]:.2f}, {parent1[2]:.2f})"
                    p2_str = f"({parent2[0]:.2f}, {parent2[1]:.2f}, {parent2[2]:.2f})"
                    c1_str = f"({x1:.2f}, {y1:.2f}, {z1:.2f})"
                    c2_str = f"({x2:.2f}, {y2:.2f}, {z2:.2f})"
                    print(f"{crossover_round+1:<6} {p1_str:<35} {p2_str:<35} {c1_str:<35} {c2_str:<35} {f1:<8.4f}")
                    crossover_round += 1
                
                new_population.append(child1)
                if len(new_population) < self.pop_size:
                    new_population.append(child2)
            
            populasi = new_population[:self.pop_size]
        
        print("─" * 130)
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
        plt.title('Perkembangan Nilai Fitness per Generasi (Real-valued)', fontsize=13, fontweight='bold')
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
        plt.savefig('hasil_genetika_real.png', dpi=300, bbox_inches='tight')
        print("✓ Grafik tersimpan sebagai 'hasil_genetika_real.png'")
        plt.show()
        
        # [9] HASIL AKHIR DAN ANALISIS
        print("\n[9] HASIL OPTIMASI AKHIR:")
        print("─" * 80)
        print(f"Solusi Terbaik:")
        print(f"    X = {best_overall[0]:.6f}")
        print(f"    Y = {best_overall[1]:.6f}")
        print(f"    Z = {best_overall[2]:.6f}")
        print(f"f(x,y,z) = {best_overall[3]:.6f} (MINIMAL)")
        print(f"Fitness = {best_overall[4]:.6f}")
        gen_conv = self.best_fitness_history.index(best_overall[4]) + 1
        print(f"Generasi Pencapaian: {gen_conv} (dari {self.max_generations})")
        
        # Hitung selisih dari solusi awal
        f_gen1_best = max([d[4] for d in data_gen1])
        f_gen1_val = min([d[3] for d in data_gen1])
        improvement = ((f_gen1_val - best_overall[3]) / abs(f_gen1_val)) * 100
        print(f"Improvement dari Gen 1: {improvement:.2f}%")
        
        # [10] ANALISIS RASIO CROSSOVER DAN MUTASI
        print("\n[10] ANALISIS RASIO CROSSOVER DAN MUTASI:")
        print("─" * 80)
        print(f"    Probabilitas Crossover: {self.crossover_rate:.0%}")
        print(f"    - Jenis: ARITHMETIC (weighted average dari parent)")
        print(f"    - Interpretasi: {self.crossover_rate:.0%} pasangan melakukan crossover")
        
        print(f"\n    Probabilitas Mutasi: {self.mutation_rate:.0%}")
        print(f"    - Jenis: GAUSSIAN (tambah Gaussian noise)")
        print(f"    - Sigma: {self.mutation_sigma}")
        print(f"    - Interpretasi: Setiap variabel {self.mutation_rate:.0%} chance dimutasi")
        print(f"    - Expected variables: {3 * self.mutation_rate:.1f} variabel per individu")
        
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
    # Buat objek Algoritma Genetika Real-valued
    ga = AlgoritmaGenetika_Real(
        pop_size=20,              # Ukuran populasi
        crossover_rate=0.8,       # Probabilitas crossover 80%
        mutation_rate=0.1,        # Probabilitas mutasi 10%
        mutation_sigma=0.5,       # Standar deviasi Gaussian
        max_generations=50        # Jumlah generasi
    )
    
    # Jalankan
    hasil = ga.run()
