
# Arachnida

The objective of this proyect is making two programs in python (Spider and Scorpion) based on web scrapping and management of metadata without using wget, scrappy, or any similar library.

### Spider
The spider program will allow you to extract all the images from a website, recursively, by providing a url as a parameter. Usage:

./spider [-rlp] URL

- Option -r: activates recursively mode.
- Option -r -l [N]: indicates the maximum depth level of the recursive download. If not indicated, it will be 5.
- Option -p [PATH]: indicates the path where the dowloaded files will be saves. If not specified, ./data/ will be used.
 
 This program also works with local paths, even /path/to/.html or localfile:///path/to/.html


### Scorpion
./scorpion FILE1 [FILE2 ...]

This program will receive image files as parameters and will be able to parse them for EXIF and other metadata, displaying them on screen.