from fastapi import FastAPI
from app.api.v1.endpoints import task
from app.db.session import Base, engine

# Create the database tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Include task routes
app.include_router(task.router, prefix="/v1/tasks", tags=["tasks"])
