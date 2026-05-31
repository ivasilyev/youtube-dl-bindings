import queue
import time
import threading
from typing import List

from log import log


class ThreadSafeDownloader:
    """
    Single video download daemon
    """
    _instance = None
    _lock = threading.Lock()
    _queue = queue.Queue()

    def __new__(cls, *args, **kwargs):
        """Ensures only one instance of the downloader is created safely across threads."""
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        """Initializes the queue and starts the background worker thread once."""
        if self._initialized:
            return

        self._is_running = True

        # Start the background polling loop
        self._worker_thread = threading.Thread(
            target=self._process_queue, daemon=True
        )
        self._worker_thread.start()

        self._initialized = True

    def push(self, url: str, ):
        """Thread-safe method to add a new download item to the queue."""
        with self._queue.mutex:
            self._queue.put(url)
        log.info(f"[Queue] Added: {url}")

    def get_queued_items(self) -> str:
        with self._queue.mutex:
            items: List[str] = list(self._queue.queue)
        if not items:
            return ""
        formatted_list = [f"{i+1}. {url}" for i, url in enumerate(items)]
        return "\n".join(formatted_list)

    def download(self, url: str):
        """Simulates a blocking download process."""
        log.info(f"[Download] Starting: {url}")
        # Simulating network latency
        time.sleep(2)
        log.info(f"[Download] Finished: {url}")

    def _process_queue(self):
        """Internal loop checking for items every 5 seconds without busy-waiting."""
        while self._is_running:
            try:
                # wait up to 5 seconds for an item
                url = self._queue.get(timeout=5)
                self.download(url)
                self._queue.task_done()
            except queue.Empty:
                # Triggered every 5 seconds if the queue remains empty
                log.info("[Worker] Checking queue... No new downloads found.")

    def stop(self):
        """Gracefully stops the worker loop."""
        self._is_running = False


downloader = ThreadSafeDownloader()
