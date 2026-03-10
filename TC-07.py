'''Rich Schema Test
Verify that the harness can handle a more complex schema with nested structures and lists.
'''


import asyncio
from typing import List
from pydantic import BaseModel
from agentfield import Agent
from agentfield.types import HarnessConfig

class CodeReview(BaseModel):
    summary: str
    score: int
    suggestions: List[str]

async def test():
    agent = Agent(
        node_id="test-rich-schema",
        harness_config=HarnessConfig(provider="claude-code"),
        auto_register=False,
    )
    result = await agent.harness(
        "Review this code: `def add(a, b): return a + b`. "
        "Provide a summary, a score from 1-10, and a list of 2-3 suggestions.",
        schema=CodeReview,
    )
    assert not result.is_error
    assert isinstance(result.parsed, CodeReview)
    assert 1 <= result.parsed.score <= 10
    assert isinstance(result.parsed.suggestions, list)
    assert len(result.parsed.suggestions) >= 1
    print("PASS — score:", result.parsed.score, "suggestions:", result.parsed.suggestions)

asyncio.run(test())
