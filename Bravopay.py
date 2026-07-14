pip install python-dotenv requests fastapi uvicorn qrcode pillow python-telegram-bot

"""
bravopay.py
Integração com a API da BravoPay
"""

import requests
from config import (
    BRAVOPAY_BASE_URL,
    HEADERS,
    PRODUCT_ID
)


class BravoPay:

    def __init__(self):
