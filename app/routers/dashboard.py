from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, extract
from typing import Optional
from datetime import datetime
from app.database import get_db
from app import models
from app.dependencies import require_role
from app.models import UserRole, TransactionType

router = APIRouter()


def analyst_or_admin(current_user=Depends(require_role(UserRole.analyst, UserRole.admin))):
    return current_user


# Summary 

@router.get("/summary")
def get_summary(
    db: Session = Depends(get_db),
    current_user=Depends(require_role(UserRole.analyst, UserRole.admin))
):
    records = db.query(models.FinancialRecord).filter(
        models.FinancialRecord.is_deleted == False
    ).all()

    total_income = sum(r.amount for r in records if r.type == TransactionType.income)
    total_expenses = sum(r.amount for r in records if r.type == TransactionType.expense)

    return {
        "total_income": round(total_income, 2),
        "total_expenses": round(total_expenses, 2),
        "net_balance": round(total_income - total_expenses, 2),
        "total_records": len(records)
    }


# Category wise totals 

@router.get("/by-category")
def get_by_category(
    db: Session = Depends(get_db),
    current_user=Depends(require_role(UserRole.analyst, UserRole.admin))
):
    records = db.query(models.FinancialRecord).filter(
        models.FinancialRecord.is_deleted == False
    ).all()

    result = {}
    for r in records:
        if r.category not in result:
            result[r.category] = {"income": 0.0, "expense": 0.0}
        result[r.category][r.type.value] += r.amount

    return result


#  Monthly trends 

@router.get("/trends")
def get_monthly_trends(
    db: Session = Depends(get_db),
    current_user=Depends(require_role(UserRole.analyst, UserRole.admin))
):
    records = db.query(models.FinancialRecord).filter(
        models.FinancialRecord.is_deleted == False
    ).all()

    trends = {}
    for r in records:
        key = r.date.strftime("%Y-%m")
        if key not in trends:
            trends[key] = {"income": 0.0, "expense": 0.0}
        trends[key][r.type.value] += r.amount

    sorted_trends = dict(sorted(trends.items()))
    return sorted_trends


#  Recent activity 

@router.get("/recent")
def get_recent(
    limit: int = Query(default=10, le=50),
    db: Session = Depends(get_db),
    current_user=Depends(require_role(UserRole.analyst, UserRole.admin))
):
    records = db.query(models.FinancialRecord).filter(
        models.FinancialRecord.is_deleted == False
    ).order_by(models.FinancialRecord.date.desc()).limit(limit).all()

    return [
        {
            "id": r.id,
            "amount": r.amount,
            "type": r.type,
            "category": r.category,
            "date": r.date,
            "notes": r.notes
        }
        for r in records
    ]