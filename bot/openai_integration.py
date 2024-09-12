import openai
import logging

from bot.prompt_builder import PromptBuilder
from bot.fine_tuned_model import FineTunedModel

class OpenAIIntegration:
    def __init__(self, config):
        self.api_key = config['openai_api_key']
        self.config = config
        
        # self.use_openai = config.get('use_openai', 'true').lower() == True
        self.use_openai = (config['use_openai']) == 'true'
        openai.api_key = self.api_key
        self.prompt_builder = PromptBuilder()
        
        self.fine_tuned_model = FineTunedModel()

    
    
    def check_for_extremism(self, message):
        logging.info(self.config['use_openai'])
        logging.info(f"OpenAI API is called")
        logging.info(str(self.use_openai))
        
        # if not self.use_openai:
        #     return self.fine_tuned_model.check_with_fine_tuned_model(message)

        # OpenAI API logic
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                # messages=[{"role":"user","content":self.prompt_builder.build_prompt_str(message)}],
                messages=[{"role": "system", "content": "You are a conversational bot."},
                          {"role": "user", "content": self.prompt_builder.build_prompt_str(message)}],
                
                max_tokens=300,
                temperature=0.7
            )
            
            result_text = response["choices"][0]["message"]["content"].strip()

            # result_text = response['choices'][0]['text'].strip().lower()
            logging.info(result_text)
            return True if "yes" in result_text.lower() else False


        except Exception as e:
            logging.error(f"OpenAI API error: {e}")
            return self.fine_tuned_model.check_with_fine_tuned_model(message)
            # return False, "OpenAI API error" result_text

        except Exception as e:
            logging.error(f"OpenAI API error: {e}")
            return self.fine_tuned_model.check_with_fine_tuned_model(message)
            # return False, "OpenAI API error"
