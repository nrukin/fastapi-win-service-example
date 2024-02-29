from fastapi import FastAPI
from uuid import uuid4

app = FastAPI()


@app.get("/generate_uuid")
def generate_uid(count: int = 1) -> list[str]:
    return [str(uuid4()) for i in range(count)]
