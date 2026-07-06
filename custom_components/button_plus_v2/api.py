from __future__ import annotations

import asyncio
import aiohttp


class ButtonPlusAPI:
    """Simple API wrapper for Button+ V2."""

    def __init__(self, host: str) -> None:
        self.host = host
        self.base_url = f"http://{host}"

    async def get_config(self) -> dict:
        """Fetch /config from device."""

        url = f"{self.base_url}/config"

        timeout = aiohttp.ClientTimeout(total=10)

        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.get(url) as resp:
                resp.raise_for_status()
                return await resp.json()
