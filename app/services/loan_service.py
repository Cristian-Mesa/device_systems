from datetime import datetime, timezone
from typing import Optional

from sqlalchemy.orm import Session, joinedload

from app.models.device_model import Device
from app.models.loan_model import Loan
from app.models.user_model import User


def get_loan_by_id(db: Session, loan_id: int) -> Optional[Loan]:
    return (
        db.query(Loan)
        .options(joinedload(Loan.user), joinedload(Loan.device))
        .filter(Loan.id == loan_id)
        .first()
    )


def list_loans(
    db: Session,
    status: Optional[str] = None,
    user_email: Optional[str] = None,
    device_type: Optional[str] = None,
) -> list[Loan]:
    query = db.query(Loan).join(Loan.user).join(Loan.device)

    if status:
        query = query.filter(Loan.status == status)
    if user_email:
        query = query.filter(User.email == user_email)
    if device_type:
        query = query.filter(Device.device_type == device_type)

    return (
        query.options(joinedload(Loan.user), joinedload(Loan.device))
        .order_by(Loan.loan_date.desc())
        .all()
    )


def list_loans_for_user(db: Session, user_id: int) -> list[Loan]:
    return (
        db.query(Loan)
        .options(joinedload(Loan.user), joinedload(Loan.device))
        .filter(Loan.user_id == user_id)
        .order_by(Loan.loan_date.desc())
        .all()
    )


def list_loans_for_device(db: Session, device_id: int) -> list[Loan]:
    return (
        db.query(Loan)
        .options(joinedload(Loan.user), joinedload(Loan.device))
        .filter(Loan.device_id == device_id)
        .order_by(Loan.loan_date.desc())
        .all()
    )


def create_loan(db: Session, user: User, device: Device) -> Loan:
    loan = Loan(user=user, device=device, status="active")
    device.is_available = False
    db.add(loan)
    db.commit()
    db.refresh(loan)
    return loan


def return_loan(db: Session, loan: Loan) -> Loan:
    loan.status = "returned"
    loan.return_date = datetime.now(timezone.utc)
    loan.device.is_available = True
    db.commit()
    db.refresh(loan)
    return loan
