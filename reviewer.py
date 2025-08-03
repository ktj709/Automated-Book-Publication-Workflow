import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

def review_chapter(original, rewritten):
    prompt = f"""
You are an expert book editor. Review the rewritten chapter based on the original below.
Give scores (1–10) for Fluency, Creativity, and Faithfulness to Original.
Conclude with either 'Accept' or 'Needs Improvement'.

Original:
{original}

Rewritten:
{rewritten}
"""
    response = model.generate_content(prompt)
    return response.text.strip()
