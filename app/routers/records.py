from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime
from app.database import get_db
from app import models, schemas
from app.dependencies import get_current_user, require_role
from app.models import UserRole, TransactionType

router = APIRouter()


# Create record (admin only) 

@router.post("/", response_model=schemas.RecordOut, status_code=201)
def create_record(
    record: schemas.RecordCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_role(UserRole.admin))
):
    if record.amount <= 0:
        raise HTTPException(status_code=400, detail="Amount must be greater than 0")

    new_record = models.FinancialRecord(
        **record.model_dump(),
        created_by=current_user.id
    )
    db.add(new_record)
    db.commit()
    db.refresh(new_record)
    return new_record


# Get all records (viewer, analyst, admin) 

@router.get("/", response_model=list[schemas.RecordOut])
def get_records(
    type: Optional[TransactionType] = Query(None),
    category: Optional[str] = Query(None),
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    query = db.query(models.FinancialRecord).filter(
        models.FinancialRecord.is_deleted == False
    )

    if type:
        query = query.filter(models.FinancialRecord.type == type)
    if category:
        query = query.filter(models.FinancialRecord.category.ilike(f"%{category}%"))
    if start_date:
        query = query.filter(models.FinancialRecord.date >= start_date)
    if end_date:
        query = query.filter(models.FinancialRecord.date <= end_date)

    return query.order_by(models.FinancialRecord.date.desc()).all()


#  Get single record 

@router.get("/{record_id}", response_model=schemas.RecordOut)
def get_record(
    record_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    record = db.query(models.FinancialRecord).filter(
        models.FinancialRecord.id == record_id,
        models.FinancialRecord.is_deleted == False
    ).first()
    if not record:
        raise HTTPException(status_code=404, detail="Record not found")
    return record


#  Update record (admin only) 

@router.patch("/{record_id}", response_model=schemas.RecordOut)
def update_record(
    record_id: int,
    update: schemas.RecordUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_role(UserRole.admin))
):
    record = db.query(models.FinancialRecord).filter(
        models.FinancialRecord.id == record_id,
        models.FinancialRecord.is_deleted == False
    ).first()
    if not record:
        raise HTTPException(status_code=404, detail="Record not found")

    if update.amount is not None:
        if update.amount <= 0:
            raise HTTPException(status_code=400, detail="Amount must be greater than 0")
        record.amount = update.amount
    if update.type is not None:
        record.type = update.type
    if update.category is not None:
        record.category = update.category
    if update.date is not None:
        record.date = update.date
    if update.notes is not None:
        record.notes = update.notes

    db.commit()
    db.refresh(record)
    return record


#  Soft delete record (admin only) 

@router.delete("/{record_id}", status_code=204)
def delete_record(
    record_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_role(UserRole.admin))
):
    record = db.query(models.FinancialRecord).filter(
        models.FinancialRecord.id == record_id,
        models.FinancialRecord.is_deleted == False
    ).first()
    if not record:
        raise HTTPException(status_code=404, detail="Record not found")

    record.is_deleted = True
    db.commit()