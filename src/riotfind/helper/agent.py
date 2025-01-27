from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder


class AgentHelper:
    def __init__(self, model_name: str, system_prompt: str, **kwargs):
        self.model_name = model_name
        self.system_prompt = system_prompt

        self.model = self._build_llm(model_name, **kwargs)
        self.prompt_template = self._build_prompt(system_prompt)

    def _build_llm(self, model_name, **kwargs):
        return ChatOpenAI(model=model_name, **kwargs)

    def _build_prompt(self, system_prompt: str):
        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", system_prompt),
                MessagesPlaceholder(variable_name="messages"),
                MessagesPlaceholder(variable_name="agent_scratchpad"),
            ]
        )
        return prompt

    def prompt(self):
        return self.prompt_template

    def llm(self):
        return self.model
