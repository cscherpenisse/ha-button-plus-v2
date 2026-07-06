from __future__ import annotations

from homeassistant.helpers.update_coordinator import DataUpdateCoordinator


class ButtonPlusCoordinator(DataUpdateCoordinator):
    """Stores MQTT state centrally."""

    def __init__(self, hass, mqtt_client):
        super().__init__(
            hass,
            logger=None,
            name="button_plus_v2",
        )

        self.mqtt = mqtt_client
        self.data = {}

    async def async_setup(self):
        """Attach MQTT callback."""
        self.mqtt.add_callback(self.handle_message)
        await self.mqtt.async_setup()

    def handle_message(self, topic: str, payload):
        """Store latest state."""
        self.data[topic] = payload
        self.async_set_updated_data(self.data)
