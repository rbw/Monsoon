# -*- coding: utf-8 -*-

from aioli import Package
from .controller import Controller
from .service import MonsoonService

__version__ = '0.1.0'

export = Package(
    name='monsoon',
    description='High performance HTTP API layer on top of Livestatus',
    controller=Controller,
    services=[MonsoonService],
    models=[],
)
