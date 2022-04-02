# NiceHash QuickMiner OCTune Integration for Home Assistant

  

[![GitHub Release][releases-shield]][releases]
[![GitHub Activity][commits-shield]][commits]
[![License][license-shield]](LICENSE)
[![Project Maintenance][maintenance-shield]](https://github.com/pascalberski)
[![BuyMeCoffee][buymecoffeebadge]][buymecoffee]

  

  

**This component only works if the miner and Home Assistant are on the same network.**


This integration is a simple method to receive data from your GPUs in your mining rigs without using the NiceHash servers.
I'm using the Excavator api (https://github.com/nicehash/excavator/tree/master/api) to communicate with the miner.

## Features
- Support for multiple mining rigs
- Sensors for each GPU
	- Hashrate
	- GPU temperature
	- Hotspot temperature
	- VRAM temperature
	- Fan speed in percent
	- Fan speed in RPM
- Sensors for the mining rig
	- Hashrate (sum of all GPUs inside the rig)
- Global sensors
	- Hashrate (sum of all GPUs)

Request a new feature [here](https://github.com/pascalberski/ha-nhqm-octune/issues/new?assignees=&labels=enhancement&template=feature_request.md).


## Installation

### 1. Prepare OCTune
In order to be able to establish a connection between OCTune and Home Assistant, it must first be ensured that OCTune can be reached by other devices.

1. **Open your Nice Hash Quick Miner config file.**
   
   You can open the file via the Windows GUI as shown in the image below or directly via the file path: `C:\NiceHash\NiceHash QuickMiner\nhqm.conf`
	
	![openconfigfile][openconfigfileimg]
2. **Change OCTune API host**

	You have to find the parameter `watchDogAPIHost` and change it from `localhost` to `0.0.0.0`.
3. **Restart**

	Now you need to restart NH QuickMiner for the changes to take effect. *not just restart the Excavator*

### 2. Enable this Integration in HACS
1. Open the `HACS` page in your Home Assistant
2. Go to the `Integrations` tab
3. Click on the `3 points` in the top right corner and click on `Custom repositories`
4. In the Repository field, type `https://github.com/pascalberski/ha-nhqm-octune` and select `Integration` for Category. Click on `ADD`.
5. Now you can browse through the HACS integrations and can install this integration.

### 3. Configuration
1. Open your Home Assistant config file `configuration.yaml`.
2. Insert this example and modify it.
	```text
	octune:
	  refreshinterval: 60
	  miners:
	    - host: 192.168.178.10
	      port: 18000
	      name: Miner1
	      auth: 6A5FDC7B932864GHNK993EEF
	    - host: 192.168.178.11
	      port: 18000
	      name: Miner2
	      auth: 034C534SDG2F1D1477E50A01
	 ```
3. Restart Home Assistant and you are to go.
  
## ToDo
View my current [ToDos][todos]
 

## Report a bug or request a feature?
  

Please let me know in the [Issues tab][issues]

  

***

  


[buymecoffee]: https://www.buymeacoffee.com/pascalberski

[buymecoffeebadge]: https://img.shields.io/badge/buy%20me%20a%20coffee-donate-yellow.svg?style=for-the-badge

[commits-shield]: https://img.shields.io/github/commit-activity/y/pascalberski/ha-nhqm-octune.svg?style=for-the-badge

[commits]: https://github.com/pascalberski/ha-nhqm-octune/commits/master

[hacs]: https://github.com/custom-components/hacs

[hacsbadge]: https://img.shields.io/badge/HACS-Custom-orange.svg?style=for-the-badge

[discord]: https://discord.gg/Qa5fW2R

[discord-shield]: https://img.shields.io/discord/330944238910963714.svg?style=for-the-badge

[openconfigfileimg]: openconfigfile.PNG

[forum-shield]: https://img.shields.io/badge/community-forum-brightgreen.svg?style=for-the-badge

[forum]: https://community.home-assistant.io/

[license-shield]: https://img.shields.io/github/license/custom-components/blueprint.svg?style=for-the-badge

[maintenance-shield]: https://img.shields.io/badge/maintainer-%40pascalberski-blue.svg?style=for-the-badge

[releases-shield]: https://img.shields.io/github/v/release/pascalberski/ha-nhqm-octune.svg?style=for-the-badge

[releases]: https://github.com/pascalberski/ha-nhqm-octune/releases

[issues]: https://github.com/pascalberski/ha-nhqm-octune/issues

[todos]: https://github.com/pascalberski/ha-nhqm-octune/issues?q=is%3Aopen+is%3Aissue+label%3Atodo
