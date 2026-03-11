from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.core.password import verify_password, hash_password
from app.core.security import create_access_token
from app.core.database import SessionLocal
from app.models.schemas import Token, UserCreate, UserResponse
from app.models.models import Utilisateur
from ldap_auth import authenticate_ldap

router = APIRouter(prefix="/auth", tags=["auth"])


# Dépendance pour obtenir une session BDD
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def authenticate_user(db: Session, username: str, password: str):
    # 1) Vérifier via LDAP
    ldap_ok = authenticate_ldap(username, password)
    if not ldap_ok:
        return None
    
    # 2) Cherche l'utilisateur en BDD par email
    user = db.query(Utilisateur).filter(Utilisateur.email == username).first()
    if not user:
        # Si l'utilisateur n'existe pas en BDD on le crée automatiquement
        hashed = hash_password(password)
        user = Utilisateur(
            nom="",
            prenom="",
            email=username,
            hashed_password=hashed,
        )
        db.add(user)
        db.commit()
        db.refresh(user)
    
    return user


@router.post("/token", response_model=Token)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Identifiants invalides",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token = create_access_token(user.email)
    return {"access_token": token, "token_type": "bearer"}


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(user: UserCreate, db: Session = Depends(get_db)):
    # 1) Vérifier si l'email existe déjà
    existing = db.query(Utilisateur).filter(Utilisateur.email == user.username).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email déjà utilisé",
        )

    # 2) Hasher le mot de passe
    hashed = hash_password(user.password)

    # 3) Créer l'utilisateur en BDD
    new_user = Utilisateur(
        nom="",
        prenom="",
        email=user.username,
        hashed_password=hashed,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # 4) Réponse
    return {"message": "Utilisateur créé", "username": new_user.email}