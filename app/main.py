from fastapi import FastAPI
from app.api.routers import users, events, addresses, transactions

app = FastAPI()

app.include_router(users.router,tags=["Users"])
app.include_router(events.router,tags=["Events"])
app.include_router(transactions.router, tags=["Transactions"])
app.include_router(addresses.router, tags=["Address"])

