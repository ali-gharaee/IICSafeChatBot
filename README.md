# Telegram Hate Speech Detection Bot

This project is a Telegram bot designed to detect and handle hate speech and inappropriate content in group chats. The bot uses **OpenAI's GPT-3.5 Turbo** to classify messages and a fallback model, [**Facebook's fine-tuned Roberta hate-speech detection model**] (https://huggingface.co/facebook/roberta-hate-speech-dynabench-r4-target)!, when the OpenAI API is unavailable.

The bot automates handling inappropriate behavior based on predefined policies, restricting users from group participation after warnings, removing harmful content, and notifying group admins and the owner. It also provides the flexibility to configure various parameters via configuration files, making the bot adaptable to different group dynamics.

## Features and Policies

### 1. Message Handling and Policy

- **Warning Policy**: Each user receives a limited number of warnings (configurable) for inappropriate content.
- **Message Removal**: When inappropriate content is detected, the message is removed from the group (if configured).
- **Notification to Admin/Owner**: Each detected hate message is forwarded to the group owner and/or admins (as specified in the configuration).
- **Restriction Policy**: After exceeding the warning limit, the user is temporarily restricted from sending messages in the group for a defined period (configurable).
- **Second-Phase Warnings**: After the restriction is lifted, the user receives a reduced number of warnings (configurable). Exceeding these warnings results in the user being kicked from the group.

### 2. Fallback Model

- **Primary Model**: The bot primarily uses **OpenAI GPT-3.5 Turbo** to classify messages. If the OpenAI API fails (due to network issues or other problems), the bot falls back to the local fine-tuned Roberta hate-speech detection model (\`facebook/roberta-hate-speech-dynabench-r4-target\`).

### 3. Logging

- All actions are logged, including warnings, restrictions, and model decisions.
- Log files are automatically created to track the bot's actions for further analysis.

### 4. Modularized Codebase

- The codebase is fully modularized to allow for easy future development and maintenance. Each major function (e.g., message classification, warnings, restriction handling) is placed in its respective module.

## Configuration

All configurations are stored in the \`config/bot_config.properties\` file. This allows customization of the bot's behavior without modifying the source code directly.

**Example configuration:**

```ini
[warning_config]
warning_limit=3
second_warning_limit=2
block_duration=24  # Block duration in hours
admin_chat_ids=  # Admin IDs to notify
notify_recipients=owner,admins  # Can be "owner", "admins", or both
remove_message=true  # Remove inappropriate messages from the group
use_openai=true  # Use OpenAI API if true; otherwise fallback to local model
openai_api_key=sk-XXXXXXXXXXXXXXXXXXXXXXXXXXX  # OpenAI API key
```

## Requirements

To run this bot, the following requirements need to be installed:

1. **Python** 3.8 or higher
2. **Required Python libraries**:
   - \`openai\` (version 0.27.0 or higher)
   - \`torch\`
   - \`transformers\`
   - \`python-telegram-bot\`
   - \`httpx\`

Install the dependencies using the following command:

```bash
pip install -r requirements.txt
```

## Test Sentences

### Trigger Warnings (Inappropriate Content)

1. **Racist Content**:
   - "All people from [ethnic group] are terrible."

2. **Gender Discrimination**:
   - "Women should stay in the kitchen."

3. **Religious Discrimination**:
   - "People of [religion] are dangerous and shouldn't be trusted."

4. **Hate Speech**:
   - "I think we should get rid of all [nationality] people."

5. **Violence Incitement**:
   - "Let's meet up and destroy everything at the protest."

6. **Extremism**:
   - "We need to start a revolution and overthrow the government."

### Neutral or Safe Content (No Warnings)

1. "I had a great day today! How about you?"
2. "Let's discuss the project timeline and next steps."
3. "I think we should promote more diversity and inclusion in our workplace."
4. "What are everyone's thoughts on the upcoming event?"
5. "Let's stay positive and work together to solve the problem."

## Future Tasks

- **Restricted User Bonuses**: Add special features or bonuses to restricted users (e.g., gamification or redemption options) to encourage positive behavior.
- **Visualization Features**: Include visualizations of bot performance, such as:
   - Number of restrictions imposed over time.
   - User statistics (e.g., frequency of inappropriate content).
   - Sentiment analysis and other metrics on group activity.

## How to Run

1. Set up the bot token in your Telegram group.
2. Configure the necessary values in \`bot_config.properties\`.
3. Run the bot:

```bash
python -m bot.main
```

Logs will be written to the \`logs/\` directory for audit and analysis purposes.
