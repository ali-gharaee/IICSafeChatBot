import logging
from bot.openai_integration import OpenAIIntegration

class MessageHandlerBot:
    def __init__(self, config):
        self.config = config
        self.bot_config = config['bot_config']
        self.warning_config = config['warning_config']
        
        # Check if use_openai is correctly loaded
        print(f"Use OpenAI: {self.bot_config.get('use_openai')}")

        # Initialize OpenAIIntegration with bot_config
        self.openai_integration = OpenAIIntegration(self.bot_config)
    async def handle_message(self, update, context):
        user = update.effective_user
        message_text = update.message.text

        # Check for extremism using the openai_integration
        is_extremist, response = self.openai_integration.check_for_extremism(message_text)

        if is_extremist:
            # Handle warnings and blocking (assuming there's a warnings manager in place)
            await self.warnings_manager.process_warning(user, update, context)
        else:
            # Log the message and the response from OpenAI for debugging
            username = user.username if user.username else "Unknown"
            logging.info(f"Message from {username}: {message_text}")
            logging.info(f"OpenAI Response: {response}")
