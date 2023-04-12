import sys

def text_analyzer(argumentos=''):
    """This function counts the number of upper characters, lower characters, punctuation and spaces in a given text."""
    if not isinstance(argumentos, str):
        print("AssertionError: argument is not a string")
        return
    if argumentos == '':
        argumentos = input("What is the text to analyze?\n")
    lower_counter = 0
    upper_counter = 0
    punctuation_counter = 0
    space_counter = 0
    for char in argumentos:
        if char.isspace():
            space_counter += 1
        elif char.isalpha():
            if char.islower():
                lower_counter += 1
            elif char.isupper():
                upper_counter += 1
        elif char.isnumeric():
            pass
        elif char.isascii():
            punctuation_counter += 1
    print("The text contains", len(argumentos), "character(s)")
    print(f"- ", upper_counter, "upper letter(s)")
    print(f"- ", lower_counter, "lower letter(s)")
    print(f"- ", punctuation_counter, "punctuation mark(s)")
    print(f"- ", space_counter, "space(s)")

if __name__ == '__main__':
    if len(sys.argv) > 2:
        print("Error: too many arguments. Usage: python3 count.py 'text'")
    else:
        text_analyzer(sys.argv[1])
