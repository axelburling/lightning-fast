from argparse import ArgumentParser
from os import path, mkdir
from cv2 import VideoCapture, CAP_PROP_FPS
from mimetypes import guess_type
from numpy import array, diff
from matplotlib.pyplot import plot, savefig, clf, xlabel, ylabel, title, close

# create a parser
parser = ArgumentParser(description="This is a simple program to calculate the average color of a video.")

# add arguments to the parser
parser.add_argument("-i", "--input", help="The video file to process.", required=True)
parser.add_argument("-o", "--output", help="The output folder to save the data to.", required=False)

# parse the arguments
args = parser.parse_args()

# check if the file exists
if not path.exists(args.input):
    print("Error: The file does not exist.")
    exit()

# check if the file is a video
if not guess_type(args.input)[0].startswith("video"):
    print("Error: The file is not a video.")
    exit()

out_dir = args.output if args.output else "output"

if not path.exists(out_dir):
    mkdir(out_dir)

cap = VideoCapture(args.input)

if not cap.isOpened():
    print("Error: Could not open file.")
    exit()

def get_average(arr):
    return sum(arr) / len(arr)

def convert_to_np(arr):
    return array(arr)

# get the fps of the video
fps = round(cap.get(CAP_PROP_FPS))

def get_color(cap: VideoCapture) -> dict[str, array]:
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

        r.append(get_average(r_frame))
        g.append(get_average(g_frame))
        b.append(get_average(b_frame))
        
    return {
        "time": convert_to_np(time),
        "red": convert_to_np(r),
        "green": convert_to_np(g),
        "blue": convert_to_np(b)
    }

def computeDerivative(x, y):
    diffY = diff(y)/diff(x)
    diffX = (x[:-1] + x[1:])/2
    return diffX, diffY

data = get_color(cap)

cap.release()

for i in list(["red", "green", "blue"]):
    plot(data["time"], data[i], color=i)
    diffX, diffY = computeDerivative(data["time"], data[i])
    plot(diffX, diffY, color="black")
    title(f"{i.capitalize()} light intensity over time at {fps} fps")
    xlabel("Time")
    ylabel(i.capitalize())
    savefig(f"./{out_dir}/{i}.png")
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
savefig(f"./{out_dir}/rgb_derivative.png")
clf()


plot(data["time"], data["red"], color="red")
plot(data["time"], data["green"], color="green")
plot(data["time"], data["blue"], color="blue")
title(f"RGB light intensity over time at {fps} fps")
xlabel("Time")
ylabel("Intensity")
savefig(f"./{out_dir}/rgb.png")

close()

print("Done!")

