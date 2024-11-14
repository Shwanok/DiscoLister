import requests
from bs4 import BeautifulSoup

# ফাংশন: পেজের টাইটেল খুঁজে বের করা
def get_page_title(url):
    try:
        if not url.startswith("http://") and not url.startswith("https://"):
            url = "http://" + url  # ডিফল্টভাবে http:// যোগ করা
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            return soup.title.string
        else:
            print(f"Failed to retrieve {url} - Status code: {response.status_code}")
            return None
    except requests.RequestException as e:
        print(f"An error occurred: {e}")
        return None

# ফাংশন: HTTP হেডার এবং সার্ভার ইনফরমেশন সংগ্রহ করা
def get_http_headers(url):
    try:
        if not url.startswith("http://") and not url.startswith("https://"):
            url = "http://" + url
        response = requests.get(url)
        if response.status_code == 200:
            headers = response.headers
            print("\n--- HTTP Headers ---")
            for key, value in headers.items():
                print(f"{key}: {value}")
            return headers
        else:
            print(f"Failed to retrieve headers from {url} - Status code: {response.status_code}")
            return None
    except requests.RequestException as e:
        print(f"An error occurred while fetching headers: {e}")
        return None

# ফাংশন: সাবডোমেইন এনুমারেশন
def enumerate_subdomains(domain):
    subdomains = ['www', 'mail', 'ftp', 'webmail', 'test', 'dev']
    found_subdomains = []

    print("\n--- Enumerating Subdomains ---")
    for subdomain in subdomains:
        subdomain_url = f"http://{subdomain}.{domain}"
        try:
            response = requests.get(subdomain_url)
            if response.status_code == 200:
                print(f"Found: {subdomain_url}")
                found_subdomains.append(subdomain_url)
        except requests.ConnectionError:
            pass

    if not found_subdomains:
        print("No subdomains found.")
    return found_subdomains

# নতুন ফাংশন: ডিরেক্টরি এনুমারেশন
def enumerate_directories(url):
    directories = ['admin', 'login', 'dashboard', 'uploads', 'images', 'css', 'js']
    found_directories = []

    if not url.startswith("http://") and not url.startswith("https://"):
        url = "http://" + url

    print("\n--- Enumerating Directories ---")
    for directory in directories:
        directory_url = f"{url}/{directory}"
        try:
            response = requests.get(directory_url)
            if response.status_code == 200 or response.status_code in [301, 302]:
                print(f"Found: {directory_url}")
                found_directories.append(directory_url)
        except requests.ConnectionError:
            pass

    if not found_directories:
        print("No directories found.")
    return found_directories

# URL ইনপুট নিন
url = input("Enter the URL (e.g., example.com or https://example.com): ")

# পেজের টাইটেল বের করা
title = get_page_title(url)
if title:
    print(f"\nPage Title: {title}")
else:
    print("Could not retrieve the page title.")

# HTTP হেডার এবং সার্ভার ইনফরমেশন বের করা
get_http_headers(url)

# সাবডোমেইন এনুমারেশন
domain = url.replace("https://", "").replace("http://", "")
enumerate_subdomains(domain)

# ডিরেক্টরি এনুমারেশন
enumerate_directories(url)
