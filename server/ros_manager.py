import os
import logging
import subprocess

FIFO_RX_FILE = '/tmp/pipe_tx'
FIFO_TX_FILE = '/tmp/pipe_rx'
manager_logger = logging.getLogger('ros_manager')

def init_fifo():
    if not os.path.exists(FIFO_TX_FILE):
        os.mkfifo(FIFO_TX_FILE)
    if not os.path.exists(FIFO_RX_FILE):
        os.mkfifo(FIFO_RX_FILE)

def start_wearable_evaluation():
    manager_logger.info('start wearable evaluation')
    #subprocess.call(['gnome-terminal', '--', 'bash', '-c', 'cd ~/ros2_ws/src/wearabie_robot_eval && ./run_eval_human_66dof.sh'])
    subprocess.call(['terminator', '-x', 'bash', '-c', '~/ros2_ws/src/wearable_robot_eval/run_eval_human_66dof.sh; read -p \"Press any key... \" -n1'])

def listen_ros_command():
    if not os.path.exists(FIFO_RX_FILE):
        return

    while True:
        with open(FIFO_RX_FILE, 'r') as fifo:
            line = fifo.readline()
            print(line)
            if line.startswith('start'):
                start_wearable_evaluation()

if __name__ == '__main__':
    init_fifo()
    listen_ros_command()
