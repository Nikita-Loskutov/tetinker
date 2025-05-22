from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Разрешаем доступ с фронтенда (например, localhost:5173)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # в реальных проектах укажи конкретный адрес
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Храним список подключённых пользователей
connected_users = []

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    connected_users.append(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            for user in connected_users:
                await user.send_text(data)
    except WebSocketDisconnect:
        connected_users.remove(websocket)
