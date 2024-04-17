from fastapi import FastAPI
from app.api.routers import users, events
from app.api.routers import transactions

app = FastAPI()

app.include_router(users.router)
app.include_router(events.router)
app.include_router(transactions.router)

