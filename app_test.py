python
import pandas as pd
import matplotlib.pyplot as plt
from tkinter import filedialog
import tkinter as tk

# Create a Tkinter root window
root = tk.Tk()
root.withdraw()

# Open a file dialog box to select the Excel file
file_path = filedialog.askopenfilename()

# Read the Excel file into a DataFrame
df = pd.read_excel(file_path)
df.columns = ["outside_temperature", "inside_temperature"]

def class_a(inside_temperature, outside_temperature):
    lower_limit = max(18.8 - 2 + 0.33 * outside_temperature, 21)
    upper_limit = max(18.8 + 2 + 0.33 * outside_temperature, 23)
    if inside_temperature >= lower_limit and inside_temperature <= upper_limit:
        return 1
    else:
        return 0

df["class_A"] = df.apply(lambda x: class_a(x["inside_temperature"], x["outside_temperature"]), axis=1)

def class_b(inside_temperature, outside_temperature):
    lower_limit = max(18.8 - 3 + 0.33 * outside_temperature, 20)
    upper_limit = max(18.8 + 3 + 0.33 * outside_temperature, 24)
    if inside_temperature >= lower_limit and inside_temperature <= upper_limit:
        return 1
    else:
        return 0

df["class_B"] = df.apply(lambda x: class_b(x["inside_temperature"], x["outside_temperature"]), axis=1)

def class_c(inside_temperature, outside_temperature):
    lower_limit = max(18.8 - 4 + 0.33 * outside_temperature, 19)
    upper_limit = max(18.8 + 4 + 0.33 * outside_temperature, 25)
    if inside_temperature >= lower_limit and inside_temperature <= upper_limit:
        return 1
    else:
        return 0

df["class_C"] = df.apply(lambda x: class_c(x["inside_temperature"], x["outside_temperature"]), axis=1)


total_hours=len(df["class_C"])

length_class_a = len(df[df["class_A"] == 1])

length_class_b = len(df[df["class_B"] == 1])

length_class_c = len(df[df["class_C"] == 1])

discomfort_precentage=((total_hours-length_class_c)/total_hours)*100
comforrt_precentage=(length_class_c/total_hours)*100
class_a_precentage=(length_class_a/total_hours)*100
class_b_precentage=(length_class_b/total_hours)*100
class_c_precentage=(length_class_c/total_hours)*100



fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10,5))

labels = ['Class A', 'Class B', 'Class C']
sizes = [class_a_precentage, class_b_precentage, class_c_precentage]
ax1.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
ax1.axis('equal')
ax1.set_title('EN 15251 COMFORT HOURS')

labels = ['Comfort', 'Discomfort']
sizes = [comforrt_precentage, discomfort_precentage]
colors = ['green', 'red']
ax2.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
ax2.axis('equal')
ax2.set_title('EN 15251 COMFORT VS DISCOMFORT')

centre_circle1 = plt.Circle((0,0),0.70,fc='white')
ax1.add_artist(centre_circle1)

centre_circle2 = plt.Circle((0,0),0.70,fc='white')
ax2.add_artist(centre_circle2)

plt.show()
