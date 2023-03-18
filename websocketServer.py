import websockets
import asyncio

async def echo(websocket, path):
    print("echo!")
    async for message in websocket:
        await websocket.send(message)
        print("sent")

async def main():
    async with websockets.serve(echo, "localhost", 6666):
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())