import os
from pathlib import Path
import shutil
from typing import Annotated
from fastapi import APIRouter, Depends, UploadFile, File, Form
from app.databases import schemas, crud
from app.routers.auth import get_current_user
from databases.getdb import get_db
from databases import models

from sqlalchemy.orm import Session

router = APIRouter(prefix="/users")


def save_upload_file(upload_file: UploadFile, user_id, destination: Path) -> None:
    
    try:
        processing_folder_path = destination / 'profile' / user_id
        processing_folder_path.mkdir(parents=True, exist_ok=True)
        file_path = processing_folder_path / f"{user_id}.{upload_file.filename.split('.')[1]}"
        with file_path.open("wb") as buffer:
            shutil.copyfileobj(upload_file.file, buffer)
    finally:
        upload_file.file.close()


@router.post("/docter/info")
def update_info(files: Annotated[list[UploadFile],File(description="Can take mutiple uploaded files")],docter: schemas.DocterInfo, db: Session = Depends(get_db), doc=Depends(get_current_user)):
    crud.update_docter_info(db=db, docter=docter, docter_id=doc.user_id)


@router.post("/patient/info")
def update_info(files: Annotated[list[UploadFile], File(description="Can take mutiple uploaded files")], age: Annotated[int, Form()], address: Annotated[str, Form()], db: Session = Depends(get_db), pat=Depends(get_current_user)):
    crud.update_patient_info(
        db=db, age=age, address=address, patient_id=pat.user_id)
    for file in files:
        save_upload_file(file, pat.user_id, Path(
            f"{os.getcwd()}/app/static"))


@router.post("/name")
def get_name(user=Depends(get_current_user), db: Session = Depends(get_db)):
    if user.role == "Docter":
        name = crud.get_info(db=db, user_id=user.user_id, model=models.Docter)
        return name
    else:
        name = crud.get_info(db=db, user_id=user.user_id, model=models.Patient)
        return name

@router.post("/history")
def get_patient_history(user = Depends(get_current_user), db: Session = Depends(get_db)):
    result = crud.get_history(user=user,db=db)
    return result


