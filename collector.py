#!/usr/bin/python
"""
This tool gathers and saves Container stats pulled from /sys/fs/cgroup,
in a mysql db.
"""

import argparse
import subprocess
import MySQLdb as mdb
import os
import time
import sys

ARGS = {'time_frame': 0.01, 'mode': 'collect', 'db_user': 'collector',
        'db_password': 'GetMe2ome2t@t2', 'db_location': 'localhost',
        'db_name': 'docker_stats', 'container_id': ''}

def read_args():
    """
    Read in arguments passed in by user
    """

    parser = argparse.ArgumentParser()
    parser.add_argument('--mode', '-m', nargs=1, dest='mode', type=str,
                        required=False, help='Mode type (collect or analyse)')
    parser.add_argument('--container-id', '-id', nargs=1, dest='container_id',
                        type=str, required=False, help='Enter container ID')
    args = parser.parse_args()

    if args.mode != None:
        ARGS['mode'] = args.mode[0]

        if ARGS['mode'] == 'analyse' and args.container_id != None:
            ARGS['container_id'] = args.container_id[0]
        elif ARGS['mode'] == 'analyse':
            print 'You have to supply a container ID.'


def get_docker_ids():
    """
    Get long docker Container id's
    """

    docker_ids = []

    proc = subprocess.Popen('docker ps -q --no-trunc', shell=True,
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    for line in proc.stdout.readlines():
        container_id = line.split( )
        docker_ids.append(container_id[0])
    proc.wait()

    return docker_ids

def get_cpu_usage(docker_id):
    """
    Collect container cpu usage data for each running continer,
    /sys/fs/cgroup/cpuacct/docker/$CONTAINER_ID/cpuacct.usage
    """

    location = '/sys/fs/cgroup/cpuacct/docker/'
    data_file = '/cpuacct.usage'
    command = location + docker_id + data_file
    if os.path.exists(command):
        command = 'cat ' + command
        proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT)
        out, _ = proc.communicate()
        proc.wait()

        data = out.split('\n')

        return data[0]

    return -1


def get_core_usage(docker_id):
    """
    Collect individual core usage data for each running continer,
    /sys/fs/cgroup/cpuacct/docker/$CONTAINER_ID/cpuacct.usage_percpu
    """

    location = '/sys/fs/cgroup/cpuacct/docker/'
    data_file = '/cpuacct.usage_percpu'

    command = location + docker_id + data_file

    if os.path.exists(command):
        command = 'cat ' + command
        proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT)
        out, _ = proc.communicate()
        proc.wait()

        data = out.split('\n')
        data = data[0].split(' ')

        return (data[0], data[1], data[2], data[3])

    return -1


def get_memory_usage(docker_id):
    """
    Collect memory usage data for each running container,
    /sys/fs/cgroup/memory/docker/$CONTAINER_ID/memory.usage_in_bytes
    """

    location = '/sys/fs/cgroup/memory/docker/'
    data_file = '/memory.usage_in_bytes'

    command = location + docker_id + data_file

    if os.path.exists(command):
        command = 'cat ' + command
        proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT)
        out, _ = proc.communicate()
        proc.wait()

        data = out.split('\n')

        return data[0]

    return -1

def empty_db():
    """
    Drop all existing tables in the db,
    this runs once before collecting new data.
    """

    drop_tables = "sudo bash table_drop.sh " + ARGS['db_user'] + ' ' \
                  + ARGS['db_password'] + ' ' + ARGS['db_name']
    proc = subprocess.Popen(drop_tables, shell=True, stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT)
    out, _ = proc.communicate()

    print out

    retval = proc.wait()

    return retval

def collect_data():
    """
    Run in a loop collecting container stats
    """

    empty_db()

    con = mdb.connect(ARGS['db_location'], ARGS['db_user'],
                      ARGS['db_password'], ARGS['db_name'])

    with con:
        cur = con.cursor()
        print 'Running ...'
        try:
            while True:
                docker_ids = get_docker_ids()
                for container_id in docker_ids:
                    create = "CREATE TABLE IF NOT EXISTS " + str(container_id) \
                    + "(Id INT PRIMARY KEY AUTO_INCREMENT, Cpu INT, Core1 INT" \
                    + ", Core2 INT, Core3 INT, Core4 INT, Memory INT)"
                    cur.execute(create)
                    cpu_data = get_cpu_usage(container_id)
                    core_data = get_core_usage(container_id)
                    memory_data = get_memory_usage(container_id)

                    if cpu_data != -1 and core_data != -1 and memory_data != -1:
                        insert = "INSERT INTO " + str(container_id) \
                        + "(Cpu,Core1,Core2,Core3,Core4,Memory) VALUES(" \
                        + str(cpu_data) + "," + core_data[0] + "," \
                        + core_data[1] + "," + core_data[2] + "," \
                        + core_data[3] + "," + str(memory_data) + ")"
                        cur.execute(insert)
                time.sleep(ARGS['time_frame'])
        except KeyboardInterrupt:
            print "Exiting"
            sys.exit()


def analyse_data():
    """
    Retrieve container's stats
    """

    con = mdb.connect(ARGS['db_location'], ARGS['db_user'],
                      ARGS['db_password'], ARGS['db_name'])

    with con:
        cur = con.cursor()
        cur.execute("SELECT * FROM " + ARGS['container_id'])

        rows = cur.fetchall()

        print "(T - Cpu - Core1 - Core2 - Core3 - Core4 - Memory)"
        for row in rows:
            print row[0], row[1], row[2], row[3], row[4], row[5], row[6]


def main():
    """
    Main method call helper fuctions
    """

    read_args()


    if ARGS['mode'] == 'collect':
        collect_data()
    elif ARGS['mode'] == 'analyse':
        analyse_data()
    else:
        print ARGS['mode'] + ' is not a valid mode.'


main()
