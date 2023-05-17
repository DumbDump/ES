import asyncio
import websockets

async def ph(websocket, path):
    while True:
        need_update = await websocket.recv()
        print('socket executed')
        await websocket.send(need_update)


start_server = websockets.serve(ph, '0.0.0.0', 5678)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()