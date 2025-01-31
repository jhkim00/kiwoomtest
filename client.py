import asyncio
import websockets
import socketio

sio = socketio.AsyncClient()

@sio.on("message")
async def on_message(data):
    print("Received from server:", data)

async def main():
    await sio.connect("http://localhost:5000")
    print("Connected:", sio.sid)

    await sio.emit("message", "Hello Server!")
    await sio.emit("login")
    await sio.wait()

    await sio.disconnect()
    print("Disconnected:")

asyncio.run(main())