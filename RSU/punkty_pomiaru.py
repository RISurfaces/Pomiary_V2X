# Wczytaj przedziały z pliku ranges.txt
ranges = []

with open("ranges.txt", "r") as file:
    for line in file:
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        start, end = map(int, line.split(","))
        ranges.append((start, end))

# Wczytaj wszystkie linie z pliku LE_logi.txt
with open("LE_logi.txt", "r") as file:
    lines = file.readlines()

# Wyniki dla każdego przedziału
results = []

for start, end in ranges:
    values_sum = [0, 0, 0]  # Suma wartości [X, Y, Z]
    count = 0

    for line in lines:
        if line.startswith("T:"):
            try:
                timestamp = int(line.split(":")[1].split(".")[0])
                if start <= timestamp <= end:
                    values = line.split("[")[1].split("]")[0].split(",")
                    values = [float(v) for v in values]
                    values_sum[0] += values[0]
                    values_sum[1] += values[1]
                    values_sum[2] += values[2]
                    count += 1
            except ValueError:
                continue

    if count > 0:
        averages = [v / count for v in values_sum]
    else:
        averages = [0, 0, 0]

    results.append(averages)  # zapisujemy tylko średnie

# Teraz zapisujemy wyniki jako listę xy_points
with open("punkty_pomiaru.txt", "w") as summary_file:
    summary_file.write("xy_points = [\n")
    for avg in results:
        x = round(avg[0], 3)  # Zaokrąglij do 3 miejsc po przecinku
        y = round(avg[1], 3)
        summary_file.write(f"    [{x}, {y}],\n")
    summary_file.write("]\n")
