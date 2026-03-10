import asyncio
from dotenv import load_dotenv
from agentfield import Agent
from agentfield.types import HarnessConfig

load_dotenv()

async def test():
    agent = Agent(
        node_id="test-override",
        harness_config=HarnessConfig(provider="codex"),
        auto_register=False,
    )
    result = await agent.harness(
        "What is 3 + 3? Reply with only the number.",
        provider="claude-code",   # override the provider for this single call
    )
    
    print("HarnessResult:",result)
    print("is_error:", result.is_error)
    print("text:", result.text)
    assert not result.is_error

    print("PASS")

asyncio.run(test())
