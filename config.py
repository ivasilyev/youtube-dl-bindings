import json
import os
import threading
from pathlib import Path

from pydantic import BaseModel, Field, ValidationError

from system_utils import is_windows_os

BINARY_DIR = os.path.join(os.getcwd(), "bin")
CONFIG_FILE = os.path.join(os.getcwd(), "config.json")


def get_default_yt_dlp_cmd() -> str:
    if is_windows_os():
        return 'yt-dlp.exe "{{ url }}" "{{ directory }}"'
    else:
        return 'yt-dlp "{{ url }}" "{{ directory }}"'


# 1. The DTO containing your exact default values and validation guardrails
class ConfigDTO(BaseModel):
    fetch_max_attempts: int = Field(
        default=10,
        gt=0,
        description="Maximum number of retry attempts for network operations"
    )
    fetch_max_delay_seconds: int = Field(
        default=10,
        gt=0,
        description="Maximum delay in seconds between retries"
    )
    yt_dlp_command_template: str = Field(
        default=get_default_yt_dlp_cmd(),
        min_length=1,
        description="Command template string for executing yt-dlp"
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

    def __init_singleton(self):
        """Internal initialization executed exactly once for the singleton instance."""
        self.__lock = threading.Lock()  # Instance-level lock for thread-safe field updates
        self.__load_from_disk()

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
            self.__yt_dlp_command_template = validated_config.yt_dlp_command_template

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
            yt_dlp_command_template=self.__yt_dlp_command_template
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
                ConfigDTO(
                    fetch_max_attempts=value,
                    fetch_max_delay_seconds=self.__fetch_max_delay_seconds,
                    yt_dlp_command_template=self.__yt_dlp_command_template
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
                ConfigDTO(
                    fetch_max_attempts=self.__fetch_max_attempts,
                    fetch_max_delay_seconds=value,
                    yt_dlp_command_template=self.__yt_dlp_command_template
                )
                self.__fetch_max_delay_seconds = value
                self.__save_to_disk()
            except ValidationError as e:
                raise ValueError(f"Invalid fetch_max_delay_seconds constraint: {e}")

    def get_yt_dlp_command_template(self) -> str:
        with self.__lock:
            return self.__yt_dlp_command_template

    def set_yt_dlp_command_template(self, value: str) -> None:
        with self.__lock:
            try:
                ConfigDTO(
                    fetch_max_attempts=self.__fetch_max_attempts,
                    fetch_max_delay_seconds=self.__fetch_max_delay_seconds,
                    yt_dlp_command_template=value
                )
                self.__yt_dlp_command_template = value
                self.__save_to_disk()
            except ValidationError as e:
                raise ValueError(f"Invalid yt_dlp_command_template constraint: {e}")
