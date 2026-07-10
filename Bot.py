import telebot
from telebot import types
import os
from dotenv import load_dotenv

load_dotenv()

# ===================== CONFIGURAÇÕES =====================
TOKEN = os.getenv("TOKEN")
if not TOKEN:
    raise ValueError("TOKEN não encontrado no arquivo .env")

bot = telebot.TeleBot(TOKEN)

# ===================== PRODUTOS =====================
PRODUTOS = {
    1: {"nome": "Pack de Fotos", "valor": "14,90"},
    2: {"nome": "Pack Fotos + Vídeos", "valor": "24,90"},
    3: {"nome": "Acesso ao Grupo VIP", "valor": "35,90"}
}

# ===================== COMANDOS =====================
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(types.InlineKeyboardButton("🔥 Ver Packs", callback_data="catalogo"))
    markup.add(types.InlineKeyboardButton("👑 Grupo VIP", callback_data="vip"))
    markup.add(types.InlineKeyboardButton("❓ Ajuda", callback_data="ajuda"))

    bot.send_message(
        message.chat.id,
        "😈 *Olá safado!* Bem-vindo ao perfil da *Vickzinhaa Safadinha* 🔥\n\n"
        "Conteúdo exclusivo +18 pra você se deliciar...\n"
        "Escolha uma opção abaixo:",
        parse_mode='Markdown',
        reply_markup=markup
    )


@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    bot.answer_callback_query(call.id)  # Remove o "carregando" do botão

    if call.data == "catalogo":
        texto = """🔥 *PACKS DA VICKZINHAA*

📸 Pack de Fotos → *R$ 14,90*
📹 Pack Fotos + Vídeos → *R$ 24,90*
👑 Grupo VIP → *R$ 35,90*

Escolha digitando:
`/comprar 1` | `/comprar 2` | `/comprar 3`"""

        bot.send_message(call.message.chat.id, texto, parse_mode='Markdown')

    elif call.data == "vip":
        bot.send_message(
            call.message.chat.id,
            "👑 *Grupo VIP*\n\n"
            "• Fotos e vídeos novos todos os dias\n"
            "• Lives exclusivas\n"
            "• Conteúdo personalizado\n"
            "• Prioridade nos pedidos\n\n"
            "Quer acesso? Digite `/comprar 3`"
        )

    elif call.data == "ajuda":
        bot.send_message(
            call.message.chat.id,
            "ℹ️ *Como comprar:*\n\n"
            "1. Escolha o pack\n"
            "2. Digite `/comprar número`\n"
            "3. Faça o PIX\n"
            "4. Envie o comprovante aqui\n\n"
            "Qualquer dúvida é só chamar!"
        )


@bot.message_handler(commands=['comprar'])
def comprar(message):
    try:
        partes = message.text.strip().split()
        if len(partes) < 2:
            raise ValueError

        opcao = int(partes[1])
        
        if opcao not in PRODUTOS:
            bot.send_message(message.chat.id, "❌ Opção inválida! Use 1, 2 ou 3.")
            return

        produto = PRODUTOS[opcao]

        texto = f"""✅ *Pedido Registrado!*

🎁 *Produto:* {produto['nome']}
💰 *Valor:* R$ {produto['valor']}

📍 Faça o PIX e envie o comprovante aqui que eu libero seu acesso na hora! 🔥"""

        bot.send_message(message.chat.id, texto, parse_mode='Markdown')

    except:
        bot.send_message(
            message.chat.id,
            "❌ Uso correto:\n"
            "`/comprar 1`\n"
            "`/comprar 2`\n"
            "`/comprar 3`",
            parse_mode='Markdown'
        )


@bot.message_handler(commands=['ajuda', 'help'])
def ajuda(message):
    bot.send_message(
        message.chat.id,
        "🆘 *Comandos disponíveis:*\n\n"
        "/start - Voltar ao menu principal\n"
        "/comprar 1, 2 ou 3 - Fazer pedido\n"
        "/ajuda - Esta mensagem",
        parse_mode='Markdown'
    )


# ===================== INICIALIZAÇÃO =====================
if __name__ == "__main__":
    print("🔥 Vickzinhaa Safadinha está online... 🔥")
    bot.infinity_polling(none_stop=True)
