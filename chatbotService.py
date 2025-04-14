from fastapi import FastAPI
from pydantic import BaseModel
import requests
from openai import AzureOpenAI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache
from redis import Redis

app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://www.poison93sc.dev.local"],  # Adjust this to allow your frontend
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Azure OpenAI API Credentials

AZURE_OPENAI_ENDPOINT = "https://sitecoreopenai.openai.azure.com/"
AZURE_OPENAI_KEY = "KEY"
# Sitecore XM Cloud API Credentials
SITECORE_API_URL =  "SITECORE_API_URL"  
SITECORE_API_TOKEN = "TOKEN"

AZURE_OPENAI_API_VERSION = "2024-10-21"

client = AzureOpenAI(
    api_key=AZURE_OPENAI_KEY,
    azure_endpoint=AZURE_OPENAI_ENDPOINT,
    api_version=AZURE_OPENAI_API_VERSION
)

class ChatRequest(BaseModel):
    user_input: str 

@app.on_event("startup")
async def startup():
    redis = Redis(host="localhost", port=6379, db=0)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")

@cache(expire=300)  # Cache for 5 minutes
async def fetch_sitecore_data():
    
     #Sitecore Item Path local: /sitecore/content/SK Sites/Basic Site1/Data/News
    GRAPHQL_QUERY = """
        query {
            item(path: "/sitecore/content/Home/News", language: "en") {
                children {
                    results {
                        id
                        Title: field(name: "Title") { value }
                        Description: field(name: "Description") { value }
                        Author: field(name: "Author") { value }
                        Authenticity: field(name: "Authenticity") { value }
                        Sentiment: field(name: "Sentiment") { value }
                        Category: field(name: "Category") { value }
                    }
                }
            }
        }
    """
    headers = {
        "Authorization": f"Bearer {SITECORE_API_TOKEN}",
        "Content-Type": "application/json"
    }
    response = requests.post(
        SITECORE_API_URL, headers=headers, verify=False, json={"query": GRAPHQL_QUERY}
    )
    #print(response.json())
    return response.json()


@app.post("/chat")
async def chatbot(request: ChatRequest):
    # Fetch relevant content from Sitecore
    sitecore_data = await fetch_sitecore_data()
    user_input = request.user_input
    # Prepare AI prompt
    #print(sitecore_response.json())
    prompt = f"User asked: {user_input}. Use this Sitecore content: {sitecore_data} to answer."

    safe_prompt = f"""
                You are an AI assistant integrated with Sitecore. Please provide helpful, professional, and neutral responses 
                based on the following Sitecore news item content like title, description, category: {sitecore_data}. 
                User question: {user_input}
                """

    # Send request to Azure OpenAI
   
    openai_response = client.chat.completions.create(
        model="gpt-4o",  # Use your Azure OpenAI deployment name
        temperature=1.0,
        top_p=1.0,
        messages=[
            {"role": "system", "content": "You are a helpful chatbot using Sitecore content."},
            {"role": "user", "content": prompt}
        ]
    )

    #print(sitecore_response.json())
    chatbot_reply = openai_response.choices[0].message.content
    return {"response": chatbot_reply}

    
