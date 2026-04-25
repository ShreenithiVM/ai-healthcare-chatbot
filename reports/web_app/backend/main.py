from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware
from chatbot import get_chatbot_response  # Your chatbot logic
from auth import router as auth_router

app = FastAPI()

# Enable CORS for your Next.js frontend.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "MedBot API is running with PostgreSQL."}

@app.post("/chat")
async def chat(user_message: str = Form(...)):
    response = get_chatbot_response(user_message)
    return {"response": response}

# Include authentication endpoints under /auth prefix.
app.include_router(auth_router, prefix="/auth")
