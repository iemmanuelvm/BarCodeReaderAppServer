from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import asyncio

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

connected_clients = []

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    print("Client connected")
    connected_clients.append(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            print(f"Message received: {data}")
            for client in connected_clients:
                await client.send_text(data)
    except WebSocketDisconnect:
        print("Client disconnected")
        connected_clients.remove(websocket)
    except Exception as e:
        print(f"Connection error: {e}")
    finally:
        print("Cleaning up connection")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
