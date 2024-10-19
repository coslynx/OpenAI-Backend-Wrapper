from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.dependencies import Depends
from sqlalchemy.orm import Session

from .models import TextRequest, TranslationRequest, SummarizationRequest
from .api import generate_text, translate_text, summarize_text
from .auth import authenticate_user, generate_jwt_token
from .database import get_db, User

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/generate_text", response_model=TextRequest, responses={400: {"model": "Bad Request"}})
async def generate_text_endpoint(request: TextRequest):
    try:
        text = await generate_text(request.text, request.model)
        return {"text": text}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error generating text: {e}")

@app.post("/translate", response_model=TranslationRequest, responses={400: {"model": "Bad Request"}})
async def translate_text_endpoint(request: TranslationRequest):
    try:
        translation = await translate_text(request.text, request.source_language, request.target_language)
        return {"translation": translation}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error translating text: {e}")

@app.post("/summarize", response_model=SummarizationRequest, responses={400: {"model": "Bad Request"}})
async def summarize_text_endpoint(request: SummarizationRequest):
    try:
        summary = await summarize_text(request.text, request.model)
        return {"summary": summary}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error summarizing text: {e}")

@app.post("/login", response_model=str, responses={400: {"model": "Bad Request"}})
async def login_endpoint(user_data: User):
    try:
        user = await authenticate_user(user_data.username, user_data.password)
        if user:
            token = generate_jwt_token(user.username)
            return JSONResponse(content={"access_token": token}, status_code=200)
        else:
            raise HTTPException(status_code=401, detail="Invalid credentials")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error during login: {e}")

@app.get("/users/{user_id}")
async def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        return user
    else:
        raise HTTPException(status_code=404, detail="User not found")

@app.on_event("startup")
async def startup_event():
    # Initialize database connection (if needed)
    # ...

@app.on_event("shutdown")
async def shutdown_event():
    # Close database connection (if needed)
    # ...