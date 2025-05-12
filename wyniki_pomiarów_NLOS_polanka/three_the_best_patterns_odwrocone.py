import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Konfiguracja
DATA_DIR = 'wyniki_pomiarów_NLOS_polanka\V2X_23_04_25_daneRAW'
OUTPUT_DIR = 'wyniki_pomiarów_NLOS_polanka\wykresy_V2X_23_04_25'
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Wymiary siatki heatmapy
GRID_SIZE = (5, 5)

# Funkcja do generowania heatmapy
def generate_heatmap(data, annotations, filename, vmin, vmax):
    plt.figure(figsize=(6, 5))
    ax = sns.heatmap(data, annot=annotations, fmt='', cmap='Spectral', cbar=True, square=True, vmin=vmin, vmax=vmax)
    cbar = ax.collections[0].colorbar
    cbar.set_label('dBm')
    plt.title(f'Heatmap - Najlepsze Wzorce')
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, f'{filename}.png'))
    plt.close()

# Główna funkcja przetwarzania plików
def main():
    files = sorted([f for f in os.listdir(DATA_DIR) if f.endswith('.csv')])
    all_data = {i: {j: np.nan for j in range(1, 26)} for i in range(1, 28)}

    for file in files:
        file_num = int(file.split('_')[-1].split('.')[0])
        filepath = os.path.join(DATA_DIR, file)
        df = pd.read_csv(filepath, delimiter=';', header=None)
        for _, row in df.iterrows():
            pattern_num = int(row[0])
            value = float(row[3])
            if file_num in all_data[pattern_num]:
                all_data[pattern_num][file_num] = value

    all_values = [value for values in all_data.values() for value in values.values() if not np.isnan(value)]
    global_min = min(all_values)
    global_max = max(all_values)

    # Tworzenie globalnej mapy
    heatmap_data = np.full(GRID_SIZE, np.nan)
    annotations = np.full(GRID_SIZE, '', dtype=object)

    # Wypełnianie danych i anotacji
    for file_num in range(1, 26):  # Dla każdego punktu w siatce
        all_point_values = {pat: all_data[pat][file_num] for pat in all_data if not np.isnan(all_data[pat][file_num])}
        top_patterns = sorted(all_point_values, key=all_point_values.get, reverse=True)[:1]
        
        # Ustalamy pozycję w siatce (odwrócone indeksowanie)
        row, col = divmod(file_num - 1, GRID_SIZE[1])
        row = GRID_SIZE[0] - row - 1
        heatmap_data[row, col] = max(all_point_values.values())  # Najwyższa wartość w danym punkcie
        annotations[row, col] = ', '.join(map(str, top_patterns))  # Top 3 wzorce

    # Generowanie wykresu
    generate_heatmap(heatmap_data, annotations, 'heatmap_best_pattern', global_min, global_max)

if __name__ == "__main__":
    main()
