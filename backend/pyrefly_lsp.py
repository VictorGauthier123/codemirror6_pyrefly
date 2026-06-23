# backend/pyrefly_lsp.py
import asyncio
import json
from pathlib import Path

class PyreflySession:
    # constructor with the commands and the path for the process (for instance "pyrefly lsp")
    def __init__(self, cmd: list[str], cwd: str):
        self.cmd = cmd
        self.cwd = cwd
        self.proc = None

    # allows to launch the pyrefly process
    async def start(self):
        self.proc = await asyncio.create_subprocess_exec(
            *self.cmd,
            cwd=self.cwd,
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
    # helper for send_lsp_message
    async def send_lsp(self, payload: dict):
        await self.send_lsp_message(json.dumps(payload))



    async def send_lsp_message(self, message: str):
        """ 
        Transforme le message en bytes pour stdin,créé un header pour le protocoloe LSP (ici len(body)), 
        envoie le message (drain à la place de write ca ca permet d'éviter de garder des messages en mémoire)
        """
        body = message.encode("utf-8")
        header = f"Content-Length: {len(body)}\r\n\r\n".encode("ascii")
        self.proc.stdin.write(header + body)
        await self.proc.stdin.drain()

    #same than before, helper for recv_lsp_message
    async def recv_lsp(self) -> dict:
        return json.loads(await self.recv_lsp_message())



    async def recv_lsp_message(self) -> str:
        """
        Processus inverse de send_lsp_message 
        """
        headers = b""
        while b"\r\n\r\n" not in headers:
            headers += await self.proc.stdout.read(1)

        header_text = headers.decode("ascii")
        content_length = 0
        for line in header_text.split("\r\n"):
            if line.lower().startswith("content-length:"):
                content_length = int(line.split(":", 1)[1].strip())

        body = await self.proc.stdout.readexactly(content_length)
        return body.decode("utf-8")

    async def stop(self):
        if self.proc and self.proc.returncode is None:
            self.proc.terminate()
            await self.proc.wait()



def prepare_client_message(message: str, cwd: str) -> str:
    """
    Allows for the initialization of the pyrefly server to give it the path of the root
    """
    payload = json.loads(message)

    if payload.get("method") == "initialize":
        params = payload.setdefault("params", {})
        params["rootUri"] = Path(cwd).resolve().as_uri()

    return json.dumps(payload)
