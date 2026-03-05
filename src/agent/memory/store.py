from langgraph.store.memory import InMemoryStore
from langchain.chat_models import init_chat_model
from agent.memory.base import BaseMemoryAgent
import json

class StoreMemoryAgent(BaseMemoryAgent):

    DEFAULT_MODEL = "anthropic:claude-haiku-4-5-20251001"
    

    def __init__(self, **kwargs):
        self.store = InMemoryStore()
        super().__init__(store=self.store, **kwargs)
        self.extractor = init_chat_model(self.DEFAULT_MODEL)
        self.namespace = ("user", "profile")
        
    @property
    def name(self) -> str:
        return "Store Memory Agent"

    def chat(self, message: str) -> str:
        item = self.store.get(self.namespace, "facts")
        facts = item.value if item else {}
        messages = []
        if facts:
            messages.append({"role": "system", "content": f"Known facts about the user: {json.dumps(facts)}"})
        messages.append({"role": "user", "content": message})
        result = self.agent.invoke({"messages": messages})
        extraction_prompt = self._extraction_prompt(message, result["messages"][-1].content)
        extraction = self.extractor.invoke(extraction_prompt)
        try:
            exetraction_content = extraction.content.strip("```json")
            exetraction_content = exetraction_content.strip("```")
            new_facts = json.loads(exetraction_content)
        except json.JSONDecodeError:
            print(f"Failed to parse JSON: {extraction.content}")
            new_facts = {}
        merged = {**facts, **new_facts}
        self.store.put(self.namespace, "facts", merged)
        return result["messages"][-1].content
    
    def _extraction_prompt(self, message: str, result: str) -> str:
        return f"""
            Extract any new facts about the user from
            this exchange. Return ONLY a valid JSON object.
            If nothing new was learned, return {{}}.

            User said: {message}
            Assistant said: {result}

            Examples of facts to extract: name, location, job, preferences, numbers they mention about themselves.
            Do not include general knowledge answers.
            """
