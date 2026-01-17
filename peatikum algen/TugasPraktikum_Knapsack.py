import random
import numpy as np
import matplotlib.pyplot as plt

class AlgoritmaGenetika_Knapsack:
    def __init__(self, capacity=50, pop_size=30, crossover_rate=0.8, 
                 mutation_rate=0.15, max_generations=100):
        """Inisialisasi parameter Algoritma Genetika untuk Knapsack Problem"""
        self.capacity = capacity
        self.pop_size = pop_size
        self.crossover_rate = crossover_rate
        self.mutation_rate = mutation_rate
        self.max_generations = max_generations
        
        # Data barang: (nama, weight, value, available_quantity)
        self.items = [
            ("Item_A", 3, 10, 5),   # weight=3, value=10, max_qty=5
            ("Item_B", 5, 15, 4),   # weight=5, value=15, max_qty=4
            ("Item_C", 2, 8, 6),    # weight=2, value=8, max_qty=6
            ("Item_D", 7, 20, 3),   # weight=7, value=20, max_qty=3
            ("Item_E", 4, 12, 5),   # weight=4, value=12, max_qty=5
        ]
        
        self.num_items = len(self.items)
        
        # Tracking untuk history
        self.fitness_history = []
        self.best_fitness_history = []
        self.worst_fitness_history = []
        self.weight_history = []
        
        print(f"\n[DATA BARANG KNAPSACK]")
        print("─" * 80)
        print(f"{'Item':<12} {'Weight':<10} {'Value':<10} {'Available':<12} {'Value/Weight':<15}")
        print("─" * 80)
        for name, weight, value, available in self.items:
            ratio = value / weight
            print(f"{name:<12} {weight:<10} {value:<10} {available:<12} {ratio:<15.4f}")
        print("─" * 80)
        print(f"Kapasitas Knapsack: {self.capacity} unit\n")
    
    def hitung_total_weight(self, chromosome):
        """Hitung total weight dari kromosom"""
        total_weight = 0
        for i in range(self.num_items):
            qty = chromosome[i]
            item_weight = self.items[i][1]
            total_weight += qty * item_weight
        return total_weight
    
    def hitung_total_value(self, chromosome):
        """Hitung total value dari kromosom"""
        total_value = 0
        for i in range(self.num_items):
            qty = chromosome[i]
            item_value = self.items[i][2]
            total_value += qty * item_value
        return total_value
    
    def is_valid_chromosome(self, chromosome):
        """Check apakah kromosom valid (weight <= capacity, qty <= available)"""
        total_weight = 0
        
        for i in range(self.num_items):
            qty = chromosome[i]
            available = self.items[i][3]
            item_weight = self.items[i][1]
            
            # Check quantity constraint
            if qty > available or qty < 0:
                return False
            
            # Check weight constraint
            total_weight += qty * item_weight
            if total_weight > self.capacity:
                return False
        
        return True
    
    def hitung_fitness(self, chromosome):
        """Hitung fitness (total value)"""
        # Jika invalid, fitness = 0
        if not self.is_valid_chromosome(chromosome):
            return 0
        
        total_value = self.hitung_total_value(chromosome)
        return total_value
    
    def inisialisasi_populasi(self):
        """
        Inisialisasi populasi awal random
        Kromosom: [qty_item_0, qty_item_1, ..., qty_item_n]
        """
        populasi = []
        
        for _ in range(self.pop_size):
            # Generate random chromosome
            valid = False
            attempts = 0
            
            while not valid and attempts < 100:
                chromosome = []
                total_weight = 0
                
                for i in range(self.num_items):
                    available = self.items[i][3]
                    item_weight = self.items[i][1]
                    
                    # Random quantity antara 0 dan available
                    max_qty = min(available, max(0, int((self.capacity - total_weight) / item_weight)))
                    qty = random.randint(0, max_qty)
                    
                    chromosome.append(qty)
                    total_weight += qty * item_weight
                
                if self.is_valid_chromosome(chromosome):
                    valid = True
                
                attempts += 1
            
            if valid:
                populasi.append(chromosome)
            else:
                # Fallback: all zero
                populasi.append([0] * self.num_items)
        
        return populasi
    
    def crossover_single_point(self, parent1, parent2):
        """Single-point crossover"""
        crossover_point = random.randint(1, self.num_items - 1)
        
        child1 = parent1[:crossover_point] + parent2[crossover_point:]
        child2 = parent2[:crossover_point] + parent1[crossover_point:]
        
        return child1, child2
    
    def mutasi_adjustment(self, chromosome):
        """Mutation: adjust quantity of random item"""
        mutated = chromosome.copy()
        
        # Select random item
        item_idx = random.randint(0, self.num_items - 1)
        available = self.items[item_idx][3]
        item_weight = self.items[item_idx][1]
        current_weight = self.hitung_total_weight(mutated)
        
        # Adjust quantity
        current_qty = mutated[item_idx]
        
        if random.random() < 0.5:
            # Increase quantity
            new_qty = min(available, current_qty + random.randint(1, 2))
        else:
            # Decrease quantity
            new_qty = max(0, current_qty - random.randint(1, 2))
        
        mutated[item_idx] = new_qty
        
        # Validate dan repair jika perlu
        if not self.is_valid_chromosome(mutated):
            # Revert
            mutated[item_idx] = current_qty
        
        return mutated
    
    def seleksi_roulette_wheel(self, populasi, fitness_scores):
        """Roulette wheel selection"""
        total_fitness = sum(fitness_scores)
        
        if total_fitness == 0:
            return random.choice(populasi)
        
        probabilitas = [f / total_fitness for f in fitness_scores]
        idx = random.choices(range(len(populasi)), weights=probabilitas, k=1)[0]
        return populasi[idx]
    
    def run(self):
        """Jalankan algoritma genetika untuk Knapsack Problem"""
        print("=" * 100)
        print("ALGORITMA GENETIKA - KNAPSACK PROBLEM (FRACTIONAL)")
        print("=" * 100)
        
        # [3] PARAMETER MODEL
        print(f"\n[3] PARAMETER MODEL ALGORITMA GENETIKA:")
        print(f"    - Jumlah Barang: {self.num_items}")
        print(f"    - Kapasitas Knapsack: {self.capacity} unit")
        print(f"    - Ukuran Populasi: {self.pop_size}")
        print(f"    - Probabilitas Crossover: {self.crossover_rate} ({self.crossover_rate*100:.0f}%)")
        print(f"    - Probabilitas Mutasi: {self.mutation_rate} ({self.mutation_rate*100:.0f}%)")
        print(f"    - Maksimal Generasi: {self.max_generations}")
        print(f"    - Tipe Kromosom: Real-valued (Quantity per item)")
        print(f"    - Tipe Crossover: SINGLE-POINT")
        print(f"    - Tipe Mutasi: QUANTITY ADJUSTMENT")
        print(f"    - Seleksi Parent: ROULETTE WHEEL")
        print(f"    - Elitisme: YA")
        
        # [4] REPRESENTASI KROMOSOM
        print(f"\n[4] REPRESENTASI KROMOSOM:")
        print(f"    - Tipe: Real-valued (Integer quantities)")
        print(f"    - Format: [qty_item_0, qty_item_1, ..., qty_item_{self.num_items-1}]")
        print(f"    - Panjang Kromosom: {self.num_items}")
        print(f"    - Contoh: [2, 3, 1, 0, 2]")
        print(f"    - Interpretasi: 2×ItemA + 3×ItemB + 1×ItemC + 0×ItemD + 2×ItemE")
        print(f"    - Constraint: qty[i] ≤ available[i], Σ(qty[i] × weight[i]) ≤ {self.capacity}")
        print(f"    - Total Kromosom Teoritis: ∏(available[i]+1) = {np.prod([av+1 for _, _, _, av in self.items])} (sangat besar)")
        
        # [5] POPULASI GENERASI PERTAMA
        populasi = self.inisialisasi_populasi()
        print(f"\n[5] POPULASI GENERASI PERTAMA ({self.pop_size} INDIVIDU):")
        print("─" * 100)
        print(f"{'No':<5} {'Kromosom':<35} {'Weight':<10} {'Value':<10} {'Fitness':<10}")
        print("─" * 100)
        
        # [6] NILAI FITNESS GENERASI PERTAMA
        fitness_gen1 = []
        weight_gen1 = []
        data_gen1 = []
        
        for idx, chromosome in enumerate(populasi, 1):
            weight = self.hitung_total_weight(chromosome)
            value = self.hitung_total_value(chromosome)
            fitness = self.hitung_fitness(chromosome)
            
            fitness_gen1.append(fitness)
            weight_gen1.append(weight)
            data_gen1.append((chromosome.copy(), weight, value, fitness))
            
            chrom_str = str(chromosome)[:35]
            print(f"{idx:<5} {chrom_str:<35} {weight:<10.1f} {value:<10.1f} {fitness:<10.1f}")
        
        print("─" * 100)
        
        # [6] ANALISIS FITNESS GENERASI 1
        print(f"\n[6] ANALISIS NILAI FITNESS GENERASI 1:")
        print(f"    - Fitness Maksimum (Terbaik): {max(fitness_gen1):.2f}")
        print(f"    - Fitness Minimum (Terburuk): {min(fitness_gen1):.2f}")
        print(f"    - Fitness Rata-rata: {np.mean(fitness_gen1):.2f}")
        print(f"    - Standar Deviasi: {np.std(fitness_gen1):.2f}")
        print(f"    - Total Weight (Rata-rata): {np.mean(weight_gen1):.2f}")
        
        # [7] CONTOH CROSSOVER & MUTASI
        print(f"\n[7] CONTOH CROSSOVER & MUTASI (GENERASI 1):")
        print("─" * 100)
        
        parent1 = populasi[0]
        parent2 = populasi[1]
        child1, child2 = self.crossover_single_point(parent1, parent2)
        child1_mutated = self.mutasi_adjustment(child1.copy())
        child2_mutated = self.mutasi_adjustment(child2.copy())
        
        w_p1 = self.hitung_total_weight(parent1)
        v_p1 = self.hitung_total_value(parent1)
        f_p1 = self.hitung_fitness(parent1)
        
        w_p2 = self.hitung_total_weight(parent2)
        v_p2 = self.hitung_total_value(parent2)
        f_p2 = self.hitung_fitness(parent2)
        
        w_c1 = self.hitung_total_weight(child1)
        v_c1 = self.hitung_total_value(child1)
        f_c1 = self.hitung_fitness(child1)
        
        w_c2 = self.hitung_total_weight(child2)
        v_c2 = self.hitung_total_value(child2)
        f_c2 = self.hitung_fitness(child2)
        
        w_c1m = self.hitung_total_weight(child1_mutated)
        v_c1m = self.hitung_total_value(child1_mutated)
        f_c1m = self.hitung_fitness(child1_mutated)
        
        w_c2m = self.hitung_total_weight(child2_mutated)
        v_c2m = self.hitung_total_value(child2_mutated)
        f_c2m = self.hitung_fitness(child2_mutated)
        
        print(f"Parent 1:          {parent1}")
        print(f"  - Weight: {w_p1:.1f}, Value: {v_p1:.1f}, Fitness: {f_p1:.1f}")
        print(f"\nParent 2:          {parent2}")
        print(f"  - Weight: {w_p2:.1f}, Value: {v_p2:.1f}, Fitness: {f_p2:.1f}")
        print(f"\n[SINGLE-POINT CROSSOVER (point={random.randint(1, self.num_items-1)})]")
        print(f"Child 1 (Pre):     {child1}")
        print(f"  - Weight: {w_c1:.1f}, Value: {v_c1:.1f}, Fitness: {f_c1:.1f}")
        print(f"\nChild 2 (Pre):     {child2}")
        print(f"  - Weight: {w_c2:.1f}, Value: {v_c2:.1f}, Fitness: {f_c2:.1f}")
        print(f"\n[QUANTITY ADJUSTMENT MUTATION]")
        print(f"Child 1 (Post):    {child1_mutated}")
        print(f"  - Weight: {w_c1m:.1f}, Value: {v_c1m:.1f}, Fitness: {f_c1m:.1f}")
        print(f"\nChild 2 (Post):    {child2_mutated}")
        print(f"  - Weight: {w_c2m:.1f}, Value: {v_c2m:.1f}, Fitness: {f_c2m:.1f}")
        print("─" * 100)
        
        best_overall = data_gen1[fitness_gen1.index(max(fitness_gen1))]
        
        # Loop Generasi
        for gen in range(1, self.max_generations + 1):
            # Hitung fitness populasi sekarang
            fitness_scores = [self.hitung_fitness(chrom) for chrom in populasi]
            weight_scores = [self.hitung_total_weight(chrom) for chrom in populasi]
            
            best_fit = max(fitness_scores)
            worst_fit = min(fitness_scores)
            avg_fit = np.mean(fitness_scores)
            avg_weight = np.mean(weight_scores)
            
            self.fitness_history.append(avg_fit)
            self.best_fitness_history.append(best_fit)
            self.worst_fitness_history.append(worst_fit)
            self.weight_history.append(avg_weight)
            
            best_idx = fitness_scores.index(best_fit)
            best_chromosome = populasi[best_idx]
            best_weight = self.hitung_total_weight(best_chromosome)
            
            if best_fit > best_overall[3]:
                best_overall = (best_chromosome.copy(), best_weight, 
                               self.hitung_total_value(best_chromosome), best_fit)
            
            # Generate new population dengan ELITISME
            new_population = [best_chromosome.copy()]
            
            while len(new_population) < self.pop_size:
                parent1 = self.seleksi_roulette_wheel(populasi, fitness_scores)
                parent2 = self.seleksi_roulette_wheel(populasi, fitness_scores)
                
                if random.random() < self.crossover_rate:
                    child1, child2 = self.crossover_single_point(parent1, parent2)
                else:
                    child1, child2 = parent1.copy(), parent2.copy()
                
                if random.random() < self.mutation_rate:
                    child1 = self.mutasi_adjustment(child1)
                if random.random() < self.mutation_rate:
                    child2 = self.mutasi_adjustment(child2)
                
                new_population.append(child1)
                if len(new_population) < self.pop_size:
                    new_population.append(child2)
            
            populasi = new_population[:self.pop_size]
        
        # [8] GRAFIK PERKEMBANGAN FITNESS
        print(f"\n[8] GRAFIK PERKEMBANGAN FITNESS PER GENERASI:")
        print("─" * 80)
        
        plt.figure(figsize=(15, 5))
        
        # Plot 1: Fitness per Generasi
        plt.subplot(1, 3, 1)
        generasi = range(1, self.max_generations + 1)
        plt.plot(generasi, self.best_fitness_history, 'g-o', label='Best Fitness', linewidth=2, markersize=3)
        plt.plot(generasi, self.fitness_history, 'b--', label='Average Fitness', linewidth=2)
        plt.plot(generasi, self.worst_fitness_history, 'r--', label='Worst Fitness', linewidth=2)
        plt.xlabel('Generasi', fontsize=11)
        plt.ylabel('Fitness (Total Value)', fontsize=11)
        plt.title('Perkembangan Fitness per Generasi', fontsize=12, fontweight='bold')
        plt.legend(fontsize=9)
        plt.grid(True, alpha=0.3)
        
        # Plot 2: Weight usage per Generasi
        plt.subplot(1, 3, 2)
        plt.plot(generasi, self.weight_history, 'purple', linewidth=2, label='Avg Weight')
        plt.axhline(y=self.capacity, color='r', linestyle='--', linewidth=2, label=f'Capacity ({self.capacity})')
        plt.xlabel('Generasi', fontsize=11)
        plt.ylabel('Weight', fontsize=11)
        plt.title('Penggunaan Kapasitas per Generasi', fontsize=12, fontweight='bold')
        plt.legend(fontsize=9)
        plt.grid(True, alpha=0.3)
        
        # Plot 3: Best solution composition
        plt.subplot(1, 3, 3)
        best_items = best_overall[0]
        item_names = [item[0] for item in self.items]
        colors = plt.cm.Set3(range(len(item_names)))
        
        plt.bar(item_names, best_items, color=colors, edgecolor='black')
        plt.xlabel('Item', fontsize=11)
        plt.ylabel('Quantity', fontsize=11)
        plt.title(f'Solusi Terbaik (Value={best_overall[3]:.0f})', fontsize=12, fontweight='bold')
        plt.grid(True, alpha=0.3, axis='y')
        
        plt.tight_layout()
        plt.savefig('hasil_knapsack.png', dpi=300, bbox_inches='tight')
        print("✓ Grafik tersimpan sebagai 'hasil_knapsack.png'")
        plt.show()
        
        # [9] HASIL AKHIR DAN ANALISIS KONVERGENSI
        print(f"\n[9] HASIL OPTIMASI AKHIR:")
        print("─" * 80)
        print(f"Solusi Terbaik (Kromosom): {best_overall[0]}")
        print(f"\nDetil Barang yang Diambil:")
        print(f"{'Item':<12} {'Qty':<6} {'Weight':<10} {'Value':<10}")
        print("─" * 40)
        total_value = 0
        total_weight = 0
        for i, (name, weight, value, available) in enumerate(self.items):
            qty = best_overall[0][i]
            if qty > 0:
                print(f"{name:<12} {qty:<6} {qty*weight:<10.1f} {qty*value:<10.1f}")
                total_value += qty * value
                total_weight += qty * weight
        print("─" * 40)
        print(f"{'TOTAL':<12} {'':<6} {total_weight:<10.1f} {total_value:<10.1f}")
        print(f"\nTotal Weight: {best_overall[1]:.1f} / {self.capacity} ({100*best_overall[1]/self.capacity:.1f}%)")
        print(f"Total Value (Fitness): {best_overall[3]:.2f}")
        gen_conv = self.best_fitness_history.index(best_overall[3]) + 1
        print(f"Generasi Pencapaian: {gen_conv} (dari {self.max_generations})")
        
        improvement = ((best_overall[3] - min(fitness_gen1)) / min(fitness_gen1)) * 100
        print(f"Improvement dari Gen 1: {improvement:.2f}%")
        
        # Analisis Konvergensi
        print(f"\n[ANALISIS KONVERGENSI]:")
        print(f"    - Gen 1-30: Improvement {(self.best_fitness_history[29] - self.best_fitness_history[0]) / self.best_fitness_history[0] * 100:.2f}%")
        print(f"    - Gen 30-60: Improvement {(self.best_fitness_history[59] - self.best_fitness_history[29]) / self.best_fitness_history[29] * 100:.2f}%")
        print(f"    - Gen 60-100: Improvement {(self.best_fitness_history[-1] - self.best_fitness_history[59]) / self.best_fitness_history[59] * 100:.2f}%")
        
        print("\n" + "=" * 100)
        
        return best_overall


# ========================================
# JALANKAN PROGRAM
# ========================================

if __name__ == "__main__":
    ga = AlgoritmaGenetika_Knapsack(
        capacity=50,
        pop_size=30,
        crossover_rate=0.8,
        mutation_rate=0.15,
        max_generations=100
    )
    
    hasil = ga.run()
