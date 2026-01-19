from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import pickle

with open("data/spam.txt") as f:
    spam = f.readlines()

with open("data/ham.txt") as f:
    ham = f.readlines()

X = spam + ham
y = [1]*len(spam) + [0]*len(ham)

vectorizer = TfidfVectorizer(stop_words="english")
X_vec = vectorizer.fit_transform(X)

model = LogisticRegression()
model.fit(X_vec, y)

pickle.dump(vectorizer, open("model/vectorizer.pkl", "wb"))
pickle.dump(model, open("model/spam_model.pkl", "wb"))

print("Model trained & saved")