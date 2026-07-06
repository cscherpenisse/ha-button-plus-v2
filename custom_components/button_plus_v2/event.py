from homeassistant.components import mqtt


async def async_setup_entry(hass, entry):
    """Create event forwarding for automations."""

    device_id = entry.data["device_id"]
    base = f"buttonplus/{device_id}"

    async def forward(msg):
        topic = msg.topic
        payload = msg.payload

        if "pushbutton" in topic:
            event_type = "buttonplus_event"

            hass.bus.async_fire(
                event_type,
                {
                    "topic": topic,
                    "payload": payload,
                },
            )

    await mqtt.async_subscribe(hass, f"{base}/button/+/pushbutton", forward)

    return True
