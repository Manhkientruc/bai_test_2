from typing import Dict
import re
from textblob import TextBlob

def analyze_transcript(transcript: str) -> Dict:
    # Đếm số từ
    words = re.findall(r'\w+', transcript)
    word_count = len(words)

    # Đếm số câu đơn giản (chấm hết câu)
    sentence_count = transcript.count(".") + transcript.count("!") + transcript.count("?")

    # Phân tích cảm xúc (polarity: [-1, 1], subjectivity: [0, 1])
    blob = TextBlob(transcript)
    sentiment = blob.sentiment

    # Gợi ý từ khoá (top 5 từ lặp nhiều nhất)
    word_freq = {}
    for w in words:
        w = w.lower()
        word_freq[w] = word_freq.get(w, 0) + 1
    keywords = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:5]

    return {
        "word_count": word_count,
        "sentence_count": sentence_count,
        "sentiment": {
            "polarity": sentiment.polarity,
            "subjectivity": sentiment.subjectivity
        },
        "top_keywords": keywords
    }