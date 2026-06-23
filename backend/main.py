from pathlib import Path

import asyncio

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pyrefly_lsp import PyreflySession, prepare_client_message

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:4200",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# we will receive 3 things by the IDE : the text, the line number and the "columns" number to see where the cursor is
class CompletionRequest(BaseModel):
    code: str
    line: int
    character: int


@app.websocket("/lsp")
async def lsp_socket(ws: WebSocket):

    # Condition for allowing a extern connection, idk if it's important in order to connect to pyrefly (because we have already a middleware) but just in case
    origin = ws.headers.get("origin")

    allowed_origins = {
        "http://localhost:4200",
    }

    if origin not in allowed_origins:
        await ws.close(code=1008)  # Policy Violation
        return
    
    # we start the session for the pyrefly process in order to receive stdin from the front and then reply to complete the differents lsp features
    await ws.accept()
    session = PyreflySession(cmd=["pyrefly", "lsp"], cwd=str(Path(__file__).parent))
    await session.start()


    # run infinitely, receive message and send the respons to the lsp server
    async def browser_to_pyrefly():
        while True:
            message = await ws.receive_text()
            await session.send_lsp_message(prepare_client_message(message, str(Path(__file__).parent)))

    # same but the opposite 
    
    async def pyrefly_to_browser():
        while True:
            await ws.send_text(await session.recv_lsp_message())

    try:
        # start the 2 tasks in the same time
        await asyncio.gather(browser_to_pyrefly(), pyrefly_to_browser())
    except WebSocketDisconnect:
        pass
    finally:
        await session.stop()
