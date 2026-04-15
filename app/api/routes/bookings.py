from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.core.dependencies import get_current_business
from app.schemas.booking import BookingCreate
from app.services.booking_service import create_booking
from app.models.business import Business
from app.models.booking import Booking
from sqlalchemy import select
from fastapi import HTTPException
from typing import Optional

router = APIRouter(prefix="/bookings")

@router.post("/")
async def create_booking_api(
    data: BookingCreate,
    db: AsyncSession = Depends(get_db),
    business: Business = Depends(get_current_business)
):
    return await create_booking(db, business.id, data)


@router.get("/")
async def get_bookings(
    db: AsyncSession = Depends(get_db),
    business: Business = Depends(get_current_business),
    customer_id: Optional[int] = None
):
  
    query = select(Booking).where(Booking.business_id == business.id)

    if customer_id:
        query = query.where(Booking.customer_id == customer_id)

    result = await db.execute(query)
    return result.scalars().all()


@router.put("/{booking_id}")
async def update_booking_status(
    booking_id: int,
    status: str,
    db: AsyncSession = Depends(get_db),
    business: Business = Depends(get_current_business)
):
    result = await db.execute(
        select(Booking).where(
            Booking.id == booking_id,
            Booking.business_id == business.id
        )
    )
    booking = result.scalar_one_or_none()

    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")

    booking.status = status  # confirmed / cancelled / completed

    await db.commit()
    await db.refresh(booking)

    return booking