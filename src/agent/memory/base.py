from abc import ABC, abstractmethod
from agent.core import make_agent

class BaseMemoryAgent(ABC):
   
    def __init__(
        self, 
        **kwargs
    ):
      """
      Initialize the memory agent.
      Args:
          **kwargs: Keyword arguments to pass to the make_agent function.
          Look inside make_agent for more details
      """
      self.agent = make_agent(**kwargs)

    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    def chat(self, message: str) -> str:
        pass