import asyncio, os, json
from pydantic import BaseModel
from agentfield.harness._runner import HarnessRunner
from agentfield.harness._schema import get_output_path

class Strict(BaseModel):
    value: int

async def test():
    cwd = "/home/sridharvetrivel/harness-test"
    # Pre-write a corrupt output file — wrong type for `value`
    output_path = get_output_path(cwd)
    with open(output_path, "w") as f:
        json.dump({"value": "not-an-int"}, f)

    runner = HarnessRunner()

    # Patch the provider so it does nothing (file is already there, corrupt)
    from agentfield.harness.providers._base import HarnessProvider
    from agentfield.harness._result import RawResult, Metrics

    class NoOpProvider(HarnessProvider):
        async def execute(self, prompt, options):
            # Return success but don't touch the file
            return RawResult(result="done", is_error=False, metrics=Metrics(num_turns=1))

    original_build = runner._build_provider
    runner._build_provider = lambda name, opts: NoOpProvider()

    result = await runner.run(
        "irrelevant",
        provider="claude-code",
        schema=Strict,
        cwd=cwd,
        schema_max_retries=0,
    )

    runner._build_provider = original_build  # restore

    print("is_error:", result.is_error)
    print("failure_type:", result.failure_type)
    print("error_message:", result.error_message)
    assert result.is_error
    print("PASS — schema retry disabled, error returned immediately")

asyncio.run(test())
