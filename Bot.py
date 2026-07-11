import telebot
from telebot import types
import os
import requests
from dotenv import load_dotenv

load_dotenv()
bot = telebot.TeleBot(os.getenv("TOKEN"))

# ================= BRAVO PAY =================
BRAVO_API_KEY = "bp_live_xNIkbn_Z_vsF9miIxndj7zNc8XMxK5BN0QO43A"
BRAVO_API_URL = "https://api.bravopay.com.br"  # Confirme a URL exata na documentação

def criar_pix_bravo(valor: float, descricao: str, user_id: int):
    url = f"{BRAVO_API_URL}/pix/create"
    headers = {
        "Authorization": f"Bearer {BRAVO_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "amount": valor,
        "description": descricao,
        "reference": f"vick_{user_id}_{int(datetime.now().timestamp())}",
        "customer": {
            "name": "Cliente Vickzinhaa"
        }
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=15)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Erro Bravo Pay: {response.text}")
            return None
    except Exception as e:
        print(f"Erro na requisição: {e}")
        return None

# ================= BOT SAFADINHO =================
@bot.message_handler(commands=['start', 'menu'])
def start(message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(types.InlineKeyboardButton("🔥 Pack 100 Fotos", callback_data="packfotos"))
    markup.add(types.InlineKeyboardButton("📹 Pack Fotos + Vídeos", callback_data="packvideos"))
    markup.add(types.InlineKeyboardButton("👑 Grupo VIP", callback_data="vip"))
    markup.add(types.InlineKeyboardButton("📹 5 Chamadas de Vídeo", callback_data="callvideo"))

    texto = """😈 <b>Vickzinhaa Safadinha aqui</b> 🔥

Tá com tesão? Escolhe o que você quer ver de mim hoje 😏"""

    bot.send_message(message.chat.id, texto, parse_mode='HTML', reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    if call.data == "packfotos":
        bot.send_message(call.message.chat.id, "📸 Pack 100 Fotos — R$ 14,90\n\nDigite: /packfotos")
    elif call.data == "packvideos":
        bot.send_message(call.message.chat.id, "📹 Pack Fotos + Vídeos — R$ 19,90\n\nDigite: /packvideos")
    elif call.data == "vip":
        bot.send_message(call.message.chat.id, "👑 Grupo VIP — R$ 23,90\n\nDigite: /vip")
    elif call.data == "callvideo":
        bot.send_message(call.message.chat.id, "📹 5 Chamadas de Vídeo — R$ 20,90\n\nDigite: /callvideo")

# ================= COMANDOS DE COMPRA =================
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
    bot.send_message(message.chat.id, f"⏳ Gerando Pix para <b>{produto}</b>...", parse_mode='HTML')
    
    pix = criar_pix_bravo(valor, produto, user_id)
    
    if pix and pix.get('qr_code'):
        bot.send_message(message.chat.id, f"✅ Pix gerado para {produto} (R$ {valor:.2f})")
        bot.send_message(message.chat.id, f"<code>{pix['qr_code']}</code>", parse_mode='HTML')
        bot.send_message(message.chat.id, "Pague e mande o comprovante aqui que eu libero na hora 😈")
    else:
        bot.send_message(message.chat.id, "❌ Erro ao gerar Pix. Tente novamente ou use Pix manual.")

print("😈 Vickzinhaa Safadinha com Bravo Pay está online...")
bot.infinity_polling()
