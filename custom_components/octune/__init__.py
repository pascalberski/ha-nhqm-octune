"""
Integrates for OCTune with Home Assistant

For more details about this integration, please refer to
https://github.com/pascalberski/ha-nhqm-octune
"""
import logging
import json
from homeassistant.core import Config, HomeAssistant
from homeassistant.helpers import discovery
from homeassistant.exceptions import PlatformNotReady

from .const import CONF_HOST, CONF_NAME, CONF_PORT, CONF_AUTH, CONF_MINERS

from .const import (
    DOMAIN,
    STARTUP_MESSAGE,
)
from .api import OCTuneApiClient
from .coordinators import (
    SensorDataUpdateCoordinator,
)

_LOGGER = logging.getLogger(__name__)


async def async_setup(hass: HomeAssistant, config: Config):
    """Set up this integration"""
    if hass.data.get(DOMAIN) is None:
        hass.data.setdefault(DOMAIN, {})
        _LOGGER.debug(STARTUP_MESSAGE)

    integration_config = config[DOMAIN]
    # Configuration
    #host = charger_config.get(CONF_HOST)

    miners = integration_config.get(CONF_MINERS)
    sensor_coordinators = []

    for miner in miners:
        host = miner.get(CONF_HOST)
        port = miner.get(CONF_PORT)
        auth = miner.get(CONF_AUTH)
        minername = miner.get(CONF_NAME)

        client = OCTuneApiClient(host, port, auth)

        _LOGGER.debug("initialising sensor coordinator %s - %s:%s - %s", minername, host, port, auth)
        sensor_coordinator = SensorDataUpdateCoordinator(hass, client, host, port, auth, minername)
        await sensor_coordinator.async_refresh()

        if not sensor_coordinator.last_update_success:
            _LOGGER.error("Unable to get data from miner")
            raise PlatformNotReady

        sensor_coordinators.append(sensor_coordinator)

    hass.data[DOMAIN]["sensor_coordinators"] = sensor_coordinators

    await discovery.async_load_platform(hass, "sensor", DOMAIN, {}, config)

    return True
