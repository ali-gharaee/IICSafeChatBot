import configparser
import os
import logging


def load_config():
    config = configparser.ConfigParser()

    # Load bot configuration
    bot_config_path = 'config/bot_config.properties'
    warning_config_path = 'config/warnings_config.properties'
    
    # Ensure both files exist
    if not os.path.exists(bot_config_path):
        raise FileNotFoundError(f"{bot_config_path} not found")
    if not os.path.exists(warning_config_path):
        raise FileNotFoundError(f"{warning_config_path} not found")
    
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

    # Return both configurations as a dictionary
    return {
        'bot_config': bot_config,
        'warning_config': warning_config
    }
    # Configure the logging format and level
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
        )
