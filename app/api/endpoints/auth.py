from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from app.core.config import settings
from app.core.security import create_access_token
from app.models.users import UserDB, UserCreate, UserResponse
from app.db.base_db import get_session
from datetime import datetime
import logging
from typing import List

router = APIRouter()

@router.post("/login", 
          summary="User login",
          description="Login with username and password")
def login(user_credentials: OAuth2PasswordRequestForm = Depends()):
    try:
        with get_session() as session:
            user = session.query(UserDB).filter(
                UserDB.username == user_credentials.username
            ).first()
            
            if not user or not user.verify_password(user_credentials.password):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid credentials",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            
            access_token = create_access_token(
                subject=user.username,
                expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
            )
            
            return {
                "access_token": access_token,
                "token_type": "bearer",
                "user_id": user.id,
                "username": user.username
            }
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Login failed: {str(e)}"
        
        
        )
    


@router.post("/register", 
          response_model=UserResponse, 
          status_code=status.HTTP_201_CREATED)
def register_user(user: UserCreate):
    try:
        with get_session() as session:
            
            if session.query(UserDB).filter(UserDB.username == user.username).first():
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Username already taken"
                )
            
            now = datetime.utcnow()
            db_user = UserDB(
                username=user.username,
                hashed_password=UserDB.hash_password(user.password),
                is_active=True,
                created_at=now,
                updated_at=now
            )
            session.add(db_user)
            session.commit()
            session.refresh(db_user)
            return db_user
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create user: {str(e)}"
        )

@router.get("/users", 
         response_model=List[UserResponse],
         summary="Get all users",
         description="Retrieve a list of all registered users")
def get_users():
    try:
        with get_session() as session:
            users = session.query(UserDB).all()
            return users
    except Exception as e:
        logging.error(f"Error retrieving users: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve users"
        )