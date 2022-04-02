"""
sensor data update coordinator
"""
import logging

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
    UpdateFailed,
)

from .const import (
    DOMAIN,
    REFRESH_INTERVAL,
)
from .api import OCTuneApiClient

_LOGGER = logging.getLogger(__name__)


class SensorDataUpdateCoordinator(DataUpdateCoordinator):
    """Manages fetching Status Data from octune api"""

    def __init__(self, hass: HomeAssistant, client: OCTuneApiClient, host: str, port: int, auth: str, minername: str):
        """Initialize"""
        self.name = f"{DOMAIN}_{host}_sensor_coordinator"
        self._client = client
        self.host = host
        self.port = port
        self.auth = auth
        self.minername = minername

        super().__init__(
            hass, _LOGGER, name=self.name, update_interval=REFRESH_INTERVAL
        )

    async def _async_update_data(self):
        """Update sensors"""
        try:
            _LOGGER.debug('raise update')
            return await self._client.get_devices()
        except Exception as exc:
            raise UpdateFailed from exc
