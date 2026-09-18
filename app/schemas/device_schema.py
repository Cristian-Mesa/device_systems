from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class DeviceBase(BaseModel):
    name: str = Field(min_length=2, max_length=150)
    serial_number: str = Field(min_length=2, max_length=100)
    device_type: str = Field(min_length=2, max_length=50)
    brand: Optional[str] = Field(default=None, max_length=100)
    is_available: bool = True


class DeviceCreate(DeviceBase):
    pass


class DeviceUpdate(DeviceBase):
    pass


class DevicePatch(BaseModel):
    name: Optional[str] = Field(default=None, min_length=2, max_length=150)
    serial_number: Optional[str] = Field(default=None, min_length=2, max_length=100)
    device_type: Optional[str] = Field(default=None, min_length=2, max_length=50)
    brand: Optional[str] = Field(default=None, max_length=100)
    is_available: Optional[bool] = None


class DeviceResponse(DeviceBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class DeviceSummary(BaseModel):
    id: int
    name: str
    serial_number: str
    device_type: str

    model_config = ConfigDict(from_attributes=True)
