from langchain.chat_models import init_chat_model

class JudgeAgent:

    def __init__(self, model: str = "anthropic:claude-haiku-4-5-20251001"):
        self.model = init_chat_model(model)

    def evaluate(self, question: str, expected_keywords: list[str], response: str) -> bool:
        prompt = f"""
        Question: {question}
        Expected answer should contain any of the following keywords: {", ".join(expected_keywords)}
        Agent response: {response}

        Did the agent correctly recall the expected information?
        Answer only YES or NO.
        """
        result = self.model.invoke(prompt)
        return result.content.strip().upper() == "YES"