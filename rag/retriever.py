import sys

from pathlib import Path

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from ollama import chat


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
# Stop retrieval when even the best chunk is not relevant enough.
minimum_score=0.15
best_score=scores.max()
if best_score < minimum_score:
   print("\nI could not find relevant information in the knowledge base.")
   sys.exit(0)
# Rank all chunks from highest similarity to lowest.
top_k = 3
ranked_indices = scores.argsort()[::-1]
# Keep up to three chunks, but only if they pass the threshold.
top_indices = [
    index
    for index in ranked_indices[:top_k]
    if scores[index] >= minimum_score
]
# Collect the actual text of the selected chunks.
retrieved_chunks = [chunks[index] for index in top_indices]

# Join the selected chunks into one context string.
context = "\n\n".join(retrieved_chunks)
# Build the complete instruction package for the future LLM.
prompt = f"""
Answer the question using only the context below.

Context:
{context}

Question:
{question}

Answer:
""".strip()
print(f"\nTop {top_k} relevant chunks:")

for rank, index in enumerate(top_indices, start=1):
    print(f"\nRank {rank}")
    print(chunks[index])
    print(f"Similarity score: {scores[index]:.3f}")
print("\nCombined context:")
print(context)
print("\nFinal prompt for the future LLM:")
print(prompt)
# Send the completed prompt to the local Qwen model.
response = chat(
    model="qwen3.5:4b",
    messages=[
        {
            "role": "user",
            "content": prompt
        }
    ],
    think=False
)

# Extract and display only the model's final answer.
generated_answer = response.message.content

print("\nGenerated answer:")
print(generated_answer)

print("\nSources:")

for index in top_indices:
    print(f"- Chunk {index + 1} (similarity: {scores[index]:.3f})")
