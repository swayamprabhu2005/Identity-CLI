"""Integration tests for the Identity CLI application."""

import json
from pathlib import Path
import pytest
from typer.testing import CliRunner
import openpyxl

from identity_cli.cli import app
from identity_cli.config import ConfigManager
from identity_cli.storage import StorageManager


def test_cli_version(cli_runner: CliRunner) -> None:
    result = cli_runner.invoke(app, ["version"])
    assert result.exit_code == 0
    assert "Identity CLI v0.1.0" in result.output


def test_cli_help(cli_runner: CliRunner) -> None:
    result = cli_runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "generate" in result.output
    assert "config" in result.output
    assert "history" in result.output


def test_cli_generate_help(cli_runner: CliRunner) -> None:
    result = cli_runner.invoke(app, ["generate", "--help"])
    assert result.exit_code == 0
    assert "--count" in result.output
    assert "--phone" in result.output
    assert "--excel" in result.output
    assert "--json" in result.output


def test_cli_generate_single(cli_runner: CliRunner, isolated_config: ConfigManager) -> None:
    result = cli_runner.invoke(app, ["generate"])
    assert result.exit_code == 0
    assert "GENERATED IDENTITY" in result.output
    assert "Name" in result.output
    assert "Email" in result.output
    assert "Password" in result.output

    # Verify persistent storage updated
    storage = StorageManager(isolated_config.get_data_dir())
    stats = storage.get_stats()
    assert stats["stored_names"] == 1
    assert stats["stored_emails"] == 1
    assert stats["stored_passwords"] == 1
    assert stats["stored_phones"] == 0


def test_cli_generate_single_with_phone(cli_runner: CliRunner, isolated_config: ConfigManager) -> None:
    result = cli_runner.invoke(app, ["generate", "--phone"])
    assert result.exit_code == 0
    assert "Phone" in result.output

    storage = StorageManager(isolated_config.get_data_dir())
    stats = storage.get_stats()
    assert stats["stored_phones"] == 1


def test_cli_generate_json(cli_runner: CliRunner, isolated_config: ConfigManager) -> None:
    result = cli_runner.invoke(app, ["generate", "--json"])
    assert result.exit_code == 0
    parsed = json.loads(result.output)
    assert "name" in parsed
    assert "email" in parsed
    assert "password" in parsed
    assert "phone" not in parsed


def test_cli_generate_batch_json(cli_runner: CliRunner, isolated_config: ConfigManager) -> None:
    result = cli_runner.invoke(app, ["generate", "--count", "3", "--json"])
    assert result.exit_code == 0
    parsed = json.loads(result.output)
    assert isinstance(parsed, list)
    assert len(parsed) == 3
    # Check all unique
    names = [x["name"] for x in parsed]
    assert len(set(names)) == 3


def test_cli_generate_batch_with_excel(cli_runner: CliRunner, isolated_config: ConfigManager) -> None:
    result = cli_runner.invoke(app, ["generate", "--count", "10", "--phone", "--excel"])
    assert result.exit_code == 0
    assert "Generated 10 identities" in result.output
    assert "Excel file created" in result.output

    storage = StorageManager(isolated_config.get_data_dir())
    stats = storage.get_stats()
    assert stats["stored_names"] == 10
    assert stats["stored_emails"] == 10
    assert stats["stored_passwords"] == 10
    assert stats["stored_phones"] == 10

    # Verify Excel file exists and has 10 data rows
    excel_files = list(storage.exports_dir.glob("*.xlsx"))
    assert len(excel_files) >= 1
    wb = openpyxl.load_workbook(excel_files[0])
    ws = wb.active
    assert ws.max_row == 11  # Header + 10 data rows


def test_cli_validation_errors(cli_runner: CliRunner, isolated_config: ConfigManager) -> None:
    # Count 0
    res_zero = cli_runner.invoke(app, ["generate", "--count", "0"])
    assert res_zero.exit_code != 0
    assert "Count must be greater than 0" in res_zero.output

    # Count too large
    res_large = cli_runner.invoke(app, ["generate", "--count", "10001"])
    assert res_large.exit_code != 0
    assert "Maximum batch size is 10,000" in res_large.output


def test_cli_config_and_history(cli_runner: CliRunner, isolated_config: ConfigManager, temp_dir: Path) -> None:
    # Check initial config
    res_config = cli_runner.invoke(app, ["config"])
    assert res_config.exit_code == 0
    assert "Identity CLI Configuration" in res_config.output

    # Check history
    res_history = cli_runner.invoke(app, ["history"])
    assert res_history.exit_code == 0
    assert "Identity CLI History" in res_history.output

    # Set new data directory
    new_dir = temp_dir / "new_storage_dir"
    res_set = cli_runner.invoke(app, ["config", "--data-dir", str(new_dir)])
    assert res_set.exit_code == 0
    assert "Data directory updated successfully" in res_set.output

    # Verify new dir is reflected in config
    assert isolated_config.get_data_dir() == new_dir.resolve()
