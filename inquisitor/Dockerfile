FROM linuxserver/wireshark:3.4.13

RUN apk update && apk add --no-cache build-base libpcap-dev libnet-dev vim tcpdump net-tools arping
RUN apk add --no-cache py-pip
RUN pip install scapy
WORKDIR /usr/src/