import argparse
from urllib.parse import urljoin
from pprint import pprint

import requests
from bs4 import BeautifulSoup as bs

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
        soup = bs(s.get(url).content, "html.parser")
    except Exception as e:
        print(e)
        quit()
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
        "unrecognized token"
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
            for input_tag in form_details["inputs"]:
                if input_tag["value"] or input_tag["type"] == "hidden":
                    try:
                        data[input_tag["name"]] = input_tag["value"] + c
                    except:
                        pass
                elif input_tag["type"] != "submit":
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
                print("\nSQL Injection vulnerability detected in:\n\t", res.url)
                print("data:")
                pprint(data)
    if not vulnerable:
        print(url, "\n\tdoesn't seem to be vulnerable")

def check_url(url, data, method):
    if data == None:
        print("No data to process. Use '--data' argument")
        quit()
    for c in "\"'":
        for k in data:
            data[k] = f"test{c}"
        try:
            if method == "GET":
                res = s.get(url, params=data)
            elif method == "POST":
                res = s.post(url, data=data)
        except Exception as e:
            print(e)
            quit()
        if is_vulnerable(res):
            print("url vulnerable")
        else:
            print("url not vulnerable")

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
    args = parser.parse_args()

    if (args.X != "GET" and args.X != "POST"):
        print("The method should be only 'GET' or 'POST'")
        quit()

    if (args.cookie):
        parse_cookies(args.cookie)

    if (args.forms):
        check_form(args.url)
    else:
        check_url(args.url, parse_data(args.data), args.X)


if __name__ == "__main__":
    main()
