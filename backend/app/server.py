import logging
import os
import re
import whisper
import uvicorn
import app.db as db
from fastapi import FastAPI, File, Form, UploadFile
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from openai import AsyncOpenAI
from dotenv import load_dotenv

UPLOAD_FOLDER = "uploads"
MODEL = "gpt-3.5-turbo"

load_dotenv()
client = AsyncOpenAI()
app = FastAPI()
origins = [
    "http://localhost:3000",  # React app
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


async def transcribe_audio_with_whisper(file_path):
    model = whisper.load_model("base")
    result = model.transcribe(file_path)
    return result["text"]


async def infer_grammer_feedback(text: str) -> tuple[int, str]:
    completion = await client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "Score the text for grammar on a 10-point scale and also provide a rationale for your score. The format should be `Score: \\nRationale:`"},
            {"role": "user", "content": f"{text}"}
        ],
        temperature=0.2,
    )
    feedback = completion.choices[0].message.content
    
    # Search for the pattern in the text
    score_pattern = r"Score: (\d+)"
    match = re.search(score_pattern, feedback)
    score = None
    if match:
        score = int(match.group(1))

    rationale_pattern = r"Rationale:\s*(.*)"
    rationale_match = re.search(rationale_pattern, feedback, re.DOTALL)
    rationale = None
    if rationale_match:
        rationale = rationale_match.group(1).strip()

    return score, rationale


@app.post("/users")
async def submit_user(name: str = Form(...), email: str = Form(...), phone: str = Form(...)):
    userid = db.get_user(email)
    if userid is None:
        userid = db.create_user(name, email, phone)
    print(userid)
    return JSONResponse(content={"userId": userid})


@app.post("/audio/upload")
async def upload_file(userid: str = Form(...), file: UploadFile = File(...)):
    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    with open(filepath, "wb") as buffer:
        buffer.write(await file.read())
    transcript = await transcribe_audio_with_whisper(filepath)
    submission_id = db.create_submission(int(userid), filepath, transcript.strip())
    return JSONResponse(content={"submissionId": submission_id})


@app.get("/audio/feedback/{submission_id}")
async def get_feedback(submission_id: int):
    feedback = db.get_feedback(submission_id, model=MODEL)
    if feedback is None:
        text = db.get_submission_transcript(submission_id)
        score, rationale = await infer_grammer_feedback(text)
        db.create_feedback(submission_id, score, rationale)
    else:
        score, rationale = feedback
    return JSONResponse(content={"score": score, "feedback": rationale})


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)
