"""Config flow for Button+ V2."""

from __future__ import annotations

import logging

import aiohttp
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_HOST

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


class ButtonPlusV2ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Button+ V2."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""

        errors = {}

        if user_input is not None:
            host = user_input[CONF_HOST]

            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(
                        f"http://{host}/config",
                        timeout=aiohttp.ClientTimeout(total=10),
                    ) as response:

                        if response.status != 200:
                            errors["base"] = "cannot_connect"

                        else:
                            data = await response.json()

                            device_id = data["info"]["deviceid"] if "deviceid" in data["info"] else data["info"]["id"]

                            await self.async_set_unique_id(device_id)
                            self._abort_if_unique_id_configured()

                            return self.async_create_entry(
                                title=data["core"]["location"],
                                data={
                                    "host": host,
                                    "device_id": device_id,
                                },
                            )

            except Exception as err:
                _LOGGER.exception(err)
                errors["base"] = "cannot_connect"

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_HOST): str,
                }
            ),
            errors=errors,
        )
