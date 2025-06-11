import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from io import StringIO
import matplotlib as mpl


mpl.rcParams['font.family'] = 'Times New Roman'
# Dane wejściowe

plik_csv = r"C:\Users\brzak\Documents\Pomiary_V2X\wyniki_pomiarów_NLOS_polanka\NLOS_RSU_12_05_25\pomiar_RSU_5.csv"

# Wczytanie danych
df = pd.read_csv(plik_csv, sep=";", header=None, names=["Pattern", "Timestamp", "X", "Y", "Frequency", "Power_dBm"])
df["X"] = np.abs(df["X"])
df["X"] = np.abs(df["X"] )
df["Y"] = np.abs(df["Y"] )

# Dodatkowy zbiór danych
xy_points = [
    [-0.374, -5.963],
    [-1.021, -5.99],
    [-1.559, -6.036],
    [-1.956, -6.036],
    [-2.366, -5.973],
    [-0.294, -5.698],
    [-0.884, -5.709],
    [-1.575, -5.76],
    [-1.997, -5.703],
    [-2.389, -5.62],
    [-0.444, -5.179],
    [-0.935, -5.199],
    [-1.434, -5.199],
    [-1.928, -5.181],
    [-2.326, -5.046],
    [-0.203, -4.663],
    [-0.78, -4.668],
    [-1.24, -4.656],
    [-1.733, -4.655],
    [-2.236, -4.666],
    [-0.057, -4.047],
    [-0.639, -4.059],
    [-1.119, -4.066],
    [-1.689, -3.997],
    [-2.187, -3.995],
]


# Konwersja dodatkowych punktów do osobnych list
xy_x = [x[0]  for x in xy_points]  # Dodajemy przesunięcie jak w oryginalnych danych
xy_y = [y[1]  for y in xy_points]
xy_x = np.abs(xy_x)
xy_y = np.abs(xy_y)



# Utworzenie wykresu
plt.figure(figsize=(12, 8))

# Scatter oryginalnych danych z większymi kółkami
sc = plt.scatter(
    df["X"], df["Y"],
    c=df["Power_dBm"],
    cmap="coolwarm",
    s=300,
    alpha=0.8,
    vmin=-119.2,
    vmax=-76.95,
    edgecolors='k'
)

# Poprawione etykiety na colorbar
cbar = plt.colorbar(sc)
cbar.set_label("[dBm]", fontsize=16, fontweight = 'bold')
cbar.ax.tick_params(labelsize=14)

# Scatter dla dodatkowych punktów
plt.scatter(
    xy_x, xy_y,
    color="black",
    s=100,
    alpha=1,
    marker="x"
)

# Numeracja dodatkowych punktów
for i, (x, y) in enumerate(zip(xy_x, xy_y)):
    plt.text(x, y +0.05, str(i), fontsize=14, ha='center', color='green')

# Numeracja punktów z danych
for i, row in df.iterrows():
    plt.text(row["X"], row["Y"], str(row["Pattern"]), fontsize=14, ha='center', va='center')

# Opisy osi
plt.xlabel("Współrzędna X", fontsize=16, fontweight = 'bold')
plt.ylabel("Współrzędna Y", fontsize=16, fontweight = 'bold')
plt.title("Moc odbierana na podstawie współrzędnych (X, Y)", fontsize=18, fontweight = 'bold')

# Dodatkowe ustawienia
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
plt.grid(alpha=0.3)
plt.legend(fontsize=14, loc='best', prop={'weight': 'bold'})
plt.tight_layout()

plt.show()