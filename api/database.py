from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.dependencies import Depends
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from typing import List
import os
from .config import settings  # Import settings from config.py
import openai  # Import OpenAI library with version 1.52.0
from .models import User  # Import User model from models.py


# Define a global variable for the database connection
engine = create_engine(settings.DATABASE_URL)  # Create an engine using the database URL from settings.py
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)  # Create a sessionmaker
Base = declarative_base()  # Create a base for declarative models


# Define a dependency function to get the database session
def get_db():
    db = SessionLocal()  # Create a database session
    try:
        yield db  # Yield the database session
    finally:
        db.close()  # Close the database session


# Define a database model for storing users
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)
    # Add more fields as needed

    def __repr__(self):
        return f"<User {self.username}>"


# Function to create a new user in the database
def create_user(db: Session, user: User):
    db.add(user)  # Add the new user object to the database session
    db.commit()  # Commit the changes to the database
    db.refresh(user)  # Refresh the user object with the new database ID
    return user


# Function to get a user by ID from the database
def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()  # Query the database for the user by ID


# Function to get a user by username from the database
def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()


# Function to update a user's data in the database
def update_user(db: Session, user_id: int, user: User):
    db_user = db.query(User).filter(User.id == user_id).first()  # Query the database for the user by ID
    if db_user:
        db_user.username = user.username  # Update the user's username
        db_user.password = user.password  # Update the user's password
        db.commit()  # Commit the changes to the database
        db.refresh(db_user)  # Refresh the user object with the updated data
        return db_user
    else:
        return None


# Function to delete a user from the database
def delete_user(db: Session, user_id: int):
    db_user = db.query(User).filter(User.id == user_id).first()  # Query the database for the user by ID
    if db_user:
        db.delete(db_user)  # Delete the user from the database session
        db.commit()  # Commit the changes to the database
        return True
    else:
        return False


# Function to get all users from the database
def get_all_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()  # Query the database for all users


# Initialize the database
Base.metadata.create_all(bind=engine)  # Create all database tables defined in the models