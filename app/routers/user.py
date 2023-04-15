
from fastapi import APIRouter, Depends
from app.databases import schemas,crud
from app.routers.auth import get_current_user
from databases.getdb import get_db

from sqlalchemy.orm import Session

router = APIRouter(prefix="/users")


@router.post("/docter/info")
def update_info(docter: schemas.DocterInfo,db: Session = Depends(get_db),doc=Depends(get_current_user)):
    crud.update_docter_info(db=db,docter=docter,docter_id=doc.user_id)



@router.post("/patient/info")
def update_info(patient: schemas.PatientInfo,db: Session = Depends(get_db),pat=Depends(get_current_user)):
    crud.update_patient_info(db=db,patient=patient,patient_id=pat.user_id)