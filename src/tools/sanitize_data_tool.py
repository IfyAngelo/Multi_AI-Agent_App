from src.agents.agent_base import AgentBase

class SanitizeDataTool(AgentBase):
    def __init__(self, max_retries, verbose=True):
        super().__init__(name="SanitizeDataTool", max_retries=max_retries, verbose=verbose)

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
        sanitized_data = self.call_openai(messages, max_tokens=300)
        return sanitized_data