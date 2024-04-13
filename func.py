from cv2 import VideoCapture, CAP_PROP_FPS
from numpy import array, diff, exp
from matplotlib import use
from matplotlib.pyplot import plot, savefig, clf, xlabel, ylabel, title, close, text, figtext
import io
from PIL import Image
from scipy.optimize import curve_fit

use("Agg")


def get_average(arr):
    return sum(arr) / len(arr)

def convert_to_np(arr):
    return array(arr)

def computeDerivative(x, y):
    diffY = diff(y)/diff(x)
    diffX = (x[:-1] + x[1:])/2
    return diffX, diffY

def eq(x, a, b):
    return a*exp(-b*x)

def get_eq(arr):
    y = array(arr[round(len(arr)*0.25):])
    x = array([i for i in range(len(y))])

    p0 = [x[0], y[0]]

    params, _ = curve_fit(eq, x, y, p0=p0)
    return params, y, x

def get_plot(p: bool = True):
    buf = io.BytesIO()
    savefig(buf, format="png")
    buf.seek(0)
    if p:
        return Image.open(buf)
    else:
        return buf

def get_color(cap: VideoCapture, norm: bool = False) -> dict[str, array]:
    time = []
    r = []
    g = []
    b = []

    counter = 0

    while True:
        ret, frame = cap.read()

        if not ret:
            break

        time.append(counter)
        counter += 1

        r_frame = []
        g_frame = []
        b_frame = []

        rows, cols, _ = frame.shape

        for i in range(0, rows):
            for j in range(0, cols):
                p = frame[i, j]
                r_frame.append(p[2])
                g_frame.append(p[1])
                b_frame.append(p[0])
        if norm == True:
            r.append(get_average(r_frame) / 255)
            g.append(get_average(g_frame) / 255)
            b.append(get_average(b_frame) / 255)
        else:
            r.append(get_average(r_frame))
            g.append(get_average(g_frame))
            b.append(get_average(b_frame))
        
    return {
        "time": convert_to_np(time),
        "red": convert_to_np(r),
        "green": convert_to_np(g),
        "blue": convert_to_np(b)
    }

def func(inp, norm: bool = False, pil: bool = True):
    cap = VideoCapture(inp)

    if not cap.isOpened():
        print("Error: Could not open file.")
        exit()

    fps = round(cap.get(CAP_PROP_FPS))
    data = get_color(cap, norm=norm)
    cap.release()

    images = {}

    for i in list(["red", "green", "blue"]):
        diffX, diffY = [], []
        e = ""

        if norm:
            params, y, x = get_eq(data[i])
            plot(x, y, color=i)
            plot(eq(x, *params), color="pink", label="Linear fit")
            diffX, diffY = computeDerivative(x, y)
            e = f"\ny = {str(round(params[0], 2))}*exp(-{str(round((params[1]/(1/fps)), 4))}*x)"
        else:
            plot(data["time"], data[i], color=i)
            diffX, diffY = computeDerivative(data["time"], data[i])

        plot(diffX, diffY, color="black")
        title(f"{i.capitalize()} light intensity over time at {fps} fps{e}")
        xlabel("Time")
        ylabel(i.capitalize())
        img = get_plot()
        images[i] = img
        clf()

    diffXR, diffYR = computeDerivative(data["time"], data["red"])
    diffXG, diffYG = computeDerivative(data["time"], data["green"])
    diffXB, diffYB = computeDerivative(data["time"], data["blue"])

    plot(diffXR, diffYR, color="red")
    plot(diffXG, diffYG, color="green")
    plot(diffXB, diffYB, color="blue")
    title(f"RGB light intensity derivative over time at {fps} fps")
    xlabel("Time")
    ylabel("Intensity")
    img = get_plot(pil)
    images["rgb_derivative"] = img
    clf()

    plot(data["time"], data["red"], color="red")
    plot(data["time"], data["green"], color="green")
    plot(data["time"], data["blue"], color="blue")
    title(f"RGB light intensity over time at {fps} fps")
    xlabel("Time")
    ylabel("Intensity")
    img = get_plot(pil)
    images["rgb"] = img
    close()

    return images
    