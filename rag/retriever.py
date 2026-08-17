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
# Rank all chunks from highest similarity to lowest.
top_k = 3
ranked_indices = scores.argsort()[::-1]
top_indices = ranked_indices[:top_k]

print(f"\nTop {top_k} relevant chunks:")

for rank, index in enumerate(top_indices, start=1):
    print(f"\nRank {rank}")
    print(chunks[index])
    print(f"Similarity score: {scores[index]:.3f}")
