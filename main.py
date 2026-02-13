from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import yfinance as yf

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Liste étendue du CAC 40 (ajoute les autres au besoin)
TICKERS = {
    "LVMH": "MC.PA", "Total": "TTE.PA", "Airbus": "AIR.PA", "Sanofi": "SAN.PA",
    "Loreal": "OR.PA", "BNP": "BNP.PA", "Hermes": "RMS.PA", "AXA": "CS.PA",
    "Renault": "RNO.PA", "Orange": "ORA.PA", "Danone": "BN.PA"
}

@app.get("/prix")
def get_prices():
    results = {}
    # On récupère les données par groupe pour aller plus vite
    symbols = list(TICKERS.values())
    data = yf.download(symbols, period="1d", interval="1m", progress=False)['Close'].iloc[-1]
    
    for name, symbol in TICKERS.items():
        results[name] = round(float(data[symbol]), 2)
    return results
