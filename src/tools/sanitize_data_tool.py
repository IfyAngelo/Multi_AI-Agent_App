from src.agents.agent_base import AgentBase

class SanitizeDataTool(AgentBase):
    def __init__(self, llm_provider="openai", max_retries=3, verbose=True):
        super().__init__(name="SanitizeDataTool", llm_provider=llm_provider, max_retries=max_retries, verbose=verbose)

    def execute(self, medical_data):
        messages = [
            {"role": "system", "content": "You are an AI assistant that sanitizes medical data by removing Prtected Health Information (PHI):"},
            {
                "role": "user",
                "content": (
                    "Remove all PHI from the following data:\n\n"
                    f"{medical_data}\n\Sanitized Data:"
                )
            }
        ]
        sanitized_data = self.call_llm(messages, max_tokens=300)
        return sanitized_data