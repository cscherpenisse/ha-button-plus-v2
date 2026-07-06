from __future__ import annotations

DOMAIN = "button_plus_v2"

MANUFACTURER = "Button+"

DEFAULT_PORT = 80

CONF_HOST = "host"

CONF_DEVICE_ID = "device_id"

CONF_NAME = "name"

BUTTON_TOPIC = "button"

DISPLAY_TOPIC = "displayitem"

LED_TOPIC = "led"

SENSOR_TOPIC = "sensor"

BRIGHTNESS_TOPIC = "brightness"

CONFIG_ENDPOINT = "/config"

PLATFORMS = (
    "sensor",
    "button",
    "light",
)
