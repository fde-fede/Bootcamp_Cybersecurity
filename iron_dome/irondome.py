#!/usr/bin/env python3

from colorama import Fore, init
import threading
import daemon
import time
import os
import sys
import psutil
import logging
import os
import math

sys.tracebacklimit = 0

class Archivo:
    def __init__(self, name, old_entropy=None, entropy=None):
        self.name = name
        self.old_entropy = old_entropy
        self.entropy = entropy

def shannon_entropy(data):
    """
    Calculates the Shannon entropy of a byte string.
    """
    if not data:
        return 0
    entropy = 0
    for x in range(256):
        p_x = float(data.count(x)) / len(data)
        if p_x > 0:
            entropy += - p_x * math.log(p_x, 2)
    return entropy

def file_entropy(file_path):
    """
    Calculates the entropy of a file.
    """
    if os.path.exists(file_path):
        with open(file_path, 'rb') as f:
            data = f.read()
            size = len(data)
            entropy = shannon_entropy(data)
            return entropy * size
    else:
        return (-1)

def detect_crypto_abuse(zone_path):
    cpu_percent = psutil.cpu_percent(interval=1)
    memory_percent = psutil.virtual_memory().percent
    if cpu_percent > 80 or memory_percent > 45:
        logging.warning(Fore.YELLOW + f"Intensive cryptographic activity detected at {zone_path}!: CPU = {cpu_percent}%, Memory = {memory_percent}%" + Fore.RESET)
        time.sleep(10)
    time.sleep(1)

def detect_disk_read_abuse(zone_path):
    """
    Detect disk read abuse in a given folder.
    """
    READ_THRESHOLD = 500000
    disk_usage = psutil.disk_usage(zone_path)
    bytes_used_start = disk_usage.used

    time.sleep(20)

    disk_usage = psutil.disk_usage(zone_path)
    bytes_used_end = disk_usage.used

    bytes_read_per_second = (bytes_used_end - bytes_used_start) / 20

    print(f"Bytes read per second: {abs(bytes_read_per_second)}")
    print(f"Limit for disk read abuse in bytes per second: {READ_THRESHOLD}")
    if abs(bytes_read_per_second) > READ_THRESHOLD:
        logging.warning(Fore.LIGHTBLUE_EX + f"Disk read abuse detected in folder {zone_path}! Average read rate: {abs(bytes_read_per_second)} bytes/second" + Fore.RESET)

saved_files = set()

def monitor_critical_zone(zone_path, extensions=None):
    # Check if the zone path is valid
    if not os.path.exists(zone_path):
        logging.error(f"{zone_path} does not exist")
        return
    # Monitor the critical zone indefinitely
    else:
        init()
        logging.basicConfig(filename='/var/log/irondome/irondome.log', level=logging.INFO, format='%(asctime)s %(message)s')
        logging.info(Fore.GREEN + "Monitoring critical zone at " + Fore.RESET + zone_path)
        #logging.Formatter
        previous_memory_mb = None
        tmp = 0
        while True:
            # Do some work here...
            try:
                for root, dirs, files in os.walk(zone_path):
                    for file in files:
                        if os.path.exists(os.path.join(root, file)):
                            if not extensions or file.endswith(tuple(extensions)):
                                file_path = os.path.join(root, file)
                                file_class = Archivo(file_path)
                                if file_class.name not in [file.name for file in saved_files]:
                                    logging.info(Fore.CYAN + "Monitoring file " + Fore.RESET + file_path)
                                    saved_files.add(file_class)
                                    time.sleep(1)
                for file in saved_files:
                    if not os.path.exists(file.name):
                        logging.info(Fore.RED + "File " + Fore.WHITE + file.name + Fore.RED + " has been deleted" + Fore.RESET)
                        saved_files.remove(file)

            # Calculate entropy
                for file in saved_files:
                    entropy = file_entropy(file.name)
                    if not file.old_entropy:
                        file.old_entropy = entropy
                    file.entropy = entropy
                    if file.entropy != file.old_entropy:
                        logging.info(Fore.MAGENTA + "Entropy of file {} has changed!: old entropy -> {} new entropy -> {}".format(file.name, file.old_entropy, file.entropy) + Fore.RESET)
                        file.old_entropy = file.entropy
                        time.sleep(1)
            except RuntimeError:
                pass

            if tmp == 0:
                disk_read_abuse_thread = threading.Thread(target=run_detect_disk_read_abuse, args=(zone_path,))
                disk_read_abuse_thread.start()
                crypto_abuse_thread = threading.Thread(target=run_detect_crypto_abuse, args=(zone_path,))
                crypto_abuse_thread.start()
                tmp = 1
            
            process = psutil.Process(os.getpid())
            memory_mb = process.memory_info().rss / 1024 / 1024
            if memory_mb != previous_memory_mb:
                print(f"The memory usage of the program is {memory_mb} MB")
            previous_memory_mb = memory_mb
            if memory_mb > 100:
                logging.warning(Fore.RED + "Memory usage exceeded 100 MB!" + Fore.RESET)
                break
                # Do something else here...

def run_detect_crypto_abuse(zone_path):
    while True:
        detect_crypto_abuse(zone_path)

def run_detect_disk_read_abuse(zone_path):
    while True:
        detect_disk_read_abuse(zone_path)

def main():
    if os.geteuid() != 0:
        print("Este programa solo puede ser ejecutado por el usuario root.")
        sys.exit(1)
    # Parse command line arguments
    if len(sys.argv) < 2:
        print("Ussage: ./irondome.py [zone_path] [<extensions>]")
        sys.exit(1)
    zone_path = sys.argv[1]
    extensions = sys.argv[2:] if len(sys.argv) > 2 else None

    # Start the daemon and monitor the critical zone
    daemon.DaemonContext(
        monitor_critical_zone(zone_path, extensions)
    )

if __name__ == "__main__":
    main()

# ~/private/iron_dome/tests
# /home/kali/Desktop/tests