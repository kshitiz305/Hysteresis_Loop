# Brayden Newlin and Ruiyao Hei
# find 2 x-intercepts [(1.557,0.4), (-0.45, -2.729)]
# find 2 y-intercepts [(0.023, 13.796), (-0.011, -18.295)]
# find absolute max and absolute min
# Read from a data file

import matplotlib.pyplot as plt
import pandas as pd

# utiiize pandas to be able to read an excel file

def get_numbers(dataframe, column_name):
    numbers = []
    for value in dataframe[column_name]:
        if isinstance(value, (int, float)):
            numbers.append(value)
    return numbers

# This function gets the positive and negative values from  the Excel.  It then adds each to their own list.

def find_positive_and_negative(list):
    positive = []
    negative = []
    for j in list:
        if j >= 0:
            positive.append(j)
        else:
            print(j)
            negative.append(j)

    return positive, negative

# This funtion gathers the coordinates that are then later plotted.

def find_coordinates(data, list, pos, neg):
    count_pos = 0
    count_neg = 0
    for m in list:
        if m == pos:
            break
        else:
            count_pos += 1
    for n in list:
        if n == neg:
            break
        else:
            count_neg += 1
    count_pos = count_pos - 1 if count_pos == len(data) else count_pos
    count_neg = count_neg - 1 if count_neg == len(data) else count_neg
    return data[count_pos], data[count_neg]

# Creating a data frame python using pandas so that we can pull numbes from it
# The excel_file_path is unique to each person and should be where the data file is stored locally.

pd.set_option('display.float_format', '{:.10f}'.format)

excel_file_path = '/Users/jnewlin98/desktop/Phone12.xlsx'
csv_file_path = 'Phone12.csv'

# df = pd.read_excel(excel_file_path, sheet_name='Sheet1')
df = pd.read_csv(csv_file_path)
# print(df)
# Pulling Values out of each Column and putting them in a list

columns = ['Hysteresis', 'Unnamed: 1', 'Unnamed: 2', 'Unnamed: 3', 'Unnamed: 4', 'Unnamed: 5', 'Unnamed: 6',
           'Unnamed: 7']
ranges_front = [6, 23, 44, 44, 44, 44, 44, 44]
ranges_back = [5, 18, 19, 19, 19, 19, 19, 19]
numbers = []

for column in columns:
    numbers_list = get_numbers(df, column)
    # Removing the Non-Numbers from the list
    numbers_list = [n for n in numbers_list if isinstance(n, (int, float)) and not pd.isna(n) and not pd.isnull(n)]
    numbers.append(numbers_list)

# Creating a list with all of the numbers in it alternating every 5

array = []
for i in range(101):
    for j in range(8):
        array.append(numbers[j][i])
x = numbers[2]
y = numbers[3]
data = list(zip(x, y))

# These below statements are used to store the min and max coordinates from the above for loop.

min_value_x = min(numbers[2])
min_value_y = min(numbers[3])
lowest = [min_value_x, min_value_y]

max_value_x = max(numbers[2])
max_value_y = max(numbers[3])
highest = [max_value_x, max_value_y]


# Graphing all of the points

plt.scatter(x, y)

plt.xlabel('Drive Voltage')
plt.ylabel('Polarization')
plt.title('Ferroelectric Hysteresis')
plt.plot(x, y, label='Connected Lines', linestyle='-', color='red')  # Connects the dots
plt.grid(True)  # Creates the grid

# Finding points closest to positive and negative X and Y intercepts
x_positive, x_negative = find_positive_and_negative(x)
x_pos_zero = min(x_positive, key=lambda x: abs(x))
x_neg_zero = min(x_negative, key=lambda x: abs(x))

y_positive, y_negative = find_positive_and_negative(y)
y_pos_zero = min(y_positive, key=lambda x: abs(x))
y_neg_zero = min(y_negative, key=lambda x: abs(x))

# Finding corodinate
x1_intercept, x2_intercept = find_coordinates(data, x, x_pos_zero, x_neg_zero)
y1_intercept, y2_intercept = find_coordinates(data, y, y_pos_zero, y_neg_zero)

# Finding Beginning and Ending

print('closest to 0 or Y-Intercept')
print('x pos zero',x_pos_zero)
print('x neg zero',x_neg_zero)

print()

print('Y closest to 0 or X-Intercept')

print('y pos zero',y_pos_zero)
print('y neg zero',y_neg_zero)

print()

# print('min value x',min_value_x)
# print('min value x',min_value_x)
# print('min_value_y',min_value_y)
# print('max valuex_x',max_value_x)
# print('max value y',max_value_y)
print('The lower beginning inteserction points are',min_value_x,'and',min_value_y)
print('The upper ending intersection points are',max_value_x,'and',max_value_y)

print('Points\n')

print('The Pr (µC/cm2) is:')
print(f"{x1_intercept}\n")

print('The -Pr (µC/cm2) is:')
print(f"{x2_intercept}\n")

print('The Vc is:')
print(f"{y1_intercept}\n")

print('The -Vc is:')
print(f"{y2_intercept}\n")

plt.show()