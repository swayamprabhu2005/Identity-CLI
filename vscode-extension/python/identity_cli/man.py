"""Built-in manual page for Identity CLI (identity man)."""

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text


def display_manual(console: Console) -> None:
    """Render a comprehensive Unix-style manual page for Identity CLI."""
    console.print()
    header_text = Text("IDENTITY(1)                   General Commands Manual                  IDENTITY(1)", style="bold")
    console.print(header_text)
    console.print()

    # NAME
    console.print("[bold cyan]NAME[/bold cyan]")
    console.print("    [bold]identity[/bold] — generate synthetic test identities with persistent local uniqueness guarantees\n")

    # SYNOPSIS
    console.print("[bold cyan]SYNOPSIS[/bold cyan]")
    console.print("    [bold]identity[/bold] [bold green]generate[/bold green] [options]")
    console.print("    [bold]identity[/bold] [bold green]man[/bold green]")
    console.print("    [bold]identity[/bold] [bold green]config[/bold green] [options]")
    console.print("    [bold]identity[/bold] [bold green]history[/bold green]")
    console.print("    [bold]identity[/bold] [bold green]--version[/bold green] | [bold green]-v[/bold green]")
    console.print("    [bold]identity[/bold] [bold green]--help[/bold green]\n")

    # DESCRIPTION
    console.print("[bold cyan]DESCRIPTION[/bold cyan]")
    console.print(
        "    The [bold]Identity CLI[/bold] is a developer and QA utility for generating realistic, synthetic test\n"
        "    identities. Generated identities are checked against a persistent local history to strictly\n"
        "    guarantee uniqueness across sessions and days.\n\n"
        "    All data generated is non-production, test-safe:\n"
        "    • Emails use official RFC-reserved test domains (example.com, example.org, example.net).\n"
        "    • Phone numbers use North American reserved fictional test ranges (555-0100 to 555-0199).\n"
        "    • Passwords are cryptographically generated using Python's secrets module.\n"
        "    • The tool is 100% offline with zero telemetry and zero network calls.\n"
    )

    # COMMANDS
    console.print("[bold cyan]COMMANDS[/bold cyan]")
    console.print("    [bold green]generate[/bold green]")
    console.print("        Generate synthetic test identities using direct flags, saved preferences, or supplied options.\n")
    console.print("    [bold green]man[/bold green]")
    console.print("        Display this comprehensive reference manual.\n")
    console.print("    [bold green]config[/bold green]")
    console.print("        View or update CLI preferences (data directory, default location, fields, quantity, format).\n")
    console.print("    [bold green]history[/bold green]")
    console.print("        Display statistics on stored names, emails, passwords, and phones.\n")

    # OPTIONS FOR GENERATE
    console.print("[bold cyan]OPTIONS FOR GENERATE[/bold cyan]")

    table = Table(box=None, show_header=False, pad_edge=False, padding=(0, 2))
    table.add_column("Option", style="bold yellow", width=30)
    table.add_column("Description", style="white")

    table.add_row(
        "-c, --count INTEGER",
        "Number of identities to generate (1 to 10,000). Default is 1 (or configured default).",
    )
    table.add_row(
        "--name",
        "Generate name field only (can be combined with other direct field flags).",
    )
    table.add_row(
        "--email",
        "Generate email field only (can be combined with other direct field flags).",
    )
    table.add_row(
        "--password",
        "Generate password field only (can be combined with other direct field flags).",
    )
    table.add_row(
        "-p, --phone",
        "Generate phone field only (can be combined with other direct field flags).",
    )
    table.add_row(
        "-f, --fields TEXT",
        "Comma-separated list of multiple fields (e.g. --fields name,email).",
    )
    table.add_row(
        "-e, --excel",
        "Export generated identities to an Excel (.xlsx) file in generated-names/ folder.",
    )
    table.add_row(
        "-j, --json",
        "Output JSON directly to stdout or export to generated-names/ if --location is set.",
    )
    table.add_row(
        "-c, --csv",
        "Export generated identities to a CSV file in generated-names/ folder.",
    )
    table.add_row(
        "-t, --terminal",
        "Output generated identities to the terminal.",
    )
    table.add_row(
        "-l, --location PATH",
        "Target folder for file exports (e.g. ., ./test-data, D:\\Exports). Does not affect history.",
    )
    console.print(table)
    console.print()

    # FIELD SPECIFICATION
    console.print("[bold cyan]FIELD SPECIFICATION & SELECTION[/bold cyan]")
    console.print(
        "    Single field: pass the field flag directly (e.g. `--name` or `--email`).\n"
        "    Multiple fields: pass multiple flags or use `--fields`:\n"
        "    • [bold]name[/bold]          — Full Name (FirstName LastName)\n"
        "    • [bold]email[/bold]         — Synthetic Email on safe domain\n"
        "    • [bold]password[/bold]      — High-entropy random password\n"
        "    • [bold]phone[/bold]         — Reserved fictional test phone (+1 555-01xx)\n\n"
        "    Default CLI fields (when no fields or flags are specified): name, email, password.\n"
    )

    # OUTPUT DIRECTORY & FOLDER STRUCTURE
    console.print("[bold cyan]FILE EXPORTS VS PERSISTENT HISTORY[/bold cyan]")
    console.print(
        "    [bold]--data-dir[/bold]  : Strictly stores persistent uniqueness history files (names.txt, emails.txt, etc.).\n"
        "    [bold]--location[/bold]  : Strictly target base directory for file-based exports (Excel, JSON, CSV).\n\n"
        "    File exports are saved in a subfolder named [bold]generated-names/[/bold]:\n"
        "        <TargetLocation>/\n"
        "        └── generated-names/\n"
        "            ├── identities.xlsx\n"
        "            ├── identities.json\n"
        "            └── identities.csv\n\n"
        "    Existing files are preserved safely with sequential suffixes (e.g. identities_1.xlsx).\n"
    )

    # PRECEDENCE RULES
    console.print("[bold cyan]PRECEDENCE RULES[/bold cyan]")
    console.print(
        "    Every setting follows this strict three-tier precedence:\n"
        "        [bold]EXPLICIT CLI ARGUMENT[/bold]  ⟶  [bold]SAVED USER PREFERENCE[/bold]  ⟶  [bold]APPLICATION DEFAULT[/bold]\n\n"
        "    • Quantity : --count          ⟶  saved default quantity ⟶  1\n"
        "    • Format   : format flags     ⟶  saved default format   ⟶  terminal\n"
        "    • Fields   : direct / --fields⟶  saved default fields   ⟶  name, email, password\n"
        "    • Location : --location       ⟶  saved default location ⟶  current working directory\n"
    )

    # CONFIGURATION & VS CODE EXTENSION
    console.print("[bold cyan]CONFIGURATION & VS CODE EXTENSION[/bold cyan]")
    console.print(
        "    Preferences can be configured in two ways:\n"
        "    1. [bold]VS Code Extension[/bold]: Install the Identity Generator extension for a one-time setup\n"
        "       wizard or run 'Identity Generator: Configure' from the Command Palette.\n"
        "    2. [bold]CLI Command[/bold]: Use `identity config` to view settings or update options:\n"
        "       • identity config --data-dir <path>     (Sets persistent history directory)\n"
        "       • identity config --location <path>     (Sets default file export base location)\n"
        "       • identity config --fields <name,email,...>\n"
        "       • identity config --quantity <int>\n"
        "       • identity config --format <terminal|excel|json|csv>\n"
    )

    # PRACTICAL EXAMPLES
    console.print("[bold cyan]EXAMPLES[/bold cyan]")
    console.print("    [bold]1. Generate default identity to terminal (name, email, password):[/bold]")
    console.print("       $ identity generate\n")

    console.print("    [bold]2. Generate a single field directly:[/bold]")
    console.print("       $ identity generate --name\n")

    console.print("    [bold]3. Generate specific combined fields:[/bold]")
    console.print("       $ identity generate --name --email\n")
    console.print("       $ identity generate --fields name,email\n")

    console.print("    [bold]4. Generate 5 identities to terminal:[/bold]")
    console.print("       $ identity generate --count 5\n")

    console.print("    [bold]5. Export 12 identities with name and email to Excel:[/bold]")
    console.print("       $ identity generate --count 12 --fields name,email --excel\n")

    console.print("    [bold]6. Export default fields directly to Excel:[/bold]")
    console.print("       $ identity generate --excel\n")

    console.print("    [bold]7. Export to CSV in a custom target location:[/bold]")
    console.print("       $ identity generate --count 50 --csv --location ./reports\n")

    console.print("    [bold]8. Output raw JSON for piping or scripting:[/bold]")
    console.print("       $ identity generate --count 3 --json\n")

    # FOOTER
    console.print("─" * 80, style="dim")
    console.print("Identity CLI • https://github.com/swayamprabhu2005/Identity-CLI", style="dim")
    console.print()
