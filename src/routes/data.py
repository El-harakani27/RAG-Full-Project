from helpers.config import get_settings,Settings
from fastapi import APIRouter, Depends, UploadFile, status
from fastapi.responses import JSONResponse
from controllers import DataController,ProjectController
import os
import aiofiles
from models import ResponseSignal
import logging
logger = logging.getLogger("uvicorn.error")
data_router = APIRouter(
    prefix="/api/v1/data",
    tags=["api_v1","data"]
)

@data_router.post("/upload/{project_id}")
async def upload_data(project_id:str,
                      file:UploadFile,
                      app_settings:Settings = Depends(get_settings)):
    is_valid,txt_status = DataController().validate_uploaded_file(file=file)
    if not is_valid:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content= {
                "is_valid":is_valid,
                "status": txt_status
            }
        )
    file_path,file_id = DataController().generate_file_path(project_id=project_id,orig_file_name=file.filename)
    try:
        async with aiofiles.open(file_path,'wb') as f:
            while chunk:= await file.read(app_settings.FILE_DEFAULT_CHUNK_SIZE):
                await f.write(chunk)
    except Exception as e:
        logger.error(f"Error while Uploading file: {e}")
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "status":ResponseSignal.FILE_UPLOADED_FAILD
            }
        )
    return JSONResponse(
        content={
            "is_valid":is_valid,
            "status":ResponseSignal.FILE_UPLOADED_SUCCESS.value,
            "file_id":file_id
        }
    )
        
