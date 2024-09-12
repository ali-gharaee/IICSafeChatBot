import logging
from datetime import timedelta, datetime

class WarningsManager:
    def __init__(self, config):
        self.config = config
        self.warning_limit = int(self.config['warning_limit'])  # First phase warning limit
        self.second_warning_limit = int(self.config['second_warning_limit'])  # Second phase warning limit
        self.block_duration = int(self.config['block_duration'])
        self.notify_recipients = self.config['notify_recipients'].split(',')  # Split the recipients string
        self.remove_message = self.config.get('remove_message', 'true').lower() == 'true'
        self.user_warnings = {}  # Stores warnings for each user
        self.user_blocked = {}  # Tracks whether the user has been blocked
    
    
    async def process_warning(self, user, update, context):
        user_id = user.id
        username = user.username or user.first_name or f"User {user_id}"

        # Notify the owner/admins with the user's message
        await self.notify_recipients_of_hate_message(user, update, context)

        # Optionally remove the hate message from the group
        if self.remove_message:
            await context.bot.delete_message(chat_id=update.effective_chat.id, message_id=update.message.message_id)
            logging.info(f"Message from {username} removed from the group.")

        # Check if the user has been blocked before
        if user_id in self.user_blocked:
            if self.user_blocked[user_id]:
                # The user has already been blocked, so check the second phase warnings
                warnings_after_block = self.user_warnings.get(user_id, 0)
                if warnings_after_block >= self.second_warning_limit:
                    # Kick the user after second-phase warnings are exceeded
                    await context.bot.kick_chat_member(update.effective_chat.id, user_id)
                    logging.info(f"{username} has been kicked out for exceeding the second warning limit.")
                    return
                else:
                    # Increment second-phase warnings
                    self.user_warnings[user_id] += 1
                    await self.send_warning(user, update, context, self.user_warnings[user_id])
            return

        # First phase: process warnings and block
        if user_id not in self.user_warnings:
            self.user_warnings[user_id] = 0

        # Increment warning count
        self.user_warnings[user_id] += 1

        # Check if the user has reached the warning limit
        if self.user_warnings[user_id] >= self.warning_limit:
            # Calculate the actual unblock time by adding the timedelta to the current time
            
            
            logging.info(self.block_duration)
            logging.info(timedelta(hours=self.block_duration))
            
            block_until = datetime.now() + timedelta(hours=self.block_duration)
            logging.info(block_until)
            # permission = context.bot.ChatPermissions = {"can_send_messages"}
            
            await context.bot.restrict_chat_member(update.effective_chat.id, user_id, permissions={'can_send_messages': False}, until_date=block_until)
            self.user_blocked[user_id] = True  # Mark the user as blocked
            self.user_warnings[user_id] = 0  # Reset warnings for the second phase
            logging.info(f"{username} has been restricted for 1 day")
            # logging.info(f"{username} has been banned for {self.block_duration} hours.")
        else:
            # Send a warning message
            await self.send_warning(user, update, context, self.user_warnings[user_id])

    # Rest of your code remains the same

    async def send_warning(self, user, update, context, warning_count):
        """Send a warning message to the user."""
        username = user.username or user.first_name or f"User {user.id}"
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"{username}, this is warning {warning_count} for inappropriate content."
        )
        logging.info(f"{username} has received warning {warning_count}.")

    async def notify_recipients_of_hate_message(self, user, update, context):
        """Notify the group owner and admins about the hate message."""
        username = user.username or user.first_name or f"User {user.id}"
        message_text = update.message.text

        # Get owner and admins dynamically
        owner, admin_chat_ids = await self.get_admins_and_owner(update, context)

        # Notify group owner
        if 'owner' in self.notify_recipients and owner:
            try:
                await context.bot.send_message(
                    chat_id=owner.id,
                    text=f"User {username} (ID: {user.id}) sent a hate message: '{message_text}'"
                )
                logging.info(f"Notified group owner {owner.id} about {username}'s hate message.")
            except Exception as e:
                logging.error(f"Failed to notify group owner {owner.id}: {e}")
        
        # Notify admins
        if 'admins' in self.notify_recipients:
            for admin_id in admin_chat_ids:
                try:
                    await context.bot.send_message(
                        chat_id=admin_id,
                        text=f"User {username} (ID: {user.id}) sent a hate message: '{message_text}'"
                    )
                    logging.info(f"Notified admin {admin_id} about {username}'s hate message.")
                except Exception as e:
                    logging.error(f"Failed to notify admin {admin_id}: {e}")

    async def get_admins_and_owner(self, update, context):
        """Fetch the group admins and the owner (creator) dynamically."""
        chat_id = update.effective_chat.id

        try:
            # Get the list of administrators for the chat
            admins = await context.bot.get_chat_administrators(chat_id)

            owner = None
            admin_chat_ids = []

            for admin in admins:
                if admin.status == 'creator':  # This is the owner (creator)
                    owner = admin.user
                elif admin.status == 'administrator':  # This is a regular admin
                    admin_chat_ids.append(admin.user.id)

            return owner, admin_chat_ids

        except Exception as e:
            logging.error(f"Error retrieving admins or owner: {e}")
            return None, []
