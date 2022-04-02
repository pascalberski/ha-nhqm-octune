"""
OCTune API interface
"""
import logging
import httpx

_LOGGER = logging.getLogger(__name__)

class OCTuneApiClient:
    """ OCTune api interface """
    def __init__(self, host, port, auth):
        self.host = host
        self.port = port
        self.auth = auth

    async def get_devices(self):
        """ return the combinded json array """
        devices = await self.get_devices_json()
        workers = await self.get_workers_json()

        i = 0
        for device in devices:
            for worker in workers:
                if (worker.get("device_uuid") == device.get("uuid")):
                    devices[i]["algorithms"] = worker.get("algorithms")
                    workers.remove(worker)
            i += 1

        return devices

    async def get_device_by_id(self, id):
        """ return a device by id or uuid """
        device = (await self.request("GET", "/api?command={\"id\":1,\"method\":\"device.get\",\"params\":[\"" + id + "\"]}")).get("device")
        workers = await self.get_workers_json()

        for worker in workers:
            if (worker.get("device_uuid") == device.get("uuid")):
                device["algorithms"] = worker.get("algorithms")

        return device

    async def get_devices_json(self):
        """ get devices json array """
        return (await self.request("GET", "/devices_cuda")).get("devices")

    async def get_workers_json(self):
        """ get workers json array """
        return (await self.request("GET", "/workers")).get("workers")

    async def request(self, method, path):
        """ Request Helper """
        async with httpx.AsyncClient() as client:
            try:
                url = "http://" + self.host + ":" + str(self.port) + path
                _LOGGER.debug("http " + method + " request: " + url)

                response = None
                if (method == "GET"):
                    response = await client.get(url)

                if response.status_code == 200:
                    return response.json()
                else:
                    raise Exception("error while communication with api")
            except Exception as exc:
                _LOGGER.error(str(type(exc)))
