import os
import pandas as pd
import matplotlib.pyplot as plt
import re

# Ścieżka do folderu z plikami
input_folder = r'wyniki'
output_folder = r'wyniki'  # Folder na wykresy

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
    global_min = all_data['Power'].min() - 5
    global_max = all_data['Power'].max() + 1  # Dodano 1, aby uniknąć ucinania danych

    # Grupowanie danych według numeru pliku
    grouped = all_data.groupby('FileNumber')

    # Wyznaczanie dwóch największych wartości dla każdej grupy
    max_values = grouped.apply(lambda x: x.nlargest(1, 'Power')).reset_index(drop=True)

    filtered_data = all_data[all_data['Index'].isin([2, 15, 16, 17, 18])]
    filtered_grouped = filtered_data.groupby('FileNumber')
    second_max_values = filtered_grouped.apply(lambda x: x.nlargest(1, 'Power')).reset_index(drop=True)

    # Oznaczenia osi X
    custom_x_labels = [
        -43.2, -38.4, -33.6, -28.8, -24.0, -19.2, -14.4, -9.6, -4.8, 0.0,
        4.8, 9.6, 14.4, 19.2, 24.0, 28.8, 33.6, 38.4, 43.2
    ]
    file_numbers = sorted(all_data['FileNumber'].unique())  # Unikalne numery plików

    # Sprawdzenie, czy liczba etykiet pasuje do liczby numerów plików
    if len(custom_x_labels) != len(file_numbers):
        raise ValueError("Liczba oznaczeń osi X (custom_x_labels) musi być równa liczbie numerów plików.")

    plt.figure(figsize=(12, 7))

    # Pierwsza linia: Maksymalne wartości
    plt.plot(max_values['FileNumber'], max_values['Power'], marker='o', linestyle='-', color='red', label='Max Power')
    for _, row in max_values.iterrows():
        plt.text(
            row['FileNumber'],
            row['Power'] + 0.5,
            str(row['Index']),
            fontsize=9,
            ha='center',
            va='bottom',
            color='red'
        )

    # Druga linia: Drugie maksymalne wartości
    plt.plot(second_max_values['FileNumber'], second_max_values['Power'], marker='o', linestyle='--', color='blue',
             label='Suboptimal Power')
    for _, row in second_max_values.iterrows():
        plt.text(
            row['FileNumber'],
            row['Power'] - 0.5,
            str(row['Index']),
            fontsize=9,
            ha='center',
            va='top',
            color='blue'
        )

    # Ustawienia osi X
    plt.xticks(ticks=file_numbers, labels=[f"{x:.1f}" for x in custom_x_labels])

    plt.title('Maximum Power (All Patterns) and Suboptimal Power (Selected 5 Patterns)')
    plt.xlabel('Angle [°]')
    plt.ylabel('Received Power [dBm]')
    plt.ylim(-60, -44)  # Zmieniono zakres osi Y, aby uniknąć ucinania wartości
    plt.grid(True)
    plt.legend()

    # Zapis wykresu
    output_file = "Zoptymalizowany_wykres.png"
    plt.savefig(output_file)
    plt.close()
    print(f"Wykres zapisany z nowymi oznaczeniami osi X: {output_file}")


# Główne wykonanie
all_data = load_data(input_folder)
generate_plots(all_data, output_folder)

print("Proces generowania wykresów zakończony.")
