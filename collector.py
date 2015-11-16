#!/usr/bin/python
"""
Container stats pulled from /sys/fs/cgroup,
Graphs created using :
"""

import argparse
import subprocess
import os
import time
import sys


ARGS = {'time_frame': 0.1, 'home_dir': '',
    'mode': 'collect', 'container_id': ''}

def read_args():
    """Read in arguments passed in by user"""
    parser = argparse.ArgumentParser()
    parser.add_argument('--time-frame', '-tf', nargs=1, dest='time_frame',
                        type=float, required=False,
                        help='Time interval between data colection.')
    parser.add_argument('--mode', '-m', nargs=1, dest='mode', type=str,
                        required=False, help='Mode type (collect or analyse)')
    parser.add_argument('--container-id', '-id', nargs=1, dest='container_id',
                        type=str, required=False, help='Enter container ID.')
    args = parser.parse_args()

    if args.time_frame != None:
        ARGS['time_frame'] = args.time_frame

    if args.mode != None:
        ARGS['mode'] = args.mode[0]

        if ARGS['mode'] == 'analyse' and args.container_id != None:
            ARGS['container_id'] = args.container_id[0]
        elif ARGS['mode'] == 'analyse':
            print 'You have to supply a container ID.'

    ARGS['home_dir'] = os.getcwd() + '/stats'

    if not os.path.exists(ARGS['home_dir']):
        os.mkdir(ARGS['home_dir'])



def get_docker_ids():
    """Get long docker Container id's"""

    docker_ids = []

    proc = subprocess.Popen('docker ps -q --no-trunc', shell=True,
           stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    for line in proc.stdout.readlines():
        docker_id = line.split()
        docker_ids.append(docker_id[0])
        storage_prep(docker_id[0])
    proc.wait()

    return docker_ids

def storage_prep(container_id):
    """Create container's data storage location """
    storage_location = ARGS['home_dir'] + '/' + container_id

    if not os.path.exists(storage_location):
        with open(storage_location, "a") as stats_file:
            stats_file.write("cpu core1 core2 core3 core4 memory")
            stats_file.write("\n")


def get_data(command):
    """Cat stats file and return data"""
    data = ['']

    if os.path.exists(command):
        command = 'cat ' + command
        proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE,
               stderr=subprocess.STDOUT)
        out, _ = proc.communicate()
        data = out.split('\n')
        proc.wait()

    return data[0]


def get_cpu_usage(docker_id):
    """Collect container cpu usage data for each running continer,
    /sys/fs/cgroup/cpuacct/docker/$CONTAINER_ID/cpuacct.usage"""

    location = '/sys/fs/cgroup/cpuacct/docker/'
    data_file = '/cpuacct.usage'

    command = location + docker_id + data_file
    return get_data(command)

def get_core_usage(docker_id):
    """Collect individual core usage data for each running continer,
    /sys/fs/cgroup/cpuacct/docker/$CONTAINER_ID/cpuacct.usage_percpu"""

    location = '/sys/fs/cgroup/cpuacct/docker/'
    data_file = '/cpuacct.usage_percpu'

    command = location + docker_id + data_file
    return get_data(command)

def get_memory_usage(docker_id):
    """Collect memory usage data for each running container,
    /sys/fs/cgroup/memory/docker/$CONTAINER_ID/memory.usage_in_bytes"""

    location = '/sys/fs/cgroup/memory/docker/'
    data_file = '/memory.usage_in_bytes'

    command = location + docker_id + data_file
    return get_data(command)


def save_data(cpu, core, memory, docker_id):
    """
    Save stats in the correct locations, and correct format.
    """

    cores = core.split()

    entry = cpu + ' '

    for core in cores:
        entry = entry + core + ' '

    storage_location = ARGS['home_dir'] + '/' + docker_id
    with open(storage_location, "a") as stats_file:
        stats_file.write(str(entry))
        stats_file.write("\n")

def collect_data():
    """
    Run in a loop collecting container stats
    """
    try:
        while True:
            docker_ids = get_docker_ids()
            for docker_id in docker_ids:
                cpu = get_cpu_usage(docker_id)
                core = get_core_usage(docker_id)
                memory = get_memory_usage(docker_id)
                save_data(cpu, core, memory, docker_id)
                time.sleep(ARGS['time_frame'])
    except KeyboardInterrupt:
        print ""
        print "Received user exit request!"
        sys.exit()

def analyse_data():
    """
    Retrieve container's stats
    """

    file_location = ARGS['home_dir'] + '/' + ARGS['container_id']
    content = []

    with open(file_location, 'r') as stats_file:
        for line in stats_file:
            line = line.rstrip('\n')
            line = line.split()
            entry = [line[0], line[1], line[2], line[3], line[4], line[5]]
            content.append(entry)

    print content

def main():
    """Main method call helper fuctions"""
    read_args()

    if ARGS['mode'] == 'collect':
        collect_data()
    elif ARGS['mode'] == 'analyse':
        analyse_data()
    else:
        print ARGS['mode'] + ' is not a valid mode.'

main()
