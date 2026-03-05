from langchain.chat_models import init_chat_model
from agent.memory.base import BaseMemoryAgent

class SummaryMemoryAgent(BaseMemoryAgent):

    DEFAULT_MODEL = "anthropic:claude-haiku-4-5-20251001"

    def __init__(self, summarizer_threshold: int = 10, **kwargs):
        summarizer_model = kwargs.pop("summarizer_model", self.DEFAULT_MODEL)
        super().__init__(**kwargs)
        self.messages = []
        self.summarizer_threshold = summarizer_threshold
        self.summarizer = init_chat_model(summarizer_model)
    
    @property
    def name(self) -> str:
        return "Summary Memory Agent"

    def chat(self, message: str) -> str:
        self.messages.append({"role": "user", "content": message})
        result = self.agent.invoke({"messages": self.messages})
        self.messages = result["messages"]
        ai_msg = result["messages"][-1]
        
        if len(self.messages) >= self.summarizer_threshold:
            self._summarize_messages()

        return ai_msg.content

    def _summarize_messages(self) -> None:
        self.messages.append({"role": "user", "content": "Please summarize our conversation so far."})
        result = self.summarizer.invoke(self.messages)
        self.messages = [{"role": "system", "content": result.content}]

        