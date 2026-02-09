from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
import os
from dotenv import load_dotenv
import google.generativeai as genai
from typing import Optional

# Load environment variables
load_dotenv()

# Configure the API key for Google Generative AI
genai.configure(api_key=os.getenv("GOOGLE_GEMINI_API_KEY"))

# Create the FastAPI router
router = APIRouter()

# Define request and response models
class ChatRequest(BaseModel):
    message: str
    history: Optional[list] = []

class ChatResponse(BaseModel):
    response: str
    conversation_id: Optional[str] = None

# Initialize the generative model
model = genai.GenerativeModel('gemini-1.5-flash')

@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """
    Endpoint to handle chat requests and return AI-generated responses
    """
    try:
        # Generate content using the Gemini model
        response = model.generate_content(request.message)
        
        # Extract the text from the response
        ai_response = response.text if response.text else "I couldn't generate a response. Please try again."
        
        return ChatResponse(
            response=ai_response,
            conversation_id=None  # Will implement conversation tracking later if needed
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating response: {str(e)}")

@router.get("/health")
async def health_check():
    """
    Health check endpoint for the chat service
    """
    return {"status": "healthy", "service": "chatbot"}