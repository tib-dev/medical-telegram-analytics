from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from ..dependencies import get_db
from ..schemas import TopProduct, VisualContentStats

router = APIRouter(prefix="/api/reports", tags=["Reports"])


@router.get("/top-products", response_model=list[TopProduct])
def top_products(limit: int = 10, db: Session = Depends(get_db)):
    query = text("""
        SELECT
            word AS product,
            COUNT(*) AS mention_count
        FROM marts.fct_messages,
             unnest(string_to_array(lower(message_text), ' ')) AS word
        WHERE length(word) > 4
        GROUP BY word
        ORDER BY mention_count DESC
        LIMIT :limit
    """)

    result = db.execute(query, {"limit": limit})
    return result.mappings().all()


@router.get("/visual-content", response_model=list[VisualContentStats])
def visual_content_stats(db: Session = Depends(get_db)):
    query = text("""
        SELECT
            c.channel_name,
            COUNT(*) AS total_messages,
            SUM(CASE WHEN f.has_image THEN 1 ELSE 0 END) AS image_messages,
            ROUND(
                SUM(CASE WHEN f.has_image THEN 1 ELSE 0 END)::decimal
                / COUNT(*), 3
            ) AS image_ratio
        FROM marts.fct_messages f
        JOIN marts.dim_channels c ON f.channel_key = c.channel_key
        GROUP BY c.channel_name
        ORDER BY image_ratio DESC
    """)

    return db.execute(query).mappings().all()
