# -*- coding: utf-8 -*-

import ujson
import asyncio


class Livestatus:
    loop = None
    _host = None
    _port = None
    _socket_path = None

    async def init(self, loop, address=None, socket_path=None):
        assert not (address and socket_path)

        if address:
            self._host, self._port = address
        elif socket_path:
            self._socket_path = socket_path

        self.loop = loop

    async def _get_connection(self):
        if self._socket_path:
            return

        return await asyncio.open_connection(host=self._host, port=self._port, loop=self.loop)

    def _format_response(self, response):
        return [dict(zip(response[0], i)) for i in response[1:]]

    async def _write(self, writer, command):
        command = f"{command}\nOutputFormat: json\n"
        writer.write(command.encode('utf-8'))

        if writer.can_write_eof():
            writer.write_eof()

        await writer.drain()

    async def _read(self, reader):
        chunks = bytes()

        while True:
            chunk = await reader.read(4096)
            if not chunk:
                break

            chunks += chunk

        return chunks

    async def _handle_request(self, *args, **kwargs):
        # @TODO - implement connection re-use / queue ?
        # @TODO - implement error handling :: result['failed'], ['total_count']
        # @TODO - implement stream parser

        reader, writer = await self._get_connection()
        await self._write(writer, *args, **kwargs)
        response = await self._read(reader)
        writer.close()

        return ujson.loads(response)

    async def send(self, command):
        response = await self._handle_request(command)
        return self._format_response(response)
