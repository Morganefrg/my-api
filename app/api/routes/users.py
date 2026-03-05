from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from typing import List

from app.core.database import SessionLocal
from app.models.models import Utilisateur
from app.api.deps import get_current_user
from pydantic import BaseModel

router = APIRouter(prefix="/users", tags=["users"])


# ─────────────────────────────────────────────
# Schémas Pydantic
# ─────────────────────────────────────────────

class UtilisateurCreate(BaseModel):
    nom: str
    prenom: str
    email: str

class UtilisateurUpdate(BaseModel):
    nom: str | None = None
    prenom: str | None = None
    email: str | None = None

class UtilisateurResponse(BaseModel):
    id_utilisateur: int
    nom: str
    prenom: str
    email: str

    class Config:
        from_attributes = True


# ─────────────────────────────────────────────
# Dépendance BDD
# ─────────────────────────────────────────────

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ─────────────────────────────────────────────
# Endpoints CRUD
# ─────────────────────────────────────────────

# GET tous les utilisateurs
@router.get("/", response_model=List[UtilisateurResponse])
def get_all_users(
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    return db.query(Utilisateur).all()


# GET un utilisateur par ID
@router.get("/{id_utilisateur}", response_model=UtilisateurResponse)
def get_user(
    id_utilisateur: int,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    user = db.query(Utilisateur).filter(Utilisateur.id_utilisateur == id_utilisateur).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Utilisateur non trouvé"
        )
    return user


# POST créer un utilisateur (sans mot de passe - pour admin)
@router.post("/", response_model=UtilisateurResponse, status_code=status.HTTP_201_CREATED)
def create_user(
    user: UtilisateurCreate,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    # Vérifier si l'email existe déjà
    existing = db.query(Utilisateur).filter(Utilisateur.email == user.email).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email déjà utilisé"
        )
    new_user = Utilisateur(
        nom=user.nom,
        prenom=user.prenom,
        email=user.email,
        hashed_password=""
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


# PUT modifier un utilisateur
@router.put("/{id_utilisateur}", response_model=UtilisateurResponse)
def update_user(
    id_utilisateur: int,
    user_update: UtilisateurUpdate,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    user = db.query(Utilisateur).filter(Utilisateur.id_utilisateur == id_utilisateur).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Utilisateur non trouvé"
        )
    if user_update.nom is not None:
        user.nom = user_update.nom
    if user_update.prenom is not None:
        user.prenom = user_update.prenom
    if user_update.email is not None:
        user.email = user_update.email

    db.commit()
    db.refresh(user)
    return user


# DELETE supprimer un utilisateur
@router.delete("/{id_utilisateur}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    id_utilisateur: int,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    user = db.query(Utilisateur).filter(Utilisateur.id_utilisateur == id_utilisateur).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Utilisateur non trouvé"
        )
    db.delete(user)
    db.commit()
    return None