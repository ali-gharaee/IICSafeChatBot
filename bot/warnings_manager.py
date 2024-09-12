class WarningsManager:
    def __init__(self, config):
        self.config = config
        self.warnings = {}  # Track warnings per user

    async def process_warning(self, user, update, context):
        user_id = user.id
        if user_id not in self.warnings:
            self.warnings[user_id] = 0

        self.warnings[user_id] += 1
        username = user.username

        # Decide which warning message to send based on the number of warnings
        if self.warnings[user_id] == 1:
            warning_message = self.config['first_warning_message'].format(username=username)
        elif self.warnings[user_id] == 2:
            warning_message = self.config['second_warning_message'].format(username=username)
        elif self.warnings[user_id] >= int(self.config['warning_limit']):
            warning_message = self.config['final_warning_message'].format(username=username, block_duration=self.config['block_duration'])
            await self.block_user(user, update, context)

        # Send the warning message
        await context.bot.send_message(chat_id=update.effective_chat.id, text=warning_message)

    async def block_user(self, user, update, context):
        block_duration = int(self.config['block_duration'])
        username = user.username

        # Block the user and notify the group
        block_message = self.config['block_message'].format(username=username, block_duration=block_duration)
        await context.bot.send_message(chat_id=update.effective_chat.id, text=block_message)

        # Notify the admin if needed
        admin_chat_id = int(self.config['admin_chat_id'])
        await context.bot.send_message(chat_id=admin_chat_id, text=block_message)

        # Block the user in the group
        await context.bot.ban_chat_member(update.effective_chat.id, user.id)
