from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

class ButtonPlusCoordinator(DataUpdateCoordinator):

    def __init__(self, hass, mqtt):
        super().__init__(hass, logger=None, name="buttonplus")
        self.mqtt = mqtt
        self.data = {}

    async def async_setup(self):
        self.mqtt.connect()

    def handle_message(self, topic, payload):
        self.data[topic] = payload
        self.async_set_updated_data(self.data)
