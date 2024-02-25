import os
from flask import Flask, request, jsonify, Response, stream_with_context, json
from flask_cors import CORS
import requests
import sseclient
from services import openai_service, pinecone_service
from utils.helper_functions import chunk_text, build_prompt, construct_messages_list,read_doc
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
CORS(app)

PINECONE_INDEX_NAME = 'vector-store-pdf'
@app.route("/")
def hello():
    return "Hello, World!"

@app.route('/get-pdfs', methods=['GET'])
def get_pdfs():
    pdf_folder = os.path.join(os.path.dirname(__file__),'utils', 'docs')
    pdfs = [f for f in os.listdir(pdf_folder) if f.endswith('.pdf')]
    return jsonify(pdfs)

@app.route('/embed-and-store', methods=['POST'])
def embed_and_store(): 
    print(request.json)
    pdf = request.json['pdf']
    # url_text = scraping_service.scrape_website(url)
    raw_text = read_doc(pdf)
    chunks = chunk_text(raw_text)
    pinecone_service.embed_chunks_and_upload_to_pinecone(chunks, PINECONE_INDEX_NAME)
    response_json = {
        "message": "Chunks embedded and stored successfully"
    }
    return jsonify(response_json)

@app.route('/handle-query', methods=['POST'])
def handle_query():
    print(request.json)
    question = request.json['question']
    chat_history = request.json['chatHistory']
    
    # Get the most similar chunks from Pinecone
    retrieved_context = pinecone_service.get_most_similar_chunks_for_query(question, PINECONE_INDEX_NAME)
    
    # Build the payload to send to OpenAI
    headers, data = openai_service.construct_llm_payload(question, retrieved_context, chat_history)

    # print("Headers: ", headers)
    # print("Data: ", data)

    # Send to OpenAI's LLM to generate a completion
    def generate():
        url = 'https://api.openai.com/v1/chat/completions'
        response = requests.post(url, headers=headers, data=json.dumps(data), stream=True)
        print(response.json)
        client = sseclient.SSEClient(response)
        for event in client.events():
            print(event.data)
            if event.data != '[DONE]':
                try:
                    text = json.loads(event.data)['choices'][0]['delta']['content']
                    print(text)
                    yield(text)
                except:
                    yield('')
    
    # Return the streamed response from the LLM to the frontend
    return Response(stream_with_context(generate()))


app.run(host='0.0.0.0', port=8080,debug=True)
