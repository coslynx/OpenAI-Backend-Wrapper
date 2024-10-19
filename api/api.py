from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.dependencies import Depends

from .models import TextRequest, TranslationRequest, SummarizationRequest
from .auth import authenticate_user, generate_jwt_token
from .database import get_db, User
from openai import OpenAI

# Import OpenAI library with version 1.52.0
openai = OpenAI()

# Import configuration settings from config.py
from .config import settings

app = FastAPI()

# Define CORS middleware for allowing cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define the endpoint for text generation
@app.post("/generate_text", response_model=TextRequest, responses={400: {"model": "Bad Request"}})
async def generate_text_endpoint(request: TextRequest):
    """
    Generates text using the OpenAI API.

    Args:
        request (TextRequest): The request body containing the text to generate and the model to use.

    Returns:
        JSONResponse: A JSON response containing the generated text.
    """
    try:
        # Use the OpenAI library to generate text
        response = openai.completions.create(
            model=request.model,
            prompt=request.text,
            max_tokens=1024,
            temperature=0.7,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0,
        )

        # Extract the generated text from the OpenAI response
        text = response.choices[0].text

        # Return the generated text as a JSON response
        return JSONResponse(content={"text": text}, status_code=200)
    except Exception as e:
        # Raise a 400 Bad Request exception if an error occurs during text generation
        raise HTTPException(status_code=400, detail=f"Error generating text: {e}")

# Define the endpoint for text translation
@app.post("/translate", response_model=TranslationRequest, responses={400: {"model": "Bad Request"}})
async def translate_text_endpoint(request: TranslationRequest):
    """
    Translates text from one language to another using the OpenAI API.

    Args:
        request (TranslationRequest): The request body containing the text to translate, the source language, and the target language.

    Returns:
        JSONResponse: A JSON response containing the translated text.
    """
    try:
        # Use the OpenAI library to translate text
        response = openai.translations.create(
            model="gpt-3.5-turbo",
            input=request.text,
            source_language=request.source_language,
            target_language=request.target_language,
        )

        # Extract the translated text from the OpenAI response
        translation = response.translation

        # Return the translated text as a JSON response
        return JSONResponse(content={"translation": translation}, status_code=200)
    except Exception as e:
        # Raise a 400 Bad Request exception if an error occurs during text translation
        raise HTTPException(status_code=400, detail=f"Error translating text: {e}")

# Define the endpoint for text summarization
@app.post("/summarize", response_model=SummarizationRequest, responses={400: {"model": "Bad Request"}})
async def summarize_text_endpoint(request: SummarizationRequest):
    """
    Summarizes a given text using the OpenAI API.

    Args:
        request (SummarizationRequest): The request body containing the text to summarize and the model to use.

    Returns:
        JSONResponse: A JSON response containing the summarized text.
    """
    try:
        # Use the OpenAI library to summarize text
        response = openai.completions.create(
            model=request.model,
            prompt=f"Summarize this text: {request.text}",
            max_tokens=1024,
            temperature=0.7,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0,
        )

        # Extract the summarized text from the OpenAI response
        summary = response.choices[0].text

        # Return the summarized text as a JSON response
        return JSONResponse(content={"summary": summary}, status_code=200)
    except Exception as e:
        # Raise a 400 Bad Request exception if an error occurs during text summarization
        raise HTTPException(status_code=400, detail=f"Error summarizing text: {e}")

# Define the endpoint for user login
@app.post("/login", response_model=str, responses={400: {"model": "Bad Request"}})
async def login_endpoint(user_data: User):
    """
    Authenticates a user and generates a JWT token.

    Args:
        user_data (User): The request body containing the user's username and password.

    Returns:
        JSONResponse: A JSON response containing the JWT access token.
    """
    try:
        # Authenticate the user using the authenticate_user function from auth.py
        user = await authenticate_user(user_data.username, user_data.password)

        if user:
            # Generate a JWT token using the generate_jwt_token function from auth.py
            token = generate_jwt_token(user.username)

            # Return the JWT access token as a JSON response
            return JSONResponse(content={"access_token": token}, status_code=200)
        else:
            # Raise a 401 Unauthorized exception if the credentials are invalid
            raise HTTPException(status_code=401, detail="Invalid credentials")
    except Exception as e:
        # Raise a 400 Bad Request exception if an error occurs during login
        raise HTTPException(status_code=400, detail=f"Error during login: {e}")

# Define the endpoint for retrieving user data
@app.get("/users/{user_id}")
async def get_user(user_id: int, db: Session = Depends(get_db)):
    """
    Retrieves a user's data from the database.

    Args:
        user_id (int): The ID of the user to retrieve.
        db (Session): The database session.

    Returns:
        User: The user data if found, otherwise raises a 404 Not Found exception.
    """
    # Retrieve the user from the database using the SQLAlchemy session
    user = db.query(User).filter(User.id == user_id).first()

    if user:
        # Return the user data as a JSON response
        return user
    else:
        # Raise a 404 Not Found exception if the user is not found
        raise HTTPException(status_code=404, detail="User not found")

# Define an event handler for application startup
@app.on_event("startup")
async def startup_event():
    """
    Handles application startup events.

    This event handler is called when the application starts.
    """
    # Initialize the OpenAI library with the API key from settings.py
    openai.api_key = settings.OPENAI_API_KEY

    # Optionally initialize the database connection here
    # ...

# Define an event handler for application shutdown
@app.on_event("shutdown")
async def shutdown_event():
    """
    Handles application shutdown events.

    This event handler is called when the application shuts down.
    """
    # Optionally close the database connection here
    # ...