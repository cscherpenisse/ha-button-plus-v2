from homeassistant.components.light import LightEntity

class ButtonPlusLight(LightEntity):

    def __init__(self, coordinator, device_id, button_id):
        self.coordinator = coordinator
        self.device_id = device_id
        self.button_id = button_id

        self._attr_name = f"Button+ LED {button_id}"
        self._attr_unique_id = f"{device_id}_led_{button_id}"

    @property
    def is_on(self):
        topic = f"buttonplus/{self.device_id}/button/{self.button_id}/led/front/on/state"
        return self.coordinator.data.get(topic)

    async def async_turn_on(self):
        topic = f"buttonplus/{self.device_id}/button/{self.button_id}/led/front/on/set"
        self.coordinator.mqtt.publish(topic, True)

    async def async_turn_off(self):
        topic = f"buttonplus/{self.device_id}/button/{self.button_id}/led/front/on/set"
        self.coordinator.mqtt.publish(topic, False)
