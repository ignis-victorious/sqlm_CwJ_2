#
#  Import LIBRARIES
from contextlib import asynccontextmanager
from typing import AsyncGenerator, Generator, Sequence

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import Engine
from sqlmodel import Session, SQLModel, create_engine, desc, select
from sqlmodel.sql._expression_select_cls import SelectOfScalar

#  Import FILES
from .models.models import Note, NoteCreate, NoteUpdate

#
#  ______________________


# 1. Engine setup
sqlite_url: str = "sqlite:///./notes.db"
engine: Engine = create_engine(url=sqlite_url, echo=True)


# 2. Define the Lifespan
@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """
    Handles the startup and shutdown logic for the application.
    """
    # --- Startup Logic ---
    # Create database tables, runs BEFORE the app starts taking requests
    SQLModel.metadata.create_all(bind=engine)
    # --- Startup Logic ---

    yield  # The app is now running and handling requests

    # --- Shutdown Logic ---
    # This runs AFTER the app stops (e.g., cleaning up resources) entirely Optional
    # engine.dispose()


def get_session() -> Generator[Session, None, None]:
    with Session(bind=engine) as session:
        yield session


# 3. Pass lifespan to the FastAPI instance
app = FastAPI(title="SQL MODEL STUFF", lifespan=lifespan)
# app = FastAPI()


# Adding the APIs
@app.get(path="/")
def main() -> dict[str, str]:
    return {"message": "Hello World"}


# BUILDING CRUD ROUTES
# {"title": "REMEMBER: code Quanta", "content": "Need to get your skates on!!!"}
# {"title": "Shopping", "content": "Milk and flowers"}
@app.post(path="/notes", response_model=Note)
def create_note(payload: NoteCreate, session: Session = Depends(dependency=get_session)) -> Note:
    note: Note = Note.model_validate(payload)
    session.add(instance=note)
    session.commit()
    session.refresh(instance=note)
    return note


@app.get(path="/notes", response_model=list[Note])
def list_notes(is_done: bool | None = None, session: Session = Depends(dependency=get_session)) -> Sequence[Note]:
    note: SelectOfScalar[Note] = select(Note)
    if is_done is not None:
        note: SelectOfScalar[Note] = note.where(bool(Note.is_done) == is_done)
    note: SelectOfScalar[Note] = note.order_by(desc(column=Note.created_at))
    return session.exec(statement=note).all()


@app.get(path="/notes/{note_id}", response_model=Note)
def get_note(note_id: int, session: Session = Depends(dependency=get_session)) -> Note:
    note: Note | None = session.get(entity=Note, ident=note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found!")
    return note


# {"title": "REMEMBER: code a lot of Q", "content": "Do it now!",  "is_done": "true"}
@app.patch(path="/notes/{note_id}", response_model=Note)
def update_note(note_id: int, payload: NoteUpdate, session: Session = Depends(dependency=get_session)) -> Note:
    note: Note | None = session.get(entity=Note, ident=note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found!")
    updates: dict[str, str | None] = payload.model_dump(exclude_unset=True)
    for key, value in updates.items():
        setattr(note, key, value)

    session.add(instance=note)
    session.commit()
    session.refresh(instance=note)
    return note


@app.delete(path="/notes/{note_id}", response_model=Note)
def delete_note(note_id: int, session: Session = Depends(dependency=get_session)) -> dict[str, bool]:
    note: Note | None = session.get(entity=Note, ident=note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found!")

    session.delete(instance=note)
    session.commit()
    session.refresh(instance=note)
    return {"OK": True}


# Substituted by the asynccontextmanager
# @app.on_event(event_type="startup")
# def on_startup() -> None :
#     SQLModel.metadata.create_all(bind= engine)


#
#  Import LIBRARIES
#  Import FILES
#
#  ______________________
