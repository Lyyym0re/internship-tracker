
from app.storage import save_application, find_application, filtered_applications,update_application_status
from fastapi import FastAPI, status, Depends, HTTPException
from app.models import ApplicationCreate, ApplicationResponse, ApplicationStatusUpdate
from typing import Annotated


app = FastAPI()

@app.get("/applications/{application_id}", response_model=ApplicationResponse)
def get_application(application: Annotated[dict | None, Depends(find_application)]) -> dict:
    if application is None:
        raise HTTPException(status_code=404, detail="Application not found")
    return application

@app.get("/applications", response_model=list[ApplicationResponse])
def list_applications(applications:
    Annotated[list[dict], Depends(filtered_applications)]) -> list[dict]:
    return applications

@app.post("/applications", response_model=ApplicationResponse, status_code=status.HTTP_201_CREATED)
def create_application(payload: ApplicationCreate) -> dict:
    return save_application(payload.company, payload.position)

@app.patch("/applications/{application_id}", response_model=ApplicationResponse)
def patch_application_status(application_id: int, payload: ApplicationStatusUpdate) -> dict:
    result = update_application_status(application_id, payload.status)
    if result is None:
        raise HTTPException(status_code=404, detail="Application not found")
    return result