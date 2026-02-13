from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import yfinance as yf

app = FastAPI()

# Configuration CORS ultra-permissive pour le développement
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Autorise absolument tout le monde
    allow_credentials=True,
    allow_methods=["*"],  # Autorise GET, POST, etc.
    allow_headers=["*"],
)

TICKERS = {
    "LVMH": "MC.PA", "TOTAL": "TTE.PA", "AIRBUS": "AIR.PA",
    "SANOFI": "SAN.PA", "LOREAL": "OR.PA", "BNP": "BNP.PA"
}

@app.get("/prix")
def get_prices():
    try:
        symbols = list(TICKERS.values())
        data = yf.download(symbols, period="1d", interval="1m", progress=False)['Close'].iloc[-1]
        results = {name: round(float(data[symbol]), 2) for name, symbol in TICKERS.items()}
        return results
    except Exception as e:
        return {"error": str(e)}

@app.get("/")
def home():
    return {"message": "API active"}
