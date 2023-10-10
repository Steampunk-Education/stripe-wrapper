from fastapi import FastAPI, HTTPException
import configparser
import stripe
import math
import os

config = configparser.ConfigParser()
config.read("config.ini")
VERSION = os.environ.get("INVOICE_APP_VERSION")
KEY = os.environ.get("STRIPE_KEY")
PRODUCT_ID = os.environ.get("STRIPE_PRODUCT_ID")

app = FastAPI()

stripe.api_key = KEY

@app.get("/")
def ping():
    return {"ping": "pong"}

@app.get(f"/{VERSION}/link")
async def getPaymentLink(hours, rate):
    hours = float(hours)
    rate = float(rate)
    if (hours == None or rate == None):
        raise HTTPException(status_code=401, detail="hours and rate are required parameters")
    if (hours*rate == 0):
        raise HTTPException(status_code=401, detail="hours AND rate must not equal zero.")
    if (hours < 0 or rate < 0):
        raise HTTPException(status_code=401, detail="hours and rate must be greater than zero")
    
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
