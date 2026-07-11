import telebot
from telebot import types
import os
from dotenv import load_dotenv

load_dotenv()
bot = telebot.TeleBot(os.getenv("TOKEN"))

@bot.message_handler(commands=['start', 'menu'])
def start(message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(types.InlineKeyboardButton("🔥 Quero ver seus packs", callback_data="packs"))
    markup.add(types.InlineKeyboardButton("👑 Quero ser VIP", callback_data="vip"))
    markup.add(types.InlineKeyboardButton("📞 Quero te ligar", callback_data="call"))
    markup.add(types.InlineKeyboardButton("😏 Ver amostra", callback_data="amostra"))

    texto = """😈 <b>Oi safado... bem vindo ao meu cantinho</b> 🔥

Eu sou a Vickzinhaa Safadinha... 
aquela que adora provocar e mostrar tudinho pra você.

Tá com tesão? Então escolhe o que você quer fazer comigo 👇"""

    bot.send_message(message.chat.id, texto, parse_mode='HTML', reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    if call.data == "packs":
        texto = """<b>🔥 MEUS PACKS BEM SAFADOS</b>

📸 <b>Pack 100 Fotos Pelada</b> — R$ 14,90
📹 <b>Pack Fotos + Vídeos Gemendo</b> — R$ 19,90
👑 <b>Grupo VIP Completo (tudo liberado)</b> — R$ 23,90

Digite o número do que você quer ver de mim:
/comprar 1
/comprar 2
/comprar 3"""

        bot.send_message(call.message.chat.id, texto, parse_mode='HTML')

    elif call.data == "vip":
        bot.send_message(call.message.chat.id, "👑 Quer ter acesso total a mim todo dia? Digite /comprar 3 safado 🔥")

    elif call.data == "call":
        bot.send_message(call.message.chat.id, "📞 Quer me ligar e me ouvir gemendo até você gozar? R$ 20,90\n\nDigite: /comprar 4")

    elif call.data == "amostra":
        bot.send_message(call.message.chat.id, "😏 Olha só uma amostrinha do que eu tenho pra você... (em breve envio foto)")

@bot.message_handler(commands=['comprar'])
def comprar(message):
    try:
        opcao = int(message.text.split()[1])
        itens = {
            1: ("Pack 100 Fotos Pelada", 14.90),
            2: ("Pack Fotos + Vídeos Gemendo", 19.90),
            3: ("Grupo VIP Completo", 23.90),
            4: ("Call Particular até Gozar", 20.90)
        }
        
        produto, valor = itens.get(opcao, (None, None))
        if not produto:
            return bot.send_message(message.chat.id, "❌ Opção errada safado!")

        texto = f"""😈 <b>Você quer {produto.lower()}?</b>

💰 Valor: R$ {valor:.2f}

Faz o Pix agora que eu libero tudo rapidinho pra você me ver bem safadinha 🔥

Manda o comprovante aqui depois do pagamento..."""

        bot.send_message(message.chat.id, texto, parse_mode='HTML')
        
    except:
        bot.send_message(message.chat.id, "Use: /comprar 1, 2, 3 ou 4")

print("😈 Vickzinhaa Safadinha está bem molhadinha e online...")
bot.infinity_polling()
