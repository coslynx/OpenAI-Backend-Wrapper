from pydantic import BaseModel, validator

class TextRequest(BaseModel):
    text: str
    model: str = "text-davinci-003"  # Default OpenAI model

    @validator("model")
    def model_validation(cls, value):
        valid_models = ["text-davinci-003", "text-curie-001", "text-babbage-001", "text-ada-001"]
        if value not in valid_models:
            raise ValueError("Invalid model. Choose from: " + ", ".join(valid_models))
        return value

class TranslationRequest(BaseModel):
    text: str
    source_language: str
    target_language: str

    @validator("source_language")
    def source_language_validation(cls, value):
        valid_languages = ["en", "fr", "es", "de", "it", "pt", "ja", "ko", "zh-CN", "zh-TW"]
        if value not in valid_languages:
            raise ValueError("Invalid source language. Choose from: " + ", ".join(valid_languages))
        return value

    @validator("target_language")
    def target_language_validation(cls, value):
        valid_languages = ["en", "fr", "es", "de", "it", "pt", "ja", "ko", "zh-CN", "zh-TW"]
        if value not in valid_languages:
            raise ValueError("Invalid target language. Choose from: " + ", ".join(valid_languages))
        return value

class SummarizationRequest(BaseModel):
    text: str
    model: str = "text-davinci-003"  # Default OpenAI model

    @validator("model")
    def model_validation(cls, value):
        valid_models = ["text-davinci-003", "text-curie-001", "text-babbage-001", "text-ada-001"]
        if value not in valid_models:
            raise ValueError("Invalid model. Choose from: " + ", ".join(valid_models))
        return value

class User(BaseModel):
    username: str
    password: str