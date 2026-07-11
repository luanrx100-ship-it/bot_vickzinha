import telebot
from telebot import types
import os
import requests
import json
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

bot = telebot.TeleBot(os.getenv("TOKEN"))

# ================= CONFIG BRAVO PAY =================
BRAVO_API_KEY = "bp_live_xNIkbn_Z_vsF9miIxndj7zNc8XMxK5BN0QO43A"
BRAVO_BASE_URL = "https://bravopay.club/api/v1"

def criar_transacao_pix(valor_cents: int, descricao: str, user_id: int, customer_data: dict = None):
    """Cria transação PIX na Bravo Pay"""
    url = f"{BRAVO_BASE_URL}/transactions"
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {BRAVO_API_KEY}"
    }
    
    payload = {
        "amount_cents": valor_cents,
        "method": "pix",
        "external_reference": f"vick_{user_id}_{datetime.now().strftime('%Y%m%d%H%M%S')}",
        "customer": customer_data or {
            "name": f"Cliente_{user_id}",
            "email": f"cliente{user_id}@example.com"
        }
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=15)
        print(f"Status: {response.status_code} | Resposta: {response.text}")
        
        if response.status_code in (200, 201):
            return response.json()
        return None
    except Exception as e:
        print(f"Erro Bravo Pay: {e}")
        return None

# ================= PRODUTOS =================
produtos = {
    "packfotos": {"nome": "Pack 100 Fotos Pelada", "preco": 1490},
    "packvideos": {"nome": "Pack Fotos + Vídeos Gemendo", "preco": 1990},
    "vip": {"nome": "Grupo VIP Completo", "preco": 2390},
    "callvideo": {"nome": "5 Chamadas de Vídeo", "preco": 2090}
}

# ================= BOT =================
@bot.message_handler(commands=['start', 'menu'])
def start(message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    for key, prod in produtos.items():
        markup.add(types.InlineKeyboardButton(f"{prod['nome']} - R$ {prod['preco']/100:.2f}", callback_data=key))
    
    bot.send_message(message.chat.id,
        "😈 <b>Vickzinhaa Safadinha</b> 🔥\n\n"
        "Escolhe o que você quer fazer comigo hoje safado 😏",
        parse_mode='HTML', reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    produto_key = call.data
    if produto_key in produtos:
        prod = produtos[produto_key]
        bot.send_message(call.message.chat.id, f"Digite: /{produto_key}")

# ================= COMANDOS DE COMPRA =================
def processar_compra(message, produto_key: str):
    prod = produtos[produto_key]
    user_id = message.from_user.id
    
    bot.send_message(user_id, f"⏳ Gerando Pix para <b>{prod['nome']}</b>...", parse_mode='HTML')
    
    # Dados do cliente (pode melhorar pedindo nome/email)
    customer = {
        "name": message.from_user.first_name or "Cliente",
        "email": f"user{user_id}@example.com"
    }
    
    transacao = criar_transacao_pix(prod['preco'], prod['nome'], user_id, customer)
    
    if transacao and transacao.get('pix', {}).get('copy_paste'):
        pix_data = transacao['pix']
        bot.send_message(user_id, f"✅ Pix gerado para {prod['nome']}\n\n"
                                  f"Valor: R$ {prod['preco']/100:.2f}\n\n"
                                  f"Copie o código abaixo:")
        bot.send_message(user_id, f"<code>{pix_data['copy_paste']}</code>", parse_mode='HTML')
        bot.send_message(user_id, "Pague e mande o comprovante aqui que eu libero na hora 😈")
    else:
        bot.send_message(user_id, "❌ Erro ao gerar Pix. Tente novamente.")

@bot.message_handler(commands=['packfotos', 'packvideos', 'vip', 'callvideo'])
def handle_compra(message):
    cmd = message.text.replace('/', '')
    processar_compra(message, cmd)

print("😈 Vickzinhaa Safadinha com Bravo Pay está online...")
bot.infinity_polling()
