import openai
import logging

from bot.prompt_builder import PromptBuilder
from fine_tuned_model import check_with_fine_tuned_model


class OpenAIIntegration:
    def __init__(self, config):
        self.api_key = config['openai_api_key']
        self.use_openai = config.get('use_openai', 'true').lower() == 'true'
        openai.api_key = self.api_key
        self.prompt_builder = PromptBuilder()

    
    def check_for_extremism(self, message):
        if not self.use_openai:
            return check_with_fine_tuned_model(message)

        # OpenAI API logic
        try:
            response = openai.Completion.create(
                model="gpt-3.5-turbo",
                prompt=self.prompt_builder.build_prompt_str(message),
                max_tokens=300,
                temperature=0.7
            )

            result_text = response['choices'][0]['text'].strip().lower()
            return "yes" in result_text, result_text

        except Exception as e:
            logging.error(f"OpenAI API error: {e}")
            return False, "OpenAI API error"

