# -*- coding: utf-8 -*-

import math

import ujson

from aioli.package.service import BaseService
from aioli_livestatus.service import LivestatusService
from aioli_redis.service import RedisService

DEFAULT_HOSTS_FIELDS = [
    'name', 'acknowledged', 'num_services', 'num_services_ok',
    'num_services_warn', 'num_services_pending', 'num_services_unknown',
    'num_services_crit'
]


class MonsoonService(BaseService):
    livestatus_svc = LivestatusService()
    redis_svc = RedisService()
    redis_conn = None

    async def on_ready(self):
        await self.livestatus_svc.init("127.0.0.1", 6557)

    async def relay_livestatus(self, channel_name, *args, **kwargs):
        connection = await self.redis_svc.get_connection()

        method = self.get_many if kwargs.pop('many', True) else self.get_one
        data = ujson.dumps(await method(channel_name, *args, **kwargs))

        await connection.publish(channel_name, data)

        connection.close()

        return {"result": f"Publish successful. Channel: {channel_name}, Size: {len(data) / 1000}kB"}

    async def get_host(self, name, **kwargs):
        query = f'name = {name}'
        return await self.get_one('hosts', query, **kwargs)

    async def get_hosts(self, **kwargs):
        return await self.get_many('hosts', fields=kwargs.pop('fields', DEFAULT_HOSTS_FIELDS), **kwargs)

    async def get_one(self, table, query, **kwargs):
        return await self.livestatus_svc.get_one(table, query_filter=query, **kwargs)

    async def get_many(self, table, **kwargs):
        return await self.livestatus_svc.get_many(table, **kwargs)

    async def get_services(self):
        return await self.livestatus_svc.send("GET services")

