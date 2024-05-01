from os import environ
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.core.settings import Settings
import pymongo
import streamlit as st

OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
MONGO_URI = st.secrets["MONGO_URI"]
DB_NAME = "itdata"
COLLECTION_NAME = "it_support_data"

embed_model = OpenAIEmbedding(model="text-embedding-3-small", dimensions=256)
llm = OpenAI()
Settings.llm = llm
Settings.embed_model = embed_model


if not MONGO_URI:
    print("MONGO_URI not set in environment variables")

def get_mongo_client(mongo_uri):
    """Establish connection to the MongoDB."""
    try:
        client = pymongo.MongoClient(mongo_uri)
        print("Connection to MongoDB successful")
        return client
    except pymongo.errors.ConnectionFailure as e:
        print(f"Connection failed: {e}")
        return None

def generate_embedding(text):
    return embed_model.get_text_embedding(text)

mongo_client = get_mongo_client(MONGO_URI)
db = mongo_client[DB_NAME]
collection = db[COLLECTION_NAME]


def getAnswer(question):
    results = collection.aggregate(
        [
            {
                "$vectorSearch": {
                    "queryVector": generate_embedding(question),
                    "path": "embedding",
                    "numCandidates": 100,
                    "limit": 3,
                    "index": "vector_index",
                }
            }
        ]
    )

    results = list(results)

    firstDocText = results[0]['text']
    return firstDocText

# query = "What is blackboard learn?"

