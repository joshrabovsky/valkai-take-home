# TODO

## Remaining Tasks

- [ ] Retune SummaryBuffer parameters and rerun harness
  - `summarizer_threshold` and `summary_buffer_amount` ratio must ensure buffer amount is significantly less than threshold
  - Use `/run-harness` skill to run with new params and save results

- [ ] Write project write-up
  - What you built (4 memory strategies + harness)
  - How you tested it (scripted conversation design, LLM-as-judge evaluation)
  - What you found (results table)
  - Trade-offs (when each strategy wins/loses, vector needs scale, tuning matters)

- [ ] Write README for the harness
  - How to run the harness (`uv run python -m evals.harness`)
  - What the output means
  - How to configure parameters
  - How to use the `/run-harness` skill

- [ ] Record Loom video walkthrough
  - Run the harness live
  - Explain each memory strategy
  - Walk through the results table and trade-offs

- [ ] Publish to public GitHub repo
  - Push final code
  - Share public link as submission
