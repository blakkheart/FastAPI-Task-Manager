
# 📋 Task Manager API 📋
This project implements a FastAPI-based API service for managing tasks.

## Features

 - User registration is available via the /users/ endpoint.
 - Users can obtain JWT access and refresh tokens through the /users/login/ endpoint
 - Documentation is accessible at /docs/
- Users can create, retrieve, update, and delete tasks via the /tasks/ endpoint.
- Tasks support pagination and filtering based on completion status.
- Only users who created the tasks have access to view and manage them.

## Technologies Used

- FastAPI for building the API service.
- PostgreSQL for the database.
- Alembic for database migrations.
- Pydantic for data validation.
- Jose for JWT tokens.
- Docker.

## Installation

Clone this repository:
```bash
git clone https://github.com/blakkheart/FastAPI-Task-Manager.git
```
Navigate to the project directory:
```bash
cd FastAPI-Task-Manager
```
Install the required dependencies:
```bash
pip install -r requirements.txt
```
Fill up the *.env* file inside the *src* directory (for example see *.env.example* in the same directory)

## Usage  

Run the following command to start the docker compose:
```bash
docker compose up
```
Make migrations and apply them via alembic command:
```bash
docker compose exec backend alembic revision --autogenerate
docker compose exec backend alembic upgrade head
``` 
If done correctly the server will be running at 127.0.0.1:8001 and you will be able to access the API [documentation](http://localhost:8001/docs.)
