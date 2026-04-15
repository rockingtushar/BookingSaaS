from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.core.dependencies import get_current_business
from app.models.business import Business
from app.models.service import Service
from app.models.booking import Booking
from app.schemas.service import ServiceCreate
from sqlalchemy import select
from fastapi import HTTPException



router = APIRouter(prefix="/services")

@router.post("/")
async def create_service(
    data: ServiceCreate,
    db: AsyncSession = Depends(get_db),
    business: Business = Depends(get_current_business)
):
    service = Service(name=data.name, description=data.description, price=data.price, duration_minutes=data.duration_minutes, business_id=business.id)
    db.add(service)
    await db.commit()
    await db.refresh(service)
    return service

@router.get("/")
async def get_services(
    db: AsyncSession = Depends(get_db),
    business: Business = Depends(get_current_business)
):
    result = await db.execute(
        select(Service).where(Service.business_id == business.id)
    )

    services = result.scalars().all()

    return services

@router.put("/{service_id}")
async def update_service(
    service_id: int,
    data: ServiceCreate,
    db: AsyncSession = Depends(get_db),
    business: Business = Depends(get_current_business)
):
    result = await db.execute(
        select(Service).where(Service.id == service_id, Service.business_id == business.id)
    )
    service = result.scalar_one_or_none()

    if not service:
        raise HTTPException(status_code=404, detail="Service not found")

    service.name = data.name
    await db.commit()
    await db.refresh(service)

    return service


@router.delete("/{service_id}")
async def delete_service(
    service_id: int,
    db: AsyncSession = Depends(get_db),
    business: Business = Depends(get_current_business)
):
    result = await db.execute(
        select(Service).where(Service.id == service_id, Service.business_id == business.id)
    )
    service = result.scalar_one_or_none()

    if not service:
        raise HTTPException(status_code=404, detail="Service not found")

    booking_check = await db.execute(
        select(Booking).where(Booking.service_id == service_id)
    )
    booking = booking_check.scalar_one_or_none()

    if booking:
        raise HTTPException(
            status_code=400,
            detail="Cannot delete service with existing bookings"
        )

    await db.delete(service)
    await db.commit()

    return {"message": "Service deleted successfully"}



   