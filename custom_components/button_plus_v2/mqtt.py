from __future__ import annotations

import json
import logging

from homeassistant.components import mqtt

_LOGGER = logging.getLogger(__name__)


class ButtonPlusMQTT:
    """MQTT wrapper."""

    def __init__(self, hass, device_id: str) -> None:
        self.hass = hass
        self.device_id = device_id
        self.base = f"buttonplus/{device_id}"
        self._callbacks = []

    async def async_setup(self) -> None:
        """Subscribe to MQTT topics."""

        topics = [
            f"{self.base}/sensor/#",
            f"{self.base}/button/+/pushbutton",
            f"{self.base}/displayitem/+/value/state",
            f"{self.base}/brightness/state",
            f"{self.base}/button/+/led/+/+/state",
        ]

        for topic in topics:
            await mqtt.async_subscribe(
                self.hass,
                topic,
                self._message_received,
            )

    def add_callback(self, cb) -> None:
        """Register callback."""
        self._callbacks.append(cb)

    async def _message_received(self, msg) -> None:
        """Handle incoming MQTT."""

        topic = msg.topic
        payload = msg.payload

        try:
            payload = json.loads(payload)
        except Exception:
            pass

        _LOGGER.debug("MQTT %s -> %s", topic, payload)

        for cb in self._callbacks:
            cb(topic, payload)

    async def publish(self, topic: str, payload) -> None:
        """Publish MQTT."""

        if isinstance(payload, (dict, list)):
            payload = json.dumps(payload)

        await mqtt.async_publish(self.hass, topic, payload)
