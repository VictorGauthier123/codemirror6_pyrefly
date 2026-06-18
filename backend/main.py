from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

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


class CompletionRequest(BaseModel):
    code: str
    line: int
    character: int


@app.post("/api/python/completions")
def completions(req: CompletionRequest):

    print(req.code)
    print(req.line)
    print(req.character)
    return [
        {
            "label": "print",
            "type": "function",
            "detail": "built-in",
            "documentation": "Print objects to stdout.",
            "insertText": "print()",
        },
        {
            "label": "np.array",
            "type": "function",
            "detail": "numpy",
            "documentation": "Create a NumPy array.",
            "insertText": "np.array()",
        },
    ]
