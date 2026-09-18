from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.dependencies.database_dependency import get_db
from app.schemas.loan_schema import LoanCreate, LoanDetailResponse, LoanResponse
from app.services import device_service, loan_service, user_service


router = APIRouter(prefix="/loans", tags=["Loans"])


@router.get("", response_model=list[LoanDetailResponse], summary="Listar prestamos con filtros")
def list_loans(
    status_filter: Optional[str] = Query(default=None, alias="status"),
    user_email: Optional[str] = Query(default=None),
    device_type: Optional[str] = Query(default=None),
    db: Session = Depends(get_db),
):
    return loan_service.list_loans(db, status_filter, user_email, device_type)


@router.get("/details", response_model=list[LoanDetailResponse], summary="Consultar detalle de prestamos")
def loan_details(db: Session = Depends(get_db)):
    return loan_service.list_loans(db)


@router.get("/{loan_id}", response_model=LoanDetailResponse, summary="Obtener prestamo")
def get_loan(loan_id: int, db: Session = Depends(get_db)):
    loan = loan_service.get_loan_by_id(db, loan_id)
    if not loan:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Prestamo no encontrado")
    return loan


@router.post("", response_model=LoanResponse, status_code=status.HTTP_201_CREATED, summary="Registrar prestamo")
def create_loan(loan_data: LoanCreate, db: Session = Depends(get_db)):
    user = user_service.obtener_usuario_por_id(db, loan_data.user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")

    device = device_service.get_device_by_id(db, loan_data.device_id)
    if not device:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Dispositivo no encontrado")
    if not device.is_available:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="El dispositivo no est? disponible")

    return loan_service.create_loan(db, user, device)


@router.patch("/{loan_id}/return", response_model=LoanResponse, summary="Devolver dispositivo")
def return_loan(loan_id: int, db: Session = Depends(get_db)):
    loan = loan_service.get_loan_by_id(db, loan_id)
    if not loan:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pr?stamo no encontrado")
    if loan.status == "returned":
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="El pr?stamo ya fue devuelto")
    return loan_service.return_loan(db, loan)
