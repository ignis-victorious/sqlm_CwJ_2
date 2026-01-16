#
#  Import LIBRARIES
from datetime import datetime, timezone

from sqlmodel import Field, SQLModel

# ,Session, create_engine, select

#  Import FILES
#
#  ______________________


class Note(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str = Field(index=True)
    content: str
    is_done: str = Field(default=False, index=True)
    # Use a lambda so default_factory gets a function, not a value
    created_at: datetime = Field(default_factory=lambda: datetime.now(tz=timezone.utc), index=True)
