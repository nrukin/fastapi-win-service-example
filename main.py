from fastapi import FastAPI
from uuid import uuid4
import uvicorn

app = FastAPI()


@app.get("/generate_uuid")
def generate_uid(count: int = 1) -> list[str]:
    return [str(uuid4()) for i in range(count)]


class Server():
    def __init__(self, as_service=False):
        self._svc = None
        self.as_service = as_service

    def start(self):

        # Здесь можно настроить параметры хоста, порта, логирования
        config = uvicorn.Config(app)
        self._srv = uvicorn.Server(config=config)

        if self.as_service:
            self._srv.install_signal_handlers = lambda: None

        self._srv.run()

    def stop(self):
        if self._srv is not None:
            self._srv.should_exit = True


def run():
    srv = Server()
    srv.start()


if __name__ == "__main__":
    run()
