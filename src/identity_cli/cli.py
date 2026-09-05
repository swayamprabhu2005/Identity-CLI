import json
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
from identity_cli.excel import export_to_excel
from identity_cli.generator import IdentityGenerator
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


@app.command(name="version", help="Display Identity CLI version.")
def version() -> None:
    """Show the application version."""
    typer.echo(f"Identity CLI v{__version__}")


@app.command(name="generate", help="Generate synthetic identities with persistent uniqueness.")
def generate(
    count: int = typer.Option(
        1,
        "--count",
        "-c",
        help="Number of identities to generate (1-10,000).",
    ),
    phone: bool = typer.Option(
        False,
        "--phone",
        "-p",
        help="Include a reserved test phone number.",
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
        help="Output in clean JSON format.",
    ),
    quiet: bool = typer.Option(
        False,
        "--quiet",
        "-q",
        help="Suppress decorative status and header messages.",
    ),
) -> None:
    """Generate one or more unique synthetic identities."""
    try:
        _, storage_mgr = get_managers()
        generator = IdentityGenerator(storage=storage_mgr)

        # Batch size validation
        if count < 1:
            err_console.print("[bold red]Error:[/bold red] Count must be greater than 0.")
            raise typer.Exit(code=1)
        if count > 10000:
            err_console.print("[bold red]Error:[/bold red] Maximum batch size is 10,000.")
            raise typer.Exit(code=1)

        if not json_output and not quiet and count > 1:
            console.print(f"Generating {count} identities...")

        # 1. Generate complete batch in memory
        batch: List[Identity] = generator.generate_batch(count=count, include_phone=phone)

        # 2. If Excel requested, prepare export
        excel_path: Optional[Path] = None
        if excel:
            excel_path = export_to_excel(batch, storage_mgr.exports_dir)

        # 3. Commit new TXT entries to persistent storage
        storage_mgr.append_batch(batch)

        # 4. Handle output formats
        if json_output:
            if count == 1:
                typer.echo(batch[0].to_json())
            else:
                data = [item.to_dict() for item in batch]
                typer.echo(json.dumps(data, indent=2))
            return

        if count == 1:
            item = batch[0]
            if not quiet:
                panel_text = f"[bold cyan]Name[/bold cyan]     : {item.name}\n"
                panel_text += f"[bold cyan]Email[/bold cyan]    : {item.email}\n"
                panel_text += f"[bold cyan]Password[/bold cyan] : {item.password}"
                if phone:
                    panel_text += f"\n[bold cyan]Phone[/bold cyan]    : {item.phone}"

                panel = Panel(
                    panel_text,
                    title="[bold green]GENERATED IDENTITY[/bold green]",
                    expand=False,
                )
                chk = get_check_mark()
                console.print(panel)
                console.print(f"\n[green]{chk}[/green] Identity generated successfully.")
                if excel and excel_path:
                    console.print(f"[green]{chk}[/green] Excel file created: {excel_path}")
            else:
                typer.echo(f"Name     : {item.name}")
                typer.echo(f"Email    : {item.email}")
                typer.echo(f"Password : {item.password}")
                if phone:
                    typer.echo(f"Phone    : {item.phone}")
        else:
            if not quiet:
                chk = get_check_mark()
                console.print(f"[green]{chk}[/green] Generated {count} identities")
                console.print(f"[green]{chk}[/green] Uniqueness verified")
                console.print(f"[green]{chk}[/green] Identity history updated")
                if excel and excel_path:
                    console.print(f"[green]{chk}[/green] Excel file created\n")
                    console.print("File:")
                    console.print(f"[bold]{excel_path}[/bold]")
            else:
                typer.echo(f"Generated {count} unique identities.")

    except typer.Exit:
        raise
    except Exception as exc:
        err_console.print(f"[bold red]Error:[/bold red] {exc}")
        raise typer.Exit(code=1)


@app.command(name="config", help="View or update Identity CLI configuration.")
def config(
    data_dir: Optional[Path] = typer.Option(
        None,
        "--data-dir",
        "-d",
        help="Set custom persistent storage directory (e.g. D:\\IdentityData).",
    ),
    show: bool = typer.Option(
        False,
        "--show",
        "-s",
        help="Display current configuration.",
    ),
) -> None:
    """Configure data directory or display current settings."""
    try:
        config_mgr, storage_mgr = get_managers()

        if data_dir is not None:
            # Set new data directory
            resolved_dir = config_mgr.set_data_dir(data_dir)
            chk = get_check_mark()
            console.print(f"[green]{chk}[/green] Data directory updated successfully.")
            console.print(f"Persistent data will now be stored in: [bold]{resolved_dir}[/bold]")
            return

        # Show current configuration
        current_data_dir = config_mgr.get_data_dir()
        stats = storage_mgr.get_stats()

        console.print("[bold]Identity CLI Configuration[/bold]\n")
        console.print("Data directory:")
        console.print(f"{current_data_dir}\n")
        console.print("Exports directory:")
        console.print(f"{storage_mgr.exports_dir}\n")
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
