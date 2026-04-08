import asyncio
from agentfield import Agent
from agentfield.types import HarnessConfig

DICT_SCHEMA = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "count": {"type": "integer"},
    },
    "required": ["name", "count"],
}

async def test():
    agent = Agent(
        node_id="test-dict-schema",
        harness_config=HarnessConfig(provider="claude-code"),
        auto_register=False,
    )
    result = await agent.harness(
        "Return name='widgets' and count=5.",
        schema=DICT_SCHEMA,
        cwd="/home/sridharvetrivel/harness-test",
    )
    assert not result.is_error, result.error_message
    # With dict schema, .parsed is the raw dict (no Pydantic model_validate)
    assert isinstance(result.parsed, dict), f"Expected dict, got {type(result.parsed)}"
    assert "name" in result.parsed
    assert "count" in result.parsed
    print("PASS — parsed:", result.parsed)

asyncio.run(test())
