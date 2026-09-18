from typing import Optional

from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.models.device_model import Device
from app.schemas.device_schema import DeviceCreate, DevicePatch, DeviceUpdate


def get_device_by_id(db: Session, device_id: int) -> Optional[Device]:
    return db.query(Device).filter(Device.id == device_id).first()


def get_device_by_serial_number(db: Session, serial_number: str) -> Optional[Device]:
    return db.query(Device).filter(Device.serial_number == serial_number).first()


def list_devices(
    db: Session,
    device_type: Optional[str] = None,
    is_available: Optional[bool] = None,
    brand: Optional[str] = None,
    search: Optional[str] = None,
) -> list[Device]:
    query = db.query(Device)

    if device_type:
        query = query.filter(Device.device_type == device_type)
    if is_available is not None:
        query = query.filter(Device.is_available == is_available)
    if brand:
        query = query.filter(Device.brand.ilike(f"%{brand}%"))
    if search:
        term = f"%{search}%"
        query = query.filter(
            or_(
                Device.name.ilike(term),
                Device.serial_number.ilike(term),
                Device.brand.ilike(term),
            )
        )

    return query.order_by(Device.created_at.desc()).all()


def create_device(db: Session, device_data: DeviceCreate) -> Device:
    device = Device(**device_data.model_dump())
    db.add(device)
    db.commit()
    db.refresh(device)
    return device


def update_device(
    db: Session, device: Device, device_data: DeviceUpdate | DevicePatch, partial: bool = False
) -> Device:
    values = device_data.model_dump(exclude_unset=partial)
    for field, value in values.items():
        setattr(device, field, value)
    db.commit()
    db.refresh(device)
    return device


def delete_device(db: Session, device: Device) -> None:
    db.delete(device)
    db.commit()
