# 📚 Automated Book Publication Workflow

An end-to-end AI-powered system to automate content scraping, rewriting, reviewing, and human-in-the-loop editing with RL-based reward scoring, version control, semantic search, and voice support.

---

## 🚀 Key Features

1. **🔍 Scraping & Screenshots**
   - Extracts clean chapter content from URLs (e.g., Wikisource).
   - Captures webpage screenshots for archival and review.

2. **✍️ AI Writing & Reviewing**
   - Rewrites chapters using LLMs (Gemini/OpenAI/etc.).
   - Automatically reviews rewritten content for quality.

3. **🧑‍💻 Human-in-the-Loop Editing**
   - Option for users to manually edit AI-generated chapters.
   - Seamless flow of iterations between agents and humans.

4. **🏆 RL-Based Reward System**
   - Scores rewritten content using a reward model based on review text.

5. **🧠 Semantic Search + Versioned Storage**
   - Uses ChromaDB to store rewritten content with version and metadata.
   - Allows querying similar chapters using vector search.

6. **🔊 Voice Narration Support**
   - Converts final text into speech using TTS (pyttsx3 or other).

---

## 🗂️ Project Structure

📁 project-root/
├── app.py # Streamlit interface
├── main.py # CLI/Orchestration runner
├── agents.py # AI agents coordination
├── scraper.py # Web scraper
├── ai_writer.py # AI rewriting module
├── reviewer.py # AI-based review module
├── rl_reward.py # Reward scoring system
├── chroma_manager.py # Semantic versioned DB with Chroma
├── voice_support.py # TTS support
├── utils.py # Helper functions (screenshot, save)
├── requirements.txt # Dependencies list
└── README.md # This file

## 🔍 Sample Flow

1. Input a chapter URL.

2. Scrape and screenshot content.

3. Rewrite using AI.

4. Review and score output.

5. Optionally edit manually (Human-in-the-loop).

6. Store in ChromaDB with reward and version.

7. Search or narrate rewritten content.

## 🧠 Tech Stack

Python, Streamlit, Playwright

Gemini 2.5 Flash

ChromaDB (semantic search)

pyttsx3 (voice support)

RL-based scoring (custom)


# Made with ❤️ by Kshitij Saxena ; )