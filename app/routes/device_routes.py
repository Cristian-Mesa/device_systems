from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.dependencies.database_dependency import get_db
from app.schemas.device_schema import DeviceCreate, DevicePatch, DeviceResponse, DeviceUpdate
from app.schemas.loan_schema import LoanDetailResponse
from app.services import device_service, loan_service


router = APIRouter(prefix="/devices", tags=["Devices"])


@router.get("", response_model=list[DeviceResponse], summary="Listar dispositivos")
def list_devices(
    device_type: Optional[str] = Query(default=None),
    is_available: Optional[bool] = Query(default=None),
    brand: Optional[str] = Query(default=None),
    search: Optional[str] = Query(default=None),
    db: Session = Depends(get_db),
):
    return device_service.list_devices(db, device_type, is_available, brand, search)


@router.get("/{device_id}", response_model=DeviceResponse, summary="Obtener dispositivo")
def get_device(device_id: int, db: Session = Depends(get_db)):
    device = device_service.get_device_by_id(db, device_id)
    if not device:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Dispositivo no encontrado")
    return device


@router.post("", response_model=DeviceResponse, status_code=status.HTTP_201_CREATED, summary="Crear dispositivo")
def create_device(device_data: DeviceCreate, db: Session = Depends(get_db)):
    if device_service.get_device_by_serial_number(db, device_data.serial_number):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El numero de serie ya esta registrado")
    return device_service.create_device(db, device_data)


@router.put("/{device_id}", response_model=DeviceResponse, summary="Actualizar dispositivo completo")
def update_device(device_id: int, device_data: DeviceUpdate, db: Session = Depends(get_db)):
    device = device_service.get_device_by_id(db, device_id)
    if not device:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Dispositivo no encontrado")

    duplicate = device_service.get_device_by_serial_number(db, device_data.serial_number)
    if duplicate and duplicate.id != device_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El numero de serie ya esta registrado")
    return device_service.update_device(db, device, device_data)


@router.patch("/{device_id}", response_model=DeviceResponse, summary="Actualizar dispositivo parcialmente")
def patch_device(device_id: int, device_data: DevicePatch, db: Session = Depends(get_db)):
    device = device_service.get_device_by_id(db, device_id)
    if not device:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Dispositivo no encontrado")

    if device_data.serial_number:
        duplicate = device_service.get_device_by_serial_number(db, device_data.serial_number)
        if duplicate and duplicate.id != device_id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El numero de serie ya esta registrado")
    return device_service.update_device(db, device, device_data, partial=True)


@router.delete("/{device_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Eliminar dispositivo")
def delete_device(device_id: int, db: Session = Depends(get_db)):
    device = device_service.get_device_by_id(db, device_id)
    if not device:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Dispositivo no encontrado")
    if loan_service.list_loans_for_device(db, device_id):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="No se puede eliminar un dispositivo con prestamos registrados",
        )
    device_service.delete_device(db, device)


@router.get("/{device_id}/loans", response_model=list[LoanDetailResponse], summary="Historial de prestamos del dispositivo")
def get_device_loans(device_id: int, db: Session = Depends(get_db)):
    device = device_service.get_device_by_id(db, device_id)
    if not device:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Dispositivo no encontrado")
    return loan_service.list_loans_for_device(db, device_id)
