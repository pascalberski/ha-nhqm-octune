"""
Sensors
"""
import logging
from time import sleep
from unittest import result

from homeassistant.helpers.entity import Entity

from custom_components.octune.api import OCTuneApiClient

from .const import (
    ATTRIBUTION,
    ICON_FAN,
    ICON_HASHRATE,
    ICON_OVERHEATING,
    ICON_POWER,
    ICON_TEMP,
    ICON_TEMP_HOTSPOT,
    ICON_TEMP_VRAM,
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
                if device.get("uuid") == self.device.get("uuid"):
                    #_LOGGER.debug("device: %s", device)
                    return device
        except Exception as exc:
            _LOGGER.error("Unable to get api data\n%s", exc)
            return None

    def log_updates(self, value):
        """ Log new values """
        _LOGGER.debug("%s (%s, %s, %s): %s", str(type(self)), self.minername, self.device.get("uuid"), self.device.get("name"), value)

    def _get_default_attributes(self, device_type):
        results = {
            "attribution": ATTRIBUTION,
        }

        if device_type == "GPU" or device_type == "RIG":
            results["rig"] = self.minername
            results["host"] = self.host
        if device_type == "GPU":
            results["uuid"] = self.device.get("uuid")

        return results


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
        self._state = float(self._get_data().get("gpu_temp"))
        self.log_updates(self._state)
        return self._state

    @property
    def unit_of_measurement(self):
        """Sensor unit of measurement"""
        return "°C"

    @property
    def icon(self):
        """Sensor icon"""
        return ICON_TEMP

    @property
    def device_state_attributes(self):
        """Sensor device state attributes"""
        results = self._get_default_attributes("GPU")
        results["temperature"] = self._state
        return results


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
        self._state = float(self._get_data().get("__vram_temp"))
        self.log_updates(self._state)
        return self._state

    @property
    def unit_of_measurement(self):
        """Sensor unit of measurement"""
        return "°C"

    @property
    def icon(self):
        """Sensor icon"""
        return ICON_TEMP_VRAM

    @property
    def device_state_attributes(self):
        """Sensor device state attributes"""
        results = self._get_default_attributes("GPU")
        results["vram temperature"] = self._state
        return results


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
        self._state = float(self._get_data().get("__hotspot_temp"))
        self.log_updates(self._state)
        return self._state

    @property
    def unit_of_measurement(self):
        """Sensor unit of measurement"""
        return "°C"

    @property
    def icon(self):
        """Sensor icon"""
        return ICON_TEMP_HOTSPOT

    @property
    def device_state_attributes(self):
        """Sensor device state attributes"""
        results = self._get_default_attributes("GPU")
        results["hotspot temperature"] = self._state
        return results


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
        self._state = 0
        try:
            self._state = round(float(self._get_data().get("algorithms")[0].get("speed"))/1000000, 2)
        except TypeError:
            _LOGGER.debug("device not mining")
        self.log_updates(self._state)
        return self._state

    @property
    def unit_of_measurement(self):
        """Sensor unit of measurement"""
        return "MH/s"

    @property
    def icon(self):
        """Sensor icon"""
        return ICON_HASHRATE

    @property
    def device_state_attributes(self):
        """Sensor device state attributes"""
        results = None
        if (self.device is None):
            results = self._get_default_attributes("RIG")
        else:
            results = self._get_default_attributes("GPU")
        results["hashrate"] = self._state
        return results

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
        self._state = float(self._get_data().get("fans")[self.fanid].get("current_rpm"))
        self.log_updates(self._state)
        return self._state

    @property
    def unit_of_measurement(self):
        """Sensor unit of measurement"""
        return "RPM"

    @property
    def icon(self):
        """Sensor icon"""
        return ICON_FAN

    @property
    def device_state_attributes(self):
        """Sensor device state attributes"""
        results = self._get_default_attributes("GPU")
        results["rpm"] = self._state
        return results

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
        self._state = float(self._get_data().get("fans")[self.fanid].get("current_level"))
        self.log_updates(self._state)
        return self._state

    @property
    def unit_of_measurement(self):
        """Sensor unit of measurement"""
        return "%"

    @property
    def icon(self):
        """Sensor icon"""
        return ICON_FAN

    @property
    def device_state_attributes(self):
        """Sensor device state attributes"""
        results = self._get_default_attributes("GPU")
        results["speed"] = self._state
        return results

class PowerSensor(Sensor):
    """
    displays power usage in watt
    """

    @property
    def name(self):
        """Sensor name"""
        device_name = self.device.get("name")
        return f"{self.minername} {device_name} Power"

    @property
    def unique_id(self):
        """Unique entity id"""
        device_uuid = self.device.get("uuid")
        return f"octune:{device_uuid}:power"

    @property
    def state(self):
        """Sensor state"""
        self._state = float(self._get_data().get("gpu_power_usage"))
        self.log_updates(self._state)
        return self._state

    @property
    def unit_of_measurement(self):
        """Sensor unit of measurement"""
        return "W"

    @property
    def icon(self):
        """Sensor icon"""
        return ICON_POWER

    @property
    def device_state_attributes(self):
        """Sensor device state attributes"""
        results = self._get_default_attributes("GPU")
        results["power"] = self._state
        return results

class OverheatingSensor(Sensor):
    """
    displays if a gpu overheats
    """

    @property
    def name(self):
        """Sensor name"""
        device_name = self.device.get("name")
        return f"{self.minername} {device_name} Overheating"

    @property
    def unique_id(self):
        """Unique entity id"""
        device_uuid = self.device.get("uuid")
        return f"octune:{device_uuid}:overheating"

    @property
    def state(self):
        """Sensor state"""
        self._state = bool(self._get_data().get("too_hot"))
        self.log_updates(self._state)
        return self._state

    @property
    def unit_of_measurement(self):
        """Sensor unit of measurement"""
        return None

    @property
    def icon(self):
        """Sensor icon"""
        return ICON_OVERHEATING

    @property
    def device_state_attributes(self):
        """Sensor device state attributes"""
        results = self._get_default_attributes("GPU")
        results["overheating"] = self._state
        return results
