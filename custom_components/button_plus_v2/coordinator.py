from __future__ import annotations

from homeassistant.helpers.update_coordinator import DataUpdateCoordinator


class ButtonPlusCoordinator(DataUpdateCoordinator):
    """Stores MQTT state."""

    def __init__(self, hass, mqtt_client):
        super().__init__(
            hass,
            logger=None,
            name="button_plus_v2",
        )

        self.hass = hass
        self.mqtt = mqtt_client
        self.data = {}

    async def async_setup(self) -> None:
        """Start MQTT and bind callback."""

        self.mqtt.add_callback(self.handle_message)

    def handle_message(self, topic: str, payload):
        """Receive MQTT updates."""

        self.data[topic] = payload

        # trigger HA update loop
        self.async_set_updated_data(dict(self.data))
