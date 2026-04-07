from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from reviewer import review_code

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class CodeRequest(BaseModel):
    code: str
    language: str

@app.get("/")
def root():
    return {"message": "CodeSense API is running!"}

@app.post("/review")
def review(request: CodeRequest):
    if not request.code.strip():
        return {"error": "Code cannot be empty"}

    result = review_code(request.code, request.language)
    return result