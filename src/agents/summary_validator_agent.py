from .agent_base import AgentBase

class SummaryValidatorAgent(AgentBase):
    def __init__(self, llm_provider="openai", max_retries=3, verbose=True):
        super().__init__(name="SummaryValidatorAgent", llm_provider=llm_provider, max_retries=max_retries, verbose=verbose)

    def execute(self, original_text, summary):
        system_message = "You are an expert AI assistant that validates the summaries of medical text."
        user_content = (
            "Given the original summary assess whether the summary accurately captures the key points and is of high quality\n"
            "Provide a brief analysis and rate the summarization process on a scale of 1 to 5, where 5 indicates excellent quality\n\n"
            f"Original Text: {original_text}\n\n"
            f"Summary: {summary}\n\n"
            "Validation"
        )

        messages = [
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_content}
        ]
        
        validation = self.call_llm(messages, max_tokens=512)
        return validation