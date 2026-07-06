from __future__ import annotations

from homeassistant.components.button import ButtonEntity
from homeassistant.config_entries import ConfigEntry

from .const import DOMAIN


async def async_setup_entry(hass, entry, async_add_entities):
    """Set up button entities."""

    coordinator = hass.data[DOMAIN][entry.entry_id]["coordinator"]
    device_id = entry.data["device_id"]

    buttons = [
        ButtonPlusButton(coordinator, device_id, "8-1"),
    ]

    async_add_entities(buttons)


class ButtonPlusButton(ButtonEntity):
    """Button+ input."""

    def __init__(self, coordinator, device_id: str, button_id: str) -> None:
        self.coordinator = coordinator
        self.device_id = device_id
        self.button_id = button_id

        self._attr_name = f"Button+ {button_id}"
        self._attr_unique_id = f"{device_id}_{button_id}"

    async def async_press(self) -> None:
        """Simulate press (mainly for testing)."""
        return
