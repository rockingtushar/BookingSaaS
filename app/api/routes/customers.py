from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.core.dependencies import get_current_business
from app.models.customer import Customer
from app.schemas.customer import CustomerCreate
from app.models.business import Business
from app.models.booking import Booking
from sqlalchemy import select
from fastapi import HTTPException

router = APIRouter(prefix="/customers")

@router.post("/")
async def create_customer(
    data: CustomerCreate,
    db: AsyncSession = Depends(get_db),
    business: Business = Depends(get_current_business)
):
    # # Yeh
    # customer = Customer(**data.dict(), business_id=business.id)
    # # Iska jagah
    # customer = Customer(**data.model_dump(), business_id=business.id)
    
    customer = Customer(**data.model_dump(), business_id=business.id)
    db.add(customer)
    await db.commit()
    await db.refresh(customer)
    return customer

@router.get("/")
async def get_customers(
    db: AsyncSession = Depends(get_db),
    business: Business = Depends(get_current_business)
):
    result = await db.execute(
        select(Customer).where(Customer.business_id == business.id)
    )
    return result.scalars().all()


@router.put("/{customer_id}")
async def update_customer(
    customer_id: int,
    data: CustomerCreate,
    db: AsyncSession = Depends(get_db),
    business: Business = Depends(get_current_business)
):
    result = await db.execute(
        select(Customer).where(Customer.id == customer_id, Customer.business_id == business.id)
    )
    customer = result.scalar_one_or_none()
    if not customer:
         raise HTTPException(status_code=404, detail="Customer not found")
    
    customer.name = data.name
    customer.phone = data.phone

    await db.commit()
    await db.refresh(customer)

    return customer

@router.delete("/{customer_id}")
async def delete_customer(
    customer_id: int,
    db: AsyncSession = Depends(get_db),
    business: Business = Depends(get_current_business)
):
    result = await db.execute(
        select(Customer).where(Customer.id == customer_id, Customer.business_id == business.id)
    )
    customer = result.scalar_one_or_none()
    if not customer:
         raise HTTPException(status_code=404, detail="Customer not found")
    
    booking_check = await db.execute(
        select(Booking).where(Booking.customer_id == customer_id)
    )
    booking = booking_check.scalar_one_or_none()

    if booking:
        raise HTTPException(
            status_code=400,
            detail="Cannot delete customer with existing bookings"
        )

    # 3. delete
    await db.delete(customer)
    await db.commit()

    return {"message": "Customer deleted successfully"}