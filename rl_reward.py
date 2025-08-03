import re

def extract_score(text, metric):
    match = re.search(rf"{metric}.*?(\d+)/?10?", text, re.IGNORECASE)
    return int(match.group(1)) if match else 0

def compute_reward(review_text):
    fluency = extract_score(review_text, "Fluency")
    creativity = extract_score(review_text, "Creativity")
    faithfulness = extract_score(review_text, "Faithfulness")
    return round((fluency + creativity + faithfulness) / 3, 2)