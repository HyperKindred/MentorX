import requests
from flask import Flask, request, jsonify
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings

embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
db = FAISS.load_local("./end/model/multi_doc_vector_db", embedding_model, allow_dangerous_deserialization=True)
app = Flask(__name__)
OLLAMA_API_URL = 'http://localhost:11434/api/generate'
model_name = 'deepseek-r1:1.5b'
@app.route('/generate', methods=['POST'])
def generate():
    data = request.get_json()
    prompt = data.get('prompt', '')

    if not prompt:
        return jsonify({'error': 'No prompt provided'}), 400
    
    related_docs = db.similarity_search(prompt, k=3)
    context = "\n".join([doc.page_content for doc in related_docs])
    full_prompt = f"""请根据以下课件内容回答问题。
    课件内容：
    {context}
    
    问题：{prompt}
    """
    # 向 Ollama 发请求
    response = requests.post(OLLAMA_API_URL, json={
        'model': model_name,
        'prompt': full_prompt,
        'stream': False
    })

    result = response.json()
    return jsonify({'response': result.get('response', '')})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
