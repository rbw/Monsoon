# -*- coding: utf-8 -*-

from aioli.schema import fields, Schema


class HostPath(Schema):
    host_name = fields.String()
