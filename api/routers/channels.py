from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from ..dependencies import get_db
from ..schemas import ChannelActivity

router = APIRouter(prefix="/api/channels", tags=["Channels"])


@router.get("/{channel_name}/activity", response_model=list[ChannelActivity])
def channel_activity(channel_name: str, db: Session = Depends(get_db)):
    query = text("""
        SELECT
            d.full_date::text AS date,
            COUNT(*) AS message_count,
            AVG(f.view_count) AS avg_views
        FROM marts.fct_messages f
        JOIN marts.dim_channels c ON f.channel_key = c.channel_key
        JOIN marts.dim_dates d ON f.date_key = d.date_key
        WHERE c.channel_name = :channel
        GROUP BY d.full_date
        ORDER BY d.full_date
    """)

    result = db.execute(query, {"channel": channel_name}).mappings().all()

    if not result:
        raise HTTPException(status_code=404, detail="Channel not found")

    return result
