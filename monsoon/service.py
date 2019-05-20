# -*- coding: utf-8 -*-

import math

import ujson

from aioli.package.service import BaseService
from aioli_livestatus.service import LivestatusService
from aioli_redis.service import RedisService

DEFAULT_HOSTS_FIELDS = [
    "name", "alias", "address", "groups", "acknowledged", "last_check",
    "num_services", "num_services_ok", "num_services_warn",
    "num_services_pending", "num_services_unknown", "num_services_crit"
]


class MonsoonService(BaseService):
    livestatus = LivestatusService()
    redis_svc = RedisService()
    redis_conn = None

    async def on_ready(self):
        await self.livestatus.init("192.168.122.240", 6557)

    async def relay_livestatus(self, table_name, key=None, **kwargs):
        connection = await self.redis_svc.get_connection()
        data = ujson.dumps(await self.get_hosts(**kwargs))
        await connection.publish(table_name, data)

        connection.close()

        return {"result": f"Publish successful. Channel: {table_name}, Size: {len(data) / 1000}kB"}

    async def get_host(self, name, **kwargs):
        query = f"name = {name}"
        return await self.livestatus.get_one("hosts", query_filter=query, **kwargs)

    async def get_host_services(self, host_name, **kwargs):
        query = f"host_name = {host_name}"
        return await self.livestatus.get_many("services", query_filter=query, **kwargs)

    async def get_hosts(self, **kwargs):
        return await self.livestatus.get_many("hosts", fields=kwargs.pop("fields", DEFAULT_HOSTS_FIELDS), **kwargs)

    async def get_services(self, **kwargs):
        return await self.livestatus.get_many("services", **kwargs)
