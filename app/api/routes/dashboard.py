from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.core.dependencies import get_current_business
from app.services.dashboard_service import get_dashboard_data
from app.models.business import Business

router = APIRouter(prefix="/dashboard")

@router.get("/")
async def dashboard(
    db: AsyncSession = Depends(get_db),
    business: Business = Depends(get_current_business)
):
    return await get_dashboard_data(db, business.id)