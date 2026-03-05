from agent.memory.base import BaseMemoryAgent

class BufferMemoryAgent(BaseMemoryAgent):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.messages = []
    
    @property
    def name(self) -> str:
        return "Buffer Memory Agent"

    def chat(self, message: str) -> str:
        self.messages.append({"role": "user", "content": message})
        result = self.agent.invoke({"messages": self.messages})
        self.messages = result["messages"]
        ai_msg = result["messages"][-1]
        return ai_msg.content
