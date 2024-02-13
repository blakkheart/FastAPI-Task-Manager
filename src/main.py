from fastapi import FastAPI
import uvicorn

from src.auth.crud import router as user_router
from src.tasks.crud import router as task_router


app = FastAPI()
app.include_router(user_router, prefix='/users')
app.include_router(task_router, prefix='/tasks')


if __name__ == '__main__':
    uvicorn.run('src.main:app', host='127.0.0.1', port=8000, reload=True)
