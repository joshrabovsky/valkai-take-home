from langgraph.store.base import BaseStore
from langgraph.types import Checkpointer
from langchain.chat_models import init_chat_model
from deepagents import create_deep_agent


def make_agent(
    model_str: str = "anthropic:claude-haiku-4-5-20251001",
    system_prompt: str | None = None,
    checkpointer: Checkpointer | None = None,
    store: BaseStore | None = None,
):
    """Create a deep agent with the specified model provider.

    Args:
        model_str: Provider and model in "provider:model" format.
                   Examples: "openai:gpt-4o", "anthropic:claude-haiku-4-5-20251001",
                   "google_genai:gemini-2.5-flash"
        system_prompt: Optional system prompt override.

    Returns:
        A compiled LangGraph agent supporting .invoke(), .stream(), .astream().
    """
    model = init_chat_model(model_str)
    kwargs = {}
    if system_prompt:
        kwargs["system_prompt"] = system_prompt
    if checkpointer:
        kwargs["checkpointer"] = checkpointer
    if store:
        kwargs["store"] = store
    return create_deep_agent(model=model, **kwargs)
