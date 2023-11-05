from flask import Flask, render_template, request
import os
#  from uwsgidecorators import thread

app = Flask(__name__)

FIFO_TX_FILE = "/tmp/pipe_tx"
FIFO_RX_FILE = "/tmp/pipe_rx"

def init_fifo():
    if not os.path.exists(FIFO_TX_FILE):
        os.mkfifo(FIFO_TX_FILE)
    if not os.path.exists(FIFO_RX_FILE):
        os.mkfifo(FIFO_RX_FILE)

#  @thread
#  def uwsgi_task(duration):
#      for i in range(duration):
#          print("Working in uwsgi thread... {}/{}".format(i + 1, duration))
#          time.sleep(1)
#
def listen_ros_command(duration):
    if not os.path.exists(FIFO_RX_FILE):
        return

    while True:
        with open(FIFO_RX_FILE, 'r') as fifo:
            line = fifo.readline()
            print(line)
            if line.startswith('finish'):
                print('finish ros simulation')
   
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/new')
def new_simulation():
    code0 = ''
    code1 = ''
    code2 = ''
    current_path = os.path.dirname(os.path.abspath(__file__))
    with open(current_path + '/app.py', 'r') as f:
        code0 = f.read()
    with open(current_path + '/../run.sh', 'r') as f:
        code1 = f.read()
    with open(current_path + '/../attach.sh', 'r') as f:
        code2 = f.read()

    return render_template('new.html', code0=code0, code1=code1, code2=code2)

@app.route('/evaluate', methods=['POST'])
def evaluate_device():
    #  print(request.form)
    editor = request.form['editor']
    with open('/tmp/new_code.py', 'w') as f:
        f.write(editor)

    # start ros launch
    with open(FIFO_TX_FILE, 'w') as f:
        f.write('start')
        print('start ros simulation')

    return render_template('result.html')

if __name__ == '__main__':
    init_fifo()
    app.run(host='0.0.0.0', port=5054, debug=True)
