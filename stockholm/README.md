
# Stockholm

In this project you will develop a small program capable of causing great havoc. Although
the greatest virtue of ransomware is its ability to spread through networks of hundreds
of computers, in this case, your program will only affect a small part of your files.


### Explanation

Stockholm is a ransomware used to encrypt every file that has a "wannacry" extension, and generates a key.key to decrypt with reversing algorithm
This program is written in python language.

### Usage
./python3 stockholm [-h | --help] [-r <key>] [-v] [-s]

```
$> python3 stockholm.py
```
this will infect the infection folder inside /$HOME path and add .ft extension to every file.

Then, you have various arguments parameters:

- [-h] Shows program help
- [-r] Indicate reversing mode, to deinfect folder
- [-v] Shows program version
- [-s] Toogle silent mode

ADVERTISEMENT: WITHOUT THE .KEY IS IMPOSSIBLE TO DECRYPT FILES, SO DON'T REMOVE IT