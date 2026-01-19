import pickle
import os

# Define paths relative to this file to prevent FileNotFoundError
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "model", "spam_model.pkl")
VEC_PATH = os.path.join(BASE_DIR, "model", "vectorizer.pkl")

# Load models safely
try:
    with open(VEC_PATH, "rb") as f:
        vectorizer = pickle.load(f)
    with open(MODEL_PATH, "rb") as f:
        model = pickle.load(f)
except FileNotFoundError as e:
    print(f"❌ Error: Could not find model files. Expected at: {e.filename}")
    exit(1)

def spam_probability(text):
    """
    Returns probability of text being spam (0.0 to 1.0).
    Matches TfidfVectorizer defaults (lowercase=True).
    """
    if not text or not isinstance(text, str):
        return 0.0

    # TfidfVectorizer handles lowercasing and tokenization internally.
    # We pass the raw text directly to match training data.
    try:
        vec = vectorizer.transform([text])
        return model.predict_proba(vec)[0][1]
    except Exception as e:
        print(f"Error processing text: {e}")
        return 0.0