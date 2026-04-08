import asyncio
from agentfield.harness._runner import HarnessRunner
from agentfield.harness._result import FailureType

async def test():
    runner = HarnessRunner()
    result = await runner.run(
        "Do something.",
        provider="codex",
        codex_bin="/nonexistent/path/to/codex",  # bad binary
        cwd="/tmp/harness-test",
        max_retries=0,
    )
    print("is_error:", result.is_error)
    print("failure_type:", result.failure_type)
    print("error_message:", result.error_message)
    assert result.is_error
    assert result.failure_type == FailureType.CRASH
    assert result.parsed is None
    print("PASS")

asyncio.run(test())
