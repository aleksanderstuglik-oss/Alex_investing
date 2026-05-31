from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import yfinance as yf

app = FastAPI()

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"])

@app.get("/price/{ticker}")
def get_price(ticker: str):
    try:
        t = yf.Ticker(ticker.upper())
        price = t.fast_info["last_price"]
        name  = t.info.get("shortName", ticker)
        return {"ticker": ticker.upper(), "price": round(price, 2), "name": name}
    except Exception as e:
        return {"error": str(e)}

@app.get("/history/{ticker}")
def get_history(ticker: str, period: str = "1mo"):
    hist = yf.Ticker(ticker.upper()).history(period=period)
    return {"dates": hist.index.strftime("%Y-%m-%d").tolist(),
            "prices": [round(p, 2) for p in hist["Close"].tolist()]}
