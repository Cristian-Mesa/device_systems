from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict

from app.schemas.device_schema import DeviceSummary


class LoanStatus(str, Enum):
    active = "active"
    returned = "returned"
    overdue = "overdue"


class LoanCreate(BaseModel):
    user_id: int
    device_id: int


class LoanUpdate(BaseModel):
    status: Optional[LoanStatus] = None
    return_date: Optional[datetime] = None


class LoanResponse(BaseModel):
    id: int
    user_id: int
    device_id: int
    loan_date: datetime
    return_date: Optional[datetime]
    status: LoanStatus

    model_config = ConfigDict(from_attributes=True)


class LoanUserSummary(BaseModel):
    id: int
    name: str
    email: str

    model_config = ConfigDict(from_attributes=True)


class LoanDetailResponse(LoanResponse):
    user: LoanUserSummary
    device: DeviceSummary


class LoanReturnResponse(LoanResponse):
    pass
