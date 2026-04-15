from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.schemas import business
from app.schemas.business import BusinessCreate, BusinessLogin, BusinessOut
from app.services.auth_service import register, login
from app.services.email_service import send_reset_email
from sqlalchemy import select
from app.models.business import Business
from fastapi import HTTPException
from app.services.auth_service import generate_reset_token
from app.core.security import create_access_token
from app.core.config import settings
from app.core.security import hash_password
from jose import JWTError, jwt
from app.models.business import Business
from app.core.limiter import limiter
from fastapi import Request


router = APIRouter(prefix="/auth")

@router.post("/register", response_model=BusinessOut)
async def register_user(data: BusinessCreate, db: AsyncSession = Depends(get_db)):
    return await register(db, data)

@router.post("/login")
@limiter.limit("5/minute")
async def login_user(request: Request,data: BusinessLogin, db: AsyncSession = Depends(get_db)):
    token, business = await login(db, data)
    return {"access_token": token, "business": {"id": business.id, "name": business.name, "email": business.email,"type": business.type}}


@router.post("/forgot-password")
async def forgot_password(data: dict, db: AsyncSession = Depends(get_db)):
    email = data.get("email")

    result = await db.execute(select(Business).where(Business.email == email))
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    token = await generate_reset_token(user)

    reset_link = f"http://localhost:3000/reset-password?token={token}"

    await send_reset_email(user.email, reset_link)

    return {"message": "Password reset link sent to email"}


@router.post("/reset-password")
async def reset_password(data: dict, db: AsyncSession = Depends(get_db)):
    token = data.get("token")
    new_password = data.get("password")

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])

        if payload.get("type") != "password_reset":
            raise HTTPException(status_code=400, detail="Invalid token")

        business_id = payload.get("business_id")

        user = await db.get(Business, business_id)

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        user.password = hash_password(new_password)

        await db.commit()

        return {"message": "Password reset successful"}

    except JWTError:
        raise HTTPException(status_code=400, detail="Invalid or expired token")