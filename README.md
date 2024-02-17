# BackWalleps #

Backend for Gradiant's HackUDC challenge 2024.
# BackWalleps

This project is the backend for Gradiant's HackUDC challenge 2024. It consists of a database and needed endpoints to store and manage data related to users and their home electrical devices.

## Preconditions:

- Python 3

## START DB

```
python3 -m pip install -r requirements.txt
```
```
docker compose up -d --build
```
```
python3 -m alembic upgrade head
```

## MIGRATE DB

```
python3 -m alembic revision --autogenerate
```
```
python3 -m alembic upgrade head
```

## START API

```
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## API documentation (provided by Swagger UI)

```
http://127.0.0.1:8000/docs
```