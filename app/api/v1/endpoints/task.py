from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.schemas import task as task_schema
from app.models import task as task_model
from fastapi.responses import JSONResponse

router = APIRouter()

# Dependency for DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#Create a new task
@router.post("/", response_model=task_schema.TaskRead, status_code=201)
def create_task(task: task_schema.TaskCreate, db: Session = Depends(get_db)):
    db_task = task_model.Task(title=task.title, is_completed=task.is_completed)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    d = {"id": db_task.id}
    return JSONResponse(content=d)


#List all tasks
@router.get("/", response_model=list[task_schema.TaskRead], status_code=200)
def list_tasks(db: Session = Depends(get_db)):
    return db.query(task_model.Task).all()

#Get a specific task by ID
@router.get("/{id}", response_model=task_schema.TaskRead, status_code=200)
def get_task(id: int, db: Session = Depends(get_db)):
    db_task = db.query(task_model.Task).filter(task_model.Task.id == id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task

#Delete a specific task
@router.delete("/{id}", status_code=204)
def delete_task(id: int, db: Session = Depends(get_db)):
    db_task = db.query(task_model.Task).filter(task_model.Task.id == id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(db_task)
    db.commit()
    return 

#Edit a task
@router.put("/{id}", status_code=204)
def update_task(id: int, task: task_schema.TaskUpdate, db: Session = Depends(get_db)):
    db_task = db.query(task_model.Task).filter(task_model.Task.id == id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")

    if task.title:
        db_task.title = task.title
    if task.is_completed is not None:
        db_task.is_completed = task.is_completed

    db.commit()
    return

#Bulk add tasks
@router.post("/bulk", status_code=201)
def bulk_add_tasks(tasks: task_schema.BulkTaskCreate, db: Session = Depends(get_db)):
    task_list = [task_model.Task(title=task.title, is_completed=task.is_completed) for task in tasks.tasks]
    db.add_all(task_list)
    db.commit()
    return {"tasks": [{"id": task.id} for task in task_list]}

#Bulk delete tasks
@router.delete("/bulk", status_code=204)
def bulk_delete_tasks(tasks: task_schema.BulkTaskDelete, db: Session = Depends(get_db)):
    db.query(task_model.Task).filter(task_model.Task.id.in_(tasks.tasks)).delete(synchronize_session=False)
    db.commit()
    return
