'''
Test that multiple harnesses can run concurrently without interfering with each other's output files.
'''


import asyncio, os, tempfile
from pydantic import BaseModel
from agentfield import Agent
from agentfield.types import HarnessConfig

class Answer(BaseModel):
    question: str
    answer: str

async def test():
    agent = Agent(
        node_id="test-concurrent",
        harness_config=HarnessConfig(provider="claude-code"),
        auto_register=False,
    )

    cwd_a = tempfile.mkdtemp(prefix="harness_a_")
    cwd_b = tempfile.mkdtemp(prefix="harness_b_")

    task_a = agent.harness(
        "Set question='What is the capital of France?' and answer='Paris'.",
        schema=Answer,
        cwd=cwd_a,
    )
    task_b = agent.harness(
        "Set question='What is 6 * 7?' and answer='42'.",
        schema=Answer,
        cwd=cwd_b,
    )

    result_a, result_b = await asyncio.gather(task_a, task_b)

    assert not result_a.is_error, f"Task A failed: {result_a.error_message}"
    assert not result_b.is_error, f"Task B failed: {result_b.error_message}"
    assert isinstance(result_a.parsed, Answer)
    assert isinstance(result_b.parsed, Answer)
    # No leftover files
    assert not os.path.exists(os.path.join(cwd_a, ".agentfield_output.json"))
    assert not os.path.exists(os.path.join(cwd_b, ".agentfield_output.json"))
    print("PASS — A:", result_a.parsed, "B:", result_b.parsed)

asyncio.run(test())
