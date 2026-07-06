async def async_setup_services(hass):

    async def set_display(call):
        device = call.data["device"]
        item = call.data["item"]
        value = call.data["value"]

        topic = f"buttonplus/{device}/displayitem/{item}/value/set"

        hass.data["buttonplus_mqtt"].publish(topic, value)

    hass.services.async_register(
        "button_plus_v2",
        "set_display",
        set_display
    )
