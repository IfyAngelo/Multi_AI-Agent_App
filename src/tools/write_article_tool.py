from src.agents.agent_base import AgentBase

class WriteArticleTool(AgentBase):
    def __init__(self, max_retries, verbose=True):
        super().__init__(name="WriteArticleTool", max_retries=max_retries, verbose=verbose)

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

        article = self.call_openai(messages, max_tokens=1000)
        return article