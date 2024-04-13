from flask import Flask, request, jsonify, send_file, Response
from gevent.pywsgi import WSGIServer
from argparse import ArgumentParser
from func import func, get_color
from os import mkdir, path, remove, listdir, rmdir as rmdir_py
from mimetypes import guess_type
from uuid import uuid4
from shutil import make_archive
import cv2
import csv
import zipfile

from io import BytesIO

print("Server is starting...")

app = Flask(__name__)

parser = ArgumentParser("Server")
parser.add_argument("--port", type=int, default=4000, help="The port to run the server on.")
parser.add_argument("--host", type=str, default="0.0.0.0", help="The host to run the server on.")
parser.add_argument("--dev", "-d", action="store_true", default=False, help="Run the server in development mode.")

args = parser.parse_args()

port = args.port
host = args.host
dev = args.dev


if not path.exists("tmp"):
    mkdir("tmp")

if not path.exists("tmp_success"):
    mkdir("tmp_success")

# wait for file to be accessed in fs
def wait_for_file(file):
    while not path.exists(file):
        pass

    return True

# remove directory and its contents
def rmdir(dir):
    for i in listdir(dir):
        if path.isdir(f"{dir}/{i}"):
            rmdir(f"{dir}/{i}")
        else:
            remove(f"{dir}/{i}")
    rmdir_py(dir)

def convert_zip_to_bytes(file):
    buf = BytesIO()
    with open(file, "rb") as f:
        buf.write(f.read())
    buf.seek(0)
    return buf

def convert_py_to_excel(num):
    return str(num).replace(".", ",")

@app.after_request
def after_request(response: Response):
    try:
        id = response.headers.get("Content-Disposition").split("=")[-1]
        if id and id != "index.html":
            remove(f"./tmp_success/{id}")
        return response
    except:
        return response



@app.route('/')
def index():
    return send_file("./website/index.html")

@app.route('/api', methods=['POST'])
def api():
    # get files from the request
    files = request.files

    if "video" not in files:
        return jsonify({"error": "No video file found."}), 400
    
    # get norm(bool) from request multipart form
    norm = eval(request.form.get("norm", False))
    
    # get the video file
    videos = files.getlist("video")
    run_id = str(uuid4())

    mkdir(f"./tmp/{run_id}")

    mkdir(f"./tmp_success/{run_id}")

    for video in videos:
        enc = video.filename.split(".")[-1]

        # check if the file is a video
        if not guess_type(video.filename)[0].startswith("video"):
            return jsonify({"error": "The file is not a video."}), 400
        
        id = str(uuid4())

        file_name = f"./tmp/{run_id}/{id}.{enc}"
        # save the video file
        video.save(file_name)

        wait_for_file(file_name)

        images = func(file_name, norm=norm, pil=True)

        remove(file_name)

        mkdir(f"./tmp_success/{run_id}/{id}")

        for i in dict(images):
            images[i].save(f"./tmp_success/{run_id}/{id}/{i}.png")

    make_archive(f"./tmp_success/{run_id}", "zip", f"./tmp_success/{run_id}")
    rmdir(f"./tmp_success/{run_id}")

    

    return send_file(f"./tmp_success/{run_id}.zip", as_attachment=True, mimetype="application/zip", download_name=f"{run_id}.zip")

@app.route('/api-csv', methods=['POST'])
def api_csv():
    files = request.files

    if "video" not in files:
        return jsonify({"error": "No video file found."})
    
    videos = files.getlist("video")

    run_id = str(uuid4())

    mkdir(f"./tmp/{run_id}")

    mkdir(f"./tmp_success/{run_id}")

    for video in videos:
        enc = video.filename.split(".")[-1]

        if not guess_type(video.filename)[0].startswith("video"):
            return jsonify({"error": "The file is not a video."})

        id = str(uuid4())

        file_name = f"./tmp/{run_id}{id}.{enc}"
        
        video.save(file_name)

        wait_for_file(file_name)

        cap = cv2.VideoCapture(file_name)

        col_dict = get_color(cap)

        cap.release()

        remove(file_name)

        with open(f"./tmp_success/{run_id}/{id}.csv", "w") as f:
            writer = csv.writer(f)
            writer.writerow(["time", "red", "green", "blue"])
            for i in range(len(col_dict["time"])):
                writer.writerow([col_dict["time"][i], convert_py_to_excel(col_dict["red"][i]), convert_py_to_excel(col_dict["green"][i]), convert_py_to_excel(col_dict["blue"][i])])

            f.close()

    with zipfile.ZipFile(f"./tmp_success/{run_id}.zip", "w") as z:
        d = listdir(f"./tmp_success/{run_id}")
        for i in d:
            z.write(f"./tmp_success/{run_id}/{i}", i)

        z.close()

    rmdir(f"./tmp_success/{run_id}")

    return send_file(f"./tmp_success/{run_id}.zip", as_attachment=True, mimetype="application/zip", download_name=f"{run_id}.zip")

if dev:
    print(f"Server is running on http://{host}:{port} in development mode.")
    app.run(host=host, port=port, debug=True)
else:
    if __name__ == "__main__":
        http_server = WSGIServer((host, port), app)

        print(f"Server is running on http://{http_server.address[0]}:{http_server.address[1]}")
        http_server.serve_forever()
    