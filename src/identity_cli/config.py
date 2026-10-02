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

    def get_default_location(self) -> Path:
        """Get the configured default export location, falling back to current working directory."""
        config = self.load_config()
        custom_loc = config.get("default_location")
        if custom_loc:
            return Path(custom_loc)
        return Path.cwd()

    def set_default_location(self, new_loc: Path | str) -> Path:
        """Set and persist default export location."""
        path = Path(new_loc).resolve()
        config = self.load_config()
        config["default_location"] = str(path)
        self.save_config(config)
        return path

    def get_default_fields(self) -> list[str]:
        """Get default fields list, falling back to name, email, password."""
        config = self.load_config()
        fields = config.get("default_fields")
        if fields and isinstance(fields, list):
            return [str(f).strip().lower() for f in fields if str(f).strip()]
        return ["name", "email", "password"]

    def set_default_fields(self, fields: list[str]) -> list[str]:
        """Set and persist default fields."""
        config = self.load_config()
        clean = [str(f).strip().lower() for f in fields if str(f).strip()]
        config["default_fields"] = clean
        self.save_config(config)
        return clean

    def get_default_quantity(self) -> int:
        """Get default quantity, strictly defaulting to 1."""
        config = self.load_config()
        val = config.get("default_quantity")
        if val is not None:
            try:
                ival = int(val)
                if ival > 0:
                    return ival
            except (ValueError, TypeError):
                pass
        return 1

    def set_default_quantity(self, qty: int) -> int:
        """Set and persist default quantity."""
        if qty < 1:
            raise ValueError("Default quantity must be at least 1.")
        config = self.load_config()
        config["default_quantity"] = qty
        self.save_config(config)
        return qty

    def get_default_format(self) -> str:
        """Get default format, strictly defaulting to 'terminal'."""
        config = self.load_config()
        fmt = config.get("default_format")
        if fmt and isinstance(fmt, str):
            clean_fmt = fmt.strip().lower()
            if clean_fmt in ["terminal", "excel", "json", "csv"]:
                return clean_fmt
        return "terminal"

    def set_default_format(self, fmt: str) -> str:
        """Set and persist default format."""
        clean_fmt = fmt.strip().lower()
        if clean_fmt not in ["terminal", "excel", "json", "csv"]:
            raise ValueError(f"Unsupported format '{fmt}'. Supported: terminal, excel, json, csv.")
        config = self.load_config()
        config["default_format"] = clean_fmt
        self.save_config(config)
        return clean_fmt

    def get_folder_name(self) -> str:
        """Get folder name for file outputs, defaulting to 'generated-names'."""
        config = self.load_config()
        folder = config.get("folder_name")
        if folder and isinstance(folder, str) and folder.strip():
            return folder.strip()
        return "generated-names"

    def set_folder_name(self, name: str) -> str:
        """Set and persist folder name."""
        clean_name = name.strip() or "generated-names"
        config = self.load_config()
        config["folder_name"] = clean_name
        self.save_config(config)
        return clean_name

    def is_setup_completed(self) -> bool:
        """Check if first-time setup has been completed."""
        config = self.load_config()
        return bool(config.get("setup_completed", False))

    def set_setup_completed(self, completed: bool = True) -> None:
        """Record whether first-time setup is completed."""
        config = self.load_config()
        config["setup_completed"] = completed
        self.save_config(config)
