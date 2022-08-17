import argparse
from urllib.parse import urljoin
from pprint import pprint

import requests
from bs4 import BeautifulSoup as bs

s = requests.Session()
s.headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) " \
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36"

def login(login_url):
    print("Log in the web")
    username = input("username:")
    password = input("password:")
    login_payload = {
        "username": username,
        "password": password,
        "Login": "Login",
    }
    r = s.get(login_url)


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



def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-o", default="output",
        help="archive file, if not specified it will stored in a default one")
    parser.add_argument("-X", default="GET",
        help="Type of request, if not specified GET will be used")
    parser.add_argument("url", help="url to scan")
    parser.add_argument("-c", "--cookie", 
            help="introduce cookies in form of 'name': 'value', etc")
    args = parser.parse_args()

    if (args.cookie):
        cookie = args.cookie.replace("'", '"')
        try:
            cookie = json.loads(cookie)
        except:
            print("Error: cookie wrong format")
            quit()
        for key in cookie:
            new_cookie = {}
            new_cookie['name'] = key
            new_cookie['value'] = cookie[key]
            s.cookies.set(**new_cookie)

if __name__ == "__main__":
    main()
