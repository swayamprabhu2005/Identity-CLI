# Identity CLI & Extension Usage Guide

Comprehensive documentation and usage examples for **Identity CLI** and the companion **VS Code Extension**.

---

## 📑 Table of Contents
* [Section 1: VS Code Extension Usage](#section-1-vs-code-extension-usage)
  * [Command Palette Shortcuts](#command-palette-shortcuts)
  * [Configuring Preferences in the UI](#configuring-preferences-in-the-ui)
  * [Integrated Terminal Workflow](#integrated-terminal-workflow)
* [Section 2: Standalone CLI Usage](#section-2-standalone-cli-usage)
  * [Command Overview](#command-overview)
  * [Generating Identities (`identity generate`)](#generating-identities-identity-generate)
  * [Single-Field Direct Flags](#single-field-direct-flags)
  * [Multi-Field Generation](#multi-field-generation)
  * [Exporting to Excel, JSON, and CSV](#exporting-to-excel-json-and-csv)
  * [Managing Configuration (`identity config`)](#managing-configuration-identity-config)
  * [Checking History & Uniqueness (`identity history`)](#checking-history--uniqueness-identity-history)
  * [Interactive Manual (`identity man`)](#interactive-manual-identity-man)
* [Practical Workflow Recipes](#practical-workflow-recipes)

---

# Section 1: VS Code Extension Usage

The **Identity Generator** extension integrates the CLI directly into the developer workflow inside Visual Studio Code.

### Command Palette Shortcuts

Press `Ctrl+Shift+P` (Windows/Linux) or `Cmd+Shift+P` (macOS) to access quick commands:

| Command | Title | Action |
| :--- | :--- | :--- |
| `identity.configure` | **Identity Generator: Configure Preferences** | Opens the visual setup wizard to customize export path, default fields, quantity, and format. |
| `identity.man` | **Identity Generator: Open Documentation (Manual)** | Opens a new integrated terminal and renders `identity man`. |
| `identity.openTerminal` | **Identity Generator: Open Terminal** | Opens a dedicated terminal ready with `identity --help`. |

---

### Configuring Preferences in the UI

1. Open the Command Palette and select **Identity Generator: Configure Preferences**.
2. Select your export destination with the interactive folder picker.
3. Check your desired default fields (`name`, `email`, `password`, `phone`).
4. Set default quantity and default output format.
5. Click **Save Preferences**.
6. All future terminal commands without explicit arguments will immediately respect these settings!

---

### Integrated Terminal Workflow

Once the extension is enabled, the `identity` binary is pre-configured in your VS Code terminals:

1. Open an integrated terminal (`Ctrl+\``).
2. Simply type `identity generate` and press Enter.
3. The generated identity appears in an attractive Rich terminal panel right inside VS Code.

---

# Section 2: Standalone CLI Usage

### Command Overview

| Command / Option | Description |
| :--- | :--- |
| `identity generate [options]` | Generate synthetic test identities. |
| `identity man` | Display the built-in Unix-style reference manual. |
| `identity config [options]` | View or update configuration preferences. |
| `identity history` | Display statistics of stored names, emails, passwords, and phones. |
| `identity --version` / `-v` | Display the application version (`Identity CLI v0.1.0`). |
| `identity --help` | Display universal command help and options. |

---

### Generating Identities (`identity generate`)

By default, running `identity generate` without flags generates **1 identity** containing **Name**, **Email**, and **Password**, rendered directly to the terminal:

```bash
identity generate
```

**Output:**
```text
┌─────────── GENERATED IDENTITY ────────────┐
│ Name     : Ethan Brooks                   │
│ Email    : ethan.brooks482@example.com    │
│ Password : V!7qL@92xK#p                   │
└───────────────────────────────────────────┘

✓ Identity generated successfully.
```

To generate multiple identities:
```bash
identity generate --count 5
# or using the short flag -c
identity generate -c 5
```

---

### Single-Field Direct Flags

When you only need a single specific field, you don't need to specify `--fields`. Simply pass the flag directly:

#### 1. Generate Name Only
```bash
identity generate --name
```
**Output:**
```text
┌─────────── GENERATED IDENTITY ────────────┐
│ Name     : Sarah Jenkins                  │
└───────────────────────────────────────────┘

✓ Identity generated successfully.
```

#### 2. Generate Email Only
```bash
identity generate --email
```
**Output:**
```text
┌─────────── GENERATED IDENTITY ────────────┐
│ Email    : sarah.jenkins821@example.org   │
└───────────────────────────────────────────┘

✓ Identity generated successfully.
```

#### 3. Generate Password Only
```bash
identity generate --password
```
**Output:**
```text
┌─────────── GENERATED IDENTITY ────────────┐
│ Password : 9m#K$zP8!wQ1                   │
└───────────────────────────────────────────┘

✓ Identity generated successfully.
```

#### 4. Generate Phone Number Only
```bash
identity generate --phone
# or short flag -p
identity generate -p
```
**Output:**
```text
┌─────────── GENERATED IDENTITY ────────────┐
│ Phone    : +1-555-0143                    │
└───────────────────────────────────────────┘

✓ Identity generated successfully.
```

---

### Multi-Field Generation

You can combine direct flags or use the `--fields` (`-f`) option:

#### Combining Direct Flags:
```bash
# Generate Name and Email only
identity generate --name --email

# Generate Name, Email, and Phone
identity generate --name --email --phone
```

#### Using `--fields`:
```bash
# Name and Email
identity generate --fields name,email

# Name, Email, and Password
identity generate --fields name,email,password

# All 4 fields
identity generate --fields name,email,password,phone
```

> [!NOTE]
> Field names are case-insensitive and support handy aliases like `fullname`, `pass`, and `phone-number`.

---

### Exporting to Excel, JSON, and CSV

Identity CLI supports direct format flags to export data instantly:

#### 1. Export to Excel (`--excel` / `-e`)
Generates a styled `.xlsx` file containing only the requested fields:
```bash
# Export 25 identities with default fields to Excel
identity generate --count 25 --excel

# Export 50 names and emails to Excel
identity generate --count 50 --fields name,email --excel
```

**Output:**
```text
✓ Generation completed

✓ Generated 50 identities
✓ Uniqueness verified
✓ Identity history updated
✓ Excel file created

Records: 50
Fields:
  Name
  Email

Format: Excel

Saved to:
./generated-names/identities.xlsx
```

#### 2. Export or Pipe JSON (`--json` / `-j`)
* Without `--location`: Outputs clean JSON directly to stdout (great for piping to `jq` or test scripts):
  ```bash
  identity generate --count 3 --name --email --json
  ```
  ```json
  [
    {
      "name": "David Martinez",
      "email": "david.martinez104@example.net"
    },
    {
      "name": "Elena Rostova",
      "email": "elena.rostova559@example.com"
    },
    {
      "name": "Marcus Vance",
      "email": "marcus.vance782@example.org"
    }
  ]
  ```
* With `--location`: Exports `identities.json` directly into the target folder:
  ```bash
  identity generate --count 50 --json --location ./test-data
  ```

#### 3. Export to CSV (`--csv`)
Generates an RFC-compliant `.csv` file:
```bash
identity generate --count 100 --fields name,email,phone --csv
```

#### 4. Custom Export Base Location (`--location` / `-l`)
Specify where the `generated-names/` folder should be placed:
```bash
identity generate --count 20 --excel --location "D:\MyProject\QA-Data"
```

Files are automatically numbered if they already exist (e.g., `identities_1.xlsx`, `identities_2.xlsx`) to prevent overwriting your existing data.

---

### Managing Configuration (`identity config`)

Preferences allow you to set your default quantity, default fields, and default locations so you don't have to retype them:

#### View Current Configuration:
```bash
identity config
# or
identity config --show
```

#### Update Preferences:
```bash
# Set persistent history directory (names.txt, emails.txt, etc.)
identity config --data-dir "D:\IdentityStorage"

# Set default location for file-based exports (Excel, JSON, CSV)
identity config --location "D:\Exports"

# Set default generation quantity
identity config --quantity 10

# Set default fields
identity config --fields name,email

# Set default format
identity config --format excel

# Set custom export folder name (default: generated-names)
identity config --folder-name custom-identities
```

---

### Checking History & Uniqueness (`identity history`)

Check how many unique records have been generated and are being guarded against repetition:

```bash
identity history
```

**Output:**
```text
Identity CLI History

Generated identities : 185
Stored names          : 185
Stored emails         : 185
Stored passwords      : 185
Stored phones         : 42

Data directory:
C:\Users\username\AppData\Local\IdentityCLI
```

---

### Interactive Manual (`identity man`)

Access the complete offline manual with all options, field aliases, precedence rules, and workflow recipes directly in your terminal:

```bash
identity man
```

---

# Practical Workflow Recipes

### Recipe 1: Quick Single Mock User for Registration Testing
```bash
identity generate
```

### Recipe 2: 100 Usernames & Emails for Load Testing (CSV)
```bash
identity generate --count 100 --fields name,email --csv --location ./load-tests
```

### Recipe 3: Generating a Fresh Excel Roster for QA Verification
```bash
identity generate --count 30 --fields name,email,password,phone --excel
```

### Recipe 4: Resetting Uniqueness History
If you want to allow previously generated names to appear again:
1. Run `identity history` to find your data directory path.
2. Delete the text files in that directory (`names.txt`, `emails.txt`, `passwords.txt`, `phones.txt`).
3. New generation runs will start fresh!
