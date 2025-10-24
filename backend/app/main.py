from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from .routes import users, numbers, messages, auth
from app.routes import instances


app = FastAPI(title="Whatsapp Manager")

# Configuração CORS
origins = [
    "http://localhost:5173",  # endereço do seu frontend
    "http://127.0.0.1:5173",
    # você pode adicionar outros domínios de produção aqui
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # GET, POST, PUT, DELETE...
    allow_headers=["*"],
)

app.include_router(users.router, prefix="/users")
# app.include_router(numbers.router, prefix="/numbers")
# app.include_router(messages.router, prefix="/messages")
app.include_router(auth.router, prefix="/login")

app.include_router(instances.router, prefix="/instances", tags=["Instances"])

@app.get("/")
def read_root():
    return {"status": "ok"}
