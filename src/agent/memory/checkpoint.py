from langgraph.checkpoint.memory import MemorySaver
from agent.memory.base import BaseMemoryAgent
import uuid

class CheckpointMemoryAgent(BaseMemoryAgent):

    def __init__(self, **kwargs):
        self.checkpointer = MemorySaver()
        super().__init__(checkpointer=self.checkpointer, **kwargs)
        self.thread_id = str(uuid.uuid4())
        
    @property
    def name(self) -> str:
        return "Checkpoint Memory Agent"

    def chat(self, message: str) -> str:
        messages = [{"role": "user", "content" : message}]
        result = self.agent.invoke(
            {"messages": messages},
            config={"configurable": {"thread_id": self.thread_id}}
        )
        return result["messages"][-1].content