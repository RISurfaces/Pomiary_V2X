import pandas as pd
import json
from datetime import datetime

with open("logi.txt", "r") as plik_wejsciowy, open("LE_logi.txt", "w") as plik_wyjsciowy:
    for linia in plik_wejsciowy:
        if ":LE:" in linia:
            plik_wyjsciowy.write(linia)

# Wczytaj mapę patternów z pliku JSON
with open('RIS_patterns.json', 'r') as f:
    ris_patterns = json.load(f)["PATTERNS"]

# Stwórz słownik: ID (int) -> HEX (string)
pattern_map = {int(pat["ID"]): pat["HEX"] for pat in ris_patterns}

# Lista plików CSV
file_template = "V2X_22_04_25_{}.csv"

ranges_output = []
max_power_patterns = []
zakres = int(input("PODAJ ILE MASZ PLIKÓW POMIAROWYCH: "))


for i in range(1, zakres+1):  # od 1 do 26
    filename = file_template.format(i)

    # Wczytaj plik CSV
    df = pd.read_csv(filename, header=None, sep=';')

    # Sprawdzenie liczby wierszy
    if len(df) < 27:
        print(f"Plik {filename} ma tylko {len(df)} wierszy! Pomijam.")
        continue

    # Wyciąganie zakresu czasu
    start_time_str = df.iloc[0, 1]
    end_time_str = df.iloc[26, 1]

    def convert_timestamp(ts):
        dt = datetime.strptime(ts, "%Y-%m-%d %H:%M:%S.%f")
        return dt.strftime("%H%M%S%f")[:-3]

    start_formatted = convert_timestamp(start_time_str)
    end_formatted = convert_timestamp(end_time_str)
    ranges_output.append(f"{start_formatted}, {end_formatted}")

    # Szukanie patternu o największej mocy
    max_power_index = df[3].idxmax()
    max_power_pattern_id = int(df.iloc[max_power_index, 0])
    max_power_patterns.append(max_power_pattern_id)

# Przygotuj dane do pliku wynikowego
output_patterns = []

for pattern_id in max_power_patterns:
    hex_value = pattern_map.get(pattern_id, "UNKNOWN_HEX")
    output_patterns.append({"ID": pattern_id, "HEX": hex_value})

# Zapisz ranges.txt
with open("ranges.txt", "w") as f:
    f.write("\n".join(ranges_output))

# Zapisz MAX_POWER_FOR_PATTERN.txt w żądanym formacie
with open("MAX_POWER_FOR_PATTERN.txt", "w") as f:
    f.write("patterns = [\n")
    for item in output_patterns:
        f.write(f'    {{"ID": {item["ID"]}, "HEX": "{item["HEX"]}"}},\n')
    f.write("]\n")

print("Pliki ranges.txt i MAX_POWER_FOR_PATTERN.txt zostały utworzone!")
