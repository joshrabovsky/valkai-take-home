# Evaluation Harness

Runs a scripted 21-turn conversation through all 6 memory agents in parallel and scores how well each one recalls facts about the user.

## Prerequisites

Make sure you have a `.env` file at the project root with your API keys:

```
ANTHROPIC_API_KEY=your-key

# Optional: enables LangSmith tracing (smith.langchain.com)
# LANGSMITH_TRACING=true
# LANGSMITH_API_KEY=your-key
# LANGSMITH_PROJECT=your-langsmith-project
```

LangSmith keys are optional. The harness runs fine without them — tracing is simply disabled.

## Running the Harness

From the project root:

```bash
cd evals && uv run python harness.py
```

## What It Does

1. Instantiates all 6 memory agents
2. Runs each agent through the same 21-turn script concurrently
3. On turns that have expected keywords, a judge LLM scores whether the agent recalled correctly
4. Prints each agent's full conversation log followed by a summary table

## CLI Options

You can tune the behavior of individual agents via flags:

| Flag | Default | Description |
|---|---|---|
| `--summary-agent-threshold` | 5 | Number of messages before Summary Agent compresses history |
| `--summary-buffer-agent-threshold` | 10 | Number of messages before Summary Buffer Agent compresses |
| `--summary-buffer-agent-buffer-amount` | 5 | Number of recent messages to keep alongside the summary |
| `--vector-agent-num-similar` | 8 | Number of similar messages to retrieve per turn |

Example:

```bash
cd evals && uv run python harness.py --summary-agent-threshold 3 --vector-agent-num-similar 5
```

## Agents Compared

| Agent | Memory Strategy |
|---|---|
| Buffer Memory Agent | Keeps full message history in a list |
| Summary Memory Agent | Compresses history into a summary after a threshold |
| Summary Buffer Memory Agent | Summary + retains the most recent N raw messages |
| Vector Memory Agent | Semantic similarity retrieval via FAISS |
| Store Memory Agent | Extracts structured facts into a LangGraph InMemoryStore |
| Checkpoint Memory Agent | LangGraph native MemorySaver checkpointer |

## Observability

If LangSmith keys are set in `.env`, all agent traces are sent automatically. You can view full reasoning chains, token usage, and latency per agent at `smith.langchain.com`.
