'''Error Handling Test
Verify that the harness raises an error when no provider is configured.
Calling .harness() with no provider (none in config, none per-call) must raise.
 '''



import asyncio
from agentfield import Agent

async def test():
    agent = Agent(node_id="test-no-provider", auto_register=False)
    try:
        await agent.harness("Do something.", cwd="/tmp/harness-test")
        print("FAIL — should have raised ValueError")
    except ValueError as e:
        print("Got expected ValueError:", e)
        print("PASS")

asyncio.run(test())
