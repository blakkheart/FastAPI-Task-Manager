FROM python:3.11
WORKDIR /fastapi_app
COPY requirements.txt .
RUN pip install -r requirements.txt --no-cache-dir
COPY . .
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8001"]