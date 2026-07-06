from __future__ import annotations

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import DOMAIN
from .mqtt import ButtonPlusMQTT
from .coordinator import ButtonPlusCoordinator

_LOGGER = logging.getLogger(__name__)

PLATFORMS = ["sensor", "button", "light"]


async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    """Set up via YAML (unused)."""
    hass.data.setdefault(DOMAIN, {})
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Button+ V2."""

    hass.data.setdefault(DOMAIN, {})

    device_id = entry.data["device_id"]
    host = entry.data["host"]

    # MQTT client
    mqtt_client = ButtonPlusMQTT(hass, device_id)

    # Coordinator
    coordinator = ButtonPlusCoordinator(hass, mqtt_client)

    # BELANGRIJK: start MQTT + callbacks
    await coordinator.async_setup()

    # optioneel: start connect (niet blocking)
    await mqtt_client.async_setup()

    hass.data[DOMAIN][entry.entry_id] = {
        "host": host,
        "device_id": device_id,
        "mqtt": mqtt_client,
        "coordinator": coordinator,
    }

    # platforms laden
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    _LOGGER.info("Button+ V2 loaded for device %s", device_id)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload integration."""

    unload_ok = await hass.config_entries.async_unload_platforms(
        entry,
        PLATFORMS,
    )

    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id, None)

    return unload_ok
