#!/usr/bin/env python

# Test Master
# A WorkQueue master coordinator for testing purposes.
# Executes the test_worker.py script on remote workers.
# Usage: test_master.py <path/to/test_worker.py> <task_count>

from work_queue import *

import urllib2
import json
import sys
import os


def get_ip():
    """Get IP
    Ping ifconfig.co and return external IP address, or -1 if unable to find.

    :return: IP address if possible, -1 on error.
    """
    try:
        response = urllib2.urlopen('http://ifconfig.co/json')
        data = json.load(response)
        return data["ip"]
    except Exception as e:
        print("WARNING: Unable to obtain IP (%s)." % e)
        return -1


def launch_message(port, ip):
    wkrstr = "work_queue_worker -d all --cores 0 %s %s" % (ip, port)
    print("Listening for workers @ %s on port %s" % (ip, port))
    print("(this is a best guess IP, depending on your computing environment you may need to adjust.)")
    print("\nHINT: To start a worker, you can probably use this command: \n%s\n" % wkrstr)


def main():

    test_worker = '/usr/local/bin/test_worker.py'
    if not os.path.exists(test_worker):
        print("ERROR: test_worker.py was not found. Please check the path.")
        sys.exit(1)

    task_count = 1
    port = WORK_QUEUE_DEFAULT_PORT

    # Spawn queue.
    try:
        q = WorkQueue(port)
        launch_message(q.port, get_ip())
    except Exception as e:
        print("WorkQueue Launch Failed.")
        print(e)

    # Add tasks to queue.
    for i in range(task_count):
        outfile = 'run%d.txt' % i
        command = './test_worker.py %s' % outfile

        t = Task(command)
        t.specify_tag("Test #%s" % i)
        t.specify_file(test_worker, os.path.basename(test_worker), WORK_QUEUE_INPUT, cache=True)
        t.specify_file(outfile, outfile, WORK_QUEUE_OUTPUT, cache=False)

        taskid = q.submit(t)
        print("Submitted task (%d): %s" % (taskid, t.command))

    print("All tasks submitted (%d)...waiting..." % task_count)

    # Wait for tasks to complete.
    while not q.empty():
        t = q.wait(5)
        if t:
            print("Task complete (%s): %d" % (t.tag, t.return_status))  # AKB Replaced t.id with t.tag
            if t.return_status == 0:
                print('..success')
            else:
                print('..failure (is psutil installed on workers?)')

    print("All tasks completed!")

if __name__ == "__main__":
    main()
    sys.exit(0)