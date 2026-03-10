'''

'''

import asyncio
from pydantic import BaseModel
from agentfield import Agent
from agentfield.types import HarnessConfig

class Greeting(BaseModel):
    message: str
    lucky_number: int

async def test():
    agent = Agent(
        node_id="test-schema",
        auto_register=False,
    )
    result = await agent.harness(
        "Return message='Hello world' and lucky_number=7.",
        schema=Greeting,
        provider="claude-code",   # explicitly specify provider here since it's not set in the Agent's harness_config
        permission_mode="auto",   # allow the sub-agent to write the output file without prompting
    )
    print("HarnessResult:",result)
    print(type(result.parsed))          # <class '__main__.Greeting'>
    print(result.parsed.message)        # Hello world
    print(result.parsed.lucky_number)   # 7
    print(result.parsed.lucky_number + 1)  # 8  ← you can do math on it, proving it's an int
    print(result.parsed.model_dump())   # {'message': 'Hello world', 'lucky_number': 7}  ← actual dict
    print(result.parsed.model_dump_json())  # {"message":"Hello world","lucky_number":7}  ← actual JSON string

    assert not result.is_error
    assert isinstance(result.parsed, Greeting)
    print("PASS")

asyncio.run(test())

