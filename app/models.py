from sqlalchemy import Boolean, Column,ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from .database import Base
######## Création du modèle user sqlachemy #############
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nom = Column(String(100))    
    prenom = Column(String(100))
    telephone = Column(String(100), unique=True, index=True)
    is_active = Column(Boolean, default=False)
    adress_id = Column(Integer, ForeignKey("adresses.id"))
    adresse = relationship("Adresse",back_populates="users")
######## Création du modèle Adresse sqlachemy #############
class Adresse(Base):
    __tablename__='adresses'
    id = Column(Integer, primary_key=True, index=True,autoincrement=True)
    num_villa = Column(Integer)
    nom_voie = Column(String(100))
    code_postal = Column(String(100))
    ville = Column(String(100))
    pays = Column(String(100))
    users = relationship("User", back_populates="adresse")
