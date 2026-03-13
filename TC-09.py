'''
Test that the agent can edit files in the current working directory and return a structured response.
This test creates a simple Python file, asks the agent to edit it by adding a docstring, and returns a structured response with the list of changed files and a description of the change.
'''


import asyncio, os
from pydantic import BaseModel
from typing import List
from agentfield import Agent
from agentfield.types import HarnessConfig

class EditResult(BaseModel):
    files_changed: List[str]
    description: str

async def test():
    cwd = "/home/sridharvetrivel/test/harness-test"
    with open(os.path.join(cwd, "calc.py"), "w") as f:
        f.write("def multiply(a, b):\n    return a * b\n")

    agent = Agent(
        node_id="test-edit-schema",
        harness_config=HarnessConfig(provider="claude-code"),
        auto_register=False,
    )
    result = await agent.harness(
        "Add a docstring to the multiply function in calc.py. "
        "Return the list of files you changed and a brief description.",
        schema=EditResult,
        cwd=cwd,
    )
    assert not result.is_error, result.error_message
    assert isinstance(result.parsed, EditResult)
    assert len(result.parsed.files_changed) > 0
    content = open(os.path.join(cwd, "calc.py")).read()
    assert '"""' in content or "'''" in content
    print("PASS — changed:", result.parsed.files_changed)
    print("PASS — description:", result.parsed.description)

asyncio.run(test())
