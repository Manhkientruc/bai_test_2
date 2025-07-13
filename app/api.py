from fastapi import APIRouter, File, UploadFile
from fastapi.responses import JSONResponse
from datetime import datetime
from app.models import Call
from datetime import datetime
from app.analyzer import analyze_transcript
from fastapi import FastAPI, Request
from pydantic import BaseModel
from app.chatbot_service import chatbot_response
import shutil
import os

from app.whisper_utils import transcribe_audio

calls_db = []
call_id_counter = 1

router = APIRouter()

UPLOAD_FOLDER = "data/audio"

@router.post("/upload")
async def upload_audio(file: UploadFile = File(...)):
    global call_id_counter

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    filename = f"{timestamp}_{file.filename}"
    filepath = os.path.join(UPLOAD_FOLDER, filename)

    # Lưu file
    with open(filepath, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Nhận diện nội dung
    transcript = transcribe_audio(filepath)

    # Tạo đối tượng Call và lưu vào "db"
    call = Call(
        id=call_id_counter,
        filename=filename,
        transcript=transcript,
        uploaded_at=datetime.now()
    )
    calls_db.append(call)
    call_id_counter += 1

    return JSONResponse(content={
        "message": "Upload và nhận diện thành công!",
        "call_id": call.id,
        "filename": filename,
        "transcript": transcript
    })
@router.get("/calls")
def list_calls():
    return calls_db
@router.get("/calls/{call_id}")
def get_call(call_id: int):
    for call in calls_db:
        if call.id == call_id:
            return call
    return JSONResponse(status_code=404, content={"error": "Call not found"})
@router.get("/calls/{call_id}/analyze")
def analyze_call(call_id: int):
    for call in calls_db:
        if call.id == call_id:
            analysis = analyze_transcript(call.transcript)
            return {
                "call_id": call_id,
                "filename": call.filename,
                "analysis": analysis
            }
    return JSONResponse(status_code=404, content={"error": "Call not found"})
class ChatRequest(BaseModel):
    transcript: str

@router.post("/chatbot")
def chat_endpoint(req: ChatRequest):
    reply = chatbot_response(req.transcript)
    return {"response": reply}
@router.get("/stats")
def get_stats():
    total_calls = len(calls_db)
    total_words = 0
    total_sentences = 0
    total_polarity = 0
    total_subjectivity = 0
    keyword_counter = {}

    for call in calls_db:
        analysis = analyze_transcript(call.transcript)
        total_words += analysis["word_count"]
        total_sentences += analysis["sentence_count"]
        total_polarity += analysis["sentiment"]["polarity"]
        total_subjectivity += analysis["sentiment"]["subjectivity"]

        for keyword, count in analysis["top_keywords"]:
            if keyword in keyword_counter:
                keyword_counter[keyword] += count
            else:
                keyword_counter[keyword] = count

    average_words = total_words / total_calls if total_calls else 0
    average_sentences = total_sentences / total_calls if total_calls else 0
    average_polarity = total_polarity / total_calls if total_calls else 0
    average_subjectivity = total_subjectivity / total_calls if total_calls else 0

    top_keywords = sorted(keyword_counter.items(), key=lambda x: x[1], reverse=True)[:5]

    return {
        "total_calls": total_calls,
        "total_words": total_words,
        "average_words_per_call": average_words,
        "average_sentences_per_call": average_sentences,
        "average_polarity": average_polarity,
        "average_subjectivity": average_subjectivity,
        "top_keywords": top_keywords
    }
