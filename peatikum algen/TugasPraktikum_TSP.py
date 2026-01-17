import random
import numpy as np
import matplotlib.pyplot as plt
from itertools import permutations
import math

class AlgoritmaGenetika_TSP:
    def __init__(self, num_houses=6, pop_size=30, crossover_rate=0.8, 
                 mutation_rate=0.2, max_generations=100, start_house=0):
        """Inisialisasi parameter Algoritma Genetika untuk TSP"""
        self.num_houses = num_houses
        self.pop_size = pop_size
        self.crossover_rate = crossover_rate
        self.mutation_rate = mutation_rate
        self.max_generations = max_generations
        self.start_house = start_house  # Rumah awal (tidak perlu kembali)
        
        # Tracking untuk history
        self.fitness_history = []
        self.best_fitness_history = []
        self.worst_fitness_history = []
        
        # Generate distance matrix (asymmetrik)
        self.distance_matrix = self.generate_asymmetric_distance_matrix()
        
        # Koordinat rumah untuk visualisasi
        self.house_coords = self.generate_house_coordinates()
    
    def generate_asymmetric_distance_matrix(self):
        """Generate matriks jarak asimetrik (A→C ≠ C→A)"""
        distance = np.zeros((self.num_houses, self.num_houses))
        
        for i in range(self.num_houses):
            for j in range(self.num_houses):
                if i != j:
                    # Generate distance asimetrik random
                    distance[i][j] = random.randint(10, 100)
        
        return distance
    
    def generate_house_coordinates(self):
        """Generate koordinat rumah untuk visualisasi"""
        coords = []
        for i in range(self.num_houses):
            x = random.uniform(0, 100)
            y = random.uniform(0, 100)
            coords.append((x, y))
        return coords
    
    def hitung_total_jarak(self, route):
        """
        Hitung total jarak untuk satu rute (TSP)
        Route tidak perlu kembali ke rumah awal
        """
        total_distance = 0
        
        # Route: start_house → rumah1 → rumah2 → ... → rumahN
        # Bukan cycle, hanya path
        for i in range(len(route) - 1):
            from_house = route[i]
            to_house = route[i + 1]
            total_distance += self.distance_matrix[from_house][to_house]
        
        return total_distance
    
    def hitung_fitness(self, route):
        """Hitung fitness (inverse dari total jarak)"""
        total_distance = self.hitung_total_jarak(route)
        
        # Fitness = 1 / (1 + jarak) agar fitness = [0,1]
        # atau bisa pakai: fitness = C - jarak
        fitness = 1.0 / (1.0 + total_distance)
        
        return fitness
    
    def inisialisasi_populasi(self):
        """
        Inisialisasi populasi awal
        Kromosom: path dari start_house ke rumah-rumah lain
        Tidak ada return ke start_house
        """
        populasi = []
        
        # Rumah selain start_house
        other_houses = [h for h in range(self.num_houses) if h != self.start_house]
        
        for _ in range(self.pop_size):
            # Shuffle rumah-rumah lain
            route = [self.start_house] + random.sample(other_houses, len(other_houses))
            populasi.append(route)
        
        return populasi
    
    def crossover_order(self, parent1, parent2):
        """
        Order Crossover (OX) - cocok untuk TSP
        Menjaga urutan relatif dan tidak ada duplikat
        """
        # Ambil segment tengah dari parent1
        size = len(parent1)
        start = random.randint(1, size - 2)
        end = random.randint(start + 1, size - 1)
        
        # Child1: ambil segment dari parent1
        child1 = [None] * size
        child1[start:end] = parent1[start:end]
        
        # Fill sisa dari parent2 (dengan order yang benar)
        pointer = end
        for house in parent2[end:] + parent2[:end]:
            if house not in child1:
                if pointer == size:
                    pointer = 0
                child1[pointer] = house
                pointer += 1
        
        # Child2: sama tapi dari parent2
        child2 = [None] * size
        child2[start:end] = parent2[start:end]
        
        pointer = end
        for house in parent1[end:] + parent1[:end]:
            if house not in child2:
                if pointer == size:
                    pointer = 0
                child2[pointer] = house
                pointer += 1
        
        return child1, child2
    
    def mutasi_swap(self, route):
        """
        Swap Mutation: tukar posisi dua rumah random
        Pertahankan start_house di posisi 0
        """
        mutated_route = route.copy()
        
        # Mutasi hanya untuk rumah selain start_house
        if len(mutated_route) > 2:
            idx1 = random.randint(1, len(mutated_route) - 1)
            idx2 = random.randint(1, len(mutated_route) - 1)
            
            mutated_route[idx1], mutated_route[idx2] = mutated_route[idx2], mutated_route[idx1]
        
        return mutated_route
    
    def seleksi_tournament(self, populasi, fitness_scores, tournament_size=3):
        """Tournament Selection"""
        tournament_idx = random.sample(range(len(populasi)), tournament_size)
        best_idx = max(tournament_idx, key=lambda i: fitness_scores[i])
        return populasi[best_idx]
    
    def run(self):
        """Jalankan algoritma genetika untuk TSP"""
        print("="*100)
        print(f"ALGORITMA GENETIKA - TRAVELING SALES PROBLEM (TSP)")
        print(f"Jumlah Rumah: {self.num_houses} | Rumah Awal: {self.start_house}")
        print("="*100)
        
        # [3] PARAMETER MODEL
        print(f"\n[3] PARAMETER MODEL ALGORITMA GENETIKA:")
        print(f"    - Jumlah Rumah: {self.num_houses}")
        print(f"    - Ukuran Populasi: {self.pop_size}")
        print(f"    - Probabilitas Crossover: {self.crossover_rate} ({self.crossover_rate*100:.0f}%)")
        print(f"    - Probabilitas Mutasi: {self.mutation_rate} ({self.mutation_rate*100:.0f}%)")
        print(f"    - Maksimal Generasi: {self.max_generations}")
        print(f"    - Rumah Awal (Start): {self.start_house}")
        print(f"    - Tipe Crossover: ORDER CROSSOVER (OX)")
        print(f"    - Tipe Mutasi: SWAP MUTATION")
        print(f"    - Seleksi Parent: TOURNAMENT SELECTION (size=3)")
        print(f"    - Elitisme: YA")
        
        # [4] REPRESENTASI KROMOSOM
        print(f"\n[4] REPRESENTASI KROMOSOM:")
        print(f"    - Tipe: Permutation (Path)")
        print(f"    - Format: [start_house, house1, house2, ..., houseN]")
        print(f"    - Panjang Kromosom: {self.num_houses} (semua rumah)")
        print(f"    - Contoh: [0, 3, 1, 4, 2, 5]")
        print(f"    - Interpretasi: Rumah 0 → 3 → 1 → 4 → 2 → 5 (tanpa kembali ke 0)")
        
        # [5] MATRIKS JARAK ASIMETRIK
        print(f"\n[5] MATRIKS JARAK ASIMETRIK (A→C ≠ C→A):")
        print("─" * 80)
        print("     ", end="")
        for j in range(self.num_houses):
            print(f"  R{j}   ", end="")
        print()
        print("─" * 80)
        for i in range(self.num_houses):
            print(f"R{i}  |", end="")
            for j in range(self.num_houses):
                if i == j:
                    print(f"  -  ", end="")
                else:
                    print(f" {self.distance_matrix[i][j]:3.0f} ", end="")
            print()
        print("─" * 80)
        
        # [6] POPULASI GENERASI PERTAMA
        populasi = self.inisialisasi_populasi()
        print(f"\n[6] POPULASI GENERASI PERTAMA ({self.pop_size} INDIVIDU):")
        print("─" * 100)
        print(f"{'No':<5} {'Kromosom Route':<30} {'Total Jarak':<15} {'Fitness':<12}")
        print("─" * 100)
        
        # [7] NILAI FITNESS GENERASI PERTAMA
        fitness_gen1 = []
        data_gen1 = []
        
        for idx, route in enumerate(populasi[:10], 1):  # Tampilkan 10 pertama
            total_distance = self.hitung_total_jarak(route)
            fitness = self.hitung_fitness(route)
            fitness_gen1.append(fitness)
            data_gen1.append((route, total_distance, fitness))
            
            route_str = str(route[:6]) if len(route) <= 6 else str(route[:4]) + "..."
            print(f"{idx:<5} {route_str:<30} {total_distance:<15.2f} {fitness:<12.6f}")
        
        # Hitung untuk semua
        for idx in range(10, len(populasi)):
            route = populasi[idx]
            total_distance = self.hitung_total_jarak(route)
            fitness = self.hitung_fitness(route)
            fitness_gen1.append(fitness)
            data_gen1.append((route, total_distance, fitness))
        
        print("─" * 100)
        
        # [8] ANALISIS FITNESS GENERASI 1
        print(f"\n[8] ANALISIS NILAI FITNESS GENERASI 1:")
        print(f"    - Fitness Maksimum (Terbaik): {max(fitness_gen1):.6f}")
        print(f"    - Fitness Minimum (Terburuk): {min(fitness_gen1):.6f}")
        print(f"    - Fitness Rata-rata: {np.mean(fitness_gen1):.6f}")
        print(f"    - Standar Deviasi: {np.std(fitness_gen1):.6f}")
        
        # [9] CROSSOVER & MUTASI SAMPEL (GEN 1)
        print(f"\n[9] CONTOH CROSSOVER & MUTASI (GENERASI 1):")
        print("─" * 120)
        
        parent1 = populasi[0]
        parent2 = populasi[1]
        child1, child2 = self.crossover_order(parent1, parent2)
        child1_mutated = self.mutasi_swap(child1)
        child2_mutated = self.mutasi_swap(child2)
        
        dist_p1 = self.hitung_total_jarak(parent1)
        dist_p2 = self.hitung_total_jarak(parent2)
        dist_c1 = self.hitung_total_jarak(child1)
        dist_c2 = self.hitung_total_jarak(child2)
        dist_c1m = self.hitung_total_jarak(child1_mutated)
        dist_c2m = self.hitung_total_jarak(child2_mutated)
        
        print(f"Parent 1:          {parent1}")
        print(f"  - Total Jarak: {dist_p1:.2f}")
        print(f"\nParent 2:          {parent2}")
        print(f"  - Total Jarak: {dist_p2:.2f}")
        print(f"\n[CROSSOVER ORDER (OX)]")
        print(f"Child 1 (Pre):     {child1}")
        print(f"  - Total Jarak: {dist_c1:.2f}")
        print(f"\nChild 2 (Pre):     {child2}")
        print(f"  - Total Jarak: {dist_c2:.2f}")
        print(f"\n[SWAP MUTATION]")
        print(f"Child 1 (Post):    {child1_mutated}")
        print(f"  - Total Jarak: {dist_c1m:.2f}")
        print(f"\nChild 2 (Post):    {child2_mutated}")
        print(f"  - Total Jarak: {dist_c2m:.2f}")
        print("─" * 120)
        
        best_overall = data_gen1[fitness_gen1.index(max(fitness_gen1))]
        
        # Loop Generasi
        for gen in range(1, self.max_generations + 1):
            # Hitung fitness populasi sekarang
            fitness_scores = [self.hitung_fitness(route) for route in populasi]
            
            best_fit = max(fitness_scores)
            worst_fit = min(fitness_scores)
            avg_fit = np.mean(fitness_scores)
            
            self.fitness_history.append(avg_fit)
            self.best_fitness_history.append(best_fit)
            self.worst_fitness_history.append(worst_fit)
            
            best_idx = fitness_scores.index(best_fit)
            best_chromosome = populasi[best_idx]
            
            if best_fit > best_overall[2]:
                best_overall = (best_chromosome, self.hitung_total_jarak(best_chromosome), best_fit)
            
            # Generate new population dengan ELITISME
            new_population = [best_chromosome]
            
            while len(new_population) < self.pop_size:
                parent1 = self.seleksi_tournament(populasi, fitness_scores)
                parent2 = self.seleksi_tournament(populasi, fitness_scores)
                
                if random.random() < self.crossover_rate:
                    child1, child2 = self.crossover_order(parent1, parent2)
                else:
                    child1, child2 = parent1[:], parent2[:]
                
                if random.random() < self.mutation_rate:
                    child1 = self.mutasi_swap(child1)
                if random.random() < self.mutation_rate:
                    child2 = self.mutasi_swap(child2)
                
                new_population.append(child1)
                if len(new_population) < self.pop_size:
                    new_population.append(child2)
            
            populasi = new_population[:self.pop_size]
        
        # [10] GRAFIK PERKEMBANGAN FITNESS
        print(f"\n[10] GRAFIK PERKEMBANGAN FITNESS PER GENERASI:")
        print("─" * 80)
        
        plt.figure(figsize=(14, 5))
        
        # Plot 1: Fitness per Generasi
        plt.subplot(1, 2, 1)
        generasi = range(1, self.max_generations + 1)
        plt.plot(generasi, self.best_fitness_history, 'g-o', label='Best Fitness', linewidth=2, markersize=3)
        plt.plot(generasi, self.fitness_history, 'b--', label='Average Fitness', linewidth=2)
        plt.plot(generasi, self.worst_fitness_history, 'r--', label='Worst Fitness', linewidth=2)
        plt.xlabel('Generasi', fontsize=12)
        plt.ylabel('Fitness', fontsize=12)
        plt.title(f'Perkembangan Fitness TSP ({self.num_houses} Rumah)', fontsize=13, fontweight='bold')
        plt.legend(fontsize=10)
        plt.grid(True, alpha=0.3)
        
        # Plot 2: Rute Terbaik
        plt.subplot(1, 2, 2)
        best_route = best_overall[0]
        route_x = [self.house_coords[h][0] for h in best_route]
        route_y = [self.house_coords[h][1] for h in best_route]
        
        plt.scatter(route_x, route_y, c='red', s=100, zorder=5)
        for i, h in enumerate(best_route):
            plt.text(route_x[i], route_y[i], f"R{h}", fontsize=10, ha='center', va='center', 
                    color='white', fontweight='bold')
        
        for i in range(len(best_route) - 1):
            plt.arrow(route_x[i], route_y[i], 
                     route_x[i+1] - route_x[i], route_y[i+1] - route_y[i],
                     head_width=2, head_length=2, fc='blue', ec='blue', alpha=0.6)
        
        plt.title(f'Rute Terbaik (TSP {self.num_houses} Rumah)', fontsize=13, fontweight='bold')
        plt.xlabel('X', fontsize=11)
        plt.ylabel('Y', fontsize=11)
        plt.grid(True, alpha=0.3)
        plt.axis('equal')
        
        plt.tight_layout()
        plt.savefig(f'hasil_tsp_{self.num_houses}_houses.png', dpi=300, bbox_inches='tight')
        print("✓ Grafik tersimpan")
        plt.show()
        
        # [11] HASIL AKHIR
        print(f"\n[11] HASIL OPTIMASI AKHIR:")
        print("─" * 80)
        print(f"Rute Terbaik: {best_overall[0]}")
        print(f"Total Jarak: {best_overall[1]:.2f}")
        print(f"Fitness: {best_overall[2]:.6f}")
        gen_conv = self.best_fitness_history.index(best_overall[2]) + 1
        print(f"Generasi Pencapaian: {gen_conv} (dari {self.max_generations})")
        
        improvement = ((max(fitness_gen1) - best_overall[2]) / max(fitness_gen1)) * 100
        print(f"Improvement: {improvement:.2f}%")
        
        print("\n" + "="*100)
        
        return best_overall


# ========================================
# JALANKAN PROGRAM UNTUK BEBERAPA SKENARIO
# ========================================

if __name__ == "__main__":
    print("\n\n")
    print("#" * 100)
    print("# SKENARIO 1: 6 RUMAH, START DARI RUMAH 0")
    print("#" * 100)
    
    ga1 = AlgoritmaGenetika_TSP(
        num_houses=6,
        pop_size=30,
        crossover_rate=0.8,
        mutation_rate=0.2,
        max_generations=100,
        start_house=0
    )
    hasil1 = ga1.run()
