# Identity CLI & VS Code Extension

<div align="center">

[![Python: 3.10+](https://img.shields.io/badge/Python-3.10%2B-3776AB.svg?style=for-the-badge&logo=python&logoColor=white)](pyproject.toml)
[![License: MIT](https://img.shields.io/badge/License-MIT-brightgreen.svg?style=for-the-badge)](LICENSE)
[![CLI: Typer](https://img.shields.io/badge/CLI-Typer-009688.svg?style=for-the-badge&logo=fastapi&logoColor=white)](https://typer.tiangolo.com)
[![VS Code: Extension](https://img.shields.io/badge/VS%20Code-Extension-007ACC.svg?style=for-the-badge&logo=visualstudiocode&logoColor=white)](vscode-extension/)
[![Platform: Cross-Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-555555.svg?style=for-the-badge)](#requirements)

**A professional developer utility and VS Code extension for generating synthetic, mock test identities with persistent local uniqueness guarantees.**

[🚀 Setup Guide](SETUP_GUIDE.md) • [📖 Usage Guide](USAGE_GUIDE.md) • [⚡ Quick Start](#-quick-start) • [💻 Command Reference](#-command-reference) • [🤝 Contributing](CONTRIBUTING.md) • [📄 License](LICENSE)

</div>

---

> [!NOTE]
> ### 🛡️ Synthetic & Test-Safe Data Guarantee
> All data produced by Identity CLI is strictly synthetic and safe for development, QA testing, and software demonstrations:
> * **Names**: Realistically synthesized by combining first and last names with persistent uniqueness checks.
> * **Emails**: Exclusively use official RFC-reserved test domains (`example.com`, `example.org`, `example.net`).
> * **Phone Numbers**: Exclusively use North American reserved fictional test ranges (`555-0100` through `555-0199`).
> * **Passwords**: High-entropy, cryptographically secure strings generated using Python's `secrets` module.
> * **100% Offline & Private**: Zero external network calls, zero tracking, and zero telemetry.

---

## ✨ Features

* 💻 **Standalone CLI & Integrated Terminal**: Works everywhere — PowerShell, Command Prompt, macOS/Linux terminals, and natively inside VS Code integrated terminals.
* 🎯 **Direct Single-Field Generation**: Generate single fields with direct flags (e.g. `identity generate --name` or `identity generate --email`) without boilerplate syntax.
* 🗂️ **Multi-Field Customization**: Combine direct flags (`--name --email`) or use `--fields name,email`. Default CLI output includes `Name`, `Email`, and `Password`.
* 📊 **Direct Output Formats**: Display instantly in terminal, or export to clean **Excel (`--excel`)**, **JSON (`--json`)**, or **CSV (`--csv`)** files.
* 📁 **Organized File Generation**: Automatically places file exports into a `generated-names/` subfolder at your specified or configured `--location`. Existing files are never overwritten.
* 🔒 **Strict Storage Separation**:
  * `--data-dir` strictly stores persistent uniqueness history (`names.txt`, `emails.txt`, `passwords.txt`, `phones.txt`).
  * `--location` strictly sets the base directory for file-based exports (`.xlsx`, `.json`, `.csv`).
* 📖 **Built-in Offline Manual (`identity man`)**: Instant comprehensive Unix-style reference documentation right in your terminal.
* ⚙️ **One-Time VS Code Setup**: Interactive setup wizard in VS Code to configure export destinations and default preferences once.
* 🔁 **Persistent Uniqueness Across Runs**: Identities already generated are saved locally so you never get duplicates, even across separate days or sessions.

---

## 🚀 Quick Start

### 1. Installation

#### Install CLI Globally via pipx (Recommended)
```bash
pipx install git+https://github.com/swayamprabhu2005/Identity-CLI.git
```
*(Or install with standard pip: `pip install git+https://github.com/swayamprabhu2005/Identity-CLI.git`)*

#### Install VS Code Extension
Install the extension package (`.vsix`) via terminal:
```bash
code --install-extension vscode-extension/identity-generator-0.1.0.vsix
```
*Or search for **Identity Generator** directly in the VS Code Extensions tab.*

👉 For detailed platform-specific installation instructions, see the complete [Setup Guide](SETUP_GUIDE.md).

---

### 2. Generate a Single Identity (Default)
Generates **1 identity** containing **Name**, **Email**, and **Password** rendered directly to the terminal:
```bash
identity generate
```

```text
┌─────────── GENERATED IDENTITY ────────────┐
│ Name     : Jeffrey Jackson                │
│ Email    : jeffrey.jackson614@example.com │
│ Password : EEoiQ-f6UuC%                   │
└───────────────────────────────────────────┘

✓ Identity generated successfully.
```

---

### 3. Generate Single Fields Directly
Need only one field? No need to type `--fields`:
```bash
# Name only
identity generate --name

# Email only
identity generate --email

# Password only
identity generate --password

# Phone only
identity generate --phone
```

---

### 4. Generate Multiple Fields or Batches
```bash
# Combine direct flags
identity generate --name --email

# Or use --fields
identity generate --fields name,email,phone

# Generate 10 identities
identity generate --count 10
# or short flag:
identity generate -c 10
```

---

### 5. Export to Excel, JSON, or CSV
Direct flags make file exports seamless:

```bash
# Export default fields to Excel (.xlsx)
identity generate --excel

# Export 25 names and emails to Excel
identity generate --count 25 --fields name,email --excel

# Output raw JSON to terminal / stdout for piping or scripting
identity generate --count 3 --json

# Export to CSV
identity generate --count 50 --fields name,email,phone --csv

# Export to a custom project directory
identity generate --count 100 --excel --location ./reports
```

Exported files are placed in:
```text
<Location>/
└── generated-names/
    ├── identities.xlsx
    ├── identities.json
    └── identities.csv
```

---

## 💻 Command Reference

| Command | Description |
| :--- | :--- |
| `identity generate [options]` | Generate synthetic test identities. |
| `identity man` | Display the built-in reference manual. |
| `identity config [options]` | View or update configuration preferences. |
| `identity history` | Display statistics of stored names, emails, passwords, and phones. |
| `identity --version` / `-v` | Display Identity CLI version. |
| `identity --help` | Display command help and options. |

### `identity generate` Options

| Flag | Short | Description |
| :--- | :---: | :--- |
| `--count INTEGER` | `-c` | Number of identities to generate (1 to 10,000). Default: `1`. |
| `--name` | | Generate name field only. |
| `--email` | | Generate email field only. |
| `--password` | | Generate password field only. |
| `--phone` | `-p` | Generate phone field only. |
| `--fields TEXT` | `-f` | Comma-separated list of fields (e.g. `name,email`). |
| `--excel` | `-e` | Export generated identities to Excel (`.xlsx`). |
| `--json` | `-j` | Output JSON directly to stdout, or export to file if `--location` is set. |
| `--csv` | | Export generated identities to CSV (`.csv`). |
| `--terminal` | `-t` | Output generated identities to terminal. |
| `--location PATH` | `-l` | Target directory for file exports (e.g. `.`, `./test-data`). |

👉 For full command recipes and workflow guides, see the [Usage Guide](USAGE_GUIDE.md).

---

## ⚙️ Configuration & Storage Separation

Identity CLI separates your **persistent uniqueness history** from your **file-based exports**:

```bash
# View current settings & stored history counts
identity config --show

# Set persistent history directory (names.txt, emails.txt, etc.)
identity config --data-dir "D:\IdentityStorage"

# Set default location for file-based exports (Excel, JSON, CSV)
identity config --location "D:\MyProject\Exports"

# Set default quantity and fields
identity config --quantity 5
identity config --fields name,email
```

### Precedence Rules
Every setting adheres to a strict three-tier precedence:
$$\text{CLI Argument} \longrightarrow \text{User Saved Preference} \longrightarrow \text{Application Default}$$

---

## 📖 Built-in Manual (`identity man`)

Run `identity man` in any terminal to read the full offline manual covering:
* SYNOPSIS & command list
* Detailed generate options and field aliases
* File output directory behavior
* Conflict prevention and precedence hierarchy
* Realistic developer recipes

---

## 🧩 VS Code Extension Integration

The companion VS Code extension provides:
1. **Interactive Setup Wizard**: Open `Identity Generator: Configure Preferences` from the Command Palette to set default export locations, fields, and quantities with a native folder browser.
2. **Integrated Terminal Access**: Automatically injects `identity` into your VS Code terminal PATH.
3. **Command Palette Integration**:
   * `Identity Generator: Configure Preferences`
   * `Identity Generator: Open Documentation (Manual)`
   * `Identity Generator: Open Terminal`

---

## 🧪 Testing

The test suite validates data models, uniqueness persistence across executions, Excel/JSON/CSV formatting, and CLI arguments:

```bash
# Windows (PowerShell)
$env:PYTHONPATH="src"; pytest -v

# Linux / macOS
PYTHONPATH=src pytest -v
```
*(All 43 tests pass with 100% test coverage).*

---

## 📚 Documentation Index

* 🚀 **[Setup Guide](SETUP_GUIDE.md)**: Detailed extension and CLI installation guides.
* 📖 **[Usage Guide](USAGE_GUIDE.md)**: Comprehensive command documentation, examples, and workflow recipes.
* 🤝 **[Contributing Guidelines](CONTRIBUTING.md)**: Guidelines for contributing code, testing, and opening PRs.
* 📄 **[License](LICENSE)**: MIT License terms.

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).
