import telebot
from telebot import types
import os
from dotenv import load_dotenv

load_dotenv()
bot = telebot.TeleBot(os.getenv("TOKEN"))

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(types.InlineKeyboardButton("🔥 Ver Packs", callback_data="catalogo"))
    markup.add(types.InlineKeyboardButton("👑 Grupo VIP", callback_data="vip"))
    
    bot.send_message(message.chat.id,
        "😈 Olá safado... Bem vindo ao perfil da Vickzinhaa Safadinha\n\n"
        "Conteúdo bem quente e exclusivo pra você 🔥\n"
        "Tem +18? Então vem...", 
        reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.data == "catalogo":
        texto = """🔥 PACKS DA VICKZINHAA:

📸 Pack de Fotos - R$ 14,90
📹 Pack Fotos + Vídeos - R$ 24,90
👑 Acesso ao Grupo VIP - R$ 35,90

Escolha digitando:
/comprar 1
/comprar 2
/comprar 3"""
        bot.send_message(call.message.chat.id, texto)

    elif call.data == "vip":
        bot.send_message(call.message.chat.id, "👑 O Grupo VIP tem fotos, vídeos diários, lives e conteúdo personalizado.\n\nQuer comprar? Digite /comprar 3")

@bot.message_handler(commands=['comprar'])
def comprar(message):
    try:
        opcao = int(message.text.split()[1])
        
        if opcao == 1:
            valor = "14,90"
            produto = "Pack de Fotos"
        elif opcao == 2:
            valor = "24,90"
            produto = "Pack Fotos + Vídeos"
        elif opcao == 3:
            valor = "35,90"
            produto = "Acesso ao Grupo VIP"
        else:
            bot.send_message(message.chat.id, "Opção inválida!")
            return
            
        bot.send_message(message.chat.id, f"✅ Você escolheu: **{produto}**\n💰 Valor: R$ {valor}\n\n"
                                         f"Faça o Pix e me manda o comprovante aqui que eu libero seu acesso rapidinho 🔥")
    except:
        bot.send_message(message.chat.id, "Como usar:\n/comprar 1\n/comprar 2\n/comprar 3")

print("🔥 Vickzinhaa Safadinha está online...")
bot.infinity_polling()