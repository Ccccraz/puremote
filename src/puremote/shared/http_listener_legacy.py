import time
import requests

import queue

from loguru import logger


class HttpListener:
    def __init__(self, address: str, queue: queue.Queue) -> None:
        self.url = address
        self._queue = queue

    def stop(self) -> None:
        self.is_running = False

    def listening(self) -> None:
        self.is_running = True
        previous_count: int = 0

        logger.info("http listener thread started")

        while self.is_running:
            try:
                response: requests.Response = requests.get(self.url, timeout=1)

                data: dict = response.json()
                count = data["trialCount"]
                if count != previous_count:
                    previous_count = count
                    self._queue.put(data)

                time.sleep(3)

            except Exception as e:
                logger.error(e)
