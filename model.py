import requests
import re
import time


TMDB_API_KEY = '51a1ca44f8c6ef491bf3a026fa607b48'


TMDB_GENRE_MAP = {
    'happy': [35, 10751],      
    'sad': [18, 10749],         
    'action': [28, 12],        
    'thriller': [53, 9648],    
    'horror': [27],            
    'sci-fi': [878]            
}


MOOD_KEYWORDS = {
    'happy': ['happy', 'fun', 'laugh', 'excited', 'joy', 'cheerful', 'positive', 'smile', 'comedy'],
    'sad': ['sad', 'depressed', 'cry', 'emotional', 'lonely', 'heartbroken', 'tears', 'sorrow'],
    'action': ['adventure', 'thrill', 'fast', 'explosion', 'intense', 'fight', 'high speed', 'adrenaline'],
    'thriller': ['mystery', 'suspense', 'intense', 'dark', 'twist', 'investigation', 'crime'],
    'horror': ['scary', 'horror', 'creepy', 'ghost', 'kill', 'haunted', 'fear', 'nightmare'],
    'sci-fi': ['space', 'future', 'sci-fi', 'technology', 'robot', 'time travel', 'aliens']
}


def infer_mood_from_text(text):
    text = text.lower()
    mood_score = {}

    for mood, keywords in MOOD_KEYWORDS.items():
        mood_score[mood] = 0
        for word in keywords:
            if re.search(r'\b' + re.escape(word) + r'\b', text):
                mood_score[mood] += 1


    best_mood = max(mood_score, key=mood_score.get)

    if mood_score[best_mood] == 0:
        print("⚠️ No clear mood found. Using default: happy")
        return 'happy'  # fallback
    else:
        print(f"✅ Inferred Mood: {best_mood} (score: {mood_score[best_mood]})")
        return best_mood


def get_movies_by_mood(mood):
    genre_ids = TMDB_GENRE_MAP.get(mood.lower())
    if not genre_ids:
        print(f"⚠️ No genre mapping for mood: {mood}")
        return []

    genre_str = ",".join(map(str, genre_ids))
    url = "https://api.themoviedb.org/3/discover/movie"
    params = {
        'api_key': TMDB_API_KEY,
        'with_genres': genre_str,
        'sort_by': 'popularity.desc',
        'page': 1
    }

    for attempt in range(5):  # Retry logic
        try:
            response = requests.get(url, params=params, timeout=5)
            response.raise_for_status()
            print(f"✅ TMDB API Success (Attempt {attempt+1})")
            return response.json().get('results', [])
        except requests.exceptions.RequestException as e:
            print(f"⏳ TMDB API Error [Attempt {attempt+1}]: {e}")
            time.sleep(1.5)

    print("❌ All TMDB API attempts failed.")
    return []
