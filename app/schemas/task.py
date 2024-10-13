from pydantic import BaseModel

# For creating a new task
class TaskCreate(BaseModel):
    title: str
    is_completed: bool = False

# For updating an existing task
class TaskUpdate(BaseModel):
    title: str = None
    is_completed: bool = None

# For reading a task
class TaskRead(BaseModel):
    id: int
    title: str
    is_completed: bool

    class Config:
        orm_mode = True

# For bulk operations
class BulkTaskCreate(BaseModel):
    tasks: list[TaskCreate]

class BulkTaskDelete(BaseModel):
    tasks: list[int]
