import matplotlib.pyplot as plt
import pandas as pd
import os
import matplotlib.ticker as ticker

#list for plotting new graph
POSITIVE_NEW_GRAPH_COORDINATES = []
NEGATIVE_NEW_GRAPH_COORDINATES = []
i_cordinate = 1


def find_start_row(file_path, keyword):
    """This is a Python function that finds the first row in a text
    file that contains a given keyword (case-insensitive"""
    with open(file_path, 'r') as f:
        for i, line in enumerate(f, start=1):
            if keyword.lower() in line.lower():
                return i
    return None

def read_csv_from_keyword(file_path, keyword="point"):
    """This is a Python function that reads a CSV file from a given row
    that contains a given keyword."""
    start_row = find_start_row(file_path, keyword)
    if start_row is not None:
        df = pd.read_csv(file_path, skiprows=range(1, start_row),encoding = 'ISO-8859-1')
        return df
    else:
        print(f'Keyword "{keyword}" not found in the file.')

def get_files(namestart,nameend):
    """This is a Python function that gets a list of files in the current directory that match a given pattern"""
    Phonefiles_list = [Phonefiles for Phonefiles in os.listdir() if namestart in Phonefiles and Phonefiles.endswith(nameend)]
    return Phonefiles_list

def calculate_x_intercept(point1, point2):
    """This is a Python function that calculates the x-intercept of a line that
    passes through two given points."""

    x1, y1 = point1
    x2, y2 = point2

    if y1 == y2:
        # The line is parallel to the x-axis; there is no x-intercept.
        return None

    x_intercept = (x1 * y2 - x2 * y1) / (y2 - y1)
    return x_intercept


def calculate_y_intercept(point1, point2):
    """This is a Python function that calculates the y-intercept of a line
    that passes through two given points."""
    x1, y1 = point1
    x2, y2 = point2

    if x1 == x2:
        # The line is parallel to the y-axis; there is no y-intercept.
        return None

    y_intercept = (x1 * y2 - x2 * y1) / (x1 - x2)
    return y_intercept


def y_axis_intercept_calculation(numbers):
    """This is a Python function that calculates the positive and negative y-intercepts of
    a curve that passes through a set of points"""
    numbers = list(numbers)
    positive_numbers_x_greater = [num for num in numbers if num[0] > 0]
    nearest_positive_x_positive_y = sorted([i for i in positive_numbers_x_greater if i[1]>0], key=lambda a: a[0])[0]
    # plt.plot(*nearest_positive_x_positive_y, '*')
    nearest_positive_x_negative_y = sorted([i for i in positive_numbers_x_greater if i[1]<0], key=lambda a: a[1])[0]
    # plt.plot(*nearest_positive_x_negative_y, '*')

    negative_numbers_x_lesser = [num for num in numbers if num[0] < 0]
    nearest_negative_x_positive_y = sorted([i for i in negative_numbers_x_lesser if i[1]<0], key=lambda a: a[0], reverse=True)[0]
    # plt.plot(*nearest_negative_x_positive_y, '*')
    nearest_negative_x_negative_y = sorted([i for i in negative_numbers_x_lesser if i[1]>0], key=lambda a: a[1], reverse=True)[0]
    # plt.plot(*nearest_negative_x_negative_y, '*')

    positive_y_intercept = calculate_y_intercept(nearest_negative_x_negative_y, nearest_positive_x_positive_y)
    negative_y_intercept = calculate_y_intercept(nearest_positive_x_negative_y, nearest_negative_x_positive_y)

    return positive_y_intercept, negative_y_intercept


def x_axis_intercept_calculation(numbers):
    """This is a Python function that calculates the positive and negative x-intercepts of
        a curve that passes through a set of points"""
    numbers = list(numbers)
    positive_numbers_y_greater = [num for num in numbers if num[1] > 0]
    nearest_positive_y_negative_x = sorted(positive_numbers_y_greater, key=lambda a: a[0])[0]
    # plt.plot(*nearest_positive_y_negative_x, '*')
    nearest_positive_y_positive_x = sorted(positive_numbers_y_greater, key=lambda a: a[1])[0]
    # plt.plot(*nearest_positive_y_positive_x, '*')

    negative_numbers_y_lesser = [num for num in numbers if num[1] < 0]
    nearest_negative_x_positive_y = sorted(negative_numbers_y_lesser, key=lambda a: a[0], reverse=True)[0]
    # plt.plot(*nearest_negative_x_positive_y, '*')
    nearest_negative_x_negative_y = sorted(negative_numbers_y_lesser, key=lambda a: a[1], reverse=True)[0]
    # plt.plot(*nearest_negative_x_negative_y, '*')

    negative_x_intercept = calculate_x_intercept(nearest_positive_y_negative_x, nearest_negative_x_negative_y)
    positive_x_intercept = calculate_x_intercept(nearest_positive_y_positive_x, nearest_negative_x_positive_y)
    #def calculate slope =  points  = nearest_negative_x_positive_y nearest_negative_x_negative_y

    return positive_x_intercept, negative_x_intercept


def iterate_over_file(file_path,POSITIVE_NEW_GRAPH_COORDINATES,NEGATIVE_NEW_GRAPH_COORDINATES):
    """The function takes three parameters: file_path, POSITIVE_NEW_GRAPH_CORDINATES,
    and NEGATIVE_NEW_GRAPH_CORDINATES. file_path is a string that represents the path of the CSV file
    to be processed. POSITIVE_NEW_GRAPH_CORDINATES and NEGATIVE_NEW_GRAPH_CORDINATES are lists that
    store the positive and negative y-intercepts of the data points, respectively."""

    df = read_csv_from_keyword(file_path)
    df.dropna(inplace=True)

    # Assuming x_points and y_points are your data
    x_points = list(df['Unnamed: 2'])
    y_points = list(df['Unnamed: 3'])


    # x points closest values
    positive_y_intercept, negative_y_intercept = y_axis_intercept_calculation(zip(x_points, y_points))
    positive_x_intercept, negative_x_intercept = x_axis_intercept_calculation(zip(x_points, y_points))

    # Calculate max x value
    max_x = max(x_points)

    # Calculate max y value
    max_y = max(y_points)

    # Calculate the result
    result = max_x / (max_y * 8.85e-12)

    # print(result)
    # print(positive_y_intercept, negative_y_intercept)
    # print(positive_x_intercept, negative_x_intercept)

    POSITIVE_NEW_GRAPH_COORDINATES.extend([(i_cordinate,positive_y_intercept)])
    NEGATIVE_NEW_GRAPH_COORDINATES.extend([(i_cordinate,negative_y_intercept)])

    def calculate_slope(point1, point2):
        """This is a Python function that calculates the slope of a line that passes
         through two given points. """
        x1, y1 = point1
        x2, y2 = point2
        # Calculate the slope
        slope = (y2 - y1) / (x2 - x1)
        return slope


    additional_json_columns = {
        "Center data before PMax, ±Pr and ±Vc Calc.": "",
        "PMax (µC/cm2)": "",
        "Pr (µC/cm2)": positive_y_intercept,
        " -Pr (µC/cm2)": negative_y_intercept,
        " PLoss (µC/cm2)": y_points[-1],
        "Vc": positive_x_intercept,
        "-Vc": negative_x_intercept,
        "CMax-Eff (nF)": "",
        "KEff": result,
        "Offset (µC/cm2)": "",
        "Vert. (±Pr) Shift (µC/cm2)": "",
        "Horiz. Shift (±Vc)": "",
        "A (Loop Area - µC/cm2·Volts)":""
    }

    df_additional_data = pd.DataFrame(list(additional_json_columns.items()), columns=['Hysteresis', 'Unnamed: 1'])
    final_df = df.append(df_additional_data)


    #Plot the points on the graph
    # Usage

    if i_cordinate  == 1:
        plt.figure()
        plt.grid(True)
        plt.plot(x_points, y_points, 'o-')  # 'o-' means markers connected by lines
        plt.xlabel('X Points')
        plt.ylabel('Y Points')
        plt.title('Plot of Y vs X')
        # plt.show()
    return final_df



for file_path in get_files("Phone12","csv"):
    ##folder name
    foldername = 'output'
    final_df = iterate_over_file(file_path, POSITIVE_NEW_GRAPH_COORDINATES, NEGATIVE_NEW_GRAPH_COORDINATES)
    if not os.path.exists (foldername):
        os.makedirs(foldername)
    final_df.to_csv(os.path.join(foldername, file_path))
    i_cordinate+=1

# print(POSITIVE_NEW_GRAPH_COORDINATES, NEGATIVE_NEW_GRAPH_COORDINATES)
x_values, y_values = zip(*POSITIVE_NEW_GRAPH_COORDINATES)


##plot the new graph coordinates on a
plt.figure()
plt.plot(x_values, y_values,'o-')
x_values, y_values = zip(*NEGATIVE_NEW_GRAPH_COORDINATES)
plt.plot(x_values, y_values,'o-')
plt.grid(True,)
ax = plt.gca()
ax.xaxis.set_major_locator(ticker.MaxNLocator(integer=True))

## TO VIEW THE CORDIATES ON THE MAP
# for x, y in NEW_GRAPH_CORDINATES:
#     ax.annotate(f'({x}, {y})', (x, y))
plt.plot(x_values, y_values,"o")
plt.xlabel('Graph number')
plt.ylabel('Y intercepts')
plt.title('New Graph')
plt.show()

#the graph will remain open for 60 minutes.
import time;time.sleep(60)

