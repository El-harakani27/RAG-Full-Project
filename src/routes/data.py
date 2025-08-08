from helpers.config import get_settings,Settings
from fastapi import APIRouter, Depends, Request, UploadFile, status
from fastapi.responses import JSONResponse
from controllers import DataController,ProjectController,ProcessController
import os
import aiofiles
from models import ResponseSignal
from models.ProjectModel import ProjectModel
from models.ChunkModel import ChunkModel
from models.db_schemes.data_chunk import DataChunk
from .schemes.data import ProcessRequest
import logging
logger = logging.getLogger("uvicorn.error")
data_router = APIRouter(
    prefix="/api/v1/data",
    tags=["api_v1","data"]
)

@data_router.post("/upload/{project_id}")
async def upload_data(request:Request,project_id:str,
                      file:UploadFile,
                      app_settings:Settings = Depends(get_settings)):
    print("Type of db_client:", type(request.app.db_client))
    project_model = await ProjectModel.create_instance(
        db_client = request.app.db_client
    )
    project = await project_model.get_project_or_create_one(project_id=project_id)

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
            "file_id":file_id,
            
        }
    )
        
@data_router.post("/process/{project_id}")
async def process_endpoint(request:Request,project_id:str,process_request:ProcessRequest):
    chunk_model = await ChunkModel.create_instance(
        db_client= request.app.db_client
    )
    
    project_model = await ProjectModel.create_instance(
        db_client=request.app.db_client
    )
    project = await project_model.get_project_or_create_one(project_id=project_id)

    file_id = process_request.file_id
    overlap_size = process_request.overlap_size
    chunk_size = process_request.chunk_size
    do_reset = process_request.do_reset



    process_controller = ProcessController(project_id=project_id)
    file_content = process_controller.get_file_content(file_id=file_id)
    file_chunks = process_controller.process_file_content(file_content=file_content,overlap_size=overlap_size,chunk_size=chunk_size,file_id=file_id)
    if file_chunks is None or len(file_chunks)==0:
        
        
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "signal":ResponseSignal.PROCESSING_FAILED.value
            }
        )

    file_chunks_records = [DataChunk(
        chunk_metadata=chunk.metadata,
        chunk_text=chunk.page_content,
        chunk_project_id= project.id,
        chunk_order= order+1 
    ) for order,chunk in enumerate(file_chunks)]

    if do_reset:
        _= await chunk_model.delete_chunks_by_project_id(project_id=project.id)


    no_records = await chunk_model.insert_many_chunk(chunks=file_chunks_records)
    return JSONResponse(
        content={
            "signal":ResponseSignal.PROCESSING_SUCCESS.value,
            "inserted_chunks":no_records
        }
    )