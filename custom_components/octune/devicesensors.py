"""
Sensors
"""
import logging
from time import sleep

from homeassistant.helpers.entity import Entity

from custom_components.octune.api import OCTuneApiClient

from .const import (
    ICON_HASHRATE,
)

from .coordinators import SensorDataUpdateCoordinator

_LOGGER = logging.getLogger(__name__)


class Sensor(Entity):
    """
    Status Api Sensor
    """

    def __init__(self, coordinator: SensorDataUpdateCoordinator, device=None):
        """Initialize the sensor"""
        self.coordinator = coordinator
        self.host = coordinator.host
        self.port = coordinator.port
        self.auth = coordinator.auth
        self.minername = coordinator.minername
        self.device = device

    @property
    def name(self):
        """Device name"""
        return "Device"

    @property
    def should_poll(self):
        """No need to poll, Coordinator notifies entity of updates"""
        return False

    @property
    def available(self):
        """Whether sensor is available"""
        return self.coordinator.last_update_success

    @property
    def icon(self):
        """Sensor icon"""
        return ICON_HASHRATE

    @property
    def unit_of_measurement(self):
        """Sensor unit of measurement"""
        return None

    async def async_added_to_hass(self):
        """Connect to dispatcher listening for entity data notifications"""
        self.async_on_remove(
            self.coordinator.async_add_listener(self.async_write_ha_state)
        )

    async def async_update(self):
        """Update entity"""
        await self.coordinator.async_request_refresh()

    def _get_data(self):
        try:
            #_LOGGER.debug("coordinator.data: %s", self.coordinator.data)
            devices = self.coordinator.data

            for device in devices:
                #_LOGGER.debug("comapre %s == %s = %s", device.get("uuid"), self.device.get("uuid"), (device.get("uuid") == self.device.get("uuid")))
                if (device.get("uuid") == self.device.get("uuid")):
                    #_LOGGER.debug("device: %s", device)
                    return device
        except Exception as exc:
            _LOGGER.error("Unable to get api data\n%s", exc)
            return None
    
    def log_updates(self, value):
        """ Log new values """
        _LOGGER.debug("%s (%s, %s, %s): %s", str(type(self)), self.minername, self.device.get("uuid"), self.device.get("name"), value)


class TemperatureSensor(Sensor):
    """
    displays GPU temperature
    """

    @property
    def name(self):
        """Sensor name"""
        device_name = self.device.get("name")
        return f"{self.minername} {device_name} Temperature"

    @property
    def unique_id(self):
        """Unique entity id"""
        device_uuid = self.device.get("uuid")
        return f"octune:{device_uuid}:temperature"

    @property
    def state(self):
        """Sensor state"""
        #_LOGGER.debug("data type: %s", str(type(self._get_data())))
        value = float(self._get_data().get("gpu_temp"))
        self.log_updates(value)
        return value

    @property
    def unit_of_measurement(self):
        """Sensor unit of measurement"""
        return "°C"


class VramTemperatureSensor(Sensor):
    """
    displays GPU vram temperature
    """

    @property
    def name(self):
        """Sensor name"""
        device_name = self.device.get("name")
        return f"{self.minername} {device_name} VRAM Temperature"

    @property
    def unique_id(self):
        """Unique entity id"""
        device_uuid = self.device.get("uuid")
        return f"octune:{device_uuid}:vramtemperature"

    @property
    def state(self):
        """Sensor state"""
        value = float(self._get_data().get("__vram_temp"))
        self.log_updates(value)
        return value

    @property
    def unit_of_measurement(self):
        """Sensor unit of measurement"""
        return "°C"


class HotspotTemperatureSensor(Sensor):
    """
    displays GPU hotspot temperature
    """

    @property
    def name(self):
        """Sensor name"""
        device_name = self.device.get("name")
        return f"{self.minername} {device_name} Hotspot Temperature"

    @property
    def unique_id(self):
        """Unique entity id"""
        device_uuid = self.device.get("uuid")
        return f"octune:{device_uuid}:hotspottemperature"

    @property
    def state(self):
        """Sensor state"""
        value = float(self._get_data().get("__hotspot_temp"))
        self.log_updates(value)
        return value

    @property
    def unit_of_measurement(self):
        """Sensor unit of measurement"""
        return "°C"


class HashrateSensor(Sensor):
    """
    displays hashrate
    """

    @property
    def name(self):
        """Sensor name"""
        if (self.device is None):
            return f"{self.minername} Hashrate"
        device_name = self.device.get("name")
        return f"{self.minername} {device_name} Hashrate"

    @property
    def unique_id(self):
        """Unique entity id"""
        if (self.device is None):
            return f"octune:{self.minername}:hashrate"
        device_uuid = self.device.get("uuid")
        return f"octune:{device_uuid}:hashrate"

    @property
    def state(self):
        """Sensor state"""
        value = round(float(self._get_data().get("algorithms")[0].get("speed"))/1000000, 2)
        self.log_updates(value)
        return value

    @property
    def unit_of_measurement(self):
        """Sensor unit of measurement"""
        return "MH/s"

class FanRpmSensor(Sensor):
    """
    displays fan rpm
    """

    def __init__(self, coordinator: SensorDataUpdateCoordinator, fanid: int, device=None):
        super().__init__(coordinator, device)
        self.fanid = fanid

    @property
    def name(self):
        """Sensor name"""
        device_name = self.device.get("name")
        return f"{self.minername} {device_name} Fan {self.fanid} RPM"

    @property
    def unique_id(self):
        """Unique entity id"""
        device_uuid = self.device.get("uuid")
        return f"octune:{device_uuid}:fanrpm:{self.fanid}"

    @property
    def state(self):
        """Sensor state"""
        value = float(self._get_data().get("fans")[self.fanid].get("current_rpm"))
        self.log_updates(value)
        return value

    @property
    def unit_of_measurement(self):
        """Sensor unit of measurement"""
        return "RPM"

class FanSensor(Sensor):
    """
    displays fan speed in percent
    """

    def __init__(self, coordinator: SensorDataUpdateCoordinator, fanid: int, device=None):
        super().__init__(coordinator, device)
        self.fanid = fanid

    @property
    def name(self):
        """Sensor name"""
        device_name = self.device.get("name")
        return f"{self.minername} {device_name} Fan {self.fanid} Speed"

    @property
    def unique_id(self):
        """Unique entity id"""
        device_uuid = self.device.get("uuid")
        return f"octune:{device_uuid}:fanspeed:{self.fanid}"

    @property
    def state(self):
        """Sensor state"""
        value = float(self._get_data().get("fans")[self.fanid].get("current_level"))
        self.log_updates(value)
        return value

    @property
    def unit_of_measurement(self):
        """Sensor unit of measurement"""
        return "%"
