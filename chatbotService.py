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
# AZURE_OPENAI_KEY = "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"
AZURE_OPENAI_ENDPOINT = "https://sitecoreopenai.openai.azure.com/"
AZURE_OPENAI_KEY = "E8PMIFK3OCBWkjfnLcAGqu1QLwPW5WiJZ1QHyZVL18cF5KCYnvZRJQQJ99BCACYeBjFXJ3w3AAABACOGzb2l"
# Sitecore XM Cloud API Credentials
SITECORE_API_URL =  "https://xmc-epamemeatraeee0-alj52a9-preview2b9e.sitecorecloud.io/sitecore/api/graph/edge"  #"https://xmcloudcm.localhost/sitecore/api/graph/edge"
SITECORE_API_TOKEN = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InpnbnhyQk9IaXJ0WXp4dnl1WVhNZyJ9.eyJodHRwczovL2F1dGguc2l0ZWNvcmVjbG91ZC5pby9jbGFpbXMvY2xpZW50X25hbWUiOiJBUElfQWRtaW4xIiwiaHR0cHM6Ly9hdXRoLnNpdGVjb3JlY2xvdWQuaW8vY2xhaW1zL29yZ19pZCI6Im9yZ196OFM0c1JQd3E2SVc0czRPIiwiaHR0cHM6Ly9hdXRoLnNpdGVjb3JlY2xvdWQuaW8vY2xhaW1zL29yZ19uYW1lIjoiZXBhbS1lbWVhLXRyYWluaW5nLTMiLCJodHRwczovL2F1dGguc2l0ZWNvcmVjbG91ZC5pby9jbGFpbXMvb3JnX2Rpc3BsYXlfbmFtZSI6IkVQQU0gRU1FQSBUcmFpbmluZyAzIiwiaHR0cHM6Ly9hdXRoLnNpdGVjb3JlY2xvdWQuaW8vY2xhaW1zL29yZ19hY2NvdW50X2lkIjoiMDAxMU4wMDAwMVV0VVhqUUFOIiwiaHR0cHM6Ly9hdXRoLnNpdGVjb3JlY2xvdWQuaW8vY2xhaW1zL29yZ190eXBlIjoicGFydG5lciIsInNjX29yZ19yZWdpb24iOiJ1c2UiLCJpc3MiOiJodHRwczovL2F1dGguc2l0ZWNvcmVjbG91ZC5pby8iLCJzdWIiOiJYMkR6a01IbW8xcTFnYkZsZ0Iweld3dDNqTWFiN3BrRUBjbGllbnRzIiwiYXVkIjoiaHR0cHM6Ly9hcGkuc2l0ZWNvcmVjbG91ZC5pbyIsImlhdCI6MTc0MjY1NDQ1NiwiZXhwIjoxNzQyNzQwODU2LCJzY29wZSI6InhtY2xvdWRkZXBsb3kub3JnYW5pemF0aW9uczptYW5hZ2UgeG1jbG91ZGRlcGxveS5wcm9qZWN0czptYW5hZ2UgeG1jbG91ZGRlcGxveS5lbnZpcm9ubWVudHM6bWFuYWdlIHhtY2xvdWRkZXBsb3kuZGVwbG95bWVudHM6bWFuYWdlIHhtY2xvdWRkZXBsb3kuY2xpZW50czptYW5hZ2UgeG1jbG91ZGRlcGxveS5zb3VyY2Vjb250cm9sOm1hbmFnZSB4bWNsb3VkZGVwbG95Lm1vbml0b3JpbmcuZGVwbG95bWVudHM6cmVhZCB4bWNsb3VkZGVwbG95LnNpdGU6bW5nIHhtY2xvdWRkZXBsb3kucmg6bW5nIHhtY2xvdWQuY206YWRtaW4iLCJndHkiOiJjbGllbnQtY3JlZGVudGlhbHMiLCJhenAiOiJYMkR6a01IbW8xcTFnYkZsZ0Iweld3dDNqTWFiN3BrRSJ9.oic-ERoyxaWh1H2oqDP2UOMMNbX4Sz2EboJZ2H5r_wRTTHIhP921ckqP3RiI8ZiA03q-M5nvXKmIfvP-Kg1Tbq44h1GiR8rKvGCytZII267jbWbne0kVShqBxOE0jy5-oZUiPzijYTrd4fwHbQfEB9MixZgizVQ9P3MB5w56J2hKjGp0h-ub2InsFeXX4WBoEN6w1th-XUx_X9tAperyDe1mlhOocPRQLjlUsgClsaUk7efvXV9N56_GjJGPt95Mits45i9OFSPgBF11VTXS5_59TX8LMCMqfOfr98F5kN3xxNcxWXnUQaY4GllgA4MlFTi6ji5hO7Tv-VqpWW3qzg"

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

    
