import asyncio
from pydantic import BaseModel
from agentfield import Agent
from agentfield.types import HarnessConfig

class FixResult(BaseModel):
    summary: str
    fixed: bool

async def test():
    import os
    cwd = "/home/sridharvetrivel/test/harness-test"
    with open(os.path.join(cwd, "square.py"), "w") as f:
        f.write("def square(x): return x * y\n")

    app = Agent(
        node_id="test-reasoner",
        harness_config=HarnessConfig(provider="claude-code"),
        auto_register=False,
    )

    @app.reasoner()
    async def fix_code(payload: dict) -> dict:
        result = await app.harness(
            f"Look at the file {payload['file']} and fix any errors in it. "
            f"Describe what the function does and whether you fixed anything.",
            schema=FixResult,
            cwd=cwd,
        )
        print("Reasoner result:", result)
        return result

    result = await fix_code({"file": "square.py"})
    print("result:", result)
    # print("summary:", result["parsed"]["summary"])
    # print("fixed:", result["parsed"]["fixed"])
    print("summary:", result.parsed.summary)
    print("fixed:", result.parsed.fixed)
    # assert result["is_error"] == False
    # assert result["parsed"]["fixed"] in (True, False)
    print("PASS")

asyncio.run(test())
