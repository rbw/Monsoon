# -*- coding: utf-8 -*-

from aioli import Package
from .controller import HttpController, HostSocketController, HostsSocketController
from .service import MonsoonService

__version__ = '0.1.0'

export = Package(
    name='monsoon',
    description='High performance WebSocket and HTTP API layer on top of Livestatus',
    controllers=[HttpController, HostSocketController, HostsSocketController],
    services=[MonsoonService],
    models=[]
)
