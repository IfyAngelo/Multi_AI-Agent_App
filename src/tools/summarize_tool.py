from src.agents.agent_base import AgentBase

class SummarizeTool(AgentBase):
    def __init__(self, llm_provider="openai", max_retries=3, verbose=True):
        super().__init__(name="SummarizeTool", llm_provider=llm_provider, max_retries=max_retries, verbose=verbose)

    def execute(self, text):
        messages = [
            {"role": "system", "content": "You are an AI assistant that summarizes medical text:"},
            {
                "role": "user",
                "content": (
                    "Please provide a concise summary of the following text:\n\n"
                    f"{text}\n\nSummary:"
                )
            }
        ]
        summary = self.call_llm(messages, max_tokens=300)
        return summary