---
name: run-harness
description: Run the memory agent evaluation harness with configurable parameters, and save results to a timestamped markdown file.
disable-model-invocation: true
---

# run-harness

Collect parameters from the user and delegate execution to the run-harness-exec skill.

## Steps

1. Ask the user for the following parameters using AskUserQuestion, grouped by agent so each question is clearly tied to the agent it configures:

   - **SummaryMemoryAgent — `summarizer_threshold`**: how many messages before summarization triggers. Default: `10`
   - **SummaryBufferMemoryAgent — `summarizer_threshold`**: how many messages before summarization triggers (can differ from SummaryMemoryAgent). Default: `10`
   - **SummaryBufferMemoryAgent — `summary_buffer_amount`**: how many recent messages to keep after summarization. Default: `5`. Must be less than the SummaryBufferMemoryAgent `summarizer_threshold`.
   - **VectorMemoryAgent — `num_similar_messages`**: how many semantically similar messages to retrieve per turn. Default: `6`

   Ask these as separate AskUserQuestion calls (or group closely related ones together, e.g. both SummaryBufferMemoryAgent params in one call) so the user always knows which agent a parameter belongs to.

2. Invoke the `run-harness-exec` skill via the Skill tool, passing the four collected values as space-separated arguments in this order:
   ```
   {summary_agent_threshold} {summary_buffer_agent_threshold} {summary_buffer_agent_buffer_amount} {vector_agent_num_similar}
   ```

3. Tell the user the file was saved and show them the summary table returned by the subagent.
