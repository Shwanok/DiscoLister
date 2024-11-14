import os
import requests
from bs4 import BeautifulSoup
import socket
import subprocess
import re

# আউটপুট সংরক্ষণের জন্য ফোল্ডার তৈরি করা
def create_output_directory(domain):
    base_dir = f"/home/kali/DiscoLister/{domain}/recon"
    os.makedirs(base_dir, exist_ok=True)
    return base_dir

# আউটপুট লেখার জন্য ফাংশন
def write_to_file(file_path, content):
    with open(file_path, 'a') as file:
        file.write(content + '\n')

# পেজের টাইটেল খুঁজে বের করা
def get_page_title(url, output_dir):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            title = soup.title.string
            write_to_file(f"{output_dir}/page_title.txt", f"Page Title: {title}")
            print(f"Page Title: {title}")
        else:
            print(f"Failed to retrieve {url} - Status code: {response.status_code}")
    except requests.RequestException as e:
        print(f"An error occurred: {e}")

# HTTP হেডার সংগ্রহ করা
def get_http_headers(url, output_dir):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            headers = response.headers
            header_content = "\n".join([f"{key}: {value}" for key, value in headers.items()])
            write_to_file(f"{output_dir}/http_headers.txt", header_content)
            print("HTTP Headers collected.")
        else:
            print(f"Failed to retrieve {url} - Status code: {response.status_code}")
    except requests.RequestException as e:
        print(f"An error occurred while fetching headers: {e}")

# Assetfinder দিয়ে সাবডোমেইন এনুমারেশন
def enumerate_subdomains(domain, output_dir):
    print("\n--- Enumerating Subdomains (using Assetfinder) ---")
    try:
        result = subprocess.run(['assetfinder', '--subs-only', domain], capture_output=True, text=True)
        write_to_file(f"{output_dir}/alive-subdomains.txt", result.stdout)
        print("Subdomains saved to alive-subdomains.txt.")
    except Exception as e:
        print(f"Assetfinder not found or an error occurred: {e}")

# Naabu দিয়ে পোর্ট স্ক্যানিং
def scan_open_ports(domain, output_dir):
    print("\n--- Scanning Open Ports (using Naabu) ---")
    try:
        result = subprocess.run(['naabu', '-host', domain], capture_output=True, text=True)
        write_to_file(f"{output_dir}/alive-hosts.txt", result.stdout)
        print("Open ports saved to alive-hosts.txt.")
    except Exception as e:
        print(f"Naabu not found or an error occurred: {e}")

# HTTPX দিয়ে HTTP প্রোবিং
def probe_http(domain, output_dir):
    print("\n--- Probing HTTP Endpoints (using HTTPX) ---")
    try:
        result = subprocess.run(['httpx', '-silent', '-status-code', '-title', '-content-length', '-u', domain], capture_output=True, text=True)
        write_to_file(f"{output_dir}/alive-hosts.txt", result.stdout)
        print("HTTP probes saved to alive-hosts.txt.")
    except Exception as e:
        print(f"HTTPX not found or an error occurred: {e}")

# Waybackurls দিয়ে পুরানো URL সংগ্রহ
def fetch_wayback_urls(domain, output_dir):
    print("\n--- Fetching URLs from Wayback Machine (using waybackurls) ---")
    try:
        result = subprocess.run(['waybackurls', domain], capture_output=True, text=True)
        write_to_file(f"{output_dir}/uniq-wayback-urls.txt", result.stdout)
        print("Wayback URLs saved to uniq-wayback-urls.txt.")
    except Exception as e:
        print(f"waybackurls not found or an error occurred: {e}")

# GF দিয়ে বিভিন্ন প্যারামিটার ফিল্টার করা
def filter_with_gf(urls, pattern, output_file):
    print(f"\n--- Filtering URLs with GF (pattern: {pattern}) ---")
    try:
        result = subprocess.run(['gf', pattern], input=urls, capture_output=True, text=True)
        write_to_file(output_file, result.stdout)
        print(f"Filtered parameters saved to {output_file}.")
    except Exception as e:
        print(f"GF not found or an error occurred: {e}")

# Nuclei দিয়ে Vulnerability স্ক্যান
def run_nuclei_scan(domain, output_dir):
    print("\n--- Running Vulnerability Scan (using Nuclei) ---")
    try:
        result = subprocess.run(['nuclei', '-u', domain], capture_output=True, text=True)
        write_to_file(f"{output_dir}/nuclei_report.txt", result.stdout)
        print("Nuclei scan results saved to nuclei_report.txt.")
    except Exception as e:
        print(f"Nuclei not found or an error occurred: {e}")

# SQL Injection Test (sqlmap ব্যবহার করে)
def sql_injection_test(url):
    print("\n--- Testing for SQL Injection (using sqlmap) ---")
    try:
        result = subprocess.run(['sqlmap', '-u', url, '--batch', '--level=2'], capture_output=True, text=True)
        print(result.stdout)
    except Exception as e:
        print(f"sqlmap not found or an error occurred: {e}")

# ব্যানার গ্র্যাবিং (socket দিয়ে)
def grab_banner(domain, port):
    print(f"\n--- Grabbing Banner for {domain} on Port {port} ---")
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)
        sock.connect((domain, port))
        banner = sock.recv(1024).decode().strip()
        print(f"Banner on Port {port}: {banner}")
    except Exception as e:
        print(f"Could not retrieve banner on Port {port}: {e}")
    finally:
        sock.close()

# ফাংশন চালানোর আগে আউটপুট ফোল্ডার তৈরি করা
url = input("Enter the URL (e.g., example.com or https://example.com): ")
domain = url.replace("https://", "").replace("http://", "")
output_dir = create_output_directory(domain)

# ফাংশনগুলো চালানো
print("\nStarting DiscoLister with automated file output...")
get_page_title(url, output_dir)
get_http_headers(url, output_dir)
enumerate_subdomains(domain, output_dir)
scan_open_ports(domain, output_dir)
probe_http(domain, output_dir)
fetch_wayback_urls(domain, output_dir)

# GF প্যাটার্ন অনুযায়ী ফিল্টার করা
wayback_urls_file = f"{output_dir}/uniq-wayback-urls.txt"
try:
    with open(wayback_urls_file, 'r') as file:
        wayback_urls = file.read()
        filter_with_gf(wayback_urls, "sqli", f"{output_dir}/sqli_params.txt")
        filter_with_gf(wayback_urls, "xss", f"{output_dir}/xss_params.txt")
        filter_with_gf(wayback_urls, "ssrf", f"{output_dir}/ssrf_params.txt")
        filter_with_gf(wayback_urls, "lfi", f"{output_dir}/lfi_params.txt")
        filter_with_gf(wayback_urls, "rce", f"{output_dir}/rce_params.txt")
        filter_with_gf(wayback_urls, "idor", f"{output_dir}/idor_params.txt")
        filter_with_gf(wayback_urls, "debug-logic", f"{output_dir}/debug_logic_params.txt")
except FileNotFoundError:
    print(f"{wayback_urls_file} not found. Please ensure waybackurls has run successfully.")

run_nuclei_scan(domain, output_dir)
sql_injection_test(url)
print("\nDiscoLister scan complete.")
