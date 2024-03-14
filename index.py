import cv2
import numpy as np
import csv

cap = cv2.VideoCapture("test2.mov")

if not cap.isOpened():
    print("Error: Could not open video.")
    exit()

r = []
g = []
b = []

def get_average(arr):
    return sum(arr) / len(arr)

def convert_to_np(arr):
    return np.array(arr)

while True:
    ret, frame = cap.read()

    if not ret:
        break

    rframe = []
    gframe = []
    bframe = []

    rows, cols,_ = frame.shape

    for i in range(0, rows):
        for j in range(0, cols):
            pixel = frame[i, j]
            rp = pixel[2]
            gp = pixel[1]
            bp = pixel[0]
            rframe.append(rp)
            gframe.append(gp)
            bframe.append(bp)

    r.append(round(get_average(rframe)))
    g.append(round(get_average(gframe)))
    b.append(round(get_average(bframe)))

    cv2.imshow("Video", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()

cv2.destroyAllWindows()

r = convert_to_np(r)
g = convert_to_np(g)
b = convert_to_np(b)

print(len(r))

with open("output3.csv", "w") as f:
    writer = csv.writer(f)
    writer.writerow(["Time","Red", "Green", "Blue"])
    for i in range(0, len(r)):
        writer.writerow([i, r[i], g[i], b[i]])


