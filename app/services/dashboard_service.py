from sqlalchemy import select, func
from datetime import datetime, date
from app.models.booking import Booking
from app.models.customer import Customer
from app.models.service import Service

async def get_dashboard_data(db, business_id):

    # total bookings
    bookings_result = await db.execute(
        select(func.count(Booking.id)).where(Booking.business_id == business_id)
    )
    total_bookings = bookings_result.scalar()

    # total customers
    customers_result = await db.execute(
        select(func.count(Customer.id)).where(Customer.business_id == business_id)
    )
    total_customers = customers_result.scalar()

    # total services
    services_result = await db.execute(
        select(func.count(Service.id)).where(Service.business_id == business_id)
    )
    total_services = services_result.scalar()

    # today bookings
    today = date.today()

    today_result = await db.execute(
        select(func.count(Booking.id)).where(
            Booking.business_id == business_id,
            func.date(Booking.date) == today
        )
    )
    today_bookings = today_result.scalar()

    return {
        "total_bookings": total_bookings,
        "total_customers": total_customers,
        "total_services": total_services,
        "today_bookings": today_bookings
    }