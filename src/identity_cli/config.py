"""Configuration management for Identity CLI."""

import json
import os
from pathlib import Path
import sys
from typing import Any, Dict, Optional


def get_default_config_dir() -> Path:
    """Return the default configuration directory based on OS or environment."""
    env_config = os.environ.get("IDENTITY_CONFIG_DIR")
    if env_config:
        return Path(env_config)
    if sys.platform == "win32":
        app_data = os.environ.get("APPDATA")
        if app_data:
            return Path(app_data) / "IdentityCLI"
        return Path.home() / "AppData" / "Roaming" / "IdentityCLI"
    # Linux / macOS / Unix fallback
    xdg_config = os.environ.get("XDG_CONFIG_HOME")
    if xdg_config:
        return Path(xdg_config) / "identity-cli"
    return Path.home() / ".config" / "identity-cli"


def get_default_data_dir() -> Path:
    """Return the default data directory based on OS or environment."""
    env_data = os.environ.get("IDENTITY_DATA_DIR")
    if env_data:
        return Path(env_data)
    if sys.platform == "win32":
        local_app_data = os.environ.get("LOCALAPPDATA")
        if local_app_data:
            return Path(local_app_data) / "IdentityCLI"
        return Path.home() / "AppData" / "Local" / "IdentityCLI"
    # Linux / macOS / Unix fallback
    xdg_data = os.environ.get("XDG_DATA_HOME")
    if xdg_data:
        return Path(xdg_data) / "identity_cli"
    return Path.home() / ".local" / "share" / "identity_cli"


class ConfigManager:
    """Manages reading and writing application configuration."""

    def __init__(self, config_file: Optional[Path] = None):
        if config_file is not None:
            self.config_file = config_file
        else:
            self.config_file = get_default_config_dir() / "config.json"

    def load_config(self) -> Dict[str, Any]:
        """Load configuration from JSON file or return defaults."""
        if not self.config_file.exists():
            return {}
        try:
            with open(self.config_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError):
            return {}

    def save_config(self, config_data: Dict[str, Any]) -> None:
        """Save configuration dictionary to JSON file."""
        self.config_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.config_file, "w", encoding="utf-8") as f:
            json.dump(config_data, f, indent=2)

    def get_data_dir(self) -> Path:
        """Get the configured data directory, falling back to OS default."""
        config = self.load_config()
        custom_dir = config.get("data_dir")
        if custom_dir:
            return Path(custom_dir)
        return get_default_data_dir()

    def set_data_dir(self, new_dir: Path | str) -> Path:
        """Set and persist a custom data directory."""
        path = Path(new_dir).resolve()
        config = self.load_config()
        config["data_dir"] = str(path)
        self.save_config(config)
        return path
