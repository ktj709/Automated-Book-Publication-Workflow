from scraper import scrape_chapter
from ai_writer import rewrite_chapter
from reviewer import review_chapter
from rl_reward import compute_reward
from chroma_manager import add_to_chroma, search_similar
from utils import save_output, take_screenshot
from voice_support import speak_text
from datetime import datetime

class ScraperAgent:
    def run(self, url):
        print(f"\n🔍 Scraping from: {url}")
        return scrape_chapter(url)

class WriterAgent:
    def run(self, text):
        print("\n✍️ Rewriting chapter with AI...")
        return rewrite_chapter(text)

class HumanEditorAgent:
    def run(self, ai_text):
        print("\n🧑‍💻 HUMAN-IN-THE-LOOP:")
        decision = input("Edit the AI version? (yes/no): ").strip().lower()
        if decision == "yes":
            print("Paste your edited version (or press Enter to skip):")
            edited = input()
            if edited.strip():
                return edited
        return ai_text

class ReviewerAgent:
    def run(self, original, rewritten):
        print("\n🕵️ Reviewing the rewritten version...")
        return review_chapter(original, rewritten)

class RewardAgent:
    def run(self, review_text):
        score = compute_reward(review_text)
        print(f"\n🏆 Reward Score: {score}/10")
        return score

class ChromaAgent:
    def store(self, rewritten_text, url, reward_score):
        metadata = {
            "url": url,
            "reward_score": reward_score,
            "timestamp": datetime.now().isoformat(),
            "version": "v1"
        }
        add_to_chroma(rewritten_text, metadata)

    def search(self):
        decision = input("🔍 Search similar chapters? (yes/no): ").strip().lower()
        if decision == "yes":
            query = input("Enter search query: ")
            results = search_similar(query)
            for i, res in enumerate(results, 1):
                print(f"\n🔹 Result {i}")
                print(res["metadata"])
                print(res["text"][:300] + "\n---")

class VoiceAgent:
    def speak(self, text):
        speak_text(text)
