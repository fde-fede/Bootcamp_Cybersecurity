# how to create a list in python?

def generator(text, sep=" ", option=None):
    if not isinstance(text, str) or option not in [None, "shuffle", "unique", "ordered"]:
        yield "ERROR"
    else:
        if option is None:
            lst = text.split(sep)
        elif option == "shuffle":
            lst = set(text.split(sep))
        elif option == "unique":
            lst = list(dict.fromkeys(text.split(sep)))
        elif option == "ordered":
            lst = sorted(text.split(sep))
        for item in lst:
            yield item

if __name__ == '__main__':
    TEXT = "Le Lorem Ipsum est simplement du faux texte."

    print("Regular split :")
    for i in generator(TEXT):
        print(i)
    print()

    print("Split with sep :")
    for i in generator(TEXT, sep="a"):
        print(i)
    print()

    print("Shuffle split :")
    for i in generator(TEXT, option="shuffle"):
        print(i)
    print()

    print("Unique split :")
    for i in generator("a a b c a b c a b b c a", option="unique"):
        print(i)
    print()

    print("Ordered split :")
    for i in generator(TEXT, option="ordered"):
        print(i)
    print()

    print("Invalid split :")
    for i in generator(TEXT, option="invalid"):
        print(i)
    print()

    print("Invalid split :")
    for i in generator(6):
        print(i)
    print()
