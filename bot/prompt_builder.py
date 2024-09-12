class PromptBuilder:
    prompt_prefix: str = (
        "Is the following user message hate speech, racist, or extremist?\n user message:`"
    )
    prompt_suffix: str = (
        "`Answer 'yes' or 'no'. Explain why if 'yes'."
    )

    def build_prompt_str(
        self, chat_message
    ) -> str:
        # prefix + chunks + chat history (ending with "Assistant:")
        prompt = self.prompt_prefix
        prompt += chat_message
        prompt += self.prompt_suffix
        return prompt
