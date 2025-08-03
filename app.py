import streamlit as st
from scraper import scrape_chapter
from utils import take_screenshot, save_output, clean_review_text
from ai_writer import rewrite_chapter
from reviewer import review_chapter
from rl_reward import compute_reward
from chroma_manager import add_to_chroma, search_similar, get_next_version
from voice_support import speak_text

import os
from datetime import datetime
from PIL import Image

st.set_page_config(page_title="Automated Book Publisher", layout="wide")

st.title("📘 Automated Book Publication Workflow")
st.markdown("End-to-end pipeline from scraping to publishing with human-AI feedback loop and RL-based evaluation.")

url = st.text_input("📥 Enter the chapter URL to process:", value="https://en.wikisource.org/wiki/The_Gates_of_Morning/Book_1/Chapter_1")

# Screenshot step
if st.button("📸 Take Screenshot"):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = f"screenshots/screenshot_{timestamp}.png"
    take_screenshot(url, path)
    st.image(Image.open(path), caption="Captured Screenshot", use_column_width=True)

# Scraping step
if st.button("🔍 Scrape Chapter"):
    original = scrape_chapter(url)
    st.session_state["original"] = original
    st.text_area("📄 Original Text", original, height=300)

# AI Rewrite
if st.button("✍️ AI Rewrite"):
    original = st.session_state.get("original", "")
    rewritten = rewrite_chapter(original)
    st.session_state["rewritten"] = rewritten
    st.text_area("📝 Rewritten by AI", rewritten, height=300)

# AI Review (Cleaned)
if st.button("🧐 AI Review"):
    original = st.session_state.get("original", "")
    rewritten = st.session_state.get("rewritten", "")
    if not original or not rewritten:
        st.warning("⚠️ Please scrape and rewrite the chapter before reviewing.")
    else:
        reviewed = review_chapter(original, rewritten)
        cleaned_review = clean_review_text(reviewed)
        st.session_state["reviewed"] = cleaned_review
        st.text_area("✅ Reviewed Version", cleaned_review, height=300)

# Human-in-the-loop editing
st.markdown("### 🧠 Human Feedback (Optional)")
user_edited = st.text_area("✏️ Edit Reviewed Version", st.session_state.get("reviewed", ""), height=300)

# Re-review after human edit
if st.button("🔁 Re-Review After Human Edit"):
    original = st.session_state.get("original", "")
    if not user_edited.strip():
        st.warning("⚠️ Please provide edited text.")
    else:
        re_reviewed = review_chapter(original, user_edited)
        cleaned_re_review = clean_review_text(re_reviewed)
        st.session_state["reviewed"] = cleaned_re_review
        st.text_area("🔄 Re-Reviewed After Human Edit", cleaned_re_review, height=300)

# RL Reward
if st.button("🏆 Compute RL Reward"):
    reviewed_text = st.session_state.get("reviewed", "")
    if not reviewed_text:
        st.warning("⚠️ Please run the AI Review or Re-Review step first.")
    else:
        reward = compute_reward(reviewed_text)
        st.success(f"📈 RL-Based Reward Score: {reward:.2f}")

# Save to ChromaDB
if st.button("💾 Save Version to ChromaDB"):
    content = user_edited.strip() or st.session_state.get("reviewed", "")
    if not content:
        st.warning("⚠️ Nothing to save. Provide content via review or manual edit.")
    else:
        metadata = {
            "url": url,
            "timestamp": datetime.now().isoformat(),
            "version": get_next_version(url)
        }

        add_to_chroma(content, metadata)

        save_output(
            st.session_state.get("original", ""),
            st.session_state.get("rewritten", ""),
            content
        )

        st.success("✅ Final version saved to ChromaDB and outputs folder.")

# Voice support
if st.button("🔊 Voice Summary"):
    content = user_edited.strip() or st.session_state.get("reviewed", "")
    if not content:
        st.warning("⚠️ Nothing to speak. Provide reviewed or edited text.")
    else:
        speak_text(content)
        st.success("🔈 Played reviewed version via voice agent.")
