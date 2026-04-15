from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException
from app.models.booking import Booking
from app.models.customer import Customer
from app.models.service import Service
from app.services.whatsapp_service import generate_whatsapp_link

async def create_booking(db: AsyncSession, business_id, data):

    stmt = select(Booking).where(
        Booking.business_id == business_id,
        Booking.date == data.date.replace(tzinfo=None)
    )

    result = await db.execute(stmt)
    existing = result.scalar_one_or_none()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Slot already booked"
        )

    booking = Booking(
        business_id=business_id,
        customer_id=data.customer_id,
        service_id=data.service_id,
        date=data.date.replace(tzinfo=None)
    )
    db.add(booking)
    await db.commit()
    await db.refresh(booking)
    
    customer = await db.get(Customer, data.customer_id)
    service = await db.get(Service, data.service_id)

    message = f"""
Namaste {customer.name},

Your booking is confirmed.

Service: {service.name}
Date: {data.date}

Thank you 🙏
"""

    link = generate_whatsapp_link(customer.phone, message)

    return {"booking_id": booking.id, "whatsapp_link": link}