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

# URL Parameter Discovery
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

# Form Enumeration
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

# Hidden Parameter Discovery
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

# Sensitive Directory Bruteforce
def brute_force_directories(url):
    sensitive_directories = ['admin', 'backup', 'config', 'db', 'logs']
    found_sensitive_directories = []

    if not url.startswith("http://") and not url.startswith("https://"):
        url = "http://" + url

    print("\n--- Bruteforcing Sensitive Directories ---")
    for directory in sensitive_directories:
        directory_url = f"{url}/{directory}"
        try:
            response = requests.get(directory_url)
            if response.status_code == 200 or response.status_code in [301, 302]:
                print(f"Found sensitive directory: {directory_url}")
                found_sensitive_directories.append(directory_url)
        except requests.ConnectionError:
            pass

    if not found_sensitive_directories:
        print("No sensitive directories found.")
    return found_sensitive_directories

# JS File Scraping
def scrape_js_files(url):
    if not url.startswith("http://") and not url.startswith("https://"):
        url = "http://" + url

    print("\n--- Scraping JavaScript Files ---")
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            scripts = soup.find_all('script', src=True)
            js_urls = [script['src'] for script in scripts if script['src'].endswith('.js')]

            for js_url in js_urls:
                if not js_url.startswith("http"):
                    js_url = url + js_url
                print(f"Found JavaScript file: {js_url}")

                try:
                    js_response = requests.get(js_url)
                    hidden_params = re.findall(r'[?&](\w+)=', js_response.text)
                    if hidden_params:
                        print(f"Hidden parameters in {js_url}: {set(hidden_params)}")
                except requests.RequestException:
                    print(f"Could not scrape {js_url}")
        else:
            print(f"Failed to retrieve {url} - Status code: {response.status_code}")
    except requests.RequestException as e:
        print(f"An error occurred: {e}")

# CMS Detection
def detect_cms(url):
    if not url.startswith("http://") and not url.startswith("https://"):
        url = "http://" + url

    print("\n--- Detecting CMS ---")
    try:
        response = requests.get(url)
        if "wp-content" in response.text or "wordpress" in response.headers.get('X-Powered-By', '').lower():
            print("Detected CMS: WordPress")
        elif "drupal" in response.text or "drupal" in response.headers.get('X-Generator', '').lower():
            print("Detected CMS: Drupal")
        elif "Joomla" in response.text or "joomla" in response.headers.get('X-Content-Managed-By', '').lower():
            print("Detected CMS: Joomla")
        else:
            print("CMS not detected.")
    except requests.RequestException as e:
        print(f"An error occurred: {e}")

# Error Message Scanning
def scan_error_messages(url):
    error_triggers = ['', "'", '"', '<>', '<script>']
    print("\n--- Scanning for Error Messages ---")
    for trigger in error_triggers:
        try:
            response = requests.get(f"{url}?test={trigger}")
            if "error" in response.text.lower() or "exception" in response.text.lower():
                print(f"Potential error message found with trigger '{trigger}': {response.url}")
        except requests.RequestException as e:
            print(f"An error occurred: {e}")

# URL ইনপুট নিন
url = input("Enter the URL (e.g., example.com or https://example.com): ")

# সকল ফাংশন চালনা
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
brute_force_directories(url)
scrape_js_files(url)
detect_cms(url)
scan_error_messages(url)
