import telebot
from telebot import types
import os
import requests
import time
from dotenv import load_dotenv

load_dotenv()

bot = telebot.TeleBot(os.getenv("TOKEN"))
BRAVO_KEY = os.getenv("BRAVO_KEY")

def criar_transacao(valor_cents, descricao, user_id):
    url = "https://bravopay.club/api/v1/transactions"
    headers = {
        "Authorization": f"Bearer {BRAVO_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "amount_cents": valor_cents,
        "method": "pix",
        "external_reference": f"vick_{user_id}"
    }
    
    r = requests.post(url, headers=headers, json=payload, timeout=15)
    print("Criação:", r.status_code)
    return r.json() if r.ok else None

def consultar_transacao(tx_id):
    url = f"https://bravopay.club/api/v1/transactions/{tx_id}"
    headers = {"Authorization": f"Bearer {BRAVO_KEY}"}
    r = requests.get(url, headers=headers, timeout=10)
    return r.json() if r.ok else None

# ================= BOT =================
@bot.message_handler(commands=['start', 'menu'])
def start(message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(types.InlineKeyboardButton("📸 Pack 100 Fotos - R$14,90", callback_data="packfotos"))
    markup.add(types.InlineKeyboardButton("📹 Pack + Vídeos - R$19,90", callback_data="packvideos"))
    markup.add(types.InlineKeyboardButton("👑 Grupo VIP - R$23,90", callback_data="vip"))
    markup.add(types.InlineKeyboardButton("📹 5 Calls - R$20,90", callback_data="callvideo"))

    bot.send_message(message.chat.id, "😈 Vickzinhaa Safadinha online... Escolhe seu desejo 🔥", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    produtos = {
        "packfotos": ("Pack 100 Fotos", 1490),
        "packvideos": ("Pack Fotos + Vídeos", 1990),
        "vip": ("Grupo VIP", 2390),
        "callvideo": ("5 Chamadas de Vídeo", 2090)
    }
    
    nome, valor = produtos.get(call.data, ("Produto", 1490))
    bot.send_message(call.message.chat.id, f"⏳ Gerando Pix para {nome}...")

    tx = criar_transacao(valor, nome, call.from_user.id)
    if not tx or not tx.get("id"):
        bot.send_message(call.message.chat.id, "❌ Erro ao criar Pix.")
        return

    tx_id = tx["id"]
    
    # Polling (espera o Pix ficar pronto)
    for i in range(12):  # tenta por até 1 minuto
        time.sleep(5)
        tx_atual = consultar_transacao(tx_id)
        
        if tx_atual and tx_atual.get("pix", {}).get("copy_paste"):
            pix_code = tx_atual["pix"]["copy_paste"]
            bot.send_message(call.message.chat.id, "✅ Pix gerado!\n\nCopie o código abaixo:")
            bot.send_message(call.message.chat.id, f"<code>{pix_code}</code>", parse_mode='HTML')
            bot.send_message(call.message.chat.id, "Pague e mande o comprovante aqui 🔥")
            return
    
    bot.send_message(call.message.chat.id, "⏳ Pix ainda gerando. Tente novamente em 30 segundos.")

print("😈 Vickzinhaa Safadinha com Bravo Pay está online...")
bot.infinity_polling()
