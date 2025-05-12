import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
#Jest tutaj odwrócona kolejność punktów pomiarowych, które były robione 23_04. Więc ten plik jest tylko do generowania wyników z 23.04
# Konfiguracja
DATA_DIR = 'wyniki_pomiarów_NLOS_polanka\V2X_23_04_25_daneRAW'
OUTPUT_DIR = 'wyniki_pomiarów_NLOS_polanka\wykresy_V2X_23_04_25'
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Wymiary siatki heatmapy
GRID_SIZE = (5, 5)

# Funkcja do generowania heatmapy
def generate_heatmap(data, pat_num, vmin, vmax):
    plt.figure(figsize=(6, 5))
    ax = sns.heatmap(data, annot=True, fmt='.2f', cmap='Spectral', cbar=True, square=True, vmin=vmin, vmax=vmax)
    cbar = ax.collections[0].colorbar
    cbar.set_label('[dBm]')
    plt.title(f'Heatmap pattern {pat_num}')
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, f'heatmap_pattern_{pat_num}.png'))
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


    all_values = [value for values in all_data.values() for value in values.values() if not np.isnan(value)]
    global_min = min(all_values)
    global_max = max(all_values)

    for pattern_num, values in all_data.items():
        heatmap_data = np.full(GRID_SIZE, np.nan)
        for file_num, value in values.items():
            row, col = divmod(file_num - 1, GRID_SIZE[1])
            
            heatmap_data[GRID_SIZE[0] - row - 1, col] = value
        generate_heatmap(heatmap_data, pattern_num, global_min, global_max)

if __name__ == "__main__":
    main()
