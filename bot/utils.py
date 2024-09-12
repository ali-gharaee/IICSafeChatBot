import configparser
import os
import logging


def load_config():
    config = configparser.ConfigParser()

    # Load bot configuration
    bot_config_path = 'config/bot_config.properties'
    warning_config_path = 'config/warnings_config.properties'
    logging_config_path = 'config/logging_config.properties'
    
    # Ensure both files exist
    if not os.path.exists(bot_config_path):
        raise FileNotFoundError(f"{bot_config_path} not found")
    if not os.path.exists(warning_config_path):
        raise FileNotFoundError(f"{warning_config_path} not found")
    if not os.path.exists(logging_config_path):
        raise FileNotFoundError(f"{logging_config_path} not found")
    
    # Load bot configuration file
    config.read(bot_config_path)
    if 'bot_config' not in config:
        raise KeyError("Section [bot_config] not found in bot_config.properties")
    bot_config = config['bot_config']

    # Load warning messages configuration file
    config.read(warning_config_path)
    if 'warning_messages' not in config:
        raise KeyError("Section [warning_messages] not found in warnings_config.properties")
    warning_config = config['warning_messages']
    
    # Load logging messages configuration file
    config.read(logging_config_path)
    if 'logging_config' not in config:
        raise KeyError("Section [logging_config] not found in logging_config.properties")
    logging_config = config['logging_config']

    # Return both configurations as a dictionary
    return {
        'bot_config': bot_config,
        'warning_config': warning_config,
        'logging_config': logging_config
    }
    
async def get_admins_and_owner(update, context):
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
    
