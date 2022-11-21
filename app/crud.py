from sqlalchemy.orm import Session

from .models import *
from .schema import *
# get all users
def get_all_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()

#get users by phone number
def get_user_by_phone(db: Session, telephone: str):
    return db.query(User).filter(User.telephone == telephone).first()

#get users by address
def get_user_by_adresse(db: Session, add_id: int):
    return db.query(Adresse.users).filter(Adresse.id == add_id).first()

#get all adress
def get_all_adresse(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Adresse).offset(skip).limit(limit).all()

#get address by user
def get_adresse(db: Session, add_id: int):
    return db.query(Adresse).filter(Adresse.id == add_id).first()

# create user
def create_user(db:Session, user : UserBase,add_id : int):
    db_user = User(nom = user.nom,prenom = user.prenom, telephone = user.telephone,adress_id = add_id)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

#create addresse
def create_adresse(db:Session, adresse : AdresseBase):
    db_addresse = Adresse(num_villa=adresse.num_villa, nom_voie = adresse.nom_voie,
    code_postal=adresse.code_postal, ville=adresse.ville,pays= adresse.pays)
    db.add(db_addresse)
    db.commit()
    db.refresh(db_addresse)
    return db_addresse

# activer user
def update_user(db:Session,tel:str):
    user = db.query(User).filter(User.telephone == tel).first()
    user.is_active = True
    db.commit()
    db.refresh(user)
    return user
    
# update addresse
def update_adresse(db:Session, add_id:int, add : AdresseBase):
    adresse = db.query(Adresse).filter(Adresse.id == add_id).first()
    adresse.num_villa = add.num_villa
    adresse.nom_voie = add.nom_voie
    adresse.code_postal = add.code_postal
    adresse.ville = add.ville
    adresse.pays = add.pays
    db.commit()
    db.refresh(adresse)
    return adresse

