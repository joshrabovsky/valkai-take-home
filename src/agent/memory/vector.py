from agent.memory.base import BaseMemoryAgent
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

class VectorMemoryAgent(BaseMemoryAgent):

    DEFAULT_HUGGINGFACE_EMBEDDINGS_MODEL = "all-MiniLM-L6-v2"

    def __init__(self, num_similar_messages=3, **kwargs):
        super().__init__(**kwargs)
        self.num_similar_messages = num_similar_messages
        self.vectorstore = None
        self.embeddings = HuggingFaceEmbeddings(model_name=self.DEFAULT_HUGGINGFACE_EMBEDDINGS_MODEL)
    
    @property
    def name(self) -> str:
        return "Vector Memory Agent"
    
    def chat(self, message: str) -> str:
        self._store_message("user", message)
        similar_messages = self._retrieve_messages(message)
        messages_to_send = [*similar_messages, {"role": "user", "content": message}]
        result = self.agent.invoke({"messages": messages_to_send})
        self._store_message("assistant", result["messages"][-1].content)
        return result["messages"][-1].content
    
    def _store_message(self, role: str, content: str) -> None:
        if not self.vectorstore:
            self.vectorstore = FAISS.from_texts([f"{role}: {content}"], self.embeddings)
        else:
            self.vectorstore.add_texts([f"{role}: {content}"])
    
    def _retrieve_messages(self, query: str) -> list[dict[str, str]]:
        docs = self.vectorstore.similarity_search(query, k=self.num_similar_messages)
        messages = []
        for doc in docs:
            role, content = doc.page_content.split(":", 1)
            messages.append({"role": role, "content": content})
        return messages
