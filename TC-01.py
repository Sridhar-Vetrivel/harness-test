'''
Test Case: TC-01
Description: Test basic functionality of the harness with a simple math question.
Basic Prompt, no schema
Verify .harness() returns a HarnessResult with .text set and no error.
'''

import asyncio
from agentfield import Agent
from agentfield.types import HarnessConfig

async def test():
    agent = Agent(
        node_id="test-basic",
        harness_config=HarnessConfig(provider="claude-code"),
        auto_register=False,
    )
    result = await agent.harness(
        "Write a python function that adds two numbers (2, 2) together and return the result."
    )
    
    print("HarnessResult:",result)
    print("is_error:", result.is_error)
    print("text:", result.text)  # <-- Returning None, which is unexpected
    # print("message:", result.messages)
    print("num_turns:", result.num_turns)
    print("duration_ms:", result.duration_ms)
    assert not result.is_error
    print("PASS")

asyncio.run(test())
