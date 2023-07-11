from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from .base import DATE_FORMAT, OPERATIONS


@dataclass
class Operation:
    user_id: int | str
    state: str
    direction: str
    income: str
    sum: float
    credit: str
    date: datetime | str
    username: str = None
    id: int = None
    comment: str = None

    def to_row(self):
        return (self.id, self.user_id, self.username, self.state, self.direction, self.income, self.sum, self.credit, self.date, self.comment)
    

async def create_operation(operation: Operation):
    row = operation.to_row()
    OPERATIONS.append_row(row)
    return True


