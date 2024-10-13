# Task API

[Postman API Test](https://documenter.getpostman.com/view/32354061/2sAXxS9CLi)

## Overview

This is a FastAPI-based Task Manager API that allows you to create, read, update, delete, and manage tasks efficiently. Each task has a unique ID, a title, and a completion status.

## Database Configuration

- **Database:** SQLite
- **ORM:** SQLAlchemy

## Models

- **Task Model:**
    - **id:** Unique identifier (integer)
    - **title:** Title of the task (string)
    - **is_completed:** Completion status (boolean)

## Pydantic Schemas

- **TaskCreate:** For creating a new task
- **TaskUpdate:** For updating an existing task
- **TaskRead:** For reading task details
- **BulkTaskCreate:** For bulk adding tasks
- **BulkTaskDelete:** For bulk deleting tasks

## Running the API

1. Set up your environment and install the dependencies.
2. Run the FastAPI application using:
   ```bash
   uvicorn app.main:app --reload
