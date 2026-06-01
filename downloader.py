import json
import queue
import threading
from copy import deepcopy
from typing import List

from log import log
from single_downloader import single_download


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
        self._downloading: dict = dict()

    def push(self, url: str, directory: str, ):
        """Thread-safe method to add a new download item to the queue."""
        self._queue.put(dict(url=url, directory=directory))
        print(f"[Queue] Added: {url}")

    def get_queued_items(self) -> List[dict]:
        items: List[dict] = list(self._queue.queue)
        if items is None:
            return list()
        return items

    def download(self, url: str, directory: str, ):
        kwargs: dict = dict(url=url, directory=directory)
        """Simulates a blocking download process."""
        print(f"[Download] Starting: {url}")
        single_download(**kwargs)
        self._downloading.clear()
        self._downloading.update(kwargs)
        print(f"[Download] Finished: {url}")
        self._downloading.clear()

    def get_currently_downloading(self) -> dict:
        return deepcopy(self._downloading)

    def _process_queue(self):
        """Internal loop checking for items every 5 seconds without busy-waiting."""
        while self._is_running:
            try:
                # wait up to 5 seconds for an item
                kwargs = self._queue.get(timeout=5)
                self.download(**kwargs)
                self._queue.task_done()
            except queue.Empty:
                # Triggered every 5 seconds if the queue remains empty
                print("[Worker] Checking queue... No new downloads found.")

    def stop(self):
        """Gracefully stops the worker loop."""
        self._is_running = False


downloader = ThreadSafeDownloader()
