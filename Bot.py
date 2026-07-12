import os
import logging
from io import BytesIO
import requests
import qrcode
from datetime import datetime

import telebot
from telebot import types
from dotenv import load_dotenv

load_dotenv()

# ================= CONFIG =================
bot = telebot.TeleBot(os.getenv("TOKEN"))
BRAVO_KEY = os.getenv("BRAVO_KEY")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ================= PRODUTOS DA VICKZINHAA =================
produtos = {
    "packfotos": {"nome": "Pack 100 Fotos Pelada", "preco": 1490},
    "packvideos": {"nome": "Pack Fotos + Vídeos Gemendo", "preco": 1990},
    "vip": {"nome": "Grupo VIP Completo", "preco": 2390},
    "callvideo": {"nome": "5 Chamadas de Vídeo", "preco": 2090}
}

def criar_pix_bravo(valor_cents: int, descricao: str, user_id: int):
    url = "https://bravopay.club/api/v1/transactions"
    
    headers = {
        "Authorization": f"Bearer {BRAVO_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "amount_cents": valor_cents,
        "method": "pix",
        "external_reference": f"vick_{user_id}_{datetime.now().strftime('%H%M%S')}",
        "customer": {
            "name": "Cliente Vickzinhaa"
        }
    }
    
    try:
        r = requests.post(url, headers=headers, json=payload, timeout=15)
        logger.info(f"Bravo Pay Status: {r.status_code}")
        
        if r.status_code in (200, 201):
            return r.json()
        else:
            logger.error(f"Erro Bravo: {r.text}")
            return None
    except Exception as e:
        logger.error(f"Exceção: {e}")
        return None

# ================= BOT =================
@bot.message_handler(commands=['start', 'menu'])
def start(message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    for key, prod in produtos.items():
        preco = prod["preco"] / 100
        markup.add(types.InlineKeyboardButton(
            f"{prod['nome']} - R$ {preco:.2f}", 
            callback_data=key
        ))

    bot.send_message(message.chat.id,
        "😈 <b>Vickzinhaa Safadinha</b> 🔥\n\n"
        "Tá com tesão? Escolhe o que você quer fazer comigo hoje safado 😏",
        parse_mode='HTML', reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    if call.data not in produtos:
        return
    
    prod = produtos[call.data]
    user_id = call.from_user.id
    
    bot.send_message(call.message.chat.id, f"⏳ Gerando Pix para <b>{prod['nome']}</b>...", parse_mode='HTML')
    
    tx = criar_pix_bravo(prod["preco"], prod["nome"], user_id)
    
    if tx and tx.get("pix", {}).get("copy_paste"):
        pix = tx["pix"]
        bot.send_message(call.message.chat.id, "✅ Pix gerado! Copie o código abaixo:")
        bot.send_message(call.message.chat.id, f"<code>{pix['copy_paste']}</code>", parse_mode='HTML')
        
        # Opcional: QR Code
        # qr = qrcode.make(pix['copy_paste'])
        # ...
    else:
        bot.send_message(call.message.chat.id, "❌ Erro ao gerar Pix. Tente novamente ou avise o suporte.")

print("😈 Vickzinhaa Safadinha com Bravo Pay está online...")
bot.infinity_polling()
