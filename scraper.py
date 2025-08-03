import requests
from bs4 import BeautifulSoup

def scrape_chapter(url):
    """
    Fetches and cleans the main chapter content from a Wikisource URL.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")
        content_div = soup.find("div", {"id": "mw-content-text"})
        if not content_div:
            print("❌ Could not find main content on the page.")
            return ""
        paragraphs = content_div.find_all(["p", "div", "li"])
        text = "\n\n".join(p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True))
        return text.strip()
    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")
        return ""