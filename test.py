from starlette.applications import Starlette
from starlette.websockets import WebSocket
from starlette.endpoints import WebSocketEndpoint
from starlette.responses import JSONResponse

app = Starlette()


@app.route("/test", methods=["GET"])
def test(request):
    print(request)
    return JSONResponse({'test': 'test'})


class App:
    def __init__(self, scope):
        assert scope['type'] == 'websocket'
        self.scope = scope

    async def __call__(self, receive, send):
        websocket = WebSocket(self.scope, receive=receive, send=send)
        await websocket.accept()
        await websocket.send_text('Test!')
        await websocket.close()


sessions = {}

from random import randint

@app.websocket_route('/test')
class Broadcast(WebSocketEndpoint):
    session_name = ''

    async def on_connect(self, websocket: WebSocket):
        app = self.scope.get('app', None)
        # self.channel_name = self.get_params(websocket).get('username', 'default_name')
        # self.channel_name = 'test'
        self.channel_name = randint(0, 1e3)
        # self.sessions = app.sessions
        await websocket.accept()
        await self.broadcast_message('User {} is connected'.format(self.channel_name))
        sessions[self.channel_name] = websocket

    async def on_disconnect(self, websocket: WebSocket, close_code: int):
        sessions.pop(self.channel_name, None)
        await self.broadcast_message('User {} is disconnected'.format(self.channel_name))

    async def broadcast_message(self, msg):
        for k in sessions:
            print('session', k)
            ws = sessions[k]
            await ws.send_text(f"message text was: {msg}")

    async def on_receive(self, ws, data):
        print(data)
        await self.broadcast_message(data)
