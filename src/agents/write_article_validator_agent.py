from .agent_base import AgentBase

class WriteArticlealidatorAgent(AgentBase):
    def __init__(self, max_retries=2, verbose=True):
        super().__init__(name="WriteArticleValidatorAgent", max_retries=max_retries, verbose=verbose)

    def execute(self, topic, article, outline=None):
        system_message = "You are an expert AI assistant that validates research articles on various topics."
        user_content = (
            "Given the topic and article, assess whether the article is well-written, coherent, and comprehensively covers the topic. Check if it maintains academic standards. Provide feedback analysis on the following article. Rate the article on a scale of 1 to 5, where 5 indicates excellent\n\n"
            f"Topic: {topic}\n\n"
            f"Article: {article}\n\n"
            "Validation:"
        )

        messages = [
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_content}
        ]
        
        validation = self.call_openai(messages, max_tokens=512)
        return validation