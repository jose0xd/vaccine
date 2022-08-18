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


def get_all_forms(url):
    """Returns all forms from the HTML content of a url"""
    soup = bs(s.get(url).content, "html.parser")
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
    }
    for error in errors:
        if error in response.content.decode().lower():
            return True
    return False

def check_form(url):
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
                print("\nSQL Injection vulnerability detected in:\n\t", url)
                print("data:")
                pprint(data)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-o", default="output",
        help="archive file, if not specified it will stored in a default one")
    parser.add_argument("-X", default="GET",
        help="Type of request, if not specified GET will be used")
    parser.add_argument("url", help="url to scan")
    parser.add_argument("-c", "--cookie", 
            help="introduce cookies in form of 'name=value&name=value...'")
    args = parser.parse_args()

    if (args.cookie):
        parse_cookies(args.cookie)

    check_form(args.url)

if __name__ == "__main__":
    main()
