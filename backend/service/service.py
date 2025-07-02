from facade.open_ai_agent import OpenAIAgent
from facade.kto_api_agent import KtoApiAgent

class Service:
    def __init__(self):
        self.__open_ai_agent = OpenAIAgent()
        self.__kto_api_agent = KtoApiAgent()

    def openai_request(self):
        print("===== OpenAI Request ... =====")
        print("========== OK!==========")

    def kto_api_request(self):
        print("===== KTO API Request ... =====")
        print("========== OK!==========")