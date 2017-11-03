#!/usr/bin/env python

# Test Worker
# A sample script to be executed by test_master.py on remote workers.
# Writes a file (or prints to STDOUT if no filename specified) reporting basic system information.
# Usage: test_worker.py <OPTIONAL output_filename>

# Imports.
try:
    import psutil
    import socket
    import sys
except ImportError:
    print("ERROR: missing python dependencies.")
    sys.exit(2)


def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    s.close()
    return ip


def human_size(num, suffix='B'):
    for unit in ['', 'K', 'M', 'G', 'T', 'P', 'E', 'Z']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Yi', suffix)


def get_sys_info():
    du = psutil.disk_usage('/')
    mem = psutil.virtual_memory()

    sys_info = {"IP": get_ip(),
                "CPU": psutil.cpu_count(logical=False),
                "vCPU": psutil.cpu_count(),
                "mem_total": human_size(mem.total),
                "mem_avail": human_size(mem.available),
                "mem_free": human_size(mem.free),
                "mem_used": human_size(mem.used),
                "mem_percent": mem.percent,
                "disk_total": human_size(du.total),
                "disk_used": human_size(du.used),
                "disk_free": human_size(du.free),
                "disk_percent": du.percent}

    return sys_info


def write_report(output_filename, sys_info):
    o = open(output_filename, 'w')
    o.write("Reporting from %s\n" % sys_info["IP"])

    o.write("\n# Processors\n")
    cstats = ["CPU", "vCPU"]
    for stat in cstats:
        o.write(stat + '=' + str(sys_info[stat]) + '\n')

    o.write("\n# Memory\n")
    mstats = ["mem_total", "mem_avail", "mem_free", "mem_used", "mem_percent"]
    for stat in mstats:
        o.write(stat + '=' + str(sys_info[stat]) + '\n')

    o.write("\n# Disk\n")
    dstats = ["disk_total", "disk_used", "disk_free", "disk_percent"]
    for stat in dstats:
        o.write(stat + '=' + str(sys_info[stat]) + '\n')

    o.close()


def print_report(sys_info):
    print("Reporting from %s" % sys_info["IP"])

    print("\n# Processors")
    cstats = ["CPU", "vCPU"]
    for stat in cstats:
        print(stat + '=' + str(sys_info[stat]))

    print("\n# Memory")
    mstats = ["mem_total", "mem_avail", "mem_free", "mem_used", "mem_percent"]
    for stat in mstats:
        print(stat + '=' + str(sys_info[stat]))

    print("\n# Disk")
    dstats = ["disk_total", "disk_used", "disk_free", "disk_percent"]
    for stat in dstats:
        print(stat + '=' + str(sys_info[stat]))


def main(argv):
    sys_info = get_sys_info()

    try:
        write_report(argv[0], sys_info)
    except IndexError:
        print_report(sys_info)


if __name__ == "__main__":
    main(sys.argv[1:])
