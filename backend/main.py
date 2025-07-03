# backend/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import OpenAI
import os
from dotenv import load_dotenv
import matplotlib.pyplot as plt
import io
from fastapi.responses import StreamingResponse

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3001"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class MessageRequest(BaseModel):
    message: str
    age: str
    gender: str
    theme: str
msg = []
@app.post("/api/chat")
async def hello(req: MessageRequest):
    try:
        print('age : ', req.age)
        print('gender : ', req.gender)
        print('theme : ', req.theme)
        print('message : ', req.message)
        msg1 = f"연령대: {req.age}, 성별: {req.gender}, 여행 테마: {req.theme}, 요청: {req.message}"

        intent_check_prompt = f"""
        다음 문장이 여행지 추천을 원하거나 여행 관련 요청인지 판단해줘.

        문장: "{req.message}"

        응답은 반드시 아래 중 하나만:
        - 여행추천
        - 일반대화
        """
        msg.append(msg1)

        intent_response = client.chat.completions.create(
            model="gpt-4.1",
            messages=[{"role": "user", "content": intent_check_prompt}]
        )
        intent = intent_response.choices[0].message.content.strip()

        if "여행추천" in intent:
            # 여기면 머신러닝 타서 함수 실행해야함.
            print('intent : ', intent)
            final_prompt = f"""
            사용자의 연령대는 {req.age}, 성별은 {req.gender}, 선호하는 여행 테마는 {req.theme}입니다.
            이 사용자에게 어울리는 여행지를 추천해 주세요. 요청: {req.message}
            """
        else:
            print('intent : ', intent)
            final_prompt = req.message  # 일반 대화는 원문 그대로

        response = client.chat.completions.create(
            model="gpt-4.1",
            messages=[{"role": "user", "content": final_prompt}]
)

        user_input = response.choices[0].message.content
    except Exception as e:
        return {"reply": f"OpenAI 호출 오류: {str(e)}"}
    
    return {"reply": user_input}

@app.get("/api/graph")
def get_graph_image():
    plt.figure()
    plt.plot([1, 2, 3, 4], [10, 20, 10, 30])
    plt.title("PNG 이미지 그래프")

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)

    return StreamingResponse(buf, media_type="image/png")
