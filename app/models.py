from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Call(BaseModel):
    id: int
    filename: str
    transcript: str
    uploaded_at: datetime