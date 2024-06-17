import logging
import os
import re
import whisper
import uvicorn
from fastapi import FastAPI, File, Form, UploadFile
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from openai import AsyncOpenAI
from dotenv import load_dotenv
from app.db import create_feedback, create_submission, create_user, get_submission_transcript, get_user

UPLOAD_FOLDER = 'uploads'

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

@app.post("/users")
async def submit_user(name: str = Form(...), email: str = Form(...), phone: str = Form(...)):
    userid = get_user(email)
    if userid is None:
        userid = create_user(name, email, phone)
    print(userid)
    return JSONResponse(content={"userId": userid})

@app.post("/audio/upload")
async def upload_file(userid: str, file: UploadFile = File(...)):
    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    with open(filepath, "wb") as buffer:
        buffer.write(await file.read())
    transcript = await transcribe_audio_with_whisper(filepath)
    submission_id = create_submission(int(userid), filepath, transcript.strip())
    return JSONResponse(content={"submissionId": submission_id})

@app.get("/audio/feedback/{submission_id}")
async def get_feedback(submission_id: int):
    text = get_submission_transcript(submission_id)
    completion = await client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Score the text for grammar on a 10-point scale and also provide a rationale for your score. The format should be `Score: \\nRationale:`"},
            {"role": "user", "content": f"{text}"}
        ],
        temperature=0.2,
    )
    feedback = completion.choices[0].message.content
    pattern = r"Score: (\d+)"

    # Search for the pattern in the text
    match = re.search(pattern, feedback)

    # Extract the score if the pattern is found
    score = None
    if match:
        score = int(match.group(1))
    create_feedback(submission_id, score, feedback)
    return {"score": score, "feedback": feedback}


if __name__ == '__main__':
    
    uvicorn.run(app, host="0.0.0.0", port=8000)
