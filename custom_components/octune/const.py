"""
Constants for nhqm-octune
"""



NAME = "NiceHash QuickMiner OCTune"
DOMAIN = "octune"
DOMAIN_DATA = f"{DOMAIN}_data"
VERSION = "0.0.3"
DEFAULT_NAME = "octune"

ISSUE_URL = "https://github.com/pascalberski/ha-nhqm-octune/issues"

# Icons
ICON_HASHRATE = "mdi:speedometer"
ICON_FAN = "mdi:fan"
ICON_TEMP_HOTSPOT = "mdi:thermometer-high"
ICON_TEMP_VRAM = "mdi:thermometer-lines"
ICON_TEMP = "mdi:thermometer"

# Platforms
SENSOR = "sensor"
PLATFORMS = [SENSOR]

# Configuration and options
CONF_MINERS = "miners"
CONF_HOST = "host"
CONF_PORT = "port"
CONF_AUTH = "auth"
CONF_NAME = "name"

REFRESH_INTERVAL = "refreshinterval"

# Startup
STARTUP_MESSAGE = f"""
-------------------------------------------------------------------
{NAME} by Pascal Berski (@pascalberski)
Version: {VERSION}
This is a custom integration!
If you have any issues with this you need to open an issue here:
{ISSUE_URL}
-------------------------------------------------------------------
"""
