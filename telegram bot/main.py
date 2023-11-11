from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

token: Final = '6420441152:AAGwVM8jp-o9jSnksQR53JMC1CCxELrBAvo'
BOT_USERNAME: Final = '@TeleHelper2_bot'


# commands

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Hello! Thanks for Chatting With me I am bele , Created by Abdelrhman Nashaat')


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('I am bele Please Write Something so I can Respond!')


async def custom_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('This is a Custom Command!')


# Responses
def handle_response(text: str) -> str:
    processed: text = text.lower()
    if 'hello' in processed:
        return 'Hey There!'
    if 'how are you' in processed:
        return 'I am good'
    if 'i love python' in processed:
        return 'me too'
    return 'sorry I didn\'t understand What you wrote!'
if __name__ == '__main__':
    app = Application.builder().token(token).build()
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('custom', custom_command))
    app.run_polling(poll_interval=3)
    print('done')
