# 
#  Import LIBRARIES
from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator, Generator
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import Engine
from sqlmodel import Field, SQLModel ,Session, create_engine, select
#  Import FILES
from models.models import Note
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
@app. post (path="/notes", response_model=Note)
def create_note(payload:NoteCreate, session: Session = Depends (dependency=get_session))
    note = Note-model_validate(payload)
    session. add (note) session.commit()
    session. refresh(note)
    return note





# Substituted by the asynccontextmanager
# @app.on_event(event_type="startup")
# def on_startup() -> None :
#     SQLModel.metadata.create_all(bind= engine)




#
#  Import LIBRARIES
#  Import FILES
#
#  ______________________
