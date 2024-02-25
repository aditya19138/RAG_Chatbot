import pinecone
import langchain.vectorstores
from pinecone import Pinecone,ServerlessSpec,PodSpec
from services.openai_service import get_embeddings
import os
from dotenv import load_dotenv
load_dotenv()
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

# PINECONE_API_KEY = os.environ.get('PINECONE_API_KEY')
pc = Pinecone(api_key=os.environ['PINECONE_API_KEY'])
embeddings = get_embeddings()
EMBEDDING_DIMENSION = 1536

def embed_chunks_and_upload_to_pinecone(chunks, index_name):
    if index_name in pc.list_indexes().names():
        print("\nIndex already exists. Deleting index ...")
        pc.delete_index(name=index_name)
    
    print("\nCreating a new index: ", index_name)
    pc.create_index(
            name=index_name, 
            dimension=1536,
            metric="cosine",
            spec=PodSpec(
                environment="gcp-starter"
        )
    )

    index = pc.Index(index_name)
    
    print("\nEmbedding chunks using OpenAI ...")

    
    langchain.vectorstores.Pinecone.from_texts(chunks,embeddings, index_name = index_name)
    # embeddings = get_embedding(chunks)
    # print(pc.describe_index("vector"))
    
        
    # index = pinecone.Index(index_name)        
    # return index

    print(f"\nUploaded ${len(chunks)} chunks to Pinecone index\n'{index_name}'.")


def get_most_similar_chunks_for_query(query, index_name):

    ## initialize the vector store
    index = pc.Index(index_name)
    vector_store = langchain.vectorstores.Pinecone(index,embeddings,"text")
    matching_chunks = vector_store.similarity_search(query,k=3)
    # print(matching_chunks)
    
    context = "\n\n---\n\n".join([x.page_content for x in matching_chunks])
    # print(context)
    return context


# def delete_index(index_name):
#   if index_name in pc.list_indexes():
#     print("\nDeleting index ...")
#     pc.delete_index(name=index_name)
#     print(f"Index {index_name} deleted successfully")
#   else:
#      print("\nNo index to delete!")