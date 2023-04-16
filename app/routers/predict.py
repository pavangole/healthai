from pathlib import Path
import os
from sqlalchemy.orm import Session
import shutil
from typing import Annotated
from fastapi import APIRouter, File, UploadFile, Depends
from databases import crud
from databases.getdb import get_db
from routers.auth import get_current_user
# from mlmodel.braintumor import create_data_batches, model, get_pred_label
from mlmodel import braintumor
from mlmodel import diabetic_retinopathy as reti
router = APIRouter(prefix="/predict")


def save_upload_file(upload_file: UploadFile, user_id, destination: Path) -> None:
    try:
        processing_folder_path = destination / user_id / 'processing'
        processing_folder_path.mkdir(parents=True, exist_ok=True)
        newf = destination / user_id / 'processed'
        newf.mkdir(parents=True,exist_ok=True)
        file_path = processing_folder_path / upload_file.filename
        with file_path.open("wb") as buffer:
            shutil.copyfileobj(upload_file.file, buffer)
    finally:
        upload_file.file.close()


@router.post("/upload")
def identify_disease(files: Annotated[list[UploadFile], File(description="Can take mutiple uploaded files")], user=Depends(get_current_user),db: Session=Depends(get_db)):
    
    user_id = user.user_id
    filename=[]
    for file in files:
        save_upload_file(file, user_id, Path(
            f"{os.getcwd()}/app/storage"))
        filename.append(file.filename)
    custom_path = f"{os.getcwd()}/app/storage/{user_id}/processing/"
    custom_image_paths = [custom_path +
                          fname for fname in os.listdir(custom_path)]
    # Turn custom images into batch datasets
    custom_data = braintumor.create_data_batches(custom_image_paths, test_data=True)
    # Make predictions on the custom data
    custom_preds =  braintumor.model.predict(custom_data)
    # Get custom image prediction labels
    custom_pred_labels = [braintumor.get_pred_label(
        custom_preds[i]) for i in range(len(custom_preds))]
    for i in range(0,len(custom_pred_labels)):
        print("hello")
        crud.create_patient_history(patient_id=user_id,db=db,disease=custom_pred_labels[i],image=filename[i])
    src_dir = f"{os.getcwd()}/app/storage/{user_id}/processing"
    dst_dir = f"{os.getcwd()}/app/storage/{user_id}/processed"

    # iterate over files in source directory and move them to destination directory
    for filename in os.listdir(src_dir):
        src_path = os.path.join(src_dir, filename)
        dst_path = os.path.join(dst_dir, filename)
        shutil.move(src_path, dst_path)
    return custom_pred_labels


@router.post("/upload/retino")
def identify_disease(files: Annotated[list[UploadFile], File(description="Can take mutiple uploaded files")], user=Depends(get_current_user),db: Session=Depends(get_db)):
    
    user_id = user.user_id
    filename=[]
    for file in files:
        save_upload_file(file, user_id, Path(
            f"{os.getcwd()}/app/storage"))
        filename.append(file.filename)
    custom_path = f"{os.getcwd()}/app/storage/{user_id}/processing/"
    custom_image_paths = [custom_path +
                          fname for fname in os.listdir(custom_path)]
    # Turn custom images into batch datasets
    custom_data = reti.create_data_batches(custom_image_paths, test_data=True)
    # Make predictions on the custom data
    custom_preds =  reti.model.predict(custom_data)
    # Get custom image prediction labels
    custom_pred_labels = [reti.get_pred_label(
        custom_preds[i]) for i in range(len(custom_preds))]
    for i in range(0,len(custom_pred_labels)):
        print("hello")
        crud.create_patient_history(patient_id=user_id,db=db,disease=custom_pred_labels[i],image=filename[i])
    src_dir = f"{os.getcwd()}/app/storage/{user_id}/processing"
    dst_dir = f"{os.getcwd()}/app/storage/{user_id}/processed"

    # iterate over files in source directory and move them to destination directory
    for filename in os.listdir(src_dir):
        src_path = os.path.join(src_dir, filename)
        dst_path = os.path.join(dst_dir, filename)
        shutil.move(src_path, dst_path)
    return custom_pred_labels
