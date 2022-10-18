from fastapi import FastAPI
from routes.user import user

app = FastAPI(
    title="CRUD API with FastAPI",
    description="Esta es una Api con FastAPI",
    version="0.0.1",
    openapi_tags=[
        {"name": "users", "description": "users routes"}
    ]
)

app.include_router(user)
