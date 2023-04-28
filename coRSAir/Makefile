INC = /Users/fde-fede/.brew/opt/openssl@3.1/include
LIB = /Users/fde-fede/.brew/opt/openssl@3.1/lib
CFLAGS = -Werror -Wall -Wextra -Wno-deprecated-declarations

all: corsair

corsair: corsair.o
	@clear
	gcc corsair.o -L$(LIB) -lssl -lcrypto -o corsair

corsair.o: corsair.c
	gcc -c corsair.c $(CFLAGS) -I$(INC) -o corsair.o

fclean:
	rm -rf corsair corsair.o resources/cert1.pem resources/cert2.pem resources/passwd.enc resources/encrypted_file.txt

generate:
	cd resources && python3 generate.py