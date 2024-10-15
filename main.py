from fastapi import FastAPI, Body, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from businessLogic import transcribe_video_orchestrator

app = FastAPI()

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/transcribe")
async def transcribe(payload: dict = Body(...), req: Request = Request):
    url = payload['url']
    language = payload['language']

    transcript = transcribe_video_orchestrator(url, language)

    return {"data":  transcript, "error": None}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=6000)
