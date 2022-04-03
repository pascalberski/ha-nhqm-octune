"""
Sensor platform for Charger
"""
import logging

from homeassistant.core import Config, HomeAssistant

from custom_components.octune.api import OCTuneApiClient

from .devicesensors import (
    FanRpmSensor,
    FanSensor,
    HashrateSensor,
    HotspotTemperatureSensor,
    OverheatingSensor,
    PowerSensor,
    TemperatureSensor,
    VramTemperatureSensor,
)

from .const import (
    DOMAIN,
)


_LOGGER = logging.getLogger(__name__)


async def async_setup_platform(
    hass: HomeAssistant, config: Config, async_add_entities, discovery_info=None
):
    """Setup charger sensor platform"""
    _LOGGER.debug("Creating new sensor components")

    data = hass.data[DOMAIN]
    # Configuration
    # host = data.get("host")
    # client = data.get("client")

    # charger sensors
    sensor_coordinators = data.get("sensor_coordinators")
    for sensor_coordinator in sensor_coordinators:
        sensors = await create_miner_sensors(sensor_coordinator)
        async_add_entities(sensors, True)


async def create_miner_sensors(coordinator):
    """ create sensor for a mining rig  """
    sensors = [
        #HashrateSensor(coordinator, coordinator.host, coordinator.port, coordinator.auth)
    ]

    _client = OCTuneApiClient(coordinator.host, coordinator.port, coordinator.auth)

    devices = (await _client.get_devices())
    for device in devices:
        sensors.extend(create_device_sensors(coordinator, device))

    return sensors

def create_device_sensors(coordinator, device):
    """ create sensor for a single GPU  """
    sensors = [
        #HashrateSensor(coordinator, coordinator.host, coordinator.port, coordinator.auth, device)
        TemperatureSensor(coordinator, device),
        VramTemperatureSensor(coordinator, device),
        HotspotTemperatureSensor(coordinator, device),
        HashrateSensor(coordinator, device),
        PowerSensor(coordinator, device),
        OverheatingSensor(coordinator, device)
    ]

    fans_len = len(device.get("fans"))
    for i in range(fans_len):
        sensors.append(FanRpmSensor(coordinator, i, device))
        sensors.append(FanSensor(coordinator, i, device))

    return sensors
