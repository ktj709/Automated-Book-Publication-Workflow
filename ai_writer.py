import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

def rewrite_chapter(text):
    prompt = f"Rewrite the following book chapter in a more engaging and modern style:\n\n{text}"
    response = model.generate_content(prompt)
    return response.text.strip()