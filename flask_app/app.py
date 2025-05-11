from flask import Flask, request, jsonify
from flask_cors import CORS
from utils.search import search_and_retrieve
from utils.process import process_content
from utils.llm import generate_response_with_memory
from dotenv import load_dotenv
import os

import time

app = Flask(__name__)
CORS(app)  # Enable CORS for Streamlit communication
load_dotenv()

@app.route('/query', methods=['POST'])
def handle_query():
    data = request.get_json()
    query = data.get('query')
    session_id = data.get('session_id', 'default')  # For conversational memory

    if not query:
        return jsonify({'error': 'Query is required'}), 400

    try:
        # Step 1: Retrieve web content
        start = time.time()
        web_content = search_and_retrieve(query)
        print(time.time() - start)

        # Step 2: Process content
        start = time.time()
        print("Enter processing state")
        processed_text = process_content(query, web_content)
        print(time.time() - start)
        # print(processed_text)
        # Step 3: Generate response with LLM
        # print(web_content)
        start = time.time()
        response = generate_response_with_memory(query, processed_text, session_id)
        print(time.time() - start)

        print(response)
        return jsonify(response)
        # return web_content
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)