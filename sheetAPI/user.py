from dataclasses import dataclass
from datetime import datetime
from .base import USERS, DATE_FORMAT


@dataclass
class User:
    user_id: int | str
    reg_date: datetime
    username: str = None
    credits: list[str] = None

    def __post_init__(self):
        self.user_id = int(self.user_id)
        self.credits = [credit.strip() for credit in self.credits.split('|')] if self.credits else []
        self.reg_date = datetime.strptime(self.reg_date, DATE_FORMAT)
    
    def to_row(self):
        date = self.reg_date.strftime(DATE_FORMAT)
        credits = ' | '.join(self.credits)
        return (self.user_id, self.username, date, credits)


async def get_user_by_id(user_id: str|int):
    cell = USERS.find(query=str(user_id), in_column=1)
    if cell:
        user_row = USERS.row_values(cell.row)
        try:
            user = User(user_id=user_row[0], username=user_row[1], reg_date=user_row[2], credits=user_row[3] if len(user_row) == 4 else None)
        except Exception as ex:
            user = None
            print(ex)
        return user


async def create_user(user: User):
    row = user.to_row()
    USERS.append_row(row)
    return True


async def edit_user_credits(user_id: int|str, credits: list[str]):
    cell = USERS.find(query=str(user_id), in_column=1)
    if cell:
        row = cell.row
        credits_str = ' | '.join(credits)
        USERS.update_cell(row=row, col=4, value=credits_str)
        return True
