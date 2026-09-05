# Identity CLI

<div align="center">

[![Python: 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg?style=for-the-badge&logo=python&logoColor=white)](pyproject.toml)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg?style=for-the-badge)](LICENSE)
[![CLI: Typer](https://img.shields.io/badge/CLI-Typer-red.svg?style=for-the-badge)](https://typer.tiangolo.com)
[![Platform: Cross-Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg?style=for-the-badge)](#requirements)

**A fast, lightweight, and elegant CLI utility for generating synthetic/mock test identities with persistent local uniqueness guarantees.**

[Installation](#installation) • [Quick Start](#quick-start) • [Command Reference](#command-reference) • [Excel Export](#excel-export) • [Custom Storage](#custom-storage-location)

</div>

---

> [!NOTE]
> ### 🛡️ Synthetic & Test Data Guarantee
> All data produced by Identity CLI is purely synthetic for development, QA testing, and software demonstrations:
> * **Names**: Realistically synthesized by combining first and last names with persistent uniqueness checks to ensure no real person's identity is targeted.
> * **Emails**: Exclusively use official RFC-reserved test domains (`example.com`, `example.org`, `example.net`).
> * **Phone Numbers**: Exclusively use North American reserved fictional test ranges (`555-0100` through `555-0199`).
> * **Local First**: Runs 100% offline on your machine. Zero tracking, zero telemetry, and zero network calls.

---

## ✨ Features

* 🔁 **Persistent Uniqueness Across Runs**: Identities already generated are saved locally so you never get duplicates, even across separate days or terminal sessions.
* 👤 **Realistic Combinations**: Full names (`FirstName LastName`) are strictly unique while naturally allowing first or last names to be reused across different pairings.
* 🔐 **Cryptographically Secure Passwords**: Generates robust random passwords using Python's standard `secrets` engine.
* 📞 **Optional Reserved Phone Numbers**: Generate valid synthetic phone numbers on demand using `--phone`.
* 📊 **Excel (.xlsx) Export**: Export large mock batches into clean spreadsheets with frozen headers, automatic column widths, and collision-proof timestamps.
* ⚡ **Batch Generation**: Generate up to 10,000 unique identities in a single command (`--count 50`).
* 📦 **Clean JSON Output**: Pure JSON formatting (`--json`) ready for API testing and piping into tools like `jq`.
* 📁 **Configurable Storage**: Effortlessly store your history and exports on any drive (e.g. `D:\IdentityData`).

---

## 🚀 Installation

Install globally using **pipx** (recommended for all Python CLI tools):

```bash
pipx install git+https://github.com/swayamprabhu2005/Identity-CLI.git
```

*Or install directly with standard pip:*
```bash
pip install git+https://github.com/swayamprabhu2005/Identity-CLI.git
```

Once installed, the `identity` command is immediately available everywhere across PowerShell, Command Prompt, macOS Terminal, and Linux shells.

---

## ⚡ Quick Start

### 1. Generate a Single Identity

```bash
identity generate
```

```text
┌─────────── GENERATED IDENTITY ────────────┐
│ Name     : Ethan Brooks                   │
│ Email    : ethan.brooks482@example.com    │
│ Password : V!7qL@92xK#p                   │
└───────────────────────────────────────────┘

✓ Identity generated successfully.
```

---

### 2. Include a Test Phone Number

```bash
identity generate --phone
```

```text
┌─────────── GENERATED IDENTITY ────────────┐
│ Name     : Maya Richardson                │
│ Email    : maya.richardson731@example.com │
│ Password : pQ8!xR2#Lm91                   │
│ Phone    : +1 202-555-0103               │
└───────────────────────────────────────────┘

✓ Identity generated successfully.
```

---

### 3. Generate Multiple Identities

```bash
identity generate --count 5
```

```text
Generating 5 identities...

✓ Generated 5 identities
✓ Uniqueness verified
✓ Identity history updated
```

---

## 📖 Command Reference

### `identity generate`

| Option | Flag | Description | Default |
|---|---|---|---|
| `--count` | `-c` | Number of identities to generate (1 to 10,000) | `1` |
| `--phone` | `-p` | Include reserved test phone number | `False` |
| `--excel` | `-e` | Export batch to an `.xlsx` spreadsheet | `False` |
| `--json` | `-j` | Output in clean JSON format (single object or array) | `False` |
| `--quiet` | `-q` | Suppress decorative banners (useful for scripts) | `False` |

---

### Other CLI Commands

| Command | Description |
|---|---|
| `identity config` | View current persistent storage location and history counts (or set `--data-dir <path>`). |
| `identity history` | Display statistics and counts for stored synthetic identities. |
| `identity version` | Display the installed version of Identity CLI. |

---

## 📊 Excel Export

Generate identities and automatically package them into an Excel `.xlsx` spreadsheet:

```bash
identity generate --count 25 --phone --excel
```

```text
Generating 25 identities...

✓ Generated 25 identities
✓ Uniqueness verified
✓ Identity history updated
✓ Excel file created

File:
<storage-directory>/exports/identity_YYYY-MM-DD_HHMMSS.xlsx
```

**Spreadsheet Features:**
* Header row is frozen (`A2`) for easy scrolling.
* Column widths automatically fit the longest values.
* Includes columns: `ID`, `Name`, `Email`, `Password`, `Phone`.
* Timestamps prevent overwriting previously exported spreadsheets.

---

## 💻 JSON Output

Pipe clean JSON directly into files, scripts, or API requests:

```bash
identity generate --count 2 --phone --json
```

```json
[
  {
    "name": "Ronald Nicholson",
    "email": "ronald.nicholson6583@example.com",
    "password": "sVb9H1P%ewIq",
    "phone": "+1 919-555-0128"
  },
  {
    "name": "Robert Terry",
    "email": "robert.terry4990@example.com",
    "password": "7yh$vu-C*s@0",
    "phone": "+1 702-555-0137"
  }
]
```

---

## 💾 Custom Storage Location

By default, persistent data is stored in your user application directory (`%LOCALAPPDATA%\IdentityCLI` on Windows, or `~/.local/share/identity_cli` on Linux/macOS).

To move your storage and Excel exports to any custom folder, drive, or path (e.g. `D:\IdentityData`, `E:\TestStorage`, or `/custom/path`), simply run:

```bash
identity config --data-dir <path-to-directory>
```

* The CLI permanently remembers this setting across all terminals and system reboots.
* All generated history (`names.txt`, `emails.txt`, `passwords.txt`, `phones.txt`) and Excel spreadsheets will automatically reside in your chosen directory.

---

## 🧪 Testing

Run the automated test suite with `pytest`:

```bash
pytest -v
```

All 30 tests run in isolated temporary environments and verify name uniqueness, cross-execution collision rejection, and Excel formatting.

---

## 📄 License

This project is licensed under the terms of the [MIT License](LICENSE).
