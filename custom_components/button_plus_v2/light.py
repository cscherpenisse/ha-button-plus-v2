from __future__ import annotations

from homeassistant.components.light import LightEntity
from homeassistant.config_entries import ConfigEntry

from .const import DOMAIN


async def async_setup_entry(hass, entry, async_add_entities):
    """Set up LED entities."""

    coordinator = hass.data[DOMAIN][entry.entry_id]["coordinator"]
    device_id = entry.data["device_id"]

    lights = [
        ButtonPlusLED(coordinator, device_id, "8-1"),
    ]

    async_add_entities(lights)


class ButtonPlusLED(LightEntity):
    """Button+ LED."""

    def __init__(self, coordinator, device_id: str, button_id: str) -> None:
        self.coordinator = coordinator
        self.device_id = device_id
        self.button_id = button_id

        self._attr_name = f"Button+ LED {button_id}"
        self._attr_unique_id = f"{device_id}_led_{button_id}"

    @property
    def is_on(self):
        topic = f"buttonplus/{self.device_id}/button/{self.button_id}/led/front/on/state"
        return self.coordinator.data.get(topic)

    async def async_turn_on(self, **kwargs):
        topic = f"buttonplus/{self.device_id}/button/{self.button_id}/led/front/on/set"
        await self.coordinator.mqtt.publish(topic, True)

    async def async_turn_off(self, **kwargs):
        topic = f"buttonplus/{self.device_id}/button/{self.button_id}/led/front/on/set"
        await self.coordinator.mqtt.publish(topic, False)
