from __future__ import annotations

import logging
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_HOST

from .api import ButtonPlusAPI
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


class ButtonPlusConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle config flow."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Initial step."""

        errors = {}

        if user_input is not None:
            host = user_input[CONF_HOST]

            try:
                api = ButtonPlusAPI(host)
                data = await api.get_config()

                device_id = data["info"]["id"]

                await self.async_set_unique_id(device_id)
                self._abort_if_unique_id_configured()

                return self.async_create_entry(
                    title=data.get("core", {}).get("location", device_id),
                    data={
                        "host": host,
                        "device_id": device_id,
                        "config": data,
                    },
                )

            except Exception as err:
                _LOGGER.exception("Failed to connect to Button+ V2: %s", err)
                errors["base"] = "cannot_connect"

        schema = vol.Schema(
            {
                vol.Required(CONF_HOST): str,
            }
        )

        return self.async_show_form(
            step_id="user",
            data_schema=schema,
            errors=errors,
        )
