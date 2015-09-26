#!/usr/bin/python
"""
Container stats pulled from /sys/fs/cgroup,
Graphs created using :
"""

import argparse
import subprocess
import os
import time


ARGS = {'time_frame': 5, 'home_dir': ''}

def read_args():
    """Read in arguments passed in by user"""
    parser = argparse.ArgumentParser()
    parser.add_argument('--time-frame', '-tf', nargs=1, dest='time_frame', type=float, required=False, help='Time interval between data polls')
    parser.add_argument('--home-dir', '-hm', nargs=1 , dest='home_dir', type=str, required=True, help='Path to data save location')
    args = parser.parse_args()
    
    if args.time_frame != None:
        ARGS['time_frame'] = args.time_frame[0]

    if args.home_dir != None:
        ARGS['home_dir'] = args.home_dir[0]

def get_docker_ids():
    """Get long docker Container id's"""

    docker_ids = []

    proc = subprocess.Popen('docker ps -q --no-trunc', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    for line in proc.stdout.readlines():
        id = line.split( )
        docker_ids.append(id[0])
        storage_prep(id[0])
    retval = proc.wait()

    return docker_ids

def storage_prep(container_id):
    """Create container's data storage location and required storage files"""
    dir = ARGS['home_dir'] + '/stats/' + container_id

    if not os.path.exists(dir):
        os.mkdir(dir)
        cpu = dir + '/cpu.txt'
        open(cpu, 'a').close()
        core = dir + '/core.txt'
        open(core, 'a').close()
        memory = dir + '/memory.txt'
        open(memory, 'a').close()
        ram = dir + '/ram.txt'
        open(ram, 'a').close()

def pull_data(command, storage_file):
    """Run command and append results to storage_file"""

    echo_command = 'echo $(' + command + ') >> ' + storage_file 

    proc = subprocess.Popen(echo_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    _, _ = proc.communicate()
    retval = proc.wait()


def get_cpu_usage(docker_ids):
    """Collect container cpu usage data for each running continer,
    /sys/fs/cgroup/cpuacct/docker/$CONTAINER_ID/cpuacct.usage"""

    location  = 'cat /sys/fs/cgroup/cpuacct/docker/'
    data_file = '/cpuacct.usage'

    for id in docker_ids:
        command = location + id + data_file
        storage_file = ARGS['home_dir'] + '/stats/' + id + '/cpu.txt'
        pull_data(command, storage_file)


def get_core_usage(docker_ids):
    """Collect individual core usage data for each running continer,
    /sys/fs/cgroup/cpuacct/docker/$CONTAINER_ID/cpuacct.usage_percpu"""

    location  = 'cat /sys/fs/cgroup/cpuacct/docker/'
    data_file = '/cpuacct.usage_percpu'

    for id in docker_ids:
        command = location + id + data_file
        storage_file = ARGS['home_dir'] + '/stats/' + id + '/core.txt'
        pull_data(command, storage_file)

def get_memory_usage(docker_ids):
    """Collect memory usage data for each running container,
    /sys/fs/cgroup/memory/docker/$CONTAINER_ID/memory.usage_in_bytes"""

    location  = 'cat /sys/fs/cgroup/memory/docker/'
    data_file = '/memory.usage_in_bytes'

    for id in docker_ids:
        command = location + id + data_file
        storage_file = ARGS['home_dir'] + '/stats/' + id + '/memory.txt'
        pull_data(command, storage_file)

def get_ram_usage(docker_ids):
    """"""

def main():
    """Main method call helper fuctions"""
    read_args()

    dir = ARGS['home_dir'] + '/stats'

    if not os.path.exists(dir):
        os.mkdir(dir)

    while True:
        docker_ids = get_docker_ids()
        get_cpu_usage(docker_ids)
        get_core_usage(docker_ids)
        get_memory_usage(docker_ids)
        get_ram_usage(docker_ids)
        time.sleep(ARGS['time_frame'])


main()
