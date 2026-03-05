from agent.memory.base import BaseMemoryAgent
from agent.memory import BufferMemoryAgent, SummaryMemoryAgent, SummaryBufferMemoryAgent, VectorMemoryAgent, StoreMemoryAgent, CheckpointMemoryAgent
from judge_agent import JudgeAgent
from harness_setup import SCRIPT

from tabulate import tabulate
from dotenv import load_dotenv
from concurrent.futures import ThreadPoolExecutor
import argparse

load_dotenv()
parser = argparse.ArgumentParser()
parser.add_argument("--summary-agent-threshold", type=int, default = 5)
parser.add_argument("--summary-buffer-agent-threshold", type=int, default = 10)
parser.add_argument("--summary-buffer-agent-buffer-amount", type=int, default = 5)
parser.add_argument("--vector-agent-num-similar", type=int, default = 8)
args = parser.parse_args()


class AgentResult:
    def __init__(self, agent_name: str):
        self.agent_name = agent_name
        self.log = []
        self.evals = []

def run_agent(agent: BaseMemoryAgent, judge: JudgeAgent) -> AgentResult:
    agent_results = AgentResult(agent.name)
    for i, turn in enumerate(SCRIPT):
        resp = agent.chat(turn.message)
        agent_results.log.append({
            "turn": i,
            "user": turn.message,
            "response": resp
        })
        if turn.expected_keywords:
            result = judge.evaluate(turn.message, turn.expected_keywords, resp)
            agent_results.evals.append(result)
    return agent_results


def print_summary(results: list[AgentResult]) -> None:
    headers = ["AGENT"]
    headers.extend([f"Turn: {i}" for i, turn in enumerate(SCRIPT) if turn.expected_keywords])
    rows = []
    for agent_result in results:
        print(f"\n{agent_result.agent_name} Conversation Log:")
        for log in agent_result.log:
            print(f"\nTurn {log['turn']}")
            print(f"You: {log['user']}")                                          
            print(f"{agent_result.agent_name}: {log['response']}")     
        row = [agent_result.agent_name]
        for evaluation in agent_result.evals:
            row.append(evaluation)
        rows.append(row)
    
    print("\nSummary:")
    print(tabulate(rows, headers=headers, tablefmt="grid"))

def main():
    agents = [
        BufferMemoryAgent(),
        SummaryMemoryAgent(summarizer_threshold=args.summary_agent_threshold),
        SummaryBufferMemoryAgent(summarizer_threshold=args.summary_buffer_agent_threshold, summary_buffer_amount=args.summary_buffer_agent_buffer_amount),
        VectorMemoryAgent(num_similar_messages=args.vector_agent_num_similar),
        StoreMemoryAgent(),
        CheckpointMemoryAgent()
    ]
    judge = JudgeAgent()
    with ThreadPoolExecutor(max_workers=len(agents)) as executor:
        all_results = list(executor.map(lambda a: run_agent(a, judge), agents))
    print_summary(all_results)
    

if __name__ == "__main__":
    main()