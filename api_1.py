@app.route("/ask",methods=["POST"]
def ask():
    data = request.get_json()
    question = data["question"]
    knowledge_base=data["knowledge_base"]
     
    answer={
   
  "success": True,
  "answer": "Start with images, containers and Dockerfiles..."
  "knowledge_base"=knowledge_base
}

return jsonify(answer)
