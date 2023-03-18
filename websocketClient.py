import asyncio
import websockets

async def hello():
    uri = "ws://localhost:6666"

    async with websockets.connect(uri) as websocket:
        while True:
            message = input("Enter message: ")
            await websocket.send(message)

            print(await websocket.recv())

asyncio.run(hello())