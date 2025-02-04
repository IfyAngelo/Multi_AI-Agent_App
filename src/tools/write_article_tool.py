from src.agents.agent_base import AgentBase

class WriteArticleTool(AgentBase):
    def __init__(self, llm_provider="openai", max_retries=3, verbose=True):
        super().__init__(name="WriteArticleTool", llm_provider=llm_provider, max_retries=max_retries, verbose=verbose)

    def execute(self, topic, outline=None):
        system_message = "You are an expert AI academic writer that writes articles on various topics."
        user_content = f"Write a research article on the topic:\nTopic: {topic}\n\n"

        if outline:
            user_content += f"Outline: {outline}\n\n"
        user_content += f"Article:\n"

        messages = [
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_content}
        ]

        article = self.call_llm(messages, max_tokens=1000)
        return article