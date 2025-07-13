from fastapi import FastAPI
from app.api import router
from fastapi.staticfiles import StaticFiles

app = FastAPI(title="Bài Test 2 - Call Analyzer")

app.include_router(router)
app.mount("/", StaticFiles(directory="public", html=True), name="static")