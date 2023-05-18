
# Iron Dome

This is the second part of the ransomware branch. In this part, you will develop a
specific tool that will detect anomalous activity by monitoring different operating system
parameters.
Unfortunately, there is no totally effective way to prevent ransomware attack, but after
completing this project you will be able to understand the weak points of a computer
system regarding these malware infections.

### Explanation

This project is developed for Linux and MacOS platform. Basically, the program must monitorize a specific folder and save every inusual behavior in a irondome.log file.

The program shows various weird behaviours:

- Disk read abuse
- Intensive use of cryptographic activity
- Changes in the entropy of the files


### Usage

The usage is very simple:
```
$> python3 irondome <path/to/monitorize> [ <file_extensions to watch> ... ]
```

All alerts would be reported in the /var/log/irondome/irondome.log file.

I also included a test program, which is a script that simulates every tipe of weird behaviour in the path you want.