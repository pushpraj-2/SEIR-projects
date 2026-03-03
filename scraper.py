import sys
import requests
from bs4 import BeautifulSoup

def fetch_page(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except Exception as e:
        print("Error fetching page:", e)
        sys.exit(1)

def extract_data(html, base_url):
    soup = BeautifulSoup(html, "html.parser")

    # Extract Title
    title = soup.title.string.strip() if soup.title else "No Title Found"

    # Extract Body Text
    body = soup.body.get_text(separator="\n", strip=True) if soup.body else "No Body Found"

    # Extract All URLs
    links = []
    for link in soup.find_all("a"):
        href = link.get("href")
        if href:
            links.append(href)

    return title, body, links

def main():
    if len(sys.argv) != 2:
        print("Usage: python web_scraper.py <URL>")
        sys.exit(1)

    url = sys.argv[1]

    html = fetch_page(url)
    title, body, links = extract_data(html, url)

    # Output
    print(title)
    print(body)

    for link in links:
        print(link)

if __name__ == "__main__":

    main()
