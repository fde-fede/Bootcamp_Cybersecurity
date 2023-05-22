if ! $(docker network ls | grep inquisitor); then
	docker-compose up -d
fi

echo "Name and IPs of containers:"
docker network inspect inquisitor_default | grep -e IPv4 -e Name

echo "Go to 'localhost:3000' to open wireshark"
echo -e "Go to 'localhost:5800' to open ftp client:\n\thost: ip of server"
echo -e "\tUsername and password: ftp\n\tPort: 21"

echo -e "\nEnter 'attacker' container...\n"
docker exec -it attacker bash