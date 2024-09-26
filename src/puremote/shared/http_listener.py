import httpx
from httpx_sse import connect_sse

from loguru import logger


class HttpListener:
    def __init__(self, address: str) -> None:
        self.url = address

    def stop(self) -> None:
        self.is_running = False

    def listen(self):
        self.is_running = True
        previous_id = 0

        logger.info(f"Listening on {self.url}")

        with httpx.Client() as client:
            while self.is_running:
                try:
                    response = client.get(self.url)

                    data: dict = response.json()
                    trial_id = data["trialId"]
                    if trial_id != previous_id:
                        previous_id = trial_id
                        yield data
                except httpx.ConnectError:
                    logger.error("Server not running")


class HttpListenerSse:
    def __init__(self, address: str) -> None:
        self.url = address

    def stop(self) -> None:
        self.is_running = False

    def listen(self):
        logger.info(f"Listening on {self.url}")
        with httpx.Client() as client:
            with connect_sse(client, "GET", self.url) as event_source:
                for sse in event_source.iter_sse():
                    yield sse.json()


if __name__ == "__main__":
    listener = HttpListenerSse("http://localhost:8000/sse")

    for data in listener.listen():
        print(data)
