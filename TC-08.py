'''
Verify that the agent can edit a file to change the return value of a function to use an f-string. 
The agent should be able to read the existing content of the file, identify the function definition, 
and modify it accordingly. After the edit, the test will check if the file content has been updated to include an f-string in the return statement.
'''

import asyncio, os
from agentfield import Agent
from agentfield.types import HarnessConfig

async def test():
    cwd = "/home/sridharvetrivel/test/harness-test"
    agent = Agent(
        node_id="test-file-edit",
        harness_config=HarnessConfig(provider="claude-code"),
        auto_register=False,
    )
    result = await agent.harness(
        "In greet.py, change the return value to use an f-string: f'Hello, {name}!'",
        cwd=cwd,
    )
    assert not result.is_error, result.error_message
    content = open(os.path.join(cwd, "greet.py")).read()
    assert "f'" in content or 'f"' in content, f"f-string not found: {content}"
    print("PASS — file content:", content)

asyncio.run(test())
