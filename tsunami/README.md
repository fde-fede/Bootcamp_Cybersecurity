
# Tsunami

Since Aleph1 created his "Smashing The Stack For Fun And Profit" decades ago, buffer
and stack overflows are a well-known technique that still cause many of the most used
vulnerabilities by attackers. Create a C program that causes a simple buffer overflow in
a Windows XP 32-bit environment. To do this you will use the strcpy function.

### Explanation

This project required us to create a vulnerable program, and one payload that will take advantage of the vulnerable program. The difficulty of this project, was getting the calculator shellcode, and understanding how the CPU debugger works (in my case, I used ollydbg), to know how the system memory works, such as the jumps or the behavior of the buffer overflow.

### How it works

To make this program works, we just need to compile both C files, and execute the payload giving 76 random characters, to force the buffer overflow. The buffer overflow is caused because we used the strcpy function in the vulnerable program, which doesn't take the string length into account.


