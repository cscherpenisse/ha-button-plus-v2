from __future__ import annotations

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from .const import DOMAIN


async def async_setup_entry(hass, entry, async_add_entities):
    """Set up sensors."""

    coordinator = hass.data[DOMAIN][entry.entry_id]["coordinator"]
    device_id = entry.data["device_id"]

    entities = [
        ButtonPlusSensor(coordinator, device_id, "sens1"),
        ButtonPlusSensor(coordinator, device_id, "sens2"),
    ]

    async_add_entities(entities)


class ButtonPlusSensor(SensorEntity):
    """Button+ sensor."""

    def __init__(self, coordinator, device_id: str, sensor_id: str) -> None:
        self.coordinator = coordinator
        self.device_id = device_id
        self.sensor_id = sensor_id

        self._attr_name = f"Button+ {sensor_id}"
        self._attr_unique_id = f"{device_id}_{sensor_id}"

    @property
    def state(self):
        topic = f"buttonplus/{self.device_id}/sensor/{self.sensor_id}"
        return self.coordinator.data.get(topic)
