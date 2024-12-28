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
def generate_plots(all_data, output_folder):
    # Ustalamy globalne minimum i maksimum dla osi Y
    global_min = all_data['Power'].min()
    global_max = all_data['Power'].max()+5
    
    # Pobieramy unikalne wartości z kolumny Index
    unique_indexes = all_data['Index'].unique()
    
    for index in unique_indexes:
        # Filtrujemy dane dla danego Index
        index_data = all_data[all_data['Index'] == index].sort_values(by='FileNumber')
        
        # Tworzymy wykres podstawowy
        plt.figure(figsize=(10, 6))
        plt.plot(index_data['FileNumber'], index_data['Power'], marker='o', linestyle='-', label=f'Index {index}')
        plt.title(f'Wykres mocy sygnału dla Index: {index}')
        plt.xlabel('Numer pliku')
        plt.ylabel('Moc sygnału [dB]')
        plt.ylim(global_min, global_max)  # Ustawiamy stały zakres osi Y
        plt.grid(True)
        plt.legend()
        
        # Zapis wykresu podstawowego
        output_file = os.path.join(output_folder, f"Index_{index}_wykres.png")
        plt.savefig(output_file)
        plt.close()
        print(f"Wykres zapisany: {output_file}")
    
    # Tworzenie jednego wykresu maksymalnych wartości ze wszystkich Index
    max_values = all_data.loc[all_data.groupby('FileNumber')['Power'].idxmax()]
    
    plt.figure(figsize=(12, 7))
    plt.plot(max_values['FileNumber'], max_values['Power'], marker='o', linestyle='-', color='red', label='Max Power')
    
    # Dodawanie oznaczeń dla numerów Index
    for _, row in max_values.iterrows():
        plt.text(row['FileNumber'], row['Power'], str(row['Index']), fontsize=9, ha='center', va='bottom')
    
    plt.title('Maksymalne wartości mocy sygnału (wszystkie Index)')
    plt.xlabel('Numer pliku')
    plt.ylabel('Moc sygnału [dB]')
    plt.ylim(global_min, global_max)  # Ustawiamy stały zakres osi Y
    plt.grid(True)
    plt.legend()
    
    # Zapis wykresu maksymalnych wartości
    max_output_file = os.path.join(output_folder, "Max_Power_wykres.png")
    plt.savefig(max_output_file)
    plt.close()
    print(f"Wykres maksymalnych wartości zapisany: {max_output_file}")

# Główne wykonanie
all_data = load_data(input_folder)
generate_plots(all_data, output_folder)

print("Proces generowania wykresów zakończony.")
