# Memory Types — Approach & Results

## Overview

We built a harness that runs six conversational agents, each implementing a different memory strategy, through the same scripted conversation. The goal is to compare how different forms of memory affect a model's ability to accurately recall information across a long conversation. Different memory strategies involve real trade-offs in cost, context size, and recall quality — the harness makes those differences visible and measurable.

The script runs for 21 turns. The first 16 turns establish personal facts about the user and ask general knowledge questions. The final 5 turns test recall by asking the agent to surface specific information introduced earlier. Each recall turn is evaluated by a secondary judge agent that checks whether the expected keyword appears in the response.

---

## Memory Strategies

There are six memory agents:

**Buffer Memory Agent** stores a running list of all user and agent messages. Every turn, the full history is passed to the model. The key trade-off is completeness vs. cost — you have everything in context, but the conversation grows unboundedly, increasing latency and token usage with every turn.

**Summary Memory Agent** summarizes the conversation every X turns using a secondary LLM call, replacing the full history with a compressed summary. This bounds context size over time but is lossy — the summarizer decides what to keep, and thin facts like bare numbers are often dropped.

**Summary Buffer Memory Agent** combines both approaches: it summarizes older history when the threshold is hit but retains the last X raw turns alongside the summary. In theory this preserves the most recent and therefore most relevant context while keeping overall size bounded. Performance is sensitive to both the summary threshold and the buffer size.

**Vector Memory Agent** stores every message as an embedding in a FAISS vector store. On each turn, cosine similarity is used to retrieve the K most relevant past messages, which are injected into context. The trade-off is that retrieval is more efficient than passing a full history, but it has failure modes: if K is too small, relevant facts get crowded out. It also depends on semantic overlap — if the recall question is phrased differently from the original statement, the right message may not rank highly enough to be retrieved.

**Store Memory Agent** uses LangGraph's native `InMemoryStore`. After each turn, a secondary extractor LLM parses the exchange and writes any new user facts as structured key-value pairs into the store. Before each turn, those facts are retrieved and prepended as a system message. Because facts are stored explicitly rather than buried in message history, recall is not affected by context length or similarity thresholds. The trade-off is additional overhead — an extra LLM call is made on every turn to extract facts.

**Checkpoint Memory Agent** uses LangGraph's native `MemorySaver` checkpointer. Rather than manually maintaining a message list, the graph persists its own full state between invocations keyed by a `thread_id` — effectively a session ID. Only the new user message needs to be passed on each call; the full history is loaded automatically. Functionally equivalent to Buffer, but the framework owns the state rather than application code, making it portable across process restarts.

---

## Results & Key Findings

Three harness runs were conducted, varying the summarizer threshold, summary buffer amount, and number of similar messages (K) for the vector agent.

**Buffer Memory Agent** should theoretically score 5/5 on every run since it passes the full conversation history on every turn. At only 21 turns the context window is never exceeded. Any failures are attributable to `deepagents`' internal `SummarizationMiddleware`, which can compress long conversations automatically regardless of the memory strategy used.

**Summary Memory Agent** behaves identically to Buffer when the threshold is set high enough that it never triggers within 21 turns. When the threshold is low, aggressive compression causes recall failures — compressing every 5 messages performed worse than compressing every 10 because personal facts introduced early get summarized away before enough conversation accumulates to reinforce them.

**Summary Buffer Memory Agent** behaves similarly to Summary. The critical edge case is when the buffer amount is set larger than the threshold — after each summarization, the retained messages immediately exceed the threshold again, triggering another summarization on the very next turn. This results in two LLM calls per turn and near-total context loss, making it both the most costly and least reliable configuration.

**Vector Memory Agent** is highly sensitive to K. With a small K (e.g. 3), the agent retrieves too few messages and personal facts get crowded out by general knowledge answers that happen to be semantically closer to the recall question. With a large K (e.g. 12), recall improves significantly because there is more opportunity for the relevant messages to surface. The failure mode is not the retrieval mechanism itself but the parameter tuning required to make it reliable.

**Checkpoint Memory Agent** behaves the same as Buffer — full history is passed on every turn, managed by the LangGraph framework rather than application code. Results track closely with Buffer across all runs.

**Store Memory Agent** consistently produced the best recall results. By extracting key facts after each turn and storing them as structured key-value pairs in LangGraph's `InMemoryStore`, the agent always has the most relevant user information available in a compact form. Context size stays minimal regardless of conversation length. The trade-off is an additional LLM call per turn for fact extraction, making it the most expensive strategy per turn.

---

## Experimental Findings

**Buffer** scored 4/5 in Tests 1 and 3, failing on Turn 18 (favourite number "9") despite having full history. This is consistent with `deepagents`' internal compression kicking in around turn 15–16, dropping semantically thin facts.

**Summary** at threshold 20 (Test 2) never triggered and scored 5/5 — identical to Buffer. At threshold 5 (Tests 1 and 3) it dropped to 4/5, losing Turn 18 to compression.

**Summary Buffer** was the most volatile. Test 1 (threshold 5, buffer 5) scored 1/5 — the only agent to catastrophically fail. Test 2 (threshold 20, buffer 7) recovered to 3/5. Test 3 (threshold 5, buffer 2) also 3/5. The small buffer means early personal facts never survive into the recall turns.

**Vector** at K=12 (Test 2) scored 5/5. At K=6 (Test 1) dropped to 4/5. At K=3 (Test 3) collapsed to 2/5, failing on job and company — facts with low semantic overlap with their recall questions.

**Store** scored 5/5 in both Test 2 and Test 3, the only agent unaffected by parameter changes.

**Checkpoint** tracked closely with Buffer — 4/5 in Test 2 and 3/5 in Test 3, with Turn 18 failing consistently.

---

## Trade-Offs & Production Considerations

The fundamental tension across all memory strategies is **context size vs. number of calls**.

One approach is to grow the context window over time — passing more and more history on each call. This is simple and high-fidelity but latency and cost increase linearly with conversation length. The other approach is to keep each call short by being selective about what gets passed, at the cost of additional work (summarization calls, retrieval, fact extraction) to decide what is relevant.

For short conversations, the difference is negligible. Over long-running sessions — which is the realistic production scenario for a platform used for many hours per day — unbounded context growth becomes a real problem. Strategies that keep context bounded and pass only the most relevant information per turn are more sustainable.

For production systems, the key-value store approach (Store Memory Agent) is the most promising of the strategies explored here. It keeps context minimal, is not sensitive to parameter tuning, and scales well with conversation length. The vector-based approach (Vector Memory Agent) is a strong complement — rather than retrieving raw messages, combining embedding-based search with structured fact storage would give both semantic flexibility and explicit reliability. A hybrid of the two is likely the best long-term architecture: structured facts for known user attributes, semantic retrieval for episodic context.
