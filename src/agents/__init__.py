from .refiner_agent import RefinerAgent
from .write_article_validator_agent import WriteArticlealidatorAgent
from .sanitize_data_validator_agent import SanitizeDataValidatorAgent
from .summary_validator_agent import SummaryValidatorAgent
from .validator_agent import ValidatorAgent

from src.tools.sanitize_data_tool import SanitizeDataTool
from src.tools.summarize_tool import SummarizeTool
from src.tools.write_article_tool import WriteArticleTool

class AgentManager:
    def __init__(self, max_retries=3, verbose=True):
        self.agents = {
        "summarize": SummarizeTool(max_retries=max_retries, verbose=verbose),
        "write_article": WriteArticleTool(max_retries=max_retries, verbose=verbose),
        "sanitize_data": SanitizeDataTool(max_retries=max_retries, verbose=verbose),

        "summarize_validator": SummaryValidatorAgent(max_retries=max_retries, verbose=verbose),
        "write_article_validator": WriteArticlealidatorAgent(max_retries=max_retries, verbose=verbose),
        "sanitize_data_validator": SanitizeDataValidatorAgent(max_retries=max_retries, verbose=verbose),
        "refiner": RefinerAgent(max_retries=max_retries, verbose=verbose),
        "validator": ValidatorAgent(max_retries=max_retries, verbose=verbose)
        }
    
    def get_agent(self, agent_name):
        agent = self.agents.get(agent_name)
        
        if not agent:
            raise ValueError(f"Agent {agent_name} not found.")
        return agent 
        
