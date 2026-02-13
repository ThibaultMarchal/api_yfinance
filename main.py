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
    results = {}
    for name, symbol in TICKERS.items():
        try:
            ticker_data = yf.Ticker(symbol)
            # On récupère l'historique des 2 derniers jours avec un intervalle de 1 heure
            df = ticker_data.history(period="2d", interval="1h")
            
            if not df.empty:
                # On prend le prix de clôture de la dernière heure complète
                prix_heure = df['Close'].iloc[-1]
                results[name] = round(float(prix_heure), 2)
            else:
                results[name] = "Indisponible"
        except Exception as e:
            results[name] = 0
    return results

@app.get("/")
def home():
    return {"message": "API active"}
