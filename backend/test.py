import asyncio
from pathlib import Path

from pyrefly_lsp import PyreflySession


async def main():
    print("Starting Pyrefly...")

    session = PyreflySession(
        cmd=["pyrefly", "lsp"],
        cwd=str(Path(__file__).parent),
    )

    await session.start()
    print("Pyrefly started")

    print("Sending initialize...")
    await session.send_lsp({
        "jsonrpc": "2.0",
        "id": 1,
        "method": "initialize",
        "params": {
            "processId": None,
            "rootUri": Path(__file__).parent.resolve().as_uri(),
            "capabilities": {},
        },
    })

    print("Waiting response...")
    response = await session.recv_lsp()

    print("Response:")
    print(response)

    

    uri = "file:///main.py"

    await session.send_lsp({
        "jsonrpc": "2.0",
        "method": "initialized",
        "params": {}
    })

    await session.send_lsp({
        "jsonrpc": "2.0",
        "method": "textDocument/didOpen",
        "params": {
            "textDocument": {
                "uri": uri,
                "languageId": "python",
                "version": 1,
                "text": "import numpy as np\nnp."
            }
        }
    })

    await session.send_lsp({
        "jsonrpc": "2.0",
        "id": 2,
        "method": "textDocument/completion",
        "params": {
            "textDocument": {
                "uri": uri
            },
            "position": {
                "line": 1,
                "character": 3
            }
        }
    })

    while True:
        response = await session.recv_lsp()
        print(response)

        if response.get("id") == 2:
            break


asyncio.run(main())