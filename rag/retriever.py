from pathlib import Path

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# Read the knowledge-base document.
document = Path("documents/docker_basics.txt").read_text(encoding="utf-8")

# Each paragraph becomes one searchable chunk.
chunks = [
    paragraph.strip()
    for paragraph in document.split("\n\n")
    if paragraph.strip()
]

# Learn the important words and convert every chunk into numbers.
vectorizer = TfidfVectorizer(stop_words="english")
chunk_vectors = vectorizer.fit_transform(chunks)

# Ask the user for a question and convert it using the same vocabulary.
question = input("Ask a question: ")
question_vector = vectorizer.transform([question])

# Compare the question with every chunk.
scores = cosine_similarity(question_vector, chunk_vectors)[0]

# Select the chunk with the highest similarity score.
best_index = scores.argmax()

print("\nMost relevant chunk:")
print(chunks[best_index])
print(f"\nSimilarity score: {scores[best_index]:.3f}")
