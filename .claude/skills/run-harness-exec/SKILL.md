---
name: run-harness-exec
description: Internal skill that executes the memory agent evaluation harness. Invoked by run-harness with collected parameters.
context: fork
disable-model-invocation: true
user-invocable: false
argument-hint: "[summary-agent-threshold] [summary-buffer-agent-threshold] [summary-buffer-agent-buffer-amount] [vector-agent-num-similar]"
---

Execute the memory agent evaluation harness with the following parameters:

- summary_agent_threshold: $0
- summary_buffer_agent_threshold: $1
- summary_buffer_agent_buffer_amount: $2
- vector_agent_num_similar: $3

## Steps

1. Determine the next test number by counting existing files in `evals/results/`. Name the output file `evals/results/test-{N}.md`.

2. Create the `evals/results/` directory if it doesn't exist.

3. Run the harness with the parameters as CLI flags:
   ```
   uv run python -m evals.harness \
     --summary-agent-threshold $0 \
     --summary-buffer-agent-threshold $1 \
     --summary-buffer-agent-buffer-amount $2 \
     --vector-agent-num-similar $3
   ```

4. Capture the full terminal output.

5. Write the results to `evals/results/test-{N}.md` with the following structure:

   ```markdown
   # Harness Run — Test {N}

   ## Parameters
   ### SummaryMemoryAgent
   - summarizer_threshold: $0

   ### SummaryBufferMemoryAgent
   - summarizer_threshold: $1
   - summary_buffer_amount: $2

   ### VectorMemoryAgent
   - num_similar_messages: $3

   ## Conversation Logs
   {full conversation output per agent}

   ## Summary Table
   {results table}
   ```

6. Return the summary table and the output file path.
