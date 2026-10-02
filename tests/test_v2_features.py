"""Comprehensive tests for new Identity CLI features (v2 enhancements)."""

import csv
import json
from pathlib import Path
import openpyxl
import pytest
from typer.testing import CliRunner

from identity_cli.cli import app
from identity_cli.config import ConfigManager
from identity_cli.generator import IdentityGenerator, normalize_fields


def test_direct_field_flags(cli_runner: CliRunner, isolated_config: ConfigManager) -> None:
    """Verify direct flags --name, --email, --password, --phone work independently and combined."""
    # Direct --name
    res_name = cli_runner.invoke(app, ["generate", "--name", "--json"])
    assert res_name.exit_code == 0
    data_name = json.loads(res_name.output)
    assert "name" in data_name
    assert "email" not in data_name

    # Direct --email
    res_email = cli_runner.invoke(app, ["generate", "--email", "--json"])
    assert res_email.exit_code == 0
    data_email = json.loads(res_email.output)
    assert "email" in data_email
    assert "password" not in data_email

    # Direct combination --name --email
    res_comb = cli_runner.invoke(app, ["generate", "--name", "--email", "--json"])
    assert res_comb.exit_code == 0
    data_comb = json.loads(res_comb.output)
    assert "name" in data_comb
    assert "email" in data_comb
    assert "password" not in data_comb


def test_independent_single_fields(cli_runner: CliRunner, isolated_config: ConfigManager) -> None:
    """Verify each supported field can be generated independently."""
    # 1. Name only
    res_name = cli_runner.invoke(app, ["generate", "--fields", "name", "--json"])
    assert res_name.exit_code == 0
    data_name = json.loads(res_name.output)
    assert "name" in data_name
    assert "email" not in data_name
    assert "password" not in data_name
    assert "phone" not in data_name

    # 2. Email only
    res_email = cli_runner.invoke(app, ["generate", "--fields", "email", "--json"])
    assert res_email.exit_code == 0
    data_email = json.loads(res_email.output)
    assert "email" in data_email
    assert "name" not in data_email
    assert "password" not in data_email
    assert "phone" not in data_email

    # 3. Password only
    res_pass = cli_runner.invoke(app, ["generate", "--fields", "password", "--json"])
    assert res_pass.exit_code == 0
    data_pass = json.loads(res_pass.output)
    assert "password" in data_pass
    assert "name" not in data_pass
    assert "email" not in data_pass
    assert "phone" not in data_pass

    # 4. Phone only
    res_phone = cli_runner.invoke(app, ["generate", "--fields", "phone", "--json"])
    assert res_phone.exit_code == 0
    data_phone = json.loads(res_phone.output)
    assert "phone" in data_phone
    assert "name" not in data_phone
    assert "email" not in data_phone
    assert "password" not in data_phone


def test_field_aliases_and_combinations(cli_runner: CliRunner, isolated_config: ConfigManager) -> None:
    """Verify field aliases and multiple field combinations."""
    # Aliases: fullname, pass, phone-number
    res = cli_runner.invoke(app, ["generate", "--fields", "fullname,pass,phone-number", "--json"])
    assert res.exit_code == 0
    data = json.loads(res.output)
    assert "name" in data
    assert "password" in data
    assert "phone" in data
    assert "email" not in data


def test_invalid_field_error(cli_runner: CliRunner, isolated_config: ConfigManager) -> None:
    """Verify invalid field names produce clear error messages."""
    res = cli_runner.invoke(app, ["generate", "--fields", "address"])
    assert res.exit_code != 0
    assert "Unknown field 'address'" in res.output
    assert "Supported fields: name, email, password, phone" in res.output


def test_conflicting_format_flags(cli_runner: CliRunner, isolated_config: ConfigManager) -> None:
    """Verify error when multiple conflicting formats are specified."""
    res = cli_runner.invoke(app, ["generate", "--json", "--excel"])
    assert res.exit_code != 0
    assert "Only one output format can be selected" in res.output


def test_format_json_with_location(cli_runner: CliRunner, isolated_config: ConfigManager, temp_dir: Path) -> None:
    """Verify --json with --location saves to generated-names/identities.json."""
    export_loc = temp_dir / "target_loc"
    res = cli_runner.invoke(app, [
        "generate",
        "--count", "3",
        "--fields", "name,email",
        "--json",
        "--location", str(export_loc),
    ])
    assert res.exit_code == 0
    assert "Generation completed" in res.output
    assert "Format: JSON" in res.output

    expected_file = export_loc / "generated-names" / "identities.json"
    assert expected_file.exists()

    with open(expected_file, "r", encoding="utf-8") as f:
        loaded = json.load(f)
    assert len(loaded) == 3
    for entry in loaded:
        assert "name" in entry
        assert "email" in entry
        assert "password" not in entry
        assert "phone" not in entry


def test_format_excel_with_location_and_strict_columns(
    cli_runner: CliRunner, isolated_config: ConfigManager, temp_dir: Path
) -> None:
    """Verify Excel export creates strict columns without unselected fields."""
    export_loc = temp_dir / "excel_loc"
    res = cli_runner.invoke(app, [
        "generate",
        "--count", "5",
        "--fields", "name,password",
        "--excel",
        "--location", str(export_loc),
    ])
    assert res.exit_code == 0
    expected_file = export_loc / "generated-names" / "identities.xlsx"
    assert expected_file.exists()

    wb = openpyxl.load_workbook(expected_file)
    ws = wb.active
    headers = [cell.value for cell in ws[1]]
    assert headers == ["ID", "Name", "Password"]
    assert "Email" not in headers
    assert "Phone" not in headers
    assert ws.max_row == 6  # header + 5 rows


def test_format_csv_with_location(
    cli_runner: CliRunner, isolated_config: ConfigManager, temp_dir: Path
) -> None:
    """Verify CSV export creates valid CSV with strictly selected fields."""
    export_loc = temp_dir / "csv_loc"
    res = cli_runner.invoke(app, [
        "generate",
        "--count", "4",
        "--fields", "email,phone",
        "--csv",
        "--location", str(export_loc),
    ])
    assert res.exit_code == 0
    expected_file = export_loc / "generated-names" / "identities.csv"
    assert expected_file.exists()

    with open(expected_file, "r", encoding="utf-8") as f:
        reader = list(csv.reader(f))
    assert reader[0] == ["ID", "Email", "Phone"]
    assert len(reader) == 5  # header + 4 rows


def test_count_precedence_and_config(cli_runner: CliRunner, isolated_config: ConfigManager) -> None:
    """Verify saved default quantity is used when --count is omitted, but overridden when supplied."""
    # Set default quantity to 4
    isolated_config.set_default_quantity(4)
    res_default = cli_runner.invoke(app, ["generate", "--json"])
    assert res_default.exit_code == 0
    data = json.loads(res_default.output)
    assert len(data) == 4

    # Explicit --count 2 overrides saved 4
    res_override = cli_runner.invoke(app, ["generate", "--count", "2", "--json"])
    assert res_override.exit_code == 0
    data_override = json.loads(res_override.output)
    assert len(data_override) == 2


def test_fields_precedence_and_config(cli_runner: CliRunner, isolated_config: ConfigManager) -> None:
    """Verify saved default fields are used when --fields is omitted, but overridden when supplied."""
    # Set default fields to name only
    isolated_config.set_default_fields(["name"])
    res_default = cli_runner.invoke(app, ["generate", "--json"])
    assert res_default.exit_code == 0
    data = json.loads(res_default.output)
    assert "name" in data
    assert "email" not in data

    # Explicit --fields overrides saved default
    res_override = cli_runner.invoke(app, ["generate", "--fields", "email,password", "--json"])
    assert res_override.exit_code == 0
    data_override = json.loads(res_override.output)
    assert "email" in data_override
    assert "password" in data_override
    assert "name" not in data_override


def test_man_command(cli_runner: CliRunner) -> None:
    """Verify identity man displays comprehensive manual."""
    res = cli_runner.invoke(app, ["man"])
    assert res.exit_code == 0
    assert "IDENTITY(1)" in res.output
    assert "SYNOPSIS" in res.output
    assert "OPTIONS FOR GENERATE" in res.output
    assert "PRECEDENCE RULES" in res.output
    assert "EXAMPLES" in res.output


def test_version_flags(cli_runner: CliRunner) -> None:
    """Verify identity --version and -v work."""
    res_long = cli_runner.invoke(app, ["--version"])
    assert res_long.exit_code == 0
    assert "Identity CLI v" in res_long.output

    res_short = cli_runner.invoke(app, ["-v"])
    assert res_short.exit_code == 0
    assert "Identity CLI v" in res_short.output


def test_config_preferences_update(
    cli_runner: CliRunner, isolated_config: ConfigManager, temp_dir: Path
) -> None:
    """Verify setting all preferences via identity config command."""
    loc_dir = temp_dir / "my_custom_loc"
    res = cli_runner.invoke(app, [
        "config",
        "--location", str(loc_dir),
        "--fields", "name,email,phone",
        "--quantity", "7",
        "--format", "json",
        "--folder-name", "custom-output",
        "--show",
    ])
    assert res.exit_code == 0
    assert "Default location updated successfully" in res.output
    assert "Default fields updated successfully" in res.output
    assert "Default quantity updated successfully: 7" in res.output
    assert "Default format updated successfully: json" in res.output
    assert "Folder name updated successfully: custom-output" in res.output

    # Check persistence
    cfg = isolated_config.load_config()
    assert cfg["default_location"] == str(loc_dir.resolve())
    assert cfg["default_fields"] == ["name", "email", "phone"]
    assert cfg["default_quantity"] == 7
    assert cfg["default_format"] == "json"
    assert cfg["folder_name"] == "custom-output"
