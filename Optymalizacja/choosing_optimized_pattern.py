import numpy as np
import itertools
import os
import csv

if __name__ == "__main__":
    """ Load measured power from files """
    folder_path = "wyniki"

    all_data = []

    for filename in os.listdir(folder_path): #there is strange sorting but for sum it doesn't matter, [10-19 1-9]
        if filename.endswith(".csv"):
            file_path = os.path.join(folder_path, filename)
            with open(file_path, 'r') as file:
                reader = csv.reader(file, delimiter=';')
                last_column_values = []
                for row in reader:
                    if row:
                        last_column_values.append(float(row[-1]))
                all_data.append(last_column_values)

    power_measured = []
    for i, data in enumerate(all_data, start=1):
        # print(f"Plik {i}: {data}")
        power_measured.append(data)

    """ Parameters """
    number_of_final_patterns = 3#5 will take longer
    min_pattern_value = 1
    max_pattern_value = 27
    number_of_measured_points = 19

    combinations = [list(comb) for comb in itertools.permutations(range(min_pattern_value, max_pattern_value + 1), number_of_final_patterns)] #List of all combinations possible

    """ Max power for each combination """
    max_for_each_combination = np.zeros((len(combinations), number_of_measured_points))
    for i, combination in enumerate(combinations):
        for j in range(number_of_measured_points):
            max_for_each_combination[i, j] = max([power_measured[j][x-1] for x in combination])
    
    pass

    """ Max power for all patterns """
    max_value_all_paterns = np.zeros((number_of_measured_points))
    for i, combination in enumerate(combinations):
        for j in range(number_of_measured_points):
            max_value_all_paterns[j] = max([power_measured[j][x] for x in range(max_pattern_value)])
    pass
    print("Max values for best patterns: ", max_value_all_paterns)


    """ Max power - Max combination power, in each point """
    sum_of_diff_max_to_final = np.zeros(len(combinations))
    for i, combination in enumerate(combinations):
        for id in range(number_of_measured_points):
            sum_of_diff_max_to_final[i] += max_for_each_combination[i][id] - max_value_all_paterns[id]

    """ plotting results """
    largest_index = np.argmax(sum_of_diff_max_to_final)
    print("Max values for chosen patterns: ", max_for_each_combination[largest_index])
    print("Min difference for patterns: ", combinations[largest_index])
    print("Min difference [dB] = ", np.max(sum_of_diff_max_to_final))



