# -*- coding: utf-8 -*-

from aioli import Package
from .controller import HttpController, WebSocketController
from .service import MonsoonService

__version__ = '0.1.0'

export = Package(
    name='monsoon',
    description='High performance WebSocket and HTTP API layer on top of Livestatus',
    controllers=[HttpController, WebSocketController],
    services=[MonsoonService],
    models=[]
)
