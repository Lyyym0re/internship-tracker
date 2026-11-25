from fastapi import APIRouter, HTTPException, Request, status
from app.storage import save_application, filtered_applications, update_application_status, find_application_async, delete_application_async
from app.models import ApplicationCreate, ApplicationResponse, ApplicationStatusUpdate, ApplicationStatus


router = APIRouter(prefix="/applications")

@router.get("/{application_id}", response_model=ApplicationResponse)
async def get_application(application_id: int, request: Request) -> dict:
    pool = request.app.state.db_pool
    application = await find_application_async(application_id, pool)
    if application is None:
        raise HTTPException(status_code=404, detail="Application not found")
    return application

@router.get("", response_model=list[ApplicationResponse])
async def list_applications(request: Request, status : ApplicationStatus | None = None) -> list[dict]:
    pool = request.app.state.db_pool
    return await filtered_applications(status, pool)

@router.post("", response_model=ApplicationResponse, status_code=status.HTTP_201_CREATED)
async def create_application(payload: ApplicationCreate, request: Request) -> dict:
    pool = request.app.state.db_pool
    return await save_application(payload.company, payload.position, pool)

@router.patch("/{application_id}", response_model=ApplicationResponse)
async def patch_application_status(application_id: int, payload: ApplicationStatusUpdate, request: Request) -> dict:
    pool = request.app.state.db_pool
    result = await update_application_status(application_id, payload.status, pool)
    if result is None:
        raise HTTPException(status_code=404, detail="Application not found")
    return result

@router.delete("/{application_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_application(application_id: int, request: Request) -> None:
    pool = request.app.state.db_pool
    delete_application = await delete_application_async(application_id, pool)
    if delete_application is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Application for delete not found")