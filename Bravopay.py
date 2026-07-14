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

"""
bravopay.py
Classe responsável pela comunicação com a API da BravoPay
"""

import requests

from config import (
    BRAVOPAY_BASE_URL,
    HEADERS,
    PRODUCT_ID
)


class BravoPay:

    def __init__(self):
        self.base_url = BRAVOPAY_BASE_URL
        self.headers = HEADERS

    # ===============================
    # Criar cobrança PIX
    # ===============================
    def criar_pix(
        self,
        amount_cents,
        nome,
        email,
        telefone,
        cpf,
        external_reference,
        utm=None
    ):

        payload = {
            "amount_cents": amount_cents,
            "method": "pix",
            "customer": {
                "name": nome,
                "email": email,
                "phone": telefone,
                "cpf": cpf
            },
            "external_reference": external_reference
        }

        # Product ID (UTMify)
        if PRODUCT_ID:
            payload["product_id"] = PRODUCT_ID

        # UTM
        if utm:
            payload["utm"] = utm

        response = requests.post(
            f"{self.base_url}/transactions",
            json=payload,
            headers=self.headers,
            timeout=20
        )

        response.raise_for_status()

        return response.json()

    # ===============================
    # Consultar status
    # ===============================
    def consultar(self, transaction_id):

        response = requests.get(
            f"{self.base_url}/transactions/{transaction_id}",
            headers=self.headers,
            timeout=20
        )

        response.raise_for_status()

        return response.json()

    # ===============================
    # Consultar saldo
    # ===============================
    def saldo(self):

        response = requests.get(
            f"{self.base_url}/balance",
            headers=self.headers,
            timeout=20
        )

        response.raise_for_status()

        return response.json()

    # ===============================
    # Solicitar saque
    # ===============================
    def saque_pix(
        self,
        amount_cents,
        pix_key,
        pix_key_type="email"
    ):

        payload = {
            "amount_cents": amount_cents,
            "method": "pix",
            "pix_key": pix_key,
            "pix_key_type": pix_key_type
        }

        response = requests.post(
            f"{self.base_url}/withdrawals",
            json=payload,
            headers=self.headers,
            timeout=20
        )

        response.raise_for_status()

        return response.json()

    # ===============================
    # Consultar saque
    # ===============================
    def consultar_saque(self, withdrawal_id):

        response = requests.get(
            f"{self.base_url}/withdrawals/{withdrawal_id}",
            headers=self.headers,
            timeout=20
        )

        response.raise_for_status()

        return response.json()
