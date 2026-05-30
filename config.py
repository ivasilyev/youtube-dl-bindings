import json
import threading
from pathlib import Path
from typing import Union

from pydantic import BaseModel, Field, ValidationError

from arch_based_data_provider import get_default_single_download_cmd, get_default_playlist_download_cmd
from constants import CONFIG_FILE


# 1. The DTO containing your exact default values and validation guardrails
from system_utils import sanitize_command


class ConfigDTO(BaseModel):
    fetch_max_attempts: int = Field(
        default=10,
        gt=0,
        description="Maximum number of fetch attempts"
    )
    fetch_max_delay_seconds: int = Field(
        default=10,
        gt=0,
        description="Maximum delay in seconds between attempts"
    )
    single_download_template: str = Field(
        default=get_default_single_download_cmd(),
        min_length=1,
        description="Single download command template"
    )
    playlist_download_template: str = Field(
        default=get_default_playlist_download_cmd(),
        min_length=1,
        description="Playlist download command template"
    )


class ConfigurationManager:
    _instance = None
    _lock = threading.Lock()
    _file_path = Path(CONFIG_FILE)

    def __new__(cls):
        # Thread-safe Double-Checked Locking Singleton
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance.__init_singleton()
        return cls._instance

    def __init__(self):
        self.__fetch_max_attempts: Union[int, None] = None
        self.__fetch_max_delay_seconds: Union[int, None] = None
        self.__single_download_template: Union[str, None] = None
        self.__playlist_download_template: Union[str, None] = None
        self.__load_from_disk()

    def __init_singleton(self):
        """Internal initialization executed exactly once for the singleton instance."""
        self.__lock = threading.Lock()  # Instance-level lock for thread-safe field updates

    def __load_from_disk(self):
        """Reads config from disk and utilizes the DTO definitions for missing keys/defaults."""
        raw_data = {}

        if self._file_path.exists():
            try:
                with open(self._file_path, "r", encoding="utf-8") as f:
                    raw_data = json.load(f)
            except json.JSONDecodeError as e:
                print(f"Warning: config.json is invalid, self-healing with DTO defaults. Error: {e}")

        try:
            # Pydantic automatically injects the DTO defaults if keys are missing
            validated_config = ConfigDTO(**raw_data)

            # Populate Java-like pseudo-private fields
            self.__fetch_max_attempts = validated_config.fetch_max_attempts
            self.__fetch_max_delay_seconds = validated_config.fetch_max_delay_seconds
            self.__single_download_template = sanitize_command(validated_config.single_download_template)
            self.__playlist_download_template = sanitize_command(validated_config.playlist_download_template)

            # Immediately generate or repair the file if it didn't exist or was missing fields
            if not self._file_path.exists() or not raw_data:
                self.__save_to_disk()

        except ValidationError as e:
            print(f"Validation failed during config startup: {e}")
            raise RuntimeError("Configuration manager failed to load valid data structural types.")

    def __save_to_disk(self):
        """Flushes the private attributes safely back to the file system as JSON."""
        current_data = ConfigDTO(
            fetch_max_attempts=self.__fetch_max_attempts,
            fetch_max_delay_seconds=self.__fetch_max_delay_seconds,
            single_download_template=self.__single_download_template,
            playlist_download_template=self.__playlist_download_template,
        )
        with open(self._file_path, "w", encoding="utf-8") as f:
            json.dump(current_data.model_dump(), f, indent=4)

    # --- Java-like Getters & Setters ---

    def get_fetch_max_attempts(self) -> int:
        with self.__lock:
            return self.__fetch_max_attempts

    def set_fetch_max_attempts(self, value: int) -> None:
        with self.__lock:
            try:
                _ = ConfigDTO(
                    fetch_max_attempts=value,
                    fetch_max_delay_seconds=self.__fetch_max_delay_seconds,
                    single_download_template=self.__single_download_template,
                    playlist_download_template=self.__playlist_download_template,
                )
                self.__fetch_max_attempts = value
                self.__save_to_disk()
            except ValidationError as e:
                raise ValueError(f"Invalid fetch_max_attempts constraint: {e}")

    def get_fetch_max_delay_seconds(self) -> int:
        with self.__lock:
            return self.__fetch_max_delay_seconds

    def set_fetch_max_delay_seconds(self, value: int) -> None:
        with self.__lock:
            try:
                _ = ConfigDTO(
                    fetch_max_attempts=self.__fetch_max_attempts,
                    fetch_max_delay_seconds=value,
                    single_download_template=self.__single_download_template,
                    playlist_download_template=self.__playlist_download_template,
                )
                self.__fetch_max_delay_seconds = value
                self.__save_to_disk()
            except ValidationError as e:
                raise ValueError(f"Invalid fetch_max_delay_seconds constraint: {e}")

    def get_single_download_template(self) -> str:
        with self.__lock:
            return self.__single_download_template

    def set_single_download_template(self, value: str) -> None:
        s = sanitize_command(value)
        with self.__lock:
            try:
                _ = ConfigDTO(
                    fetch_max_attempts=self.__fetch_max_attempts,
                    fetch_max_delay_seconds=self.__fetch_max_delay_seconds,
                    single_download_template=s,
                    playlist_download_template=self.__playlist_download_template,
                )
                self.__single_download_template = s
                self.__save_to_disk()
            except ValidationError as e:
                raise ValueError(f"Invalid single_download_template constraint: {e}")

    def get_playlist_download_template(self) -> str:
        with self.__lock:
            return self.__single_download_template

    def set_playlist_download_template(self, value: str) -> None:
        s = sanitize_command(value)
        with self.__lock:
            try:
                _ = ConfigDTO(
                    fetch_max_attempts=self.__fetch_max_attempts,
                    fetch_max_delay_seconds=self.__fetch_max_delay_seconds,
                    single_download_template=self.__single_download_template,
                    playlist_download_template=s,
                )
                self.__playlist_download_template = s
                self.__save_to_disk()
            except ValidationError as e:
                raise ValueError(f"Invalid single_download_template constraint: {e}")


# tests


