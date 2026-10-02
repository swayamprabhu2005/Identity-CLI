import json
import os
from pathlib import Path
import sys
from typing import List, Optional

# Ensure clean UTF-8 handling on Windows terminals
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
if hasattr(sys.stderr, "reconfigure"):
    try:
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

import typer
from rich.console import Console
from rich.panel import Panel

from identity_cli import __version__
from identity_cli.config import ConfigManager
from identity_cli.exports import FIELD_LABELS, export_to_csv, export_to_excel, export_to_json
from identity_cli.generator import IdentityGenerator, normalize_fields
from identity_cli.man import display_manual
from identity_cli.models import Identity
from identity_cli.storage import StorageManager

app = typer.Typer(
    name="identity",
    help="Identity CLI: Generate synthetic test identities with persistent uniqueness.",
    no_args_is_help=True,
    add_completion=False,
)
console = Console()
err_console = Console(stderr=True)


def version_callback(value: bool) -> None:
    """Callback for --version flag."""
    if value:
        typer.echo(f"Identity CLI v{__version__}")
        raise typer.Exit()


@app.callback()
def main(
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        "-v",
        callback=version_callback,
        is_eager=True,
        help="Display Identity CLI version and exit.",
    ),
) -> None:
    """Identity CLI entrypoint."""
    pass


def get_check_mark() -> str:
    """Return a checkmark or safe fallback depending on console capabilities."""
    try:
        encoding = sys.stdout.encoding or "utf-8"
        "✓".encode(encoding)
        return "✓"
    except Exception:
        return "[OK]"


def get_managers(custom_config_file: Optional[Path] = None) -> tuple[ConfigManager, StorageManager]:
    """Helper to initialize config and storage managers."""
    config_mgr = ConfigManager(config_file=custom_config_file)
    data_dir = config_mgr.get_data_dir()
    storage_mgr = StorageManager(data_dir)
    return config_mgr, storage_mgr


@app.command(name="man", help="Display comprehensive reference manual.")
def man_command() -> None:
    """Display Identity CLI reference manual."""
    display_manual(console)


@app.command(
    name="generate",
    help="Generate synthetic identities with persistent uniqueness.",
    context_settings={"help_option_names": []},
)
def generate(
    count: Optional[int] = typer.Option(
        None,
        "--count",
        "-c",
        help="Number of identities to generate (1-10,000).",
    ),
    name: bool = typer.Option(
        False,
        "--name",
        help="Generate name field.",
    ),
    email: bool = typer.Option(
        False,
        "--email",
        help="Generate email field.",
    ),
    password: bool = typer.Option(
        False,
        "--password",
        help="Generate password field.",
    ),
    phone: bool = typer.Option(
        False,
        "--phone",
        "-p",
        help="Generate phone field.",
    ),
    fields: Optional[str] = typer.Option(
        None,
        "--fields",
        "-f",
        help="Comma-separated list of multiple fields (e.g. name,email).",
    ),
    excel: bool = typer.Option(
        False,
        "--excel",
        "-e",
        help="Export generated identities to an Excel (.xlsx) file.",
    ),
    json_output: bool = typer.Option(
        False,
        "--json",
        "-j",
        help="Output or export generated identities in JSON format.",
    ),
    csv_output: bool = typer.Option(
        False,
        "--csv",
        help="Export generated identities to CSV.",
    ),
    terminal_output: bool = typer.Option(
        False,
        "--terminal",
        "-t",
        help="Output generated identities to the terminal.",
    ),
    location: Optional[Path] = typer.Option(
        None,
        "--location",
        "-l",
        help="Target folder for file exports (e.g. . or ./test-data).",
    ),
) -> None:
    """Generate one or more unique synthetic identities."""
    try:
        config_mgr, storage_mgr = get_managers()
        generator = IdentityGenerator(storage=storage_mgr)

        # 1. Resolve quantity (precedence: CLI argument -> saved preference -> 1)
        if count is not None:
            batch_count = count
        else:
            batch_count = config_mgr.get_default_quantity()

        if batch_count < 1:
            err_console.print("[bold red]Error:[/bold red] Count must be greater than 0.")
            raise typer.Exit(code=1)
        if batch_count > 10000:
            err_console.print("[bold red]Error:[/bold red] Maximum batch size is 10,000.")
            raise typer.Exit(code=1)

        # 2. Resolve fields (precedence: Direct flags -> CLI --fields argument -> saved preference)
        direct_fields = []
        if name:
            direct_fields.append("name")
        if email:
            direct_fields.append("email")
        if password:
            direct_fields.append("password")
        if phone:
            direct_fields.append("phone")

        if direct_fields:
            active_fields = direct_fields
            if fields is not None:
                for f in normalize_fields(fields):
                    if f not in active_fields:
                        active_fields.append(f)
        elif fields is not None:
            active_fields = normalize_fields(fields)
            if not active_fields:
                err_console.print("[bold red]Error:[/bold red] At least one valid field must be specified.")
                raise typer.Exit(code=1)
        else:
            saved_fields = config_mgr.get_default_fields()
            active_fields = list(saved_fields)

        # 3. Resolve output format
        format_flags = []
        if excel:
            format_flags.append("excel")
        if json_output:
            format_flags.append("json")
        if csv_output:
            format_flags.append("csv")
        if terminal_output:
            format_flags.append("terminal")

        if len(format_flags) > 1:
            err_console.print("[bold red]Error:[/bold red] Only one output format can be selected.")
            raise typer.Exit(code=1)

        if format_flags:
            selected_format = format_flags[0]
        else:
            selected_format = config_mgr.get_default_format()

        # 4. Resolve output location
        if location is not None:
            base_location = Path(location).resolve()
        else:
            base_location = config_mgr.get_default_location().resolve()

        folder_name = config_mgr.get_folder_name()
        export_folder = base_location / folder_name

        if selected_format == "terminal" and batch_count > 1:
            console.print(f"Generating {batch_count} identities...")

        # 5. Generate complete batch
        batch: List[Identity] = generator.generate_batch(
            count=batch_count,
            fields=active_fields,
            include_phone=False,
        )

        # 6. Commit new records to persistent history
        storage_mgr.append_batch(batch)

        # 7. Render or export
        chk = get_check_mark()

        # JSON format handling:
        # If --location is provided, export to identities.json file.
        # Otherwise, output clean JSON directly to terminal/stdout (supporting CLI piping & tests).
        if selected_format == "json" and location is None:
            if batch_count == 1:
                typer.echo(batch[0].to_json(selected_fields=active_fields))
            else:
                data = [item.to_dict(selected_fields=active_fields) for item in batch]
                typer.echo(json.dumps(data, indent=2))
            return

        if selected_format == "terminal":
            if batch_count == 1:
                item = batch[0]
                lines = []
                for f in active_fields:
                    val = getattr(item, f, "")
                    label = FIELD_LABELS.get(f, f.title())
                    lines.append(f"[bold cyan]{label:<8}[/bold cyan] : {val}")
                panel_text = "\n".join(lines)
                panel = Panel(
                    panel_text,
                    title="[bold green]GENERATED IDENTITY[/bold green]",
                    expand=False,
                )
                console.print(panel)
                console.print(f"\n[green]{chk}[/green] Identity generated successfully.")
            else:
                for idx, item in enumerate(batch, 1):
                    console.print(f"[bold green]Identity {idx}[/bold green]")
                    for f in active_fields:
                        val = getattr(item, f, "")
                        label = FIELD_LABELS.get(f, f.title())
                        console.print(f"  [bold cyan]{label:<8}[/bold cyan] : {val}")
                    if idx < batch_count:
                        console.print()
                console.print(f"\n[green]{chk}[/green] Generated {batch_count} identities")
                console.print(f"[green]{chk}[/green] Uniqueness verified")
                console.print(f"[green]{chk}[/green] Identity history updated")
            return

        # File-based export (excel, json with location, csv)
        if selected_format == "excel":
            exported_file = export_to_excel(batch, export_folder, fields=active_fields)
            format_display = "Excel"
            if storage_mgr.exports_dir.resolve() != export_folder.resolve():
                import shutil
                storage_mgr.exports_dir.mkdir(parents=True, exist_ok=True)
                shutil.copy2(exported_file, storage_mgr.exports_dir / exported_file.name)
        elif selected_format == "json":
            exported_file = export_to_json(batch, export_folder, fields=active_fields)
            format_display = "JSON"
        elif selected_format == "csv":
            exported_file = export_to_csv(batch, export_folder, fields=active_fields)
            format_display = "CSV"
        else:
            err_console.print(f"[bold red]Error:[/bold red] Unknown format: {selected_format}")
            raise typer.Exit(code=1)

        console.print(f"[green]{chk}[/green] Generation completed\n")
        console.print(f"[green]{chk}[/green] Generated {batch_count} identities")
        console.print(f"[green]{chk}[/green] Uniqueness verified")
        console.print(f"[green]{chk}[/green] Identity history updated")
        if selected_format == "excel":
            console.print(f"[green]{chk}[/green] Excel file created\n")
        else:
            console.print()
        console.print(f"Records: {batch_count}")
        console.print("Fields:")
        for f in active_fields:
            console.print(f"  {FIELD_LABELS.get(f, f.title())}")
        console.print(f"\nFormat: {format_display}\n")
        console.print("Saved to:")
        console.print(f"[bold]{exported_file}[/bold]")

    except typer.Exit:
        raise
    except Exception as exc:
        err_console.print(f"[bold red]Error:[/bold red] {exc}")
        raise typer.Exit(code=1)


@app.command(name="config", help="View or update Identity CLI configuration.")
def config_command(
    data_dir: Optional[Path] = typer.Option(
        None,
        "--data-dir",
        "-d",
        help="Set custom persistent storage directory (e.g. D:\\IdentityData).",
    ),
    location: Optional[Path] = typer.Option(
        None,
        "--location",
        "-l",
        help="Set default output location for generated files.",
    ),
    fields: Optional[str] = typer.Option(
        None,
        "--fields",
        "-f",
        help="Set default fields (comma-separated: name, email, password, phone).",
    ),
    quantity: Optional[int] = typer.Option(
        None,
        "--quantity",
        "-q",
        help="Set default generation quantity.",
    ),
    format_opt: Optional[str] = typer.Option(
        None,
        "--format",
        help="Set default output format (terminal, excel, json, csv).",
    ),
    folder_name: Optional[str] = typer.Option(
        None,
        "--folder-name",
        help="Set folder name for file outputs (default: generated-names).",
    ),
    show: bool = typer.Option(
        False,
        "--show",
        "-s",
        help="Display current configuration.",
    ),
) -> None:
    """Configure CLI preferences or display current settings."""
    try:
        config_mgr, storage_mgr = get_managers()
        chk = get_check_mark()
        updated = False

        if data_dir is not None:
            resolved_dir = config_mgr.set_data_dir(data_dir)
            console.print(f"[green]{chk}[/green] Data directory updated successfully.")
            console.print(f"Persistent data will now be stored in: [bold]{resolved_dir}[/bold]")
            updated = True

        if location is not None:
            resolved_loc = config_mgr.set_default_location(location)
            console.print(f"[green]{chk}[/green] Default location updated successfully: [bold]{resolved_loc}[/bold]")
            updated = True

        if fields is not None:
            clean_fields = normalize_fields(fields)
            config_mgr.set_default_fields(clean_fields)
            console.print(f"[green]{chk}[/green] Default fields updated successfully: [bold]{', '.join(clean_fields)}[/bold]")
            updated = True

        if quantity is not None:
            clean_qty = config_mgr.set_default_quantity(quantity)
            console.print(f"[green]{chk}[/green] Default quantity updated successfully: [bold]{clean_qty}[/bold]")
            updated = True

        if format_opt is not None:
            clean_fmt = config_mgr.set_default_format(format_opt)
            console.print(f"[green]{chk}[/green] Default format updated successfully: [bold]{clean_fmt}[/bold]")
            updated = True

        if folder_name is not None:
            clean_folder = config_mgr.set_folder_name(folder_name)
            console.print(f"[green]{chk}[/green] Folder name updated successfully: [bold]{clean_folder}[/bold]")
            updated = True

        if updated and not show:
            return

        # Show current configuration
        current_data_dir = config_mgr.get_data_dir()
        current_location = config_mgr.get_default_location()
        current_fields = config_mgr.get_default_fields()
        current_quantity = config_mgr.get_default_quantity()
        current_format = config_mgr.get_default_format()
        current_folder = config_mgr.get_folder_name()
        stats = storage_mgr.get_stats()

        console.print("[bold]Identity CLI Configuration[/bold]\n")
        console.print("Data directory:")
        console.print(f"{current_data_dir}\n")
        console.print("Default location:")
        console.print(f"{current_location}\n")
        console.print("Default folder:")
        console.print(f"{current_folder}\n")
        console.print("Default fields:")
        console.print(f"{', '.join(current_fields)}\n")
        console.print("Default quantity:")
        console.print(f"{current_quantity}\n")
        console.print("Default format:")
        console.print(f"{current_format}\n")
        console.print("Stored names:")
        console.print(f"{stats['stored_names']}\n")
        console.print("Stored emails:")
        console.print(f"{stats['stored_emails']}\n")
        console.print("Stored passwords:")
        console.print(f"{stats['stored_passwords']}\n")
        console.print("Stored phones:")
        console.print(f"{stats['stored_phones']}")

    except Exception as exc:
        err_console.print(f"[bold red]Error:[/bold red] {exc}")
        raise typer.Exit(code=1)


@app.command(name="history", help="Display statistics about stored identity history.")
def history() -> None:
    """Show counts of generated names, emails, passwords, and phones."""
    try:
        config_mgr, storage_mgr = get_managers()
        current_data_dir = config_mgr.get_data_dir()
        stats = storage_mgr.get_stats()

        console.print("[bold]Identity CLI History[/bold]\n")
        console.print(f"Generated identities : {stats['total_identities']}")
        console.print(f"Stored names          : {stats['stored_names']}")
        console.print(f"Stored emails         : {stats['stored_emails']}")
        console.print(f"Stored passwords      : {stats['stored_passwords']}")
        console.print(f"Stored phones         : {stats['stored_phones']}\n")
        console.print("Data directory:")
        console.print(f"{current_data_dir}")

    except Exception as exc:
        err_console.print(f"[bold red]Error:[/bold red] {exc}")
        raise typer.Exit(code=1)


if __name__ == "__main__":
    app()
