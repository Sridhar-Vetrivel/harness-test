import asyncio
from agentfield import Agent
from agentfield.types import HarnessConfig

async def test():
    agent = Agent(
        node_id="test-override",
        harness_config=HarnessConfig(provider="claude-code"),
        auto_register=False,
    )
    result = await agent.harness(
        "What is 3 + 3? Reply with only the number.",
        provider="codex",   # override the provider for this single call
    )
    
    print("HarnessResult:",result)
    print("is_error:", result.is_error)
    print("text:", result.text)
    assert not result.is_error

    print("PASS")

asyncio.run(test())
