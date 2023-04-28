#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <fcntl.h>
#include "openssl/ssl.h"
#include "openssl/bn.h"
#include "openssl/bio.h"
#include "openssl/evp.h"
#include "openssl/pem.h"
#include "openssl/x509.h"

#define BUFFER 1024

RSA *get_rsa(char *path) {
    X509        *cert;
    EVP_PKEY    *pkey;
    RSA         *rsa;
    BIO         *bio;
    int         fd;

    bio = BIO_new(BIO_s_file());
    fd = BIO_read_filename(bio, path);
    if (fd != 1) {
        printf("Error while reading file '%s'.\n", path);
        exit(1);
    }
    cert = PEM_read_bio_X509(bio, NULL, 0, NULL);
    pkey = X509_get_pubkey(cert);
    rsa = EVP_PKEY_get1_RSA(pkey);
    if (!cert || !pkey || !rsa)
    {
        printf("Error while reading certificate and private key.\n");
        exit(1);
    }

    X509_free(cert);
    EVP_PKEY_free(pkey);
    BIO_free(bio);

    return rsa;
}

int main(int argc, char *argv[])
{
    unsigned char *res;
    unsigned char *sol;

    BN_CTX  *ctx;           // Context for RSA algorithm
    RSA     *private;       // Private RSA key
    BIO     *bioprint;      // Basic Input/Output print
    BIGNUM  *one;           // Number '1' in BIGNUM format

    RSA     *rsa1;          //                    # -> Public key
    BIGNUM  *n1;            // First Certificate # -> Prime number 'n1'
    BIGNUM  *q1;            //                    # -> Prime number 'q1'

    RSA     *rsa2;          //                     # -> Public key
    BIGNUM  *n2;            // Second Certificate # -> Prime number 'n2'
    BIGNUM  *q2;            //                     # -> Prime number 'q2'

    BIGNUM  *p;             // Prime number common to both certificates

    BIGNUM  *total;         // Total number of certificates
    BIGNUM  *eu1;           // Number of prime factors of 'n1'
    BIGNUM  *eu2;           // Number of prime factors of 'n2'

    BIGNUM  *e;             // Exponent of public key
    BIGNUM  *d;             // Exponent of private key

    int     fd;             // Decrypter of entry file
    int     len;            // Length of entry file

    if (argc != 4) {
        printf("Usage: %s <cert1.pem> <cert2.pem> <passwd.enc>\n", argv[0]);
        return (0);
    }
    // Initialize variables
    res = malloc(sizeof(unsigned char) * BUFFER);
    sol = malloc(sizeof(unsigned char) * BUFFER);
    ctx = BN_CTX_new();
    bioprint = BIO_new_fp(stdout, BIO_NOCLOSE);
    rsa1 = get_rsa(argv[1]);
    rsa2 = get_rsa(argv[2]);

    one = BN_new();
    q1 = BN_new();
    q2 = BN_new();
    p = BN_new();
    d = BN_new();
    total = BN_new();
    eu1 = BN_new();
    eu2 = BN_new();
    private = RSA_new();

    // Operations to get data
    n1 = (BIGNUM*) RSA_get0_n(rsa1);    // Get 'n1' from first certificate
    n2 = (BIGNUM*) RSA_get0_n(rsa2);    // Get 'n2' from second certificate
    e = (BIGNUM*) RSA_get0_e(rsa1);     // Get 'e' from first certificate

    BN_gcd(p, n1, n2, ctx);         // Calculates MCD and store it on p
    BN_div(q1, NULL, n1, p, ctx);   // Calculates prime factors and store it on q1
    BN_div(q2, NULL, n2, p, ctx);   // Calculates prime factors and store it on q2

    BN_dec2bn(&one, "1");               // Initialize 'one' to 1
    BN_sub(eu1, q1, one);               // Caculates φ Euler function -> 'eu1' = 'q1' - '1' (one)
    BN_sub(eu2, p, one);                // Caculates φ Euler function -> 'eu2' = 'p' - '1' (one)
    BN_mul(total, eu1, eu2, ctx);       // Calculates 'total' = 'eu1' * 'eu2'
    BN_mod_inverse(d, e, total, ctx);   // Calculates the inverse modular of e -> 'd' = 'e' ^ (-1) (mod 'total')

    // Generate private key
    RSA_set0_key(private, n1, e, d);    //Sets the private key, with public key e and n1 in private

    // Associate prime numbers to each RSA
    RSA_set0_factors(rsa1, p, q1);      //Sets the prime factors p and q1 in rsa1
    RSA_set0_factors(rsa2, p, q2);      //Sets the prime factors p and q2 in rsa2

    // Reads entry file, sees if it's possible to read it and decrypt it's content
    fd = open(argv[3], O_RDONLY);
    if (fd < 1)
    {
        printf("\nError opening file %s\n", argv[3]);
        exit(1);
    }
    len = read(fd, res, BUFFER);

    // Print the certificates data
    printf("\nFirst Certificate:\n");
    RSA_print(bioprint, rsa1, 0);
    RSA_print(bioprint, private, 0);

    printf("\nSecond Certificate:\n");
    RSA_print(bioprint, rsa2, 0);
    RSA_print(bioprint, private, 0);

    RSA_private_decrypt(len, res, sol, private, RSA_PKCS1_PADDING);     // Function that decrypts the message

    // Print the file content
    printf("\nEncrypted text:\n");
    printf("%s\n", res);

    printf("\nDesencrypted text:\n");
    printf("%s\n", sol);

    // Free memory
    BN_CTX_free(ctx);
    BIO_free(bioprint);

    BN_free(one);
    BN_free(n1);
    BN_free(q1);
    BN_free(n2);
    BN_free(q2);

    BN_free(p);
    BN_free(d);
    BN_free(e);

    BN_free(total);
    BN_free(eu1);
    BN_free(eu2);

    return 0;
}