# -*- coding: utf-8 -*-

from aioli.utils.http import jsonify
from aioli.controller import BaseController, route, input_load
from .service import MonsoonService
from .schema import HostPath


class Controller(BaseController):
    def __init__(self):
        self.service = MonsoonService()

    @route('/hosts', 'GET')
    async def hosts_get(self, _):
        return jsonify(await self.service.get_hosts())

    @route('/hosts/{host_name}', 'GET')
    @input_load(path=HostPath)
    async def host_get(self, host_name):
        return jsonify(await self.service.get_host(host_name))

    @route('/services', 'GET')
    async def services_get(self, _):
        return jsonify(await self.service.get_services())
