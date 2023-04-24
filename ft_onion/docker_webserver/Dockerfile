FROM debian:latest

RUN apt-get update -y && apt upgrade -y
RUN apt-get install nginx tor openssh-server vim -y

COPY sshd_config /etc/ssh/sshd_config

COPY torrc /etc/tor/torrc

COPY index.html /usr/share/nginx/html/index.html

COPY nginx.conf /etc/nginx/nginx.conf

RUN useradd -m pepe
RUN echo "pepe:onion" | chpasswd

ENTRYPOINT service ssh start; nginx; tor