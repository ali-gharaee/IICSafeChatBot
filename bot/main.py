import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters

from bot.message_handler import MessageHandlerBot
from bot.utils import load_config

logging.basicConfig(filename='logs/bot.log', level=logging.INFO)

class TelegramBot:
    def __init__(self):
        # Load all configurations
        self.config = load_config()

        # Pass the entire configuration dictionary to the message handler
        self.message_handler = MessageHandlerBot(self.config)

        # Access individual sections as needed
        self.bot_config = self.config['bot_config']
        self.application = Application.builder().token(self.bot_config['telegram_bot_token']).build()
        self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.message_handler.handle_message))
    
    def run(self):
        logging.info("Starting the bot")
        self.application.run_polling()

if __name__ == '__main__':
    bot = TelegramBot()
    bot.run()
