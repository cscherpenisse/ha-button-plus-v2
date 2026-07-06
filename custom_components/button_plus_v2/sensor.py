from homeassistant.components.sensor import SensorEntity

class ButtonPlusSensor(SensorEntity):

    def __init__(self, coordinator, device_id, sensor_id):
        self.coordinator = coordinator
        self.device_id = device_id
        self.sensor_id = sensor_id
        self._attr_name = f"Button+ {sensor_id}"
        self._attr_unique_id = f"{device_id}_{sensor_id}"

    @property
    def state(self):
        topic = f"buttonplus/{self.device_id}/sensor/{self.sensor_id}"
        return self.coordinator.data.get(topic)
