import asyncio

from fastapi import APIRouter, HTTPException
from sqlalchemy import text
from src.core.db import db_helper
from sqlalchemy import select, func

from src.core.models import RespondentsData, PercentResponse

router = APIRouter(tags=["respondents"])


async def get_avg_weight_by_audience(audience_condition: str) -> dict[int, float]:
    # защита от sql инъекции(ради галочки, на самом деле такое не проканает на prod:)
    #
    if ";" in audience_condition:
        raise HTTPException(status_code=400, detail="Недопустимый символ ';'")

    # сам запрос в который передаются аудитории как фильтр
    # query = f"""
    #     SELECT respondent, AVG("weight") AS avg_weight
    #     FROM respondentsdata
    #     WHERE {audience_condition}
    #     GROUP BY respondent
    # """
    async with db_helper.session_getter() as db:
        stmt = (
            select(
                RespondentsData.respondent,
                func.avg(RespondentsData.weight).label("avg_weight"),
            )
            # text сюда передавать небезопасно, но тогда придется парсить строку
            .where(text(audience_condition))
            .group_by(RespondentsData.respondent)
        )

        result = await db.execute(stmt)
        rows = result.all()
        return {row.respondent: float(row.avg_weight) for row in rows}


@router.get("/getPercent", response_model=PercentResponse)
async def get_percent(audience1: str, audience2: str):
    # avg1 = await get_avg_weight_by_audience(db, audience1)
    # avg2 = await get_avg_weight_by_audience(db, audience2)
    avg1, avg2 = await asyncio.gather(get_avg_weight_by_audience(audience1), get_avg_weight_by_audience(audience2))

    set1 = set(avg1.keys())
    set2 = set(avg2.keys())
    intersection = set1 & set2

    sum_a1 = sum(avg1[r] for r in set1)
    sum_overlap = sum(avg1[r] for r in intersection)

    percent = (sum_overlap / sum_a1) if sum_a1 > 0 else 0.0
    return {"percent": percent}
