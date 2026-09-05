"""Tests for configuration manager."""

from pathlib import Path
import pytest
from identity_cli.config import ConfigManager, get_default_config_dir, get_default_data_dir


def test_default_directories() -> None:
    config_dir = get_default_config_dir()
    data_dir = get_default_data_dir()
    assert isinstance(config_dir, Path)
    assert isinstance(data_dir, Path)
    assert "IdentityCLI" in str(config_dir) or "identity-cli" in str(config_dir)


def test_empty_config(temp_dir: Path) -> None:
    config_file = temp_dir / "nonexistent_config.json"
    mgr = ConfigManager(config_file=config_file)
    assert mgr.load_config() == {}
    # Defaults to OS data dir
    assert mgr.get_data_dir() == get_default_data_dir()


def test_set_custom_data_dir(temp_dir: Path) -> None:
    config_file = temp_dir / "config.json"
    mgr1 = ConfigManager(config_file=config_file)

    custom_path = temp_dir / "custom_identity_data"
    mgr1.set_data_dir(custom_path)

    # Re-initialize new ConfigManager pointing to same file
    mgr2 = ConfigManager(config_file=config_file)
    loaded_dir = mgr2.get_data_dir()
    assert loaded_dir == custom_path.resolve()


def test_windows_drive_path_persistence(temp_dir: Path) -> None:
    config_file = temp_dir / "config.json"
    mgr1 = ConfigManager(config_file=config_file)

    # Use simulated Windows D drive path format
    d_path = Path("D:/IdentityData")
    mgr1.set_data_dir(d_path)

    mgr2 = ConfigManager(config_file=config_file)
    assert "IdentityData" in str(mgr2.get_data_dir())
