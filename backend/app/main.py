from fastapi import FastAPI
from .routes import users, numbers, messages, auth

app = FastAPI(title="Whatsapp Manager")

app.include_router(users.router, prefix="/users")
# app.include_router(numbers.router, prefix="/numbers")
# app.include_router(messages.router, prefix="/messages")
app.include_router(auth.router, prefix="/login")

@app.get("/")
def read_root():
    return {"status": "ok"}
