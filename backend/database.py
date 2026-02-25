from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Replace these with your actual SQL Server details
SERVER = "your_server_name"
DATABASE = "your_database_name"
USERNAME = "your_username"
PASSWORD = "your_password"

# Connection string for SQL Server
DATABASE_URL = f"mssql+pyodbc://{USERNAME}:{PASSWORD}@{SERVER}/{DATABASE}?driver=ODBC+Driver+18+for+SQL+Server"

# Create engine and session
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()
