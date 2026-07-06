from homeassistant.components.button import ButtonEntity

class ButtonPlusButton(ButtonEntity):

    def __init__(self, coordinator, device_id, button_id):
        self.coordinator = coordinator
        self.device_id = device_id
        self.button_id = button_id

        self._attr_name = f"Button+ {button_id}"
        self._attr_unique_id = f"{device_id}_{button_id}"

    async def async_press(self):
        topic = f"buttonplus/{self.device_id}/button/{self.button_id}/pushbutton"
        self.coordinator.mqtt.publish(topic, {"event_type": "click"})
