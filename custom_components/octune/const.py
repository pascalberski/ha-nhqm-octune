"""
Constants for nhqm-octune
"""

from datetime import timedelta


NAME = "NiceHash QuickMiner OCTune"
DOMAIN = "octune"
DOMAIN_DATA = f"{DOMAIN}_data"
VERSION = "0.0.3"
DEFAULT_NAME = "octune"

ISSUE_URL = "https://github.com/pascalberski/ha-nhqm-octune/issues"

# Icons
ICON_HASHRATE = "mdi:speedometer"

# Platforms
SENSOR = "sensor"
PLATFORMS = [SENSOR]

# Configuration and options
CONF_MINERS = "miners"
CONF_HOST = "host"
CONF_PORT = "port"
CONF_AUTH = "auth"
CONF_NAME = "name"

REFRESH_INTERVAL = timedelta(seconds=10)

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
