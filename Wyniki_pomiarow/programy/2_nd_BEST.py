import os
import pandas as pd
import matplotlib.pyplot as plt
import re 

# Ścieżka do folderu z plikami
input_folder = r'C:\Users\Paweł\Desktop\RIS\Ris\Python_RIS\Pomiary_SYBIS\wyniki'
output_folder = r'C:\Users\Paweł\Desktop\RIS\Ris\Python_RIS\Pomiary_SYBIS\wykresy'  # Folder na wykresy


# Tworzenie folderu na wykresy, jeśli nie istnieje
os.makedirs(output_folder, exist_ok=True)

# Funkcja do wyciągania numeru pliku z nazwy pliku
def extract_file_number(file_name):
    match = re.search(r'_(\d+)\.csv$', file_name)  # Wyszukujemy "_[numer].csv" w nazwie
    if match:
        return int(match.group(1))
    return None

# Funkcja do wczytania danych ze wszystkich plików i ich połączenia
def load_data(input_folder):
    combined_data = []

    # Iterujemy przez pliki w folderze
    for file_name in sorted(os.listdir(input_folder)):
        if file_name.endswith('.csv'):
            file_path = os.path.join(input_folder, file_name)
            file_number = extract_file_number(file_name)  # Wyciągamy numer pliku
            
            if file_number is not None:
                # Wczytujemy dane z pliku
                df = pd.read_csv(file_path, sep=';', header=None, names=['Index', 'Timestamp', 'Frequency', 'Power'])
                df['FileNumber'] = file_number  # Dodajemy kolumnę z numerem pliku
                combined_data.append(df)
    
    # Łączymy wszystkie dane w jeden DataFrame
    if combined_data:
        all_data = pd.concat(combined_data, ignore_index=True)
    else:
        all_data = pd.DataFrame(columns=['Index', 'Timestamp', 'Frequency', 'Power', 'FileNumber'])
    
    return all_data

# Funkcja do generowania wykresów
# Funkcja do generowania wykresów
def generate_plots(all_data, output_folder):
    # Ustalamy globalne minimum i maksimum dla osi Y
    global_min = all_data['Power'].min()-5
    global_max = all_data['Power'].max()+5
    
    # Grupowanie danych według numeru pliku
    grouped = all_data.groupby('FileNumber')

    # Wyznaczanie dwóch największych wartości dla każdej grupy
    max_values = grouped.apply(lambda x: x.nlargest(1, 'Power')).reset_index(drop=True)
    second_max_values = grouped.apply(lambda x: x.nlargest(2, 'Power').iloc[1] if len(x) > 1 else None).dropna().reset_index(drop=True)
    
    # Wyznaczanie minimalnych wartości dla każdej grupy
    min_values = grouped.apply(lambda x: x.nsmallest(1, 'Power')).reset_index(drop=True)

    plt.figure(figsize=(12, 7))
    
    # Pierwsza linia: Maksymalne wartości
    plt.plot(max_values['FileNumber'], max_values['Power'], marker='o', linestyle='-', color='red', label='Max Power')
    for _, row in max_values.iterrows():
        # Przesuwamy etykiety dla maksymalnych wartości nieco w górę i w prawo
        plt.text(
            row['FileNumber'], 
            row['Power'] + 0.5,  # Przesunięcie w osi Y
            str(row['Index']), 
            fontsize=9, 
            ha='center', 
            va='bottom', 
            color='red'
        )
    
    # Druga linia: Drugie największe wartości
    plt.plot(second_max_values['FileNumber'], second_max_values['Power'], marker='o', linestyle='--', color='blue', label='Second Max Power')
    for _, row in second_max_values.iterrows():
        # Przesuwamy etykiety dla drugich maksymalnych wartości nieco w dół i w lewo
        plt.text(
            row['FileNumber'], 
            row['Power'] - 0.5,  # Przesunięcie w osi Y
            str(row['Index']), 
            fontsize=9, 
            ha='center', 
            va='top', 
            color='blue'
        )
    
    # Trzecia linia: Minimalne wartości
    plt.plot(min_values['FileNumber'], min_values['Power'], marker='o', linestyle='-.', color='green', label='Min Power')
    for _, row in min_values.iterrows():
        # Przesuwamy etykiety dla minimalnych wartości nieco w dół i w prawo
        plt.text(
            row['FileNumber'], 
            row['Power'] - 0.5,  # Przesunięcie w osi Y
            str(row['Index']), 
            fontsize=9, 
            ha='center', 
            va='top', 
            color='green'
        )
    
    plt.title('Maksymalne, drugie maksymalne i minimalne wartości mocy sygnału (wszystkie Index)')
    plt.xlabel('Numer pliku')
    plt.ylabel('Moc sygnału [dB]')
    plt.ylim(global_min, global_max)  # Stały zakres osi Y
    plt.grid(True)
    plt.legend()
    
    # Zapis wykresu maksymalnych i minimalnych wartości
    output_file = os.path.join(output_folder, "Max_Min_and_Second_Max_Power_wykres.png")
    plt.savefig(output_file)
    plt.close()
    print(f"Wykres maksymalnych, drugich maksymalnych i minimalnych wartości zapisany: {output_file}")

# Główne wykonanie
all_data = load_data(input_folder)
generate_plots(all_data, output_folder)

print("Proces generowania wykresów zakończony.")
