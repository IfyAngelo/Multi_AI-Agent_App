from agents.agent_base import AgentBase

class RefinerAgent (AgentBase):
    def __init__(self, max_retries, verbose=True):
        super().__init__(name="RefinerAgent", max_retries=max_retries, verbose=verbose)

    def execute(self, topic, outline=None):
        messages = [
            {"role": "system",
            
            "content": [
                {
                    "type": "text",
                    "text": "You are an expert editor who refines and enhances articles for clarity, coherence and academic quality."
                }
            ]
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": (
                            "Please refine and enhance the following article draft on the topic of " + topic + ". This is to improve its language, coherence, and overall quality. Think step-by-step and provide detailed explanations for each change you make:\n\n"
                        )
                    }
                ]
            }
        ]
        
        refined_article = self.call_openai(messages, max_tokens=1024)
        return refined_article