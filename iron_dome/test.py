#!/usr/bin/env python3
import os
import sys
import time
import psutil
import hashlib
import logging

LOG_FILE = "/var/log/irondome/irondome.log"
CRITICAL_ZONE = sys.argv[1] if len(sys.argv) > 1 else "/"
EXTENSIONS = sys.argv[2:] if len(sys.argv) > 2 else None
MAX_MEMORY_USAGE = 100 * 1024 * 1024  # 100 MB
logging.basicConfig(filename=LOG_FILE, level=logging.INFO)

def is_running_as_root():
    return os.geteuid() == 0

def has_access_to_critical_zone():
    return os.access(CRITICAL_ZONE, os.R_OK)

def is_extension_monitored(file_path):
    if not EXTENSIONS:
        return True
    return os.path.splitext(file_path)[1] in EXTENSIONS

def calculate_file_entropy(file_path):
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.digest()

def monitor_critical_zone():
    for root, dirs, files in os.walk(CRITICAL_ZONE):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            if not is_extension_monitored(file_path):
                continue
            try:
                with open(file_path, "rb") as f:
                    f.read()
            except Exception as e:
                logging.error(f"Detected disk read abuse in {file_path}: {e}")
            try:
                calculate_file_entropy(file_path)
            except Exception as e:
                logging.error(f"Detected change in entropy in {file_path}: {e}")
        memory_usage = psutil.Process(os.getpid()).memory_info().rss
        if memory_usage > MAX_MEMORY_USAGE:
            logging.error(f"Memory usage exceeded {MAX_MEMORY_USAGE} bytes")

def main():
    if not is_running_as_root():
        print("This program must be executed as root.")
        sys.exit(1)
    if not has_access_to_critical_zone():
        print(f"Could not read {CRITICAL_ZONE}")
        sys.exit(1)
    while True:
        monitor_critical_zone()
        time.sleep(60)

if __name__ == "__main__":
    main()