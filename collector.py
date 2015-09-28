#!/usr/bin/python
"""
Container stats pulled from /sys/fs/cgroup,
Graphs created using :
"""

import subprocess
import MySQLdb as mdb
import os
import time
import sys

#bash table_drop.sh collector GetMe2ome2t@t2 docker_stats


ARGS = {'time_frame': 0.01, 'mode': 'collect'}


def get_docker_ids():
    """Get long docker Container id's"""

    docker_ids = []

    proc = subprocess.Popen('docker ps -q --no-trunc', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    for line in proc.stdout.readlines():
        id = line.split( )
        docker_ids.append(id[0])
    retval = proc.wait()

    return docker_ids

def get_cpu_usage(docker_id):
    """Collect container cpu usage data for each running continer,
    /sys/fs/cgroup/cpuacct/docker/$CONTAINER_ID/cpuacct.usage"""

    location  = '/sys/fs/cgroup/cpuacct/docker/'
    data_file = '/cpuacct.usage'
    command = location + docker_id + data_file
    if os.path.exists(command):
        command = 'cat ' + command
        proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        out, _ = proc.communicate()
        retval = proc.wait()

        data = out.split('\n')

        return data[0]

    return -1


def get_core_usage(docker_id):
    """Collect individual core usage data for each running continer,
    /sys/fs/cgroup/cpuacct/docker/$CONTAINER_ID/cpuacct.usage_percpu"""

    location  = '/sys/fs/cgroup/cpuacct/docker/'
    data_file = '/cpuacct.usage_percpu'

    command = location + docker_id + data_file

    if os.path.exists(command):
        command = 'cat ' + command
        proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        out, _ = proc.communicate()
        retval = proc.wait()

        data = out.split('\n')
        data = data[0].split(' ')

        return (data[0], data[1], data[2], data[3])

    return -1


def get_memory_usage(docker_id):
    """Collect memory usage data for each running container,
    /sys/fs/cgroup/memory/docker/$CONTAINER_ID/memory.usage_in_bytes"""

    location  = 'cat /sys/fs/cgroup/memory/docker/'
    data_file = '/memory.usage_in_bytes'

    command = location + docker_id + data_file

    if os.path.exists(command):
        command = 'cat ' + command
        proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        out, _ = proc.communicate()
        retval = proc.wait()

        data = out.split('\n')

        return data[0]

    return -1

def get_ram_usage(docker_ids):
    """"""


def main():
    """Main method call helper fuctions"""

    con = mdb.connect('localhost', 'collector', 'GetMe2ome2t@t2', 'docker_stats');

    with con:
        cur = con.cursor()
        try:
            while True:
                docker_ids = get_docker_ids()
                for id in docker_ids:
                    create = "CREATE TABLE IF NOT EXISTS " + str(id) + "(Id INT PRIMARY KEY AUTO_INCREMENT, Cpu INT, Core1 INT, Core2 INT, Core3 INT, Core4 INT, Memory INT, Ram INT)"
                    cur.execute(create)
                    cpu_data = get_cpu_usage(id)
                    core_data = get_core_usage(id)
                    memory_data = get_memory_usage(id)
                    #ram_data = get_ram_usage(id)

                    if cpu_data != -1 and core_data != -1 and memory_data != -1:
                        insert = "INSERT INTO " + str(id) + "(Cpu,Core1,Core2,Core3,Core4,Memory,Ram) VALUES(" + str(cpu_data) + "," + core_data[0] + "," + core_data[1] + "," + core_data[2] + "," + core_data[3] + "," + str(memory_data) + ",0)"
                        cur.execute(insert)
                time.sleep(ARGS['time_frame'])
        except KeyboardInterrupt:
            print "Exiting"
            sys.exit()

main()
