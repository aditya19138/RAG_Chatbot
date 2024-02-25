# RAG-PDF-Chatbot
*Full-stack RAG-PDF-Chatbot with OpenAI, Flask, React, and Pinecone*
<img width="870" alt="ss2" src="https://github.com/aditya19138/RAG_Chatbot/assets/74404047/5e7a0fde-f125-4af8-a37c-0dc5ff9f2d1f">
<img width="960" alt="ss1" src="https://github.com/aditya19138/RAG_Chatbot/assets/74404047/2524fe60-341e-4d05-a131-958807324565">

This is an application built for the retrieval-augmented generation for document understanding and question answering, integrated within a web applications. It allows a user to input the PDF file and ask questions about the content of that PDF. It demonstrates the use of Retrieval Augmented Generation, OpenAI, and vector databases.

## Architecture
<img width="581" alt="image" src="https://github.com/aditya19138/RAG_Chatbot/assets/74404047/056871d7-c49b-468d-95b3-151a634ddcf1">
## Setup

**Install Python dependencies**

```sh
cd backend
pip install -r requirements.txt
```
**Install React dependencies**
```sh
cd client
npm install
```

**Create .env file**
```sh
OPENAI_API_KEY=<YOUR_API_KEY>
PINECONE_API_KEY=<YOUR_API_KEY>
```

**Start the Flask server**
```sh
cd backend
python run.py
```

**Start the React app**
```sh
cd client
npm start
```
