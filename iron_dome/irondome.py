#!/usr/bin/env python3
import os
import sys
import time
import hashlib
import psutil
import logging

LOG_FILE = "/var/log/irondome/irondome.log"
MAX_MEMORY_USAGE = 100 * 1024 * 1024 # 100 MB
logging.basicConfig(filename=LOG_FILE, level=logging.INFO)

def calculate_file_entropy(file_path):
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.digest()

def monitor_critical_zone(path, extensions):
    for root, dirs, files in os.walk(path):
        for file in files:
            file_path = os.path.join(root, file)
            if extensions:
                if not os.path.splitext(file_path)[1] in extensions:
                    continue
            try:
                with open(file_path, "rb") as f:
                    f.read()
            except Exception as e:
                logging.error("Detected disk read abuse in %s: %s" % (file_path, e))
            try:
                calculate_file_entropy(file_path)
            except Exception as e:
                logging.error("Detected change in entropy in %s: %s" % (file_path, e))
        memory_usage = psutil.Process(os.getpid()).memory_info().rss
        if memory_usage > MAX_MEMORY_USAGE:
            logging.error("Memory usage exceded {} bytes".format(MAX_MEMORY_USAGE))

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Ussage: irondome.py <path_to_defend> <extensions of files to defend>")
        exit()
    path = sys.argv[1]
    if len(sys.argv) > 2:
        extensions = set(sys.argv[2:])
    else:
        extensions = None
    if os.geteuid() == 0:
        print("Irondome is running as root. Defending {0}".format(path))
    else:
        print("Error, Irondome must be executed as root")
        sys.exit(1)
    if not os.access(path, os.R_OK):
        print("Couldn't read {}".format(path))
        exit(1)
    while True:
        monitor_critical_zone(path, extensions)
        time.sleep(60)