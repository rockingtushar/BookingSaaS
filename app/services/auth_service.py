from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.business import Business
from fastapi import HTTPException
from app.core.security import hash_password, verify_password, create_access_token

async def register(db: AsyncSession, data):
    user = Business(
        name=data.name,
        email=data.email,
        password=hash_password(data.password),
        type=data.type
    )
    db.add(user)
    await db.commit()
    return user

async def login(db: AsyncSession, data):
    result = await db.execute(select(Business).where(Business.email == data.email))
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if not verify_password(data.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid password")

    token = create_access_token({"business_id": user.id})
    return token, user

async def generate_reset_token(user):
    return create_access_token({"business_id": user.id, "type": "password_reset"})  