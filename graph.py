import matplotlib.pyplot as plt
import numpy as np
import csv

time = []
r = []
g = []
b = []

def computeDerivative(x, y):
    diffY = np.diff(y)/np.diff(x)
    diffX = (x[:-1] + x[1:])/2
    return diffX, diffY

with open("output3.csv", "r") as f:
    reader = csv.reader(f)
    next(reader)
    for row in reader:
        time.append(int(row[0]))
        r.append(int(row[1]))
        g.append(int(row[2]))
        b.append(int(row[3]))

time = np.array(time)
r = np.array(r)
g = np.array(g)
b = np.array(b)

for i in list(["Red", "Green", "Blue"]):
    if i == "Red":
        plt.plot(time, r, color="red")

        diffX, diffY = computeDerivative(time, r)

        plt.plot(diffX, diffY, color="black")
        plt.title("Red light intensity over time")
        plt.xlabel("Time")
        plt.ylabel("Red")
        plt.savefig("red.png")
        plt.clf()
    elif i == "Green":
        plt.plot(time, g, color="green")

        diffX, diffY = computeDerivative(time, g)

        plt.plot(diffX, diffY, color="black")
        plt.title("Green light intensity over time")
        plt.xlabel("Time")
        plt.ylabel("Green")
        plt.savefig("green.png")
        plt.clf()
    else:
        plt.plot(time, b, color="blue")

        diffX, diffY = computeDerivative(time, b)

        plt.plot(diffX, diffY, color="black")
        plt.title("Blue light intensity over time")
        plt.xlabel("Time")
        plt.ylabel("Blue")
        plt.savefig("blue.png")
        plt.clf()


diffXR, diffYR = computeDerivative(time, r)
diffXG, diffYG = computeDerivative(time, g)
diffXB, diffYB = computeDerivative(time, b)

plt.plot(diffXR, diffYR, color="red")
plt.plot(diffXG, diffYG, color="green")
plt.plot(diffXB, diffYB, color="blue")
plt.title("RGB light intensity derivative over time")
plt.xlabel("Time")
plt.ylabel("Intensity")
plt.savefig("rgb_derivative.png")
plt.clf()


plt.plot(time, r, color="red")
plt.plot(time, g, color="green")
plt.plot(time, b, color="blue")
plt.title("RGB light intensity over time")
plt.xlabel("Time")
plt.ylabel("Intensity")
plt.savefig("rgb.png")
plt.show()
plt.clf()


plt.close()
