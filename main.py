from fastapi import FastAPI, HTTPException
import configparser
import stripe
import math
import os

config = configparser.ConfigParser()
config.read("config.ini")
VERSION = config.get("APP", "VERSION")
KEY = os.environ.get("STRIPE_KEY", config.get("STRIPE", "KEY"))
PRODUCT_ID = os.environ.get("STRIPE_PRODUCT_ID", config.get("STRIPE", "PRODUCT_ID"))

stripe.api_key = KEY

app = FastAPI()

@app.get("/")
def ping():
    return {"ping": "pong"}

@app.get(f"/{VERSION}/link")
async def getPaymentLink(hours: float = 0, rate: float = 0):
    if (hours*rate == 0):
        raise HTTPException(status_code=401, detail="hours AND rate must not equal zero.")
    
    unit_amount = int(math.floor(hours*rate*100))
    priceResponse = stripe.Price.create(
        unit_amount=unit_amount,
        currency="cad",
        product=PRODUCT_ID,
    )

    linkResponse = stripe.PaymentLink.create(
        line_items=[
            {
                "price": priceResponse["id"],
                "quantity": 1,
            }
        ]
    )

    return { "link": linkResponse["url"] }
