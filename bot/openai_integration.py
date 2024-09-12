from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import openai
import logging

class OpenAIIntegration:
    def __init__(self, config):
        self.api_key = config['openai_api_key']
        self.use_openai = config.get('use_openai', 'true').lower() == 'true'
        openai.api_key = self.api_key

        # Load the fine-tuned hate speech model
        self.tokenizer = AutoTokenizer.from_pretrained("facebook/roberta-hate-speech-dynabench-r4-target")
        self.model = AutoModelForSequenceClassification.from_pretrained("facebook/roberta-hate-speech-dynabench-r4-target")
    
    def check_for_extremism(self, message):
        if not self.use_openai:
            return self.check_with_fine_tuned_model(message)

        # OpenAI API logic
        try:
            response = openai.Completion.create(
                engine="text-davinci-003",
                prompt=f"Is the following message hate speech, racist, or extremist? '{message}'\n"
                       f"Answer 'yes' or 'no'. Explain why if 'yes'.",
                max_tokens=100
            )

            result_text = response['choices'][0]['text'].strip().lower()
            return "yes" in result_text, result_text

        except Exception as e:
            logging.error(f"OpenAI API error: {e}")
            return False, "OpenAI API error"

    def check_with_fine_tuned_model(self, message):
        """Use the fine-tuned model to detect hate speech."""
        logging.info("Using fine-tuned model for extremism check")

        # Tokenize the input message
        inputs = self.tokenizer(message, return_tensors="pt")

        # Get model predictions
        with torch.no_grad():
            outputs = self.model(**inputs)

        # Get the predicted class (logits)
        logits = outputs.logits
        predicted_class = torch.argmax(logits, dim=1).item()

        # Interpret the class label (assuming class 1 = hate speech, 0 = not hate speech)
        if predicted_class == 1:
            return True, "The message contains hate speech."
        else:
            return False, "The message does not contain hate speech."
