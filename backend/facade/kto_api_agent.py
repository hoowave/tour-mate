from dotenv import load_dotenv
from openai import OpenAI
import os

class KtoApiAgent:
    def __init__(self):
        load_dotenv()
        __OPENAI_API_KEY = os.getenv('KTO_API_KEY')

    def request(self):
        pass