'''Cleanup Test
Verify the harness cleans up temporary files after execution.
This test runs a harness with a schema and checks that the .agentfield_output.json file is removed after execution.
'''


import asyncio, os
from pydantic import BaseModel
from agentfield import Agent
from agentfield.types import HarnessConfig

class Simple(BaseModel):
    value: str

async def test():
    cwd = "/home/sridharvetrivel/harness-test"
    agent = Agent(
        node_id="test-cleanup",
        harness_config=HarnessConfig(provider="claude-code"),
        auto_register=False,
    )
    await agent.harness(
        "Return value='done'.",
        schema=Simple,
        cwd=cwd,
    )
    output_file = os.path.join(cwd, ".agentfield_output.json")
    assert not os.path.exists(output_file), f"Output file not cleaned up: {output_file}"
    print("Output file cleaned up successfully.")
    print("PASS")

asyncio.run(test())
