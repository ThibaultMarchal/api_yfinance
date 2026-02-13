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
    "LVMH": "MC.PA", "TOTALENERGIES": "TTE.PA", "AIRBUS": "AIR.PA",
    "SANOFI": "SAN.PA", "L'OREAL": "OR.PA", "BNP PARIBAS": "BNP.PA",
    "HERMES": "RMS.PA", "AXA": "CS.PA", "VINCI": "DG.PA",
    "SCHNEIDER": "SU.PA", "SAFRAN": "SAF.PA", "AIR LIQUIDE": "AI.PA",
    "STELLANTIS": "STLAP.PA", "ESSILOR": "EL.PA", "DANONE": "BN.PA",
    "RENAULT": "RNO.PA", "ORANGE": "ORA.PA", "CARREFOUR": "CA.PA",
    "MICHELIN": "ML.PA", "SOC GENERALE": "GLE.PA", "KERING": "KER.PA",
    "THALES": "HO.PA", "VEOLIA": "VIE.PA", "SAINT GOBAIN": "SGO.PA",
    "PUBLICIS": "PUB.PA", "EDENRED": "EDEN.PA", "ENGIE": "ENGI.PA",
    "LEGRAND": "LR.PA", "BOUYGUES": "EN.PA", "ALSTOM": "ALO.PA",
    "PERNOD RICARD": "RI.PA", "CAPGEMINI": "CAP.PA", "DASSAULT": "AM.PA"
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
