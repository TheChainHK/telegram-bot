from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes
import configparser
import logging
import asyncio

def main():
    config = configparser.ConfigParser()
    config.read('config.ini')
    
    application = Application.builder().token(config['TELEGRAM']['ACCESS_TOKEN']).build()

    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
    application.initialize()
    application.start()
    application.run_polling()

async def echo(update, context):
    reply_message = update.message.text.upper()
    logging.info("Update: " + str(update))
    logging.info("Context: " + str(context))
    await context.bot.send_message(chat_id=update.message.chat_id, text=reply_message)

if __name__ == '__main__':
    main()
    