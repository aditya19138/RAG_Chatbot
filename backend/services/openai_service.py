import requests
import json
import os
from utils.helper_functions import build_prompt, construct_messages_list
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv
load_dotenv()

OPENAI_API_KEY = os.environ['OPENAI_API_KEY']
OPENAI_EMBEDDING_MODEL = 'text-embedding-ada-002'
CHATGPT_MODEL = 'gpt-3.5-turbo'

def get_embeddings():
    embedding = OpenAIEmbeddings(api_key=OPENAI_API_KEY, model=OPENAI_EMBEDDING_MODEL)
    # embeddings = embedding.embed_query(chunk)
    return embedding

def construct_llm_payload(question, context, chat_history):
  prompt = build_prompt(question, context)
  print("\n==== PROMPT ====\n")
  print(prompt)

  messages = construct_messages_list(chat_history, prompt)

#   print("\n==== Messages ====\n")
#   print(messages)

  headers = {
      'content-type': 'application/json; charset=utf-8',
      'Authorization': f"Bearer {OPENAI_API_KEY}"            
  }  

  data = {
      'model': CHATGPT_MODEL,
      'messages': messages,
      'temperature': 1, 
      'max_tokens': 1000,
      'stream': True
  }

  return headers, data
#   return "",""

