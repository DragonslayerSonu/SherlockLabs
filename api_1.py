from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/ask", methods=["POST"])
def ask():

    data = request.get_json()

    question = data["question"]
    knowledge_base = data["knowledge_base"]

    if "docker" in question.lower():
        generated_answer = "Start with images, containers, volumes, networks, and Dockerfiles."
    elif "python" in question.lower():
        generated_answer = "Start with variables, conditions, loops, functions, collections, and classes."
    else:
        generated_answer = "I do not have an answer for that topic yet."

    return jsonify({
        "success": True,
        "question": question,
        "knowledge_base": knowledge_base,
        "answer": generated_answer
    })

if __name__ == "__main__":
    app.run(debug=True)