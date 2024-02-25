# Utility functions like chunk_text, build_prompt, etc.
import os 
import PyPDF2
from PyPDF2 import PdfReader

def read_doc(pdf):
    raw_text = ""
    pdf_path = os.path.join(os.path.dirname(__file__), 'docs', pdf)
    print(pdf_path)
    pdfReader = PdfReader(pdf_path)
    for i,page in enumerate(pdfReader.pages):
        content = page.extract_text()
        if content:
            raw_text += content
    return raw_text


def chunk_text(text, chunk_size=800):
    sentences = text.split('. ')
    chunks = []
    current_chunk = ""
    for sentence in sentences:
        if len(current_chunk) + len(sentence) <= chunk_size:
            current_chunk += sentence + '. '
        else:
            chunks.append(current_chunk)
            current_chunk = sentence + '. '
    # Add the last chunk if it's not empty
    if current_chunk:
        chunks.append(current_chunk)

    return chunks

def build_prompt(query, context):
    prompt_start = (
        "Answer the question based on the context below. Don't start your response with the word 'Answer:'"
        "Context:\n"
    )
    prompt_end = (
        f"\n\nQuestion: {query}\nAnswer:"
    )
    prompt = prompt_start + context + prompt_end
    
    return prompt   

def construct_messages_list(chat_history, prompt):
    messages = [{"role": "system", "content": "You are a helpful assistant."}]
    
    # adding the current chat history in messages
    for message in chat_history:
        if message['isBot']:
            messages.append({"role": "assistant", "content": message["text"]})
        else:
            messages.append({"role": "user", "content": message["text"]})
    
    messages.append({"role": "user", "content": prompt})    
    return messages