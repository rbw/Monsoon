# -*- coding: utf-8 -*-

from aioli.service import BaseService
from ._livestatus import Livestatus
from aioli.exceptions import NoMatchFound, AioliException


class MonsoonService(BaseService):
    livestatus = Livestatus()

    async def on_ready(self):
        await self.livestatus.init(self.loop, address=("192.168.122.240", 6557))

    async def get_host(self, host_name):
        response = await self.livestatus.send(f"GET hosts\nFilter: display_name = {host_name}\n")
        if len(response) == 0:
            raise NoMatchFound()
        elif len(response) > 1:
            self.log.error(f"Got multiple results for host: {host_name}")
            raise AioliException()

        return response[0]

    async def get_hosts(self):
        return await self.livestatus.send("GET hosts")

    async def get_services(self):
        return await self.livestatus.send("GET services")

