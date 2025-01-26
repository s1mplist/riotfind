from typing import Any
from langchain_openai import ChatOpenAI
from langchain_core.runnables import Runnable, RunnableConfig

class LolAgent:
    def __init__(self,
                 runnable: Runnable,
                 config: RunnableConfig,
                 model_name: str = "gpt-4o-mini",
                 temperature: float = 0.0,
                 **kwargs
    ):
        self.runnable = runnable
        self.config = config
        self.llm = ChatOpenAI(model=model_name, temperature=temperature)