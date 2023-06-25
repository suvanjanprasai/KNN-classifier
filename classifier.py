import math
import linecache
import matplotlib.pyplot as plt
from mpl_interactions import panhandler, zoom_factory
import mplcursors
from collections import Counter


scatter_plot = input("Scatter plot (y/n): ")
string_data_point = input("Enter a data point (x,y,z,..): ")
k = int(input("Enter K: "))
file_name = input("Enter the name of the file without(.txt) which contains the dataset: ")
actual_datapoint = eval(string_data_point)

print("\nNote: If the data points have more than 2 dimension, only the first 2 coordinates(x,y) will be plotted.")

color_map = {
    1: 'brown',2: 'green',3: 'yellow',4: 'blue',5: 'orange',6: 'purple',7: 'cyan',8: 'magenta',9: 'lime',10: 'pink'

}

p = []
with open(f'{file_name}.txt', 'r') as file:

    line_count = len(file.readlines())
    for i in range(1,line_count+1):
        line = linecache.getline(f'{file_name}.txt', i).strip()
        line = eval(line)
        l = []

        for j in range(0,len(line)):
            q = 0
            max_dimensions = max(len(actual_datapoint), len(line[j]))

            for m in range(max_dimensions):
                actual_coord = actual_datapoint[m] if m < len(actual_datapoint) else 0
                test_coord = line[j][m] if m < len(line[j]) else 0
                q += (test_coord - actual_coord) ** 2
            if i <= 10:
                try:
                    plt.axvline(0, c='black',linewidth=1.5)
                    plt.axhline(0, c='black', linewidth=1.5)
                    plt.scatter(line[j][0], line[j][1],c=color_map[i])
                    
                except:
                    None
            else:
                try:
                    plt.axvline(0, c='black',linewidth=1.5)
                    plt.axhline(0, c='black', linewidth=1.5)
                    plt.scatter(line[j][0], line[j][1],c="blue")
                except:
                    None
            l.append(math.sqrt(q))
        p.append(l)

flattened_list = [value for sublist in p for value in sublist]

min_values = sorted(flattened_list)[:k]
positions = []
for sublist in p:
    for value in min_values:
        if value in sublist:
            positions.append(p.index(sublist))
            break

counts = Counter(positions)
max_repeats = max(counts.values())

print(f"The data point {string_data_point} with K={k}, is closest to the data points on the line [{max_repeats+1}] of the {file_name}.txt file")

if scatter_plot == "y":
    try:
        plt.scatter(actual_datapoint[0], actual_datapoint[1],c="red")
    except:
        None
def find_line(input_coordinates):
    with open(f'{file_name}.txt', 'r') as file:

        line_count = len(file.readlines())
        for i in range(1,line_count+1):
            line = linecache.getline(f'{file_name}.txt', i).strip()
            line = eval(line)

            for j in range(0,len(line)):
                if line[j] == input_coordinates:
                    return i


cursor = mplcursors.cursor(hover=True)
@cursor.connect("add")
def on_add(sel):
    x, y = sel.target[0], sel.target[1]
    line_number = find_line((int(x),int(y)))
    sel.annotation.set_text(f"Line: {line_number}, ({x}, {y})")

disconnect_zoom = zoom_factory(plt.gca())
pan_handler = panhandler(plt.gcf())
plt.grid()
plt.show()
