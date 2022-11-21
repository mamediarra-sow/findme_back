from typing import List
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from .crud import * 
from .models import *
from .schema import *
from .database import SessionLocal, engine
from authy.api import AuthyApiClient
from .config import *
import  phonenumbers

from fastapi.middleware.cors import CORSMiddleware

Base.metadata.create_all(bind=engine)

app = FastAPI()

api = AuthyApiClient(AUTHY_API_KEY)
origins = [
    "https://findme-01.web.app"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
) 

############ Create session #########
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
################ accueil #############
@app.get('/')
async def main():
    return {"message":"hello_world"}

########### post client ###############
@app.post('/sendUser/',response_model=UserSchema)
async def sendClient(user : UserBase, db: Session = Depends(get_db)):
    db_user = get_user_by_phone(db, telephone=user.telephone)
    add = AdresseBase(
        num_villa=0,
        nom_voie="",
        code_postal = "",
        ville = "",
        pays = ""
    )
    count_code = phonenumbers.parse(user.telephone, None).country_code
   
    if db_user:
        raise HTTPException(status_code=400, detail="user already registered")
    api.phones.verification_start(user.telephone, count_code, via="sms")
    adresse = create_adresse(db, add)
    resp = create_user(db=db, user=user,add_id=adresse.id)
    return resp

##### Verifier numéro téléphone #######
@app.get('/verify/{telephone}/{code}')
def verify_phone(code : int, telephone:str, db : Session = Depends(get_db)):
    count_code = phonenumbers.parse(telephone, None).country_code
    verification = api.phones.verification_check(telephone, count_code, code)
    if verification.ok():
        user = update_user(db,telephone)
        return user
    else : 
        raise HTTPException(status_code=400, detail="Code Not Valid")

############ post adresse ################
@app.post('/sendAdress/{telephone}', response_model = AdresseSchema)
async def sendAdress(add:AdresseBase, telephone:str, db:Session = Depends(get_db)):
    db_user = get_user_by_phone(db,telephone=telephone)
    if not db_user:
        raise HTTPException(status_code=404, detail="user not found")
    adresse = update_adresse(db,db_user.adress_id,add)
    return adresse

########## get all users #########
@app.get('/getAdresse/{telephone}', response_model=AdresseSchema)
async def getAdresse( telephone:str, db:Session = Depends(get_db)):
    user = get_user_by_phone(db, telephone)
    if not user:
        raise HTTPException(status_code=404, detail="user not found")
    return get_adresse(db, user.adress_id)

