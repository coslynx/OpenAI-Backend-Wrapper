import pytest
from fastapi import HTTPException
from openai import OpenAI
from api.api import generate_text_endpoint, translate_text_endpoint, summarize_text_endpoint
from api.models import TextRequest, TranslationRequest, SummarizationRequest
from unittest.mock import patch, Mock

# Mock OpenAI client with version 1.52.0
@pytest.fixture
def mock_openai():
    with patch("api.api.OpenAI") as mock_client:
        mock_client.return_value = Mock()
        yield mock_client

# Test case for text generation
def test_generate_text_endpoint(mock_openai):
    mock_openai.completions.create.return_value = {"choices": [{"text": "This is generated text."}]}
    request = TextRequest(text="Input text", model="text-davinci-003")
    response = generate_text_endpoint(request)
    assert response.status_code == 200
    assert response.json() == {"text": "This is generated text."}

# Test case for text translation
def test_translate_text_endpoint(mock_openai):
    mock_openai.translations.create.return_value = {"translation": "Translated text."}
    request = TranslationRequest(text="Text to translate", source_language="en", target_language="fr")
    response = translate_text_endpoint(request)
    assert response.status_code == 200
    assert response.json() == {"translation": "Translated text."}

# Test case for text summarization
def test_summarize_text_endpoint(mock_openai):
    mock_openai.completions.create.return_value = {"choices": [{"text": "This is a summary."}]}
    request = SummarizationRequest(text="Text to summarize", model="text-davinci-003")
    response = summarize_text_endpoint(request)
    assert response.status_code == 200
    assert response.json() == {"summary": "This is a summary."}

# Test case for handling OpenAI API errors
def test_generate_text_endpoint_error(mock_openai):
    mock_openai.completions.create.side_effect = Exception("OpenAI API error")
    request = TextRequest(text="Input text", model="text-davinci-003")
    with pytest.raises(HTTPException) as e:
        generate_text_endpoint(request)
    assert e.value.status_code == 400
    assert "Error generating text" in str(e.value.detail)