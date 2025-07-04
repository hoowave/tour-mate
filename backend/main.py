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
from model.model_1 import run, show_graph
from fastapi import HTTPException

chat_session = [] # 대화 세션 유지 용도
# 전역 변수 선언
global_model = None
global_top_5 = None

def travel_list(Age, Gender, Theme):
    global global_model, global_top_5
    filepath = './model/final_file_cleaned.csv'
    modelpath = './catboost_model.cbm'
    print('Age : ', Age)
    print('Gender : ', Gender)
    print('Theme : ', Theme)
    print("travel_list!!")

    print('================== Start Model ==================')
    model, top_5 = run(Age, Gender, Theme, filepath, modelpath)
    global_model = model
    global_top_5 = top_5
    # show_graph(model, top_5, filepath)
    print('==================  END Model  ==================')
    if global_model is not None and global_top_5 is not None:
        print('여기 둘다 값있네..')
    return top_5




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
            top_5 = travel_list(**args)

            # 3. API + 웹 서치
            # pass

            # 4. 최종 자연어 생성 (GPT)
            # pass
            reply = json.dumps(top_5.to_dict(orient="records"), ensure_ascii=False)
            reply = top_5.to_string(index=False)
            
            print('reply : ', reply)
            print('reply : type', type(reply))
            # ----------------------밑 테스트용(삭제할것)----------------------- #
            # print('intent : ', intent)
            # final_prompt = f"""
            # 사용자의 연령대는 {req.age}, 성별은 {req.gender}, 선호하는 여행 테마는 {req.theme},
            # 여행 기간은 {req.duration} 입니다.
            # 이 사용자에게 어울리는 여행지를 추천해 주세요. 요청: {req.message}
            # """

            # response = client.chat.completions.create(
            # model="gpt-4.1",
            # messages=[{"role": "user", "content": final_prompt}]
            # )
            # reply = response.choices[0].message.content
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
            print('reply : ', reply)
            print('reply type : ', type(reply))
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
    global global_model, global_top_5
    
    if global_top_5 is None or global_model is None:
        print("값이 없어서 그래프를 그릴 수가 없음")
        raise HTTPException(status_code=400, detail="그래프를 그릴 수 없습니다.")

    print("값있는데..?")
    filepath = './model/final_file_cleaned.csv'
    buf = show_graph(global_model, global_top_5, filepath)
    

    return StreamingResponse(buf, media_type="image/png")
