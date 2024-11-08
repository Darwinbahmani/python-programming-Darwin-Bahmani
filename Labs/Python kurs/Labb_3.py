import matplotlib.pyplot as plt 
import numpy as np 

# Läs in data
with open(r"C:\\Users\\darwi\\Code\\python-programming-Darwin-Bahmani\\Labs\\unlabelled_data.csv", "r") as file:
    x = []
    y = []
    for line in file:
        values = line.strip().split(",")
        x.append(float(values[0]))
        y.append(float(values[1]))

x = np.array(x)
y = np.array(y)

# Linjens ekvation
k = -2  # Sätt värde för k
m = 0   # Sätt värde för m

print(f"Linje: y = {k:.2f}x + {m:.2f}")


x_line = np.linspace(min(x), max(x), 100)  
y_line = k * x_line + m 

# Scatterplot
plt.scatter(x, y, color='blue')
plt.plot(x_line, y_line, color='red', label='Linje')
plt.xlabel("x")
plt.ylabel("y")
plt.legend()
plt.show() 

# Klassificera punkter
def classify_point(x_point, y_point, k, m):
    y_on_line = k * x_point + m
    return 1 if y_point > y_on_line else 0


labels = []
for i in range(len(x)):
    label = classify_point(x[i], y[i], k, m)
    labels.append(label)

# labelled_data.csv
with open("labelled_data.csv", "w") as file:
    file.write("x,y,label\n")  # Skriv header
    for i in range(len(x)):
        file.write(f"{x[i]},{y[i]},{labels[i]}\n")

print("Klassificeringen har sparats i labelled_data.csv")

# Visa graf med klassificeringar
x_left = [x[i] for i in range(len(x)) if labels[i] == 0]
y_left = [y[i] for i in range(len(y)) if labels[i] == 0]

x_right = [x[i] for i in range(len(x)) if labels[i] == 1]
y_right = [y[i] for i in range(len(y)) if labels[i] == 1]

plt.scatter(x_left, y_left, color='blue', label='Vänster/Nedanför linjen (0)')
plt.scatter(x_right, y_right, color='green', label='Höger/Ovanför linjen (1)')
plt.plot(x_line, y_line, color='red', label='Linje')
plt.xlabel("x")
plt.ylabel("y")
plt.legend()
plt.show()

