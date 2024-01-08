import matplotlib.pyplot as plt
import pandas as pd

def get_numbers(dataframe, column_name):
    numbers = []
    for value in dataframe[column_name]:
        if isinstance(value, (int, float)):
            numbers.append(value)
    return numbers

def find_positive_and_negative(numbers_list):
    positive = []
    negative = []
    for j in numbers_list:
        if j >= 0:
            positive.append(j)
        else:
            negative.append(j)

    return positive, negative

def find_coordinates(data, values, pos, neg):
    count_pos = 0
    count_neg = 0
    for m in values:
        if m == pos:
            break
        else:
            count_pos += 1
    for n in values:
        if n == neg:
            break
        else:
            count_neg += 1
    count_pos = count_pos - 1 if count_pos == len(data) else count_pos
    count_neg = count_neg - 1 if count_neg == len(data) else count_neg
    return data[count_pos], data[count_neg]

def process_data(file_path):
    df = pd.read_csv(file_path)
    columns = ['Hysteresis', 'Unnamed: 1', 'Unnamed: 2', 'Unnamed: 3', 'Unnamed: 4', 'Unnamed: 5', 'Unnamed: 6', 'Unnamed: 7']
    numbers = []

    for column in columns:
        numbers_list = get_numbers(df, column)
        numbers_list = [n for n in numbers_list if isinstance(n, (int, float)) and not pd.isna(n) and not pd.isnull(n)]
        numbers.append(numbers_list)

    x = numbers[2]
#    print('x =',x)
    y = numbers[3]
    data = list(zip(x, y))
    min_value_x = min(numbers[2])
    min_value_y = min(numbers[3])

    max_value_x = max(numbers[2])
    max_value_y = max(numbers[3])

    x_positive, x_negative = find_positive_and_negative(x)
    x_pos_zero = min(x_positive, key=lambda x: abs(x))
    x_neg_zero = min(x_negative, key=lambda x: abs(x))

    y_positive, y_negative = find_positive_and_negative(y)
    y_pos_zero = min(y_positive, key=lambda x: abs(x))
    y_neg_zero = min(y_negative, key=lambda x: abs(x))

    x1_intercept, x2_intercept = find_coordinates(data, x, x_pos_zero, x_neg_zero)
    y1_intercept, y2_intercept = find_coordinates(data, y, y_pos_zero, y_neg_zero)

    offset = min_value_y
    loop_area = sum([abs(y[i]) * (x[i + 1] - x[i]) for i in range(len(x) - 1)])
    vert_shift = min_value_y
    horiz_shift = min_value_x
    cmax_eff = max_value_y
    keff = max_value_x

    return offset, loop_area, vert_shift, horiz_shift, cmax_eff, keff, x1_intercept, x2_intercept, y1_intercept, y2_intercept

def main():
    num_files = 10000
    data_list = []

    for i in range(1, num_files + 1):
        file_path = f'Phone12.csv'
        data_list.append(process_data(file_path))
    loop_numbers = list(range(1, num_files + 1))
    y_intercepts_pos = [data[8] for data in data_list]
    y_intercepts_neg = [data[9] for data in data_list]
    plt.figure(figsize=(10, 6))
    for i, data in enumerate(data_list):
        x, y = data[6], data[7]
        plt.plot(x, y, label=f'Data {i + 1}')
    plt.xlabel('Drive Voltage')
    plt.ylabel('Polarization')
    plt.title('Ferroelectric Hysteresis')
    plt.legend()
    plt.grid(True)
    plt.show()

    plt.figure(figsize=(10, 6))
    plt.plot(loop_numbers, y_intercepts_pos, label='Positive Y-Intercepts')
    plt.plot(loop_numbers, y_intercepts_neg, label='Negative Y-Intercepts')

    plt.xlabel('Loop Number')
    plt.ylabel('Polarization')
    plt.title('Positive and Negative Y-Intercepts')
    plt.legend()
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    main()