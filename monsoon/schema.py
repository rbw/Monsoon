# -*- coding: utf-8 -*-

from aioli.package.controller.schema import fields, Schema


class HostPath(Schema):
    host_name = fields.String()


class Alert(Schema):
    message = fields.String()
