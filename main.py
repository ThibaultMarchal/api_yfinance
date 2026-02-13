from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import yfinance as ticker

app = FastAPI()

# IMPORTANT : Autorise votre site Render (le front-end) à appeler cette API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # En production, remplacez par votre URL Render
    allow_methods=["*"],
    allow_headers=["*"],
)

# Liste des entreprises du CAC 40 (Symboles Yahoo Finance)
CAC40_TICKERS = {
    "LVMH": "MC.PA",
    "Total": "TTE.PA",
    "Airbus": "AIR.PA",
    "Sanofi": "SAN.PA",
    "Loreal": "OR.PA"
}

@app.get("/prix")
def get_prices():
    results = {}
    for name, symbol in CAC40_TICKERS.items():
        data = ticker.Ticker(symbol)
        # On récupère le dernier prix de marché
        current_price = data.fast_info['last_price']
        results[name] = round(current_price, 2)
    return results

@app.get("/")
def read_root():
    return {"status": "Le cerveau du trading est en ligne"}
