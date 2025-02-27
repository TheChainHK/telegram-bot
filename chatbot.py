from telegram import Update
from telegram.ext import Application, MessageHandler, CommandHandler, filters, CallbackContext
from ChatGPT_HKBU import HKBU_ChatGPT
import configparser
import logging
import redis

def main():
    config = configparser.ConfigParser()
    config.read('config.ini')

    global chatgpt
    chatgpt = HKBU_ChatGPT(config)
    
    application = Application.builder().token(config['TELEGRAM']['ACCESS_TOKEN']).build()

    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, equiped_chatgpt))
    
    # application.add_handler(CommandHandler("add", add))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("add", add))

    global redis1
    redis1 = redis.Redis(
        host=config['REDIS']['HOST'],
        port=config['REDIS']['REDISPORT'],
        decode_responses=config['REDIS']['DECODE_RESPONSE'],
        username=config['REDIS']['USER_NAME'],
        password=config['REDIS']['PASSWORD'],
    )

    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
    application.initialize()
    application.start()
    application.run_polling()

async def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    reply_message = "Helping you helping you."
    await context.bot.send_message(chat_id=update.message.chat_id, text=reply_message)

async def add(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /add is issued."""
    try:
        global redis1
        logging.info(context.args[0])
        msg = context.args[0]
        redis1.incr(msg)

        reply_message = f"You have said {msg} for {redis1.get(msg)} times."
        await context.bot.send_message(chat_id=update.message.chat_id, text=reply_message)
    except (IndexError, ValueError):
        await context.bot.send_message(chat_id=update.message.chat_id, text='Usage: /add <keyword>')

async def equiped_chatgpt(update, context):
    global chatgpt
    reply_message = chatgpt.submit(update.message.text)
    logging.info("Update: " + str(update))
    logging.info("context: " + str(context))
    await context.bot.send_message(chat_id=update.effective_chat.id, text=reply_message)

if __name__ == '__main__':
    main()
    