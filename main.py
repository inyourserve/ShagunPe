from fastapi import FastAPI
from app.api.routers import users, events

app = FastAPI()

app.include_router(users.router)
app.include_router(events.router)

