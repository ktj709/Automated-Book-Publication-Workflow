from scraper import scrape_chapter
from ai_writer import rewrite_chapter
from reviewer import review_chapter
from rl_reward import compute_reward
from utils import save_output, take_screenshot
from chroma_manager import add_to_chroma, search_similar, get_next_version
from voice_support import speak_text
from datetime import datetime

# ────────────────────────
# 📦 AGENTS
# ────────────────────────

def ScraperAgent(url):
    print(f"\n🔍 Scraping chapter from: {url}")
    return scrape_chapter(url)

def WriterAgent(original_text):
    print("\n✍️ Rewriting the chapter using AI...")
    return rewrite_chapter(original_text)

def HumanEditorAgent(rewritten_text):
    print("\n🧑‍💻 HUMAN-IN-THE-LOOP:")
    edit = input("Do you want to manually edit the rewritten chapter? (yes/no): ").strip().lower()
    if edit == "yes":
        print("\nPaste your revised chapter (or press Enter to keep AI version):")
        user_input = input()
        if user_input.strip():
            return user_input
    return rewritten_text

def ReviewerAgent(original, rewritten):
    print("\n🕵️ Reviewing the rewritten version...")
    return review_chapter(original, rewritten)

def RewardAgent(review_text):
    score = compute_reward(review_text)
    print(f"\n🏆 RL-Based Reward Score: {score}/10")
    return score

def VoiceAgent(text):
    speak = input("\n🔊 Do you want to listen to the rewritten chapter or review? (chapter/review/none): ").strip().lower()
    if speak == "chapter":
        speak_text(text['rewritten'])
    elif speak == "review":
        speak_text(text['review'])

def ChromaAgent(rewritten_text, url, reward_score):
    timestamp = datetime.now().isoformat()
    version = get_next_version(url)
    metadata = {
        "url": url,
        "reward_score": reward_score,
        "timestamp": timestamp,
        "version": version
    }
    add_to_chroma(rewritten_text, metadata)

def SmartSearchAgent():
    search_decision = input("\n🔍 Do you want to search for similar chapters? (yes/no): ").strip().lower()
    if search_decision == "yes":
        query = input("Enter your search query: ")
        results = search_similar(query)
        print("\n📚 Top Similar Results:\n")
        for idx, res in enumerate(results, 1):
            print(f"🔹 Result {idx}")
            print("Metadata:", res["metadata"])
            print("Preview:", res["text"][:300], "\n---\n")

# ────────────────────────
# 🚀 EXECUTION PIPELINE
# ────────────────────────

def run_pipeline():
    url = input("📘 Enter Wikisource Chapter URL: ").strip()

    original = ScraperAgent(url)
    rewritten = WriterAgent(original)
    rewritten = HumanEditorAgent(rewritten)
    review = ReviewerAgent(original, rewritten)
    reward_score = RewardAgent(review)

    print("\n✅ Chapter Processing Complete!\n")
    print("--- Original Preview ---")
    print(original[:500], "...\n")
    print("--- Rewritten Preview ---")
    print(rewritten[:500], "...\n")
    print("--- Review Summary ---")
    print(review)

    save_output(original, rewritten, review)
    take_screenshot(url, "screenshots/chapter1.png")
    ChromaAgent(rewritten, url, reward_score)
    VoiceAgent({"rewritten": rewritten, "review": review})
    SmartSearchAgent()

# ────────────────────────
# 🧠 ENTRY POINT
# ────────────────────────

if __name__ == "__main__":
    run_pipeline()
