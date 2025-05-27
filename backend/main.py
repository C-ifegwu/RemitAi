from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.v1.endpoints import auth, nlp, transactions, wallet, voice

app = FastAPI(
    title="RemitAI API",
    description="API for RemitAI services including NLP, transactions, and security features.",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers from the endpoints
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(nlp.router, prefix="/api/v1/nlp", tags=["NLP"])
app.include_router(transactions.router, prefix="/api/v1/transactions", tags=["Transactions"])
app.include_router(wallet.router, prefix="/api/v1/wallet", tags=["Wallet"])
app.include_router(voice.router, prefix="/api/v1/voice", tags=["Voice Biometrics"])

@app.get("/")
async def read_root():
    return {"message": "Welcome to RemitAI API", "version": "1.0.0"}

# To run this app:
# uvicorn main:app --reload
