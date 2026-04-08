import asyncio
from agentfield import Agent
from agentfield.types import HarnessConfig

async def test():
    agent = Agent(
        node_id="test-bad-schema",
        harness_config=HarnessConfig(provider="claude-code"),
        auto_register=False,
    )
    try:
        await agent.harness(
            "Do something.",
            schema="this is a string, not a schema",  # invalid
            cwd="/home/sridharvetrivel/harness-test",
        )
        print("FAIL — should have raised TypeError")
    except TypeError as e:
        print("Got expected TypeError:", e)
        assert "Unsupported schema type" in str(e) or "str" in str(e)
        print("PASS")

asyncio.run(test())
