import pytest

import pypixiv as _pypixiv


@pytest.mark.asyncio
async def test_context_manager() -> None:
    async with _pypixiv.Client():
        pass
    return None
