"""
Container stats pulled from /sys/fs/cgroup,
Graphs created using :
"""

import argparse
import subprocess


ARGS = {'mode':'collect', 'time_frame': '5',
        'home_dir': ''}

DOCKER_IDS = []

def read_args():
    """Read in arguments passed in by user"""
    parser = argparse.ArgumentParser()
    parser.add_argument('--mode', '-m', nargs=1, dest='mode' , type=str, required=False, help='collect or analyse')
    parser.add_argument('--time-frame', '-tf', nargs=1, dest='time_frame', type=int, required=False, help='Time interval between data polls')
    parser.add_argument('--home-dir', '-hm', nargs=1 , dest='home_dir', type=str, required=True, help='Path to data save location')
    args = parser.parse_args()

    if args.mode != None:
        ARGS['mode'] = args.mode
    
    if args.time_frame != None:
        ARGS['time_frame'] = args.time_frame

    if args.home_dir != None:
        ARGS['home_dir'] = args.home_dir

def get_docker_ids():
    """Get long docker Container id's"""

    DOCKER_IDS = []

    proc = subprocess.Popen('docker ps -q --no-trunc', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    for line in proc.stdout.readlines():
        id = line.split( )
        DOCKER_IDS.append(id[0])
    retval = proc.wait()

def get_cpu_usage():
    """"""

def get_core_usage():
    """"""

def get_memory_usage():
    """"""

def get_ram_usage():
    """"""

def main():
    """Main method call helper fuctions"""

    read_args()

main()
