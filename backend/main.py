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
import json

chat_session = [] # 대화 세션 유지 용도

def travel_list(Age, Gender, Theme):
    print('Age : ', Age)
    print('Gender : ', Gender)
    print('Theme : ', Theme)
    print("travel_list!!")



def request_function_call(age, gender, theme, duration):
    func_call_msg = f"나이: {age}, 성별: {gender}, 테마: {theme}, 기간: {duration}"
    input_messages = [
        {'role': 'user', 'content': func_call_msg}
    ]

    response = client.responses.create(
    model ='gpt-4.1',
    input=input_messages,
    tools = tools
    )
    print(response)
    
    tool_call = response.output[0]
    args = json.loads(tool_call.arguments)

    if tool_call.name == "travel_list":
        return args
    else:
        return False
    

tools = [
    {
        "type": "function",
        "name": "travel_list",
        "description": "여행지 추천 리스트 제공",
        "parameters": {
            "type": "object",
            "properties":{
                "Age": {"type": "number"},
                "Gender": {"type": "number"},
                "Theme": {"type": "string"}
            },
            "required": ["Age", "Gender", "Theme"],
            "additionalProperties": False
        },
        "strict": True
    }
]




load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class MessageRequest(BaseModel):
    message: str
    age: str
    gender: str
    theme: str
    duration: str

@app.post("/api/session_reset")
async def reset():
    try:
        chat_session.clear()
        print('초기화')
    except Exception as e:
        print(f"/app/session_reset Error : {e}")
        

@app.post("/api/chat")
async def hello(req: MessageRequest):
    try:
        

        print('age : ', req.age)
        print('gender : ', req.gender)
        print('theme : ', req.theme)
        print('message : ', req.message)
        print('duration : ', req.duration)
        

        intent_check_prompt = f"""
        다음 문장이 여행지 추천을 원하거나 여행 관련 요청인지 판단해줘.

        문장: "{req.message}"

        응답은 반드시 아래 중 하나만:
        - 여행추천
        - 일반대화
        """
        # 1. 의도파악
        intent_response = client.chat.completions.create(
            model="gpt-4.1",
            messages=[{"role": "user", "content": intent_check_prompt}],
        )

        intent = intent_response.choices[0].message.content.strip()

        if "여행추천" in intent:
            chat_session.append({"role": "user", "content": req.message})
            # 2. Function Call 호출(머신러닝)
            args = request_function_call(req.age, req.gender, req.theme, req.duration)

            if args==False:
                return {"reply": "Function Calling 호출 오류"}
            
            # 결과
            # 주소 5개 (시/도, 구/면/읍 (ex: 서울특별시 강남구 등)
            # 머신러닝 분석 시각화 자료(그래프? 등)
            travel_list(**args)

            # 3. API + 웹 서치

            # 4. 최종 자연어 생성 (GPT)

            # ----------------------밑 테스트용(삭제할것)----------------------- #
            print('intent : ', intent)
            final_prompt = f"""
            사용자의 연령대는 {req.age}, 성별은 {req.gender}, 선호하는 여행 테마는 {req.theme},
            여행 기간은 {req.duration} 입니다.
            이 사용자에게 어울리는 여행지를 추천해 주세요. 요청: {req.message}
            """

            response = client.chat.completions.create(
            model="gpt-4.1",
            messages=[{"role": "user", "content": final_prompt}]
            )
            reply = response.choices[0].message.content
            chat_session.append({"role": "assistant", "content": reply})

            # ----------------------밑 테스트용(삭제할것)----------------------- #
        else:
            chat_session.append({"role": "user", "content": req.message})
            print('intent : ', intent)
            final_prompt = req.message  # 일반 대화는 원문 그대로

            response = client.chat.completions.create(
                model="gpt-4.1",
                #messages=[{"role": "user", "content": final_prompt}]
                messages = chat_session
            )
            reply = response.choices[0].message.content
            chat_session.append({"role": "assistant", "content": reply})

        #user_input = response.choices[0].message.content

    except Exception as e:
        return {"reply": f"OpenAI 호출 오류: {str(e)}"}
    
    test_input = "1. 첫번쨰 사진 https://images.unsplash.com/photo-1506744038136-46273834b3fb\n" \
    "2. 두번째 사진 이거는 답변을 좀 길게 해봐야겠다. ㅅㅅㅅㅅㅅㅅㅅㅅㅅㅅㅅㅅㅅㅅㅅ https://images.unsplash.com/photo-1506744038136-46273834b3fb " \
    "3. 이거는 세번째 사진이여https://images.unsplash.com/photo-1506744038136-46273834b3fb\n" \
    "4. 이거는 네번째 사진이렘ㄴㅇㅁㅈㅇhttps://images.unsplash.com/photo-1506744038136-46273834b3fb"

    mark_input = "wadsdwads adwasdawd asd awdasdwasdaw dad![추천 이미지](https://images.unsplash.com/photo-1506744038136-46273834b3fb)daw asdwads"
    # return {"reply": user_input,
    #         "image_url":"https://images.unsplash.com/photo-1506744038136-46273834b3fb"}

    # return {"reply": mark_input }
    # return {"reply": test_input }
    return {"reply": reply }

@app.get("/api/graph")
def get_graph_image():
    plt.figure()
    plt.plot([1, 2, 3, 4], [10, 20, 10, 30])
    plt.title("PNG 이미지 그래프")

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)

    return StreamingResponse(buf, media_type="image/png")
