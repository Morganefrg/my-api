from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.models import Base

# DATABASE_URL ="mssql+pyodbc://api_user:cestlaVM69170@localhost/my_api_db?driver=ODBC+Driver+17+for+SQL+Server&TrustServerCertificate=yes"
DATABASE_URL = "sqlite:///./my_api.db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

def create_tables():
    Base.metadata.create_all(bind=engine)