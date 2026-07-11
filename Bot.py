import telebot
from telebot import types
import os
import requests
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
bot = telebot.TeleBot(os.getenv("TOKEN"))

# ================= CONFIG BRAVO PAY =================
BRAVO_API_KEY = "bp_live_xNIkbn_Z_vsF9miIxndj7zNc8XMxK5BN0QO43A"
BRAVO_BASE_URL = "https://api.bravopay.com.br"  # Mude se a documentação for diferente

def criar_pix_bravo(valor: float, descricao: str, user_id: int):
    """Cria Pix via Bravo Pay"""
    url = f"{BRAVO_BASE_URL}/pix"   # Ajuste o endpoint se necessário
    
    headers = {
        "Authorization": f"Bearer {BRAVO_API_KEY}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    
    payload = {
        "amount": float(valor),
        "description": descricao,
        "reference_id": f"vick_{user_id}_{datetime.now().strftime('%Y%m%d%H%M%S')}",
        "payer": {
            "name": "Cliente"
        }
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=20)
        
        print(f"Status Code: {response.status_code}")
        print(f"Resposta: {response.text}")
        
        if response.status_code in [200, 201]:
            data = response.json()
            return data
        else:
            bot.send_message(user_id, f"❌ Erro na Bravo Pay: {response.status_code}")
            return None
    except Exception as e:
        print(f"Erro exceção: {e}")
        return None

# ================= BOT =================
@bot.message_handler(commands=['start', 'menu'])
def start(message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(types.InlineKeyboardButton("📸 Pack 100 Fotos", callback_data="packfotos"))
    markup.add(types.InlineKeyboardButton("📹 Pack Fotos + Vídeos", callback_data="packvideos"))
    markup.add(types.InlineKeyboardButton("👑 Grupo VIP", callback_data="vip"))
    markup.add(types.InlineKeyboardButton("📹 5 Chamadas de Vídeo", callback_data="callvideo"))

    bot.send_message(message.chat.id,
        "😈 <b>Vickzinhaa Safadinha</b> 🔥\n\n"
        "Escolhe o que você quer de mim hoje safado 😏",
        parse_mode='HTML', reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    if call.data == "packfotos":
        bot.send_message(call.message.chat.id, "Digite: /packfotos")
    elif call.data == "packvideos":
        bot.send_message(call.message.chat.id, "Digite: /packvideos")
    elif call.data == "vip":
        bot.send_message(call.message.chat.id, "Digite: /vip")
    elif call.data == "callvideo":
        bot.send_message(call.message.chat.id, "Digite: /callvideo")

# ================= COMANDOS =================
@bot.message_handler(commands=['packfotos'])
def packfotos(message):
    criar_e_enviar_pix(message, "Pack 100 Fotos Pelada", 14.90)

@bot.message_handler(commands=['packvideos'])
def packvideos(message):
    criar_e_enviar_pix(message, "Pack Fotos + Vídeos Gemendo", 19.90)

@bot.message_handler(commands=['vip'])
def vip(message):
    criar_e_enviar_pix(message, "Grupo VIP Completo", 23.90)

@bot.message_handler(commands=['callvideo'])
def callvideo(message):
    criar_e_enviar_pix(message, "5 Chamadas de Vídeo", 20.90)

def criar_e_enviar_pix(message, produto: str, valor: float):
    user_id = message.from_user.id
    bot.send_message(user_id, f"⏳ Gerando Pix para <b>{produto}</b>...", parse_mode='HTML')
    
    pix = criar_pix_bravo(valor, produto, user_id)
    
    if pix:
        qr_code = pix.get('qr_code') or pix.get('pix_code') or pix.get('payload')
        if qr_code:
            bot.send_message(user_id, f"✅ Pix gerado!\n\nCopie o código abaixo:")
            bot.send_message(user_id, f"<code>{qr_code}</code>", parse_mode='HTML')
            bot.send_message(user_id, "Pague e mande o comprovante aqui que eu libero tudo 😈")
            return
    
    # Fallback se der erro
    bot.send_message(user_id, "❌ Não consegui gerar o Pix automático.\nFaça o Pix manual e mande o comprovante.")

print("😈 Vickzinhaa com Bravo Pay está online...")
bot.infinity_polling()
