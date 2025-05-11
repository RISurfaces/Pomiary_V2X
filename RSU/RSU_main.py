import time
import glob
import os
import math
import ast  # Importujemy moduł ast
from RIS_usb_class import RIS_usb
import json
import numpy as np
from RsSmw import *
import serial
import datetime
import analyzer
import generator

try:
    with open ("config.json") as config_f:
        config = json.load(config_f)
        trace_file = config["TRACE_FILE"]
        start_freq=config["START_FREQ"]
        end_freq=config["END_FREQ"]
        step_freq=config["STEP_FREQ"]
        span=config["SPAN"]
        analyzer_mode=config["ANALYZER_MODE"]
        revlevel=config["REVLEVEL"]
        rbw=config["RBW"]
        ris_ports = config["RIS_PORTS"]
        generator_amplitude=config["GENERATOR_AMPLITUDE"]
        pattern_for_negation = config["ID_FOR_NEGATION"]
        # More modes will be add later.
        if config["GENERATOR_MODE"] == "CW":
            generator_mode = enums.FreqMode.CW
        else: 
            generator_mode = enums.FreqMode.CW
        config_f.close()
except FileNotFoundError:
    print("File with configuration doesn't exist.")
    exit()

print('start')

wybor = int(input("Podaj tryb RSU\n1 - Wszystkie patterny, 2 - Reduce SET \n"))

if wybor == 1: 



    patterns = [
        {"ID": 15, "HEX": "0xCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC"},
        {"ID": 15, "HEX": "0xCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC"},
        {"ID": 5, "HEX": "0xFF00FF00FF00FF00FF00FF00FF00FF00FF00FF00FF00FF00FF00FF00FF00FF00"},
        {"ID": 15, "HEX": "0xCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC"},
        {"ID": 18, "HEX": "0x0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F"},
        {"ID": 25, "HEX":"0x9F8D6B5A3C2E1D0F9B7A5C3E1D0F9B7A5C3E1D0F9B7A5C3E1D0F9B7A5C3E1D0F"},
        {"ID": 26, "HEX": "0xD3E7F0A2B4C6E8D1F2A3B5C7E9F0A2B4C6E8D1F2A3B5C7E9F0A2B4C6E8D1F28C"},
        {"ID": 17, "HEX": "0xF0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0"},
        {"ID": 5, "HEX": "0xFF00FF00FF00FF00FF00FF00FF00FF00FF00FF00FF00FF00FF00FF00FF00FF00"},
        {"ID": 6, "HEX": "0x00FF00FF00FF00FF00FF00FF00FF00FF00FF00FF00FF00FF00FF00FF00FF00FF"},
        {"ID": 2, "HEX": "0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF"},
        {"ID": 2, "HEX": "0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF"},
        {"ID": 6, "HEX": "0x00FF00FF00FF00FF00FF00FF00FF00FF00FF00FF00FF00FF00FF00FF00FF00FF"},
        {"ID": 6, "HEX": "0x00FF00FF00FF00FF00FF00FF00FF00FF00FF00FF00FF00FF00FF00FF00FF00FF"},
        {"ID": 18, "HEX": "0x0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F"},
        {"ID": 17, "HEX": "0xF0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0"},
        {"ID": 18, "HEX": "0x0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F"},
        {"ID": 27, "HEX": "0x5A3C2E1D0F9B7A5C3E1D0F9B7A5C3E1D0F9B7A5C3E1D0F9B7A5C3E1D0F9B7AB3"},
        {"ID": 22, "HEX": "0x000000003FFC3FFC300C300C33CC33CC33CC33CC300C300C3FFC3FFC00000000"},
        {"ID": 16, "HEX": "0x3333333333333333333333333333333333333333333333333333333333333333"},
        {"ID": 16, "HEX": "0x3333333333333333333333333333333333333333333333333333333333333333"},
        {"ID": 25, "HEX": "0x9F8D6B5A3C2E1D0F9B7A5C3E1D0F9B7A5C3E1D0F9B7A5C3E1D0F9B7A5C3E1D0F"},
        {"ID": 16, "HEX": "0x3333333333333333333333333333333333333333333333333333333333333333"},
        {"ID": 16, "HEX": "0x3333333333333333333333333333333333333333333333333333333333333333"},
        {"ID": 16, "HEX": "0x3333333333333333333333333333333333333333333333333333333333333333"},
        {"ID": 22, "HEX": "0x000000003FFC3FFC300C300C33CC33CC33CC33CC300C300C3FFC3FFC00000000"}]

elif wybor ==2: 

    patterns = [
        {"ID": 16, "HEX": "0x3333333333333333333333333333333333333333333333333333333333333333"},
        {"ID": 15, "HEX": "0xCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC"},
        {"ID": 18, "HEX": "0x0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F"},
        {"ID": 18, "HEX": "0x0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F"},
        {"ID": 17, "HEX": "0xF0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0"},
        {"ID": 18, "HEX": "0x0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F"},
        {"ID": 18, "HEX": "0x0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F"},
        {"ID": 2, "HEX": "0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF"},
        {"ID": 2, "HEX": "0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF"},
        {"ID": 2, "HEX": "0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF"},
        {"ID": 2, "HEX": "0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF"},
        {"ID": 2, "HEX": "0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF"},
        {"ID": 17, "HEX": "0xF0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0"},
        {"ID": 17, "HEX": "0xF0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0"},
        {"ID": 17, "HEX": "0xF0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0"},
        {"ID": 17, "HEX": "0xF0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0"},
        {"ID": 17, "HEX": "0xF0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0"},
        {"ID": 16, "HEX": "0x3333333333333333333333333333333333333333333333333333333333333333"},
        {"ID": 15, "HEX": "0xCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC"}]
        
        

else: 
    print("Błędny wybór")
    exit()


def set_pattern_ris(pattern : str, ris : RIS_usb):
        if ris.id % 2 == 1 and int(pattern["ID"]) in pattern_for_negation:
            ris_pattern = ris.ris_pattern_negation(pattern["HEX"])
        else:
            ris_pattern = pattern["HEX"]
        ris.set_pattern(ris_pattern)
        return True

def ris_usb_init() -> list:
    RIS_list = []
    id = 0
    for port in ris_ports:
        print(port, " ", id)
        RIS_list.append(RIS_usb(port, id))
        id += 1
    for ris in RIS_list:
        ris.reset()
    return RIS_list






# Ścieżka do pliku, z którego będą odczytywane liczby

def find_latest_file(directory_path):
    print(directory_path)
    # Wyszukanie wszystkich plików w folderze
    files = glob.glob(os.path.join(directory_path, "*"))
    
    if not files:  # Sprawdzenie, czy folder jest pusty
        print("Folder jest pusty!")
        return None
    
    # Znalezienie najnowszego pliku na podstawie czasu modyfikacji
    latest_file = max(files, key=os.path.getmtime)
    print("LA CUCA= ", latest_file)
    return latest_file

# Ścieżka do folderu, w którym szukasz plików
folder_path = "Logs"

# Znajdź najnowszy plik
latest_file = find_latest_file(folder_path)
print(latest_file)


# Ścieżka do pliku, z którego będą odczytywane liczby
file_path = latest_file



xy_points = [
    [-1.723, -2.582],
    [-1.852, -2.432],
    [-1.962, -2.255],
    [-2.057, -2.045],
    [-2.143, -1.89],
    [-2.202, -1.646],
    [-2.22, -1.304],
    [-2.257, -1.005],
    [-2.289, -0.73],
    [-2.326, -0.458],
    [-2.335, -0.169],
    [-2.309, 0.139],
    [-2.279, 0.345],
    [-2.224, 0.612],
    [-2.209, 1.007],
    [-2.111, 1.32],
    [-1.997, 1.577],
    [-1.872, 1.902],
    [-1.76, 2.112],
    [-1.603, 2.301],
    [-1.502, 2.399],
    [-1.332, 2.605],
    [-1.186, 2.706],
    [-1.017, 2.78],
    [-0.846, 2.873],
    [-0.825, 2.809]
]


# Definiowanie znanych patternów dla każdego punktu

# Łączenie współrzędnych z patternami
xy_points_with_patterns = [
    [x, y, patterns[i]] for i, [x, y] in enumerate(xy_points)
]




# Funkcja obliczająca odległość Euklidesową
def euclidean_distance(point1, point2):
    return math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)


# Funkcja do śledzenia nowej zawartości pliku
def follow_file(file_path,freq):
    prev_pattern = None
    numer_pomiaru = input("Podaj numer pomiaru: ")
    with open(file_path, "r") as file:
        #file.seek(0, 2)  # Przesunięcie wskaźnika na koniec pliku
        while True:
            file.seek(0, 2)
            line = file.readline()
            if not line:
                continue

            split_values = line.split(":")
            if len(split_values) > 6 and split_values[2] == "LE":
                try:
                    timestamp = float(split_values[1])  # Timestamp - tutaj możemy go zignorować
                    # Parsowanie współrzędnych w formie listy
                    coordinates = ast.literal_eval(split_values[6])  # Parsowanie ciągu na listę
                    x_val = coordinates[0]  # Pierwsza wartość to x
                    y_val = coordinates[1]  # Druga wartość to y

                    # Szukamy najbliższego punktu
                    closest_point = min(xy_points, key=lambda point: euclidean_distance(point, [x_val, y_val]))
                    distance = euclidean_distance(closest_point, [x_val, y_val])


                    if distance > 0.3:
                        print(f"Odległość ({distance}) jest większa niż 30cm, pomijam punkt.")
                        continue

                    index = xy_points.index(closest_point)
                    pattern = patterns[index]
                    analyzer.meas_prep(freq, span, analyzer_mode, revlevel, rbw)
                    if pattern != prev_pattern:
                        for ris in RIS_list:
                            is_pattern_set = set_pattern_ris(pattern, ris)
                        print("Ustawiono pattern: ", pattern)
                        with open(f"pomiar_RSU_{numer_pomiaru}.csv", 'a+') as file_to_write:
                                current_time = datetime.datetime.now()
                                file_to_write.write(f"{pattern['ID']};{current_time};{x_val};{y_val};")
                        analyzer.trace_get(f"pomiar_RSU_{numer_pomiaru}.csv")

                        prev_pattern = pattern
                    else: 
                        with open(f"pomiar_RSU_{numer_pomiaru}.csv", 'a+') as file_to_write:
                                current_time = datetime.datetime.now()
                                file_to_write.write(f"{pattern['ID']};{current_time};{x_val};{y_val};")
                        analyzer.trace_get(f"pomiar_RSU_{numer_pomiaru}.csv")

                        print("Nie zmieniono patternu")
                        #print(x_val,",",y_val)

                except Exception as e:
                    print(f"Błąd podczas przetwarzania linii: {line}")
                    print(f"Błąd: {e}")





# Śledzenie pliku w czasie rzeczywistym
RIS_list = ris_usb_init()
analyzer.com_prep()
analyzer.com_check()
generator.com_check()

freq = 5.5e9
generator.meas_prep(True, generator_mode, generator_amplitude,freq)


try:
    print(f"Śledzenie pliku: {file_path}")
    for new_line in follow_file(file_path,freq):
        print(f"Najnowsza wartość: {new_line}")
except KeyboardInterrupt:
    print("\nZakończono śledzenie pliku.")