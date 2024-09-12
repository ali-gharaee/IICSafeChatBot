import torch
import logging
from transformers import AutoTokenizer, AutoModelForSequenceClassification

# Load the fine-tuned hate speech model globally, so it's loaded only once
tokenizer = AutoTokenizer.from_pretrained("facebook/roberta-hate-speech-dynabench-r4-target")
model = AutoModelForSequenceClassification.from_pretrained("facebook/roberta-hate-speech-dynabench-r4-target")

def check_with_fine_tuned_model(message):
    """Use the fine-tuned model to detect hate speech."""
    logging.info("Using fine-tuned model for extremism check")

    # Tokenize the input message
    inputs = tokenizer(message, return_tensors="pt")

    # Get model predictions
    with torch.no_grad():
        outputs = model(**inputs)

    # Get the predicted class (logits)
    logits = outputs.logits
    predicted_class = torch.argmax(logits, dim=1).item()

    # Interpret the class label (assuming class 1 = hate speech, 0 = not hate speech)
    if predicted_class == 1:
        return True, "The message contains hate speech."
    else:
        return False, "The message does not contain hate speech."
