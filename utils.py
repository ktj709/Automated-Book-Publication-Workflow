import os
from datetime import datetime
from playwright.sync_api import sync_playwright
import asyncio
import sys
import re

if sys.platform.startswith('win'):
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())


os.makedirs("screenshots", exist_ok=True)
os.makedirs("outputs", exist_ok=True)

def clean_review_text(text):
    """
    Removes markdown symbols and extra whitespace from review text.
    """
    # Remove markdown-like characters
    text = re.sub(r"[#*`_>\-]+", "", text)
    # Normalize spacing
    text = re.sub(r"\s+", " ", text).strip()
    # Reintroduce newlines after punctuation where appropriate
    text = re.sub(r"(?<=[.!?])\s+(?=[A-Z])", "\n\n", text)
    return text

def save_output(original, rewritten, review):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    with open(f"outputs/original_{timestamp}.txt", "w", encoding="utf-8") as f:
        f.write(original)
    with open(f"outputs/rewritten_{timestamp}.txt", "w", encoding="utf-8") as f:
        f.write(rewritten)
    with open(f"outputs/review_{timestamp}.txt", "w", encoding="utf-8") as f:
        f.write(review)

def take_screenshot(url, path):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(url)
        page.screenshot(path=path)
        browser.close()
