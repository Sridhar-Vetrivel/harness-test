


import asyncio
from agentfield import Agent

async def test():
    agent = Agent(node_id="test-bad-provider", auto_register=False)
    try:
        await agent.harness(
            "Do something.",
            provider="gpt-5-turbo-ultra",  # not real
            cwd="/tmp/harness-test",
        )
        print("FAIL — should have raised ValueError")
    except ValueError as e:
        print("Got expected ValueError:", e)
        # Should mention supported providers in the message
        assert "claude-code" in str(e) or "Supported" in str(e), \
            f"Error doesn't mention supported providers: {e}"
        print("PASS")

asyncio.run(test())
