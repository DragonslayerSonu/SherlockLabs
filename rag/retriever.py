from rag_engine import answer_question


# Ask through the terminal interface.
question = input("Ask a question: ")

# Send the question to the reusable RAG engine.
result = answer_question(question)

print("\nAnswer:")
print(result["answer"])

# Display sources only when the engine returned some.
if result["sources"]:
    print("\nSources:")

    for source in result["sources"]:
        print(
            f'- {source["document"]}, '
            f'Chunk {source["chunk"]} '
            f'(similarity: {source["similarity"]:.3f})'
        )