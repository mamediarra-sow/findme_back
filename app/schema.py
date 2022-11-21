from pydantic import BaseModel
from typing import List, Union


########## Adreese ################
class UserBase(BaseModel):
    nom : str
    prenom : str
    telephone : str

class UserSchema(UserBase):
    id : int
    adress_id : int 
    is_active : bool

    class Config:
       orm_mode = True


######### Adresse ##########""""
class AdresseBase(BaseModel):
    num_villa : int
    nom_voie : str
    code_postal : str
    ville : str
    pays : str
    
class AdresseSchema(AdresseBase):
    id : int
    users : List[UserSchema] = []

    class Config:
        orm_mode = True
