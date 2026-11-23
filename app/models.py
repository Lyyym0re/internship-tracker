from typing import Literal
from pydantic import BaseModel

ApplicationStatus = Literal['applied', 'interview', 'offer', 'rejected']

class ApplicationCreate(BaseModel):
    company: str
    position: str

class ApplicationResponse(BaseModel):
    id: int
    company: str
    position: str
    status: str

class ApplicationStatusUpdate(BaseModel):
    status: ApplicationStatus