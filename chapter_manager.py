from scraper import scrape_chapter
from ai_writer import rewrite_chapter
from reviewer import review_chapter
from rl_reward import compute_reward
from utils import save_output, take_screenshot

def process_chapter(url):
    print(f"\n🔍 Scraping chapter from: {url}")
    original_text = scrape_chapter(url)

    print("\n✍️ Rewriting the chapter using AI...")
    rewritten_text = rewrite_chapter(original_text)

    print("\n🧑‍💻 HUMAN-IN-THE-LOOP:")
    edit_decision = input("Do you want to manually edit the rewritten chapter? (yes/no): ").strip().lower()
    if edit_decision == "yes":
        print("\nPaste your revised chapter (or press Enter to keep AI version):")
        manual_input = input()
        if manual_input.strip():
            rewritten_text = manual_input

    print("\n🕵️ Reviewing the rewritten version...")
    review_result = review_chapter(original_text, rewritten_text)

    print("\n✅ Chapter Processing Complete!")
    print("\n--- Original (Preview) ---")
    print(original_text[:500], "...\n")
    print("--- Rewritten (Preview) ---")
    print(rewritten_text[:500], "...\n")
    print("--- Review Summary ---")
    print(review_result)

    reward_score = compute_reward(review_result)
    print(f"\n🏆 RL-Based Reward Score: {reward_score}/10")

    save_output(original_text, rewritten_text, review_result)
    take_screenshot(url, "screenshots/chapter1.png")

    return {
        "original": original_text,
        "rewritten": rewritten_text,
        "review": review_result,
        "reward": reward_score
    }

if __name__ == "__main__":
    url = input("📘 Enter Wikisource Chapter URL: ").strip()
    process_chapter(url)