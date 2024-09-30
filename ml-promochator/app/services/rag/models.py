import os
from typing import Optional

from langchain_community.llms import Ollama
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_openai import OpenAI


def get_supported_models():
    """Get all avalaible models"""
    models = {}
    if "OPENAI_API_KEY" in os.environ:
        models["gpt-3.5-turbo"] = {
            "chat_model": OpenAI(model="gpt-3.5-turbo", temperature=0),
            "description": "GPT-3.5 Turbo",
        }
        if os.environ.get("DISABLE_GPT4", "").lower() != "true":
            models["gpt-4-0125-preview"] = {
                "chat_model": OpenAI(model="gpt-4-0125-preview", temperature=0),
                "description": "GPT-4 0125 Preview",
            }
    if os.environ.get("OLLAMA_AVAILABLE", "").lower() == "true":
        if os.environ.get("MODEL", "").lower() == "ollama-llama3":
            models["ollama-llama3"] = {
                "chat_model": Ollama(model='llama3'),
                "description": "Ollama Llama3",
            }
        if os.environ.get("MODEL", "").lower() == "ollama-gemma2":
            models["ollama-gemma2"] = {
                "chat_model": Ollama(model='gemma2'),
                "description": "Ollama Gemma2",
            }

    return models


SUPPORTED_MODELS = get_supported_models()
DEFAULT_MODEL = "ollama-llama3"


def get_model(model_name: Optional[str] = None) -> BaseChatModel:
    """Get the model"""
    if model_name is None:
        return SUPPORTED_MODELS[DEFAULT_MODEL]["chat_model"]
    else:
        supported_model_names = list(SUPPORTED_MODELS.keys())
        if model_name not in supported_model_names:
            raise ValueError(
                f"Model {model_name} not found. "
                f"Supported models: {supported_model_names}"
            )
        else:
            return SUPPORTED_MODELS[model_name]["chat_model"]