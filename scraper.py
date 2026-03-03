import sys
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def fetch_page(url):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0"
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return response.text
    except Exception as e:
        print("Error fetching page:", e)
        sys.exit(1)

def extract_data(html, base_url):
    soup = BeautifulSoup(html, "html.parser")

    # Extract Title 
    title = soup.title.get_text(strip=True) if soup.title else "No Title Found"

    # Extract Body Text
    body = soup.body.get_text(separator="\n", strip=True) if soup.body else "No Body Found"

    # Extract All URLs 
    links = set()
    for link in soup.find_all("a", href=True):
        full_url = urljoin(base_url, link["href"])
        links.add(full_url)

    return title, body, list(links)

def main():
    if len(sys.argv) == 2:
        url = sys.argv[1]
    else:
        url = input("Enter Website URL: ")

    html = fetch_page(url)
    title, body, links = extract_data(html, url)

    # Output
    print("\nTitle:\n", title)
    print("\nBody:\n", body)

    print("\nLinks:")
    for link in links:
        print(link)

if __name__ == "__main__":
    main()
