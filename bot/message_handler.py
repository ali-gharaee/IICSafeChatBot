import logging
from bot.openai_integration import OpenAIIntegration
from bot.warnings_manager import WarningsManager

class MessageHandlerBot:
    def __init__(self, config):
        self.config = config
        self.bot_config = config['bot_config']
        self.warning_config = config['warning_config']
        
        # Initialize WarningsManager
        self.warnings_manager = WarningsManager(self.warning_config)

        # Initialize OpenAIIntegration with bot_config
        self.openai_integration = OpenAIIntegration(self.bot_config)

    async def handle_message(self, update, context):
        user = update.effective_user
        message_text = update.message.text

        # Check for extremism using the openai_integration
        is_extremist = self.openai_integration.check_for_extremism(message_text)

        if is_extremist:
            # Handle warnings and blocking using WarningsManager
            await self.warnings_manager.process_warning(user, update, context)
        else:
            logging.info(f"Message from {user.username}: {message_text}")
            # logging.info(f"OpenAI Response: {response}")
