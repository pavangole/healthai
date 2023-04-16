
from datetime import datetime
from operator import or_
from pydoc import doc
from unicodedata import name
from sqlalchemy.orm import Session
from sqlalchemy import or_
from databases import models, schemas
from typing import List
from datetime import datetime

def get_time():
    current_time = datetime.now()
    # format current time as MySQL DATETIME string
    return current_time.strftime('%Y-%m-%d %H:%M:%S') 




# generate random user_id that is always unique
def generate_user_id():
    import random
    import string
    user_id = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
    return user_id


def create_user(db: Session, user: schemas.Auth):
    db_user = db.query(models.Auth).filter(models.Auth.email == user.email).first()
    if db_user:
        return None
    id = generate_user_id()
    db_user = models.Auth(email=user.email,password=user.password,user_id=id,role=user.role)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    if user.role == "Docter":
        docter_info(db=db,name=user.name,docter_id=id)
    else:
        patient_info(db=db,name=user.name,patient_id=id)
    return id

def docter_info(db: Session,name,docter_id):
    db_user = models.Docter(name=name,docter_id = docter_id)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return True


def patient_info(db: Session, name, patient_id):
    db_user = models.Patient(name=name,patient_id = patient_id)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return True

def update_docter_info(db: Session,docter: schemas.DocterInfo,docter_id):
    db_user = models.Docter(speciality = docter.speciality, age = docter.age, clinic_address=docter.clinic)
    hello = db_user.__dict__.copy()
    hello.pop('_sa_instance_state')
    db.query(models.Docter).filter(models.Docter.docter_id == docter_id).update(hello)
    db.commit()



def update_patient_info(db: Session,age,address,patient_id):
    db_user = models.Patient(age=age,address = address)
    hello = db_user.__dict__.copy()
    hello.pop('_sa_instance_state')
    print(hello)
    db.query(models.Patient).filter(models.Patient.patient_id == patient_id).update(hello)
    db.commit()


def get_user_by_email(db: Session, email: str):
    return db.query(models.Auth).filter(models.Auth.email == email).first()


def get_user_by_id(db: Session, user_id: str):
    return db.query(models.Auth).filter(models.Auth.user_id == user_id).first()


def get_info(db: Session, user_id: str, model):
    if model == models.Patient:
        return db.query(model).filter(model.patient_id == user_id).first()
    else:
        return db.query(model).filter(model.docter_id == user_id).first()


def create_patient_history(db: Session, patient_id,disease,image,scan_type):
    db_user = models.patientHistory(patient_id=patient_id,disease=disease,image=image,date=get_time(),scan_type=scan_type)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return True


def get_history(user: schemas.Auth,db):
    if user.role == "Docter":
        return db.query(models.Docter).filter(models.Docter.docter_id == user.user_id).all()
    else:
        return db.query(models.patientHistory).filter(models.patientHistory.patient_id == user.user_id).all()
# def create_user_info(db: Session, user: schemas.User):
#     result = get_user_by_email(db, user.email)
#     if result.age is not None:
#         return False
#     db_user = models.User(club_member_status=user.club_member_status,
#                           fashion_news_frequency=user.fashion_news_frequency, age=user.age,
#                           postal_code=user.postal_code, name=user.name)
#     hello = db_user.__dict__.copy()
#     hello.pop('_sa_instance_state')
#     db.query(models.User).filter(models.User.email == user.email).update(hello)
#     db.commit()
#     return True


# def update_user_info(db: Session, update_items: dict, user_id: str):
#     print("I am in Crud")
#     db.query(models.User).filter(models.User.user_id == user_id).update(update_items)
#     db.commit()


# def get_transactions_by_id(db: Session, id: str):
#     # return all transactions and items descrption and price for a user id
#     return db.query(models.Transactions, models.Item).filter(models.Transactions.user_id == id).join(models.Item).all()


# def creat_item(db: Session, item: schemas.ItemBase):
#     # check item already exists otherwise create item
#     db_item = db.query(models.Item).filter(models.Item.item_id == item.item_id).first()
#     if db_item:
#         return False
#     db_item = models.Item(item_id=item.item_id, product_name=item.product_name,
#                           product_type_no=item.product_type_no, product_group_name=item.product_group_name,
#                           graphical_appearance_no=item.graphical_appearance_no,
#                           colour_group_code=item.colour_group_code,
#                           department_no=item.department_no, index_code=item.index_code,
#                           index_group_no=item.index_group_no,
#                           section_no=item.section_no, garment_group_no=item.garment_group_no,
#                           description=item.description,
#                           price=item.price)
#     db.add(db_item)
#     db.commit()
#     db.refresh(db_item)
#     return True


# def create_transactions(db: Session, transaction: schemas.Transactions):
#     # create transaction
#     db_transaction = models.Transactions(user_id=transaction.user_id, item_id=transaction.item_id,
#                                          sales_channel_id=transaction.sales_channel_id, timestamp=get_current_time(),
#                                          event_type=transaction.event_type)

#     db.add(db_transaction)
#     db.commit()
#     db.refresh(db_transaction)
#     return True




# def get_items_by_item_id(db: Session, item_ids: List[str]):
#     return db.query(models.Item).filter(or_(*[models.Item.item_id == id for id in item_ids])).all()

# def get_transactions_for_item(db: Session , user_id: str):
#     return db.query(models.Transactions).filter(models.Transactions.user_id == user_id).first()

# def update_password(db: Session, email: str,update_items):
#     db.query(models.User).filter(models.User.email == email).update(update_items)
#     db.commit()

# def suggest(db, query):
#     result =  db.query(models.Item).filter(models.Item.product_name.like('%' + query + '%')).limit(50).distinct().all()
#     items =  [item.product_name for item in result]
#     return set(items)

