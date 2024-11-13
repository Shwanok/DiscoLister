# DiscoLister.py ফাইল তৈরি করুন
import requests
from bs4 import BeautifulSoup

def get_page_title(url):
    try:
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

# URL ইনপুট নিন
url = input("Enter the URL (e.g., https://example.com): ")
title = get_page_title(url)

if title:
    print(f"Page Title: {title}")
else:
    print("Could not retrieve the page title.")
