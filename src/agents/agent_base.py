# import openai
# from abc import ABC, abstractmethod
# from loguru import logger
# import os
# from dotenv import load_dotenv

# # Load environment variables
# load_dotenv()

# openai.api_key = os.getenv("OPENAI_API_KEY")

# class AgentBase(ABC):
#     def __init__(self, name, max_retries=2, verbose=True):
#         self.name = name
#         self.max_retries = max_retries
#         self.verbose = verbose

#     @abstractmethod
#     def execute(self, *args, **kwargs):
#         pass

#     def call_openai(self, messages, temperature=0.7, max_tokens=150):
#         retries = 0
#         while retries < self.max_retries:
#             try:
#                 if self.verbose:
#                     logger.info(f"[{self.name}] Sending messages to OpenAI:")
#                     for msg in messages:
#                         logger.debug(f"  {msg['role']}: {msg['content']}")
#                 response = openai.chat.completions.create(
#                     model="gpt-4",
#                     messages=messages,
#                     temperature=temperature,
#                     max_tokens=max_tokens,
#                 )
#                 reply = response.choices[0].message
#                 if self.verbose:
#                     logger.info(f"[{self.name}] Received response: {reply}")
#                 return reply
#             except Exception as e:
#                 retries += 1
#                 logger.error(f"[{self.name}] Error during OpenAI call: {e}. Retry {retries}/{self.max_retries}")
#         raise Exception(f"[{self.name}] Failed to get response from OpenAI after {self.max_retries} retries.")

import os
from abc import ABC, abstractmethod
from loguru import logger
import openai
import litellm  # Lightweight wrapper for Groq API
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Retrieve API keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
DEFAULT_LLM = os.getenv("DEFAULT_LLM", "openai").lower()  # Default is OpenAI

class AgentBase(ABC):
    def __init__(self, name, llm_provider=DEFAULT_LLM, max_retries=2, verbose=True):
        self.name = name
        self.llm_provider = llm_provider
        self.max_retries = max_retries
        self.verbose = verbose

    @abstractmethod
    def execute(self, *args, **kwargs):
        pass

    def call_llm(self, messages, temperature=0.7, max_tokens=150):
        """
        Calls either OpenAI or Groq based on the selected LLM provider.
        """
        retries = 0
        while retries < self.max_retries:
            try:
                if self.verbose:
                    logger.info(f"[{self.name}] Using LLM Provider: {self.llm_provider.upper()}")
                    logger.info(f"[{self.name}] Sending messages to LLM:")
                    for msg in messages:
                        logger.debug(f"  {msg['role']}: {msg['content']}")

                # Select API call based on provider
                if self.llm_provider == "openai":
                    openai.api_key = OPENAI_API_KEY
                    response = openai.chat.completions.create(
                        model="gpt-4",
                        messages=messages,
                        temperature=temperature,
                        max_tokens=max_tokens,
                    )
                    reply = response.choices[0].message
                elif self.llm_provider == "groq":
                    response = litellm.completion(
                        model="groq/llama3-70b-8192",
                        messages=messages,
                        api_key=GROQ_API_KEY,
                        temperature=temperature,
                        max_tokens=max_tokens,
                    )
                    reply = response["choices"][0]["message"]
                else:
                    raise ValueError(f"Invalid LLM provider: {self.llm_provider}")

                if self.verbose:
                    logger.info(f"[{self.name}] Received response: {reply}")
                return reply

            except Exception as e:
                retries += 1
                logger.error(f"[{self.name}] Error during LLM call: {e}. Retry {retries}/{self.max_retries}")

        raise Exception(f"[{self.name}] Failed to get response from LLM after {self.max_retries} retries.")
