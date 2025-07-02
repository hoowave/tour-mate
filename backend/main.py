from fastapi import FastAPI
import interfaces.controller as Controller

app = FastAPI()

app.include_router(Controller.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)