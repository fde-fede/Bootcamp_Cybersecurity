
# coRSAir

This project introduces specific concepts about the strength of the RSA algorithm andits potential vulnerabilities.  Although the algorithm is considered strong enough forthe computational power of current devices, certain ways of using it can lead to serioussecurity problems.

In this project we had to use C as the language, and we were able to use the openssl library.

## How it works?

### Generate test key files

The resources dir contains a Python script that allows to generate certifies and RSA keys and a file encrypted with the symetric key, which content we have to get back using the program.

### Compile

We need to use the Makefile to compile the program:
```
make generate
```
this command will execute the script and generate the keys and the encrypted file
```
make
```
and this will just compile the coRSAir program.

## Usage

```
./coRSAir <first_key> <second_key> <encrypted_file>
```

