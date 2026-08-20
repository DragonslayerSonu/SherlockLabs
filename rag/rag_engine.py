from pathlib import Path

from ollama import chat
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


DOCUMENT_PATH = Path(__file__).parent / "documents" / "docker_basics.txt"
MINIMUM_SCORE = 0.15
TOP_K = 3
MODEL_NAME = "qwen3.5:4b"


# Prepare the knowledge base once when this module is imported.
document = DOCUMENT_PATH.read_text(encoding="utf-8")

chunks = [
    paragraph.strip()
    for paragraph in document.split("\n\n")
    if paragraph.strip()
]

vectorizer = TfidfVectorizer(stop_words="english")
chunk_vectors = vectorizer.fit_transform(chunks)


def answer_question(question):
    """Retrieve relevant context for a question."""

    # Convert the question using the knowledge-base vocabulary.
    question_vector = vectorizer.transform([question])

    # Calculate one similarity score for every chunk.
    scores = cosine_similarity(question_vector, chunk_vectors)[0]
    best_score = scores.max()

    # Return normally when nothing passes the relevance gate.
    if best_score < MINIMUM_SCORE:
        return {
            "question": question,
            "answer": "I could not find relevant information in the knowledge base.",
            "sources": []
        }

    # Rank chunks and keep only strong top-k results.
    ranked_indices = scores.argsort()[::-1]

    top_indices = [
        index
        for index in ranked_indices[:TOP_K]
        if scores[index] >= MINIMUM_SCORE
    ]

    # Combine the accepted chunks into one context string.
    retrieved_chunks = [chunks[index] for index in top_indices]
    context = "\n\n".join(retrieved_chunks)

    # Build structured source information for an API.
    sources = [
        {
            "document": DOCUMENT_PATH.name,
            "chunk": int(index) + 1,
            "similarity": round(float(scores[index]), 3)
        }
        for index in top_indices
    ]
# Build the grounded prompt for the local LLM.
    # Build the grounded prompt for the local LLM.
    prompt = f"""
Answer the question using only the context below.
Do not use outside knowledge.
If the context does not contain the answer, say that clearly.

Context:
{context}

Question:
{question}

Answer:
""".strip()

    # Send the prompt to Qwen through the local Ollama server.
    response = chat(
        model=MODEL_NAME,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        think=False
    )

    generated_answer = response.message.content.strip()

    return {
        "question": question,
        "answer": generated_answer,
        "sources": sources
    }