from os import environ
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.core.settings import Settings
from llama_index.vector_stores.mongodb import MongoDBAtlasVectorSearch
from llama_index.core import VectorStoreIndex, StorageContext
import pymongo
import streamlit as st
from openai import OpenAI as OpenAIClient

OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
MONGO_URI = st.secrets["MONGO_URI"]
DB_NAME = "itdata"
COLLECTION_NAME = "it_support_data"

openAIClient = OpenAIClient(api_key=OPENAI_API_KEY)
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
vector_store = MongoDBAtlasVectorSearch(
    mongo_client,
    db_name=DB_NAME,
    collection_name=COLLECTION_NAME,
    index_name="vector_index",
)
storage_context = StorageContext.from_defaults(vector_store=vector_store)
index = VectorStoreIndex.from_documents([], storage_context=storage_context)
query_engine = index.as_query_engine(similarity_top_k=3)


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

    if len(results) == 0:
        return "Sorry, I don't have an answer for that question."
    return results


def getSummarizedAnswer(question):
    response = query_engine.query(question)
    summary = response.response
    sources = response.source_nodes

    sourcesData = []
    for item in sources:

        ticket_number = item.metadata["ticket-number"].strip('"')
        text = item.text
        score = item.score
        sourceData = {"ticket-number": ticket_number, "text": text, "score": score}
        sourcesData.append(sourceData)

    result = {"summary": summary, "sources": sourcesData}
    return result


def getSummarizedAnswerGPT4(question):
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

    fullanswer = "Top 3 results: \n"
    sourcesData = []

    i = 0
    for document in results:
        i += 1
        metadata = document["metadata"]
        ticket_number = metadata.get("ticket-number", "N/A")
        text = document["text"]

        fullanswer += "#" + str(i) + ": " + text + "\n"
        sourceData = {"ticket-number": ticket_number, "text": text, "score": -1}
        sourcesData.append(sourceData)

    input = question + "this is the raw answer use it in your response, Answer in max 5 sentences structure your response for readability" + fullanswer
    response = openAIClient.chat.completions.create(
        model="gpt-4-turbo",
        messages=[
            {
                "role": "system",
                "content": """You are a helpful assistant for Boston University IT Support, mention this when greeted.
             Your role is to answer questions about Bu Login, Blackboard and other IT related issues.""",
            },
            {"role": "user", "content": input},
        ],
    )

    summary = response.choices[0].message.content
    result = {"summary": summary, "sources": sourcesData}
    return result


# query = "How to get BU account?"
# print(getSummarizedAnswerGPT4(query))
