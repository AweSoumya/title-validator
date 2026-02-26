import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL")
DATA_PATH = os.getenv("DATA_PATH")
HF_TOKEN = os.getenv("HF_TOKEN")