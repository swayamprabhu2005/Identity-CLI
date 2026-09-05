"""Shared pytest fixtures."""

import os
from pathlib import Path
import pytest
from typer.testing import CliRunner

from identity_cli.config import ConfigManager
from identity_cli.storage import StorageManager


@pytest.fixture
def temp_dir(tmp_path: Path) -> Path:
    """Provide a temporary directory for isolated tests."""
    return tmp_path


@pytest.fixture
def isolated_config(temp_dir: Path, monkeypatch: pytest.MonkeyPatch) -> ConfigManager:
    """Provide an isolated ConfigManager backed by a temporary file."""
    config_dir = temp_dir / "app_config"
    data_dir = temp_dir / "identity_data"

    monkeypatch.setenv("IDENTITY_CONFIG_DIR", str(config_dir))
    monkeypatch.setenv("IDENTITY_DATA_DIR", str(data_dir))
    monkeypatch.setenv("LOCALAPPDATA", str(temp_dir))
    monkeypatch.setenv("APPDATA", str(temp_dir))

    cfg_mgr = ConfigManager()
    cfg_mgr.set_data_dir(data_dir)
    return cfg_mgr


@pytest.fixture
def storage(temp_dir: Path) -> StorageManager:
    """Provide an isolated StorageManager."""
    return StorageManager(base_dir=temp_dir / "storage")


@pytest.fixture
def cli_runner() -> CliRunner:
    """Provide a Typer CliRunner for testing CLI commands."""
    return CliRunner()
