
# Ft_onion

The goal of this project is to crate a web page and make it accessible from the Tor network by creating a hidden service.

## Introduction

To make this project, we are going to use Docker to generate the server, I focused on creating every configuration file of the services we had to implement and the just copy inside the server.

## Usage

Inside the project folder, we need to execute two commands to initialize the docker service:
- $> docker build -t <the_tag_that_we_want> docker_webserver
- $> docker run -d -p 4242:4242 -p 80:80 <tag>

There we go, the server is running!

As a bonus, I added a pong game (2 players) I made with js and added it to the html webpage.