import requests
from bs4 import BeautifulSoup
import socket
import re

# পেজের টাইটেল খুঁজে বের করা
def get_page_title(url):
    try:
        if not url.startswith("http://") and not url.startswith("https://"):
            url = "http://" + url
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

# HTTP হেডার সংগ্রহ করা
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

# সাবডোমেইন এনুমারেশন
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

# ডিরেক্টরি এনুমারেশন
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

# ওপেন পোর্ট স্ক্যানিং
def scan_open_ports(domain):
    ports = [21, 22, 23, 25, 80, 443, 8080]
    open_ports = []

    print("\n--- Scanning Open Ports ---")
    for port in ports:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((domain, port))
        if result == 0:
            print(f"Port {port} is open")
            open_ports.append(port)
        sock.close()

    if not open_ports:
        print("No open ports found.")
    return open_ports

# কমন ফাইল এনুমারেশন
def enumerate_common_files(url):
    files = ['robots.txt', 'sitemap.xml', '.htaccess']
    found_files = []

    if not url.startswith("http://") and not url.startswith("https://"):
        url = "http://" + url

    print("\n--- Enumerating Common Files ---")
    for file in files:
        file_url = f"{url}/{file}"
        try:
            response = requests.get(file_url)
            if response.status_code == 200:
                print(f"Found: {file_url}")
                found_files.append(file_url)
        except requests.ConnectionError:
            pass

    if not found_files:
        print("No common files found.")
    return found_files

# ব্যানার গ্র্যাবিং
def grab_banner(domain, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        sock.connect((domain, port))
        banner = sock.recv(1024).decode().strip()
        print(f"Banner on Port {port}: {banner}")
    except Exception as e:
        print(f"Could not retrieve banner on Port {port}: {e}")
    finally:
        sock.close()

# নতুন ফাংশন: URL Parameter Discovery
def discover_url_parameters(url):
    if not url.startswith("http://") and not url.startswith("https://"):
        url = "http://" + url

    print("\n--- Discovering URL Parameters ---")
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            links = soup.find_all('a', href=True)
            parameter_links = []

            for link in links:
                href = link['href']
                if '?' in href:
                    parameter_links.append(href)
                    print(f"Found parameterized URL: {href}")
            
            if not parameter_links:
                print("No parameterized URLs found.")
            return parameter_links
        else:
            print(f"Failed to retrieve {url} - Status code: {response.status_code}")
            return []
    except requests.RequestException as e:
        print(f"An error occurred: {e}")
        return []

# নতুন ফাংশন: Form Enumeration
def enumerate_forms(url):
    if not url.startswith("http://") and not url.startswith("https://"):
        url = "http://" + url

    print("\n--- Enumerating Forms ---")
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            forms = soup.find_all('form')

            for i, form in enumerate(forms, 1):
                print(f"\nForm #{i}")
                action = form.get('action')
                method = form.get('method', 'GET')
                print(f"Action: {action}, Method: {method}")
                inputs = form.find_all('input')
                
                for input_field in inputs:
                    input_type = input_field.get('type', 'text')
                    input_name = input_field.get('name')
                    print(f"Input field - Type: {input_type}, Name: {input_name}")
        else:
            print(f"Failed to retrieve {url} - Status code: {response.status_code}")
    except requests.RequestException as e:
        print(f"An error occurred: {e}")

# নতুন ফাংশন: Hidden Parameter Discovery
def discover_hidden_parameters(url):
    if not url.startswith("http://") and not url.startswith("https://"):
        url = "http://" + url

    print("\n--- Discovering Hidden Parameters ---")
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            forms = soup.find_all('form')

            for i, form in enumerate(forms, 1):
                hidden_inputs = form.find_all('input', {'type': 'hidden'})
                
                if hidden_inputs:
                    print(f"\nForm #{i} - Hidden Fields Found:")
                    for hidden_input in hidden_inputs:
                        input_name = hidden_input.get('name')
                        input_value = hidden_input.get('value', 'N/A')
                        print(f"Hidden field - Name: {input_name}, Value: {input_value}")
                else:
                    print(f"Form #{i} - No hidden fields found.")
        else:
            print(f"Failed to retrieve {url} - Status code: {response.status_code}")
    except requests.RequestException as e:
        print(f"An error occurred: {e}")

# URL ইনপুট নিন
url = input("Enter the URL (e.g., example.com or https://example.com): ")

# আগের সব ফাংশন চালান
title = get_page_title(url)
if title:
    print(f"\nPage Title: {title}")
else:
    print("Could not retrieve the page title.")

get_http_headers(url)
domain = url.replace("https://", "").replace("http://", "")
enumerate_subdomains(domain)
enumerate_directories(url)
open_ports = scan_open_ports(domain)
for port in open_ports:
    grab_banner(domain, port)
enumerate_common_files(url)
discover_url_parameters(url)
enumerate_forms(url)
discover_hidden_parameters(url)
