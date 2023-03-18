import asyncio
import websockets

async def hello():
    uri = "ws://localhost:6666"

    async with websockets.connect(uri) as websocket:
        while True:
            print(await websocket.recv())

asyncio.run(hello())