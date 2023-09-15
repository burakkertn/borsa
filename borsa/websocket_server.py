import asyncio
import websockets

async def main(websocket, path):
    while True:
        message = await websocket.recv()
        print(f"Alınan veri: {message}")

        response = f"Yanıt: {message}"
        await websocket.send(response)

start_server = websockets.serve(main, "localhost", 5000)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
