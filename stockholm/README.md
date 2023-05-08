# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#                                                                                                                                     #
#     #####      ###########       ####          #####     ##     ##    ###     ###       ####       ###         ######      ######   #
#   ###  ####    ###########     ########      #########   ##    ##     ###     ###     ########     ###         ### ###    ### ###   #
#   ###              ###        ##      ##    ###          ##   ##      ###     ###    ##      ##    ###         ###  ###  ###  ###   #
#      ###           ###       ##        ##   ##           #####        ###########   ##        ##   ###         ###   ######   ###   #
#         ###        ###       ##        ##   ##           #####        ###########   ##        ##   ###         ###     ##     ###   #
#         ####       ###        ##      ##    ###          ##  ##       ###     ###    ##      ##    ###         ###            ###   #
#   ###  ####        ###         ########      #########   ##    ##     ###     ###     ########     #########   ###            ###   #
#     #####          ###           ####          #####     ##      ##   ###     ###       ####       #########   ###            ###   #
#                                                                                                                                     #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

Welcome to Stockholm!

Stockholm is a ransomware used to encrypt every file that has a "wannacry" extension, and generates a key.key to decrypt with reversing algorithm
This program is written in python language, here are the instructions to use it:

-   Usage: stockholm.py [ -r <key> ] [ -s ] [ -v ] [ -h | --help ]

-   stockholm.py            Encrypts files in $HOME/infection path, and generates key.key in the execution directory

-   stockholm.py -r <key>   Decrypts files affected by infection in $HOME/infection path, using the key given as argument to decrypt them

-   stockholm.py -v         Shows the version of the program

-   stockholm.py -s         Launch with silent mode (no console outputs)

The program uses the Fernet algorithm (included in cryptography library), to encrypt the files and generate the .key file.
Stockholm only affects to the files that have one of the extensions that was affected by wannacry attack.

ADVERTISEMENT: WITHOUT THE .KEY IS IMPOSSIBLE TO DECRYPT FILES, SO DON'T REMOVE IT