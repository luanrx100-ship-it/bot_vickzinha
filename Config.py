"""
config.py
Configurações do projeto BravoPay + Telegram
"""

import os
from dotenv import load_dotenv

# Carrega as variáveis do arquivo .env
load_dotenv()

# ============================
# BRAVOPAY
# ============================

BRAVOPAY_API_KEY = os.getenv("BRAVOPAY_API_KEY")

BRAVOPAY_BASE_URL = "https://bravopay.club/api/v1"

# Product ID (caso utilize UTMify)
PRODUCT_ID = os.getenv("PRODUCT_ID", "")

# ============================
# TELEGRAM
# ============================

BOT_TOKEN = os.getenv("BOT_TOKEN")

# ============================
# SITE
# ============================

SITE_URL = os.getenv("SITE_URL", "http://localhost:8000")

WEBHOOK_URL = os.getenv(
    "WEBHOOK_URL",
    f"{SITE_URL}/webhook/bravopay"
)

# ============================
# BANCO
# ============================

DATABASE = os.getenv(
    "DATABASE",
    "database.db"
)

# ============================
# CHECKOUT
# ============================

DEFAULT_AMOUNT = int(
    os.getenv("DEFAULT_AMOUNT", "1000")
)
# 1000 = R$10,00

CURRENCY = "BRL"

# ============================
# LOGS
# ============================

LOG_LEVEL = os.getenv(
    "LOG_LEVEL",
    "INFO"
)

# ============================
# HEADERS PADRÃO
# ============================

HEADERS = {
    "Authorization": f"Bearer {BRAVOPAY_API_KEY}",
    "Content-Type": "application/json"
}
