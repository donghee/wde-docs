from flask import Flask, render_template, request
import os
import requests

app = Flask(__name__)

FIFO_TX_FILE = "/tmp/wde_ros_tx"
FIFO_RX_FILE = "/tmp/wde_ros_rx"

def init_fifo():
    if not os.path.exists(FIFO_TX_FILE):
        os.mkfifo(FIFO_TX_FILE)
    if not os.path.exists(FIFO_RX_FILE):
        os.mkfifo(FIFO_RX_FILE)


def listen_ros_command(duration):
    if not os.path.exists(FIFO_RX_FILE):
        return

    while True:
        with open(FIFO_RX_FILE, "r") as fifo:
            line = fifo.readline()
            print(line)
            if line.startswith("finish"):
                print("finish ros simulation")


@app.route("/")
def index():
    subject = 'home'
    return render_template('index.html', subject=subject)

@app.route("/new", methods=["GET"])
def new_simulation():
    code0 = ""
    code1 = ""
    code2 = ""
    current_path = os.path.dirname(os.path.abspath(__file__))
    with open(current_path + "/control_node_1.py", "r") as f:
        code0 = f.read()
    with open(current_path + "/control_node_2.py", "r") as f:
        code1 = f.read()
    with open(current_path + "/control_node_3.py", "r") as f:
        code2 = f.read()
        subject = 'new'
    return render_template("new.html", code0=code0, code1=code1, code2=code2)

@app.route("/evaluate", methods=["POST"])
def evaluate_device():
    print(request.form)
    device = request.form["device"]
    body = request.form["body"]
    task = request.form["task"]
    code = request.form["code"]
    # TODO: change me
    joint = "joint3"
    url = f"?device={device}&body={body}&joint={joint}&task={task}&code=code{code}"
    editor = request.form["editor"]
    with open("/tmp/new_code.py", "w") as f:
        f.write(editor)

    # start ros launch
    with open(FIFO_TX_FILE, "w") as f:
        if device == "upper":
            f.write("start upper ")
        if device == "lower":
            f.write("start lower ")
        print(f"start simulation: {device}")

    #  ros launch
    with open(FIFO_RX_FILE, "r") as f:
        line = f.readline()
        if line.startswith("finish"):
            print("finish simulation")
        else:
            print("error simulation")

    if device == "upper":
        os.system(f"cp /tmp/visualization-upper.csv ~/src/wde-visualization/web/static/{joint}.csv")
        os.system(f"cp /tmp/interaction-upper.csv ~/src/wde-interactivity/interaction_control_node_1.csv")
        os.system(f"cp /tmp/wearability-upper.csv ~/src/wde-wearability/device_1DOF/python/wearability/input.csv")        
    if device == "lower":
        os.system(f"cp /tmp/lower.csv ~/src/wde-visualization/web/static/{joint}.csv")

    r = requests.get(f"http://localhost/usability/score{url}")
    usability = r.text
    r = requests.get(f"http://localhost/wearability/score{url}")
    wearability = r.text
    r = requests.get(f"http://localhost/interactivity/score{url}")
    interactivity = r.text
    totalscore = round((float(usability) + float(wearability) + float(interactivity)) / 3, 1)

    return render_template("result.html", url=url, device=device, body=body, task=task, code=f"code{code}", totalscore=totalscore, usability=usability, wearability=wearability, interactivity=interactivity)


if __name__ == "__main__":
    init_fifo()
    app.run(host="0.0.0.0", port=5054, debug=True)
