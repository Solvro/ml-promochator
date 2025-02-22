import os

from dotenv import load_dotenv

load_dotenv()

VECTORSTORE_PATH = './vectorstores/test_vectorstore'  # for launch in main.py
OPEN_AI_API_KEY = os.getenv('OPEN_AI_API_KEY', '')
