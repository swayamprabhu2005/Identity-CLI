# Identity Generator for VS Code

**A polished developer utility that enables you to generate unique, synthetic mock test identities directly from your VS Code integrated terminal.**

---

## 📑 Quick Navigation
* [⚡ Quick Start & Terminal Usage](#-the-integrated-terminal-experience)
* [⚙️ Configuration & Preferences](#-configuration--preferences)
* [✨ Features](#-features)
* [🚀 Command Examples](#-quick-usage-examples)
* [🔒 Storage Separation & Data Directory](#-storage-separation--data-directory)
* [📖 Built-in Manual (`identity man`)](#-built-in-manual)
* [📄 License](#-license)

---

## ⚡ The Integrated Terminal Experience

Once installed, Identity Generator prompts you with a quick setup screen to configure your preferred defaults. Afterward, you simply work directly from the **VS Code integrated terminal**:

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

No Command Palette browsing every time you need mock data. Just open your terminal (`Ctrl+\``) and generate!

---

## ⚙️ Configuration & Preferences

You can access and update your preferences anytime in two convenient ways:

### Method 1: The Visual Setup Wizard
1. Open the Command Palette (`Ctrl+Shift+P` on Windows/Linux or `Cmd+Shift+P` on macOS).
2. Type and select **`Identity Generator: Configure Preferences`**.
3. Use the interactive folder pickers and checkboxes, then click **Save Preferences**.

### Method 2: Standard VS Code Settings
Press `Ctrl+,` (or `Cmd+,` on macOS), search for **`Identity Generator`**, and adjust your preferences:
* **Default Export Location**: Target folder where exported files are saved.
* **Data Directory**: Dedicated storage folder for persistent uniqueness history (`names.txt`, `emails.txt`, etc.).
* **Default Fields**: Check/uncheck Full Name, Email, Password, or Phone.
* **Default Quantity**: Default number of identities to generate.
* **Default Format**: `terminal`, `excel`, `json`, or `csv`.
* **Folder Name**: Automatic subfolder name (default: `generated-names`).

---

## ✨ Features

- 🛠️ **Terminal-First Workflow**: Run `identity generate` natively in any integrated terminal inside VS Code.
- 🎯 **Direct Single-Field Flags**: Generate single fields with zero boilerplate (e.g. `identity generate --name` or `identity generate --email`).
- 📊 **Instant File Exports**: Direct flags for **Excel (`--excel`)**, **JSON (`--json`)**, and **CSV (`--csv`)**.
- 🔒 **Persistent Local Uniqueness**: Names and emails already generated are remembered locally so you never get duplicates, even across different sessions.
- ⚙️ **One-Time Graphical Wizard**: Configure paths and fields visually without manually editing JSON files.
- 📦 **Zero-Setup Python Runtime**: Comes with self-contained logic and automated dependency resolution—works out of the box on any system with Python installed.
- 📖 **Built-in Manual**: Instant Unix-style reference documentation right in your terminal with `identity man`.

---

## 🚀 Quick Usage Examples

Inside any VS Code integrated terminal:

```bash
# Generate 1 identity to terminal (default: name, email, password)
identity generate

# Generate single fields directly
identity generate --name
identity generate --email
identity generate --password
identity generate --phone

# Generate multiple identities
identity generate --count 5

# Export directly to Excel (.xlsx)
identity generate --excel

# Export 25 names and emails to Excel
identity generate --count 25 --fields name,email --excel

# Output raw JSON to terminal / stdout
identity generate --count 3 --json

# Export to CSV in a custom target folder
identity generate --count 50 --csv --location ./test-data

# Open comprehensive built-in reference manual
identity man
```

---

## 🔒 Storage Separation & Data Directory

Identity Generator cleanly separates your **exports** from your **history**:

| Setting | Purpose | Configuration Flag |
| :--- | :--- | :--- |
| **Default Export Location** | Where generated Excel, JSON, and CSV files are saved | `identity generate --location <path>` |
| **Data Directory** | Where persistent uniqueness history (`names.txt`, `emails.txt`, etc.) is kept | `identity config --data-dir <path>` |

* Neither setting overwrites or interferes with the other.
* If you ever want to reset your uniqueness history to allow old names to appear again, simply clear the text files in your Data Directory.

---

## 📖 Built-in Manual

Whenever you need a refresher on options, precedence rules, or field aliases, simply run:

```bash
identity man
```

---

## 📄 License

This extension is licensed under the [MIT License](LICENSE).
