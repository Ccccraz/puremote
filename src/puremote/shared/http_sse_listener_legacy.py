import json
from sseclient import SSEClient

import queue

from loguru import logger


class HttpSSEListener:
    def __init__(self, address: str, queue: queue.Queue) -> None:
        self.url = address
        self._queue = queue

    def stop(self):
        self.is_running = False

    def listening(self) -> None:
        self.is_running = True
        previous_count: int = 0
        messages = SSEClient(self.url)
        logger.info("http listener thread started")

        try:
            for message in messages:
                if not self.is_running:
                    break

                data = json.loads(message.data)
                count = data["totalTrials"]
                if count != previous_count:
                    previous_count = count
                    self._queue.put(data)

        except Exception as e:
            logger.error(e)
