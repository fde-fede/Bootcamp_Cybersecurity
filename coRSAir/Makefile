INC		=		/Users/fde-fede/.brew/opt/openssl@3.1/include
LIB		=		/Users/fde-fede/.brew/opt/openssl@3.1/lib
CFLAGS	=		-Werror -Wall -Wextra

all:
	@clear
	gcc -Wno-deprecated-declarations corsair.c $(CFLAGS) -I$(INC) -L$(LIB) -lssl -lcrypto -o corsair

fclean:
	rm -rf corsair resources/cert1.pem resources/cert2.pem resources/passwd.enc resources/encrypted_file.txt