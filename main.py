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
@app.get("/prix")
def get_prices():
    results = {}
    for name, symbol in TICKERS.items():
        try:
            # On récupère les données du jour
            ticker_data = yf.Ticker(symbol)
            # 'fast_info' est plus léger et évite souvent les bugs de colonnes
            price = ticker_data.fast_info['last_price']
            
            # Sécurité : si le prix est délirant, on essaie une autre méthode
            if price > 10000 and "PA" in symbol: # Une action CAC40 ne dépasse pas 10k€ (sauf Hermès qui est vers 2k€)
                hist = ticker_data.history(period="1d")
                price = hist['Close'].iloc[-1]

            results[name] = round(float(price), 2)
        except Exception as e:
            print(f"Erreur sur {name}: {e}")
            results[name] = "Indisponible"
    return results

@app.get("/")
def home():
    return {"message": "API active"}
