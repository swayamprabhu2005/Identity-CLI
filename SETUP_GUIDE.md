# Identity CLI & Extension Setup Guide

Welcome to the **Identity CLI** setup guide. This guide explains how to install, configure, and verify both the **VS Code Extension** and the **Standalone CLI**.

---

## 📑 Table of Contents
* [Section 1: VS Code Extension Setup](#section-1-vs-code-extension-setup)
  * [Option A: Install from VS Code Marketplace](#option-a-install-from-vs-code-marketplace)
  * [Option B: Install from Local Package (.vsix)](#option-b-install-from-local-package-vsix)
  * [First-Time Configuration Wizard](#first-time-configuration-wizard)
  * [Terminal Integration & Verification](#terminal-integration--verification)
* [Section 2: Standalone CLI Setup](#section-2-standalone-cli-setup)
  * [Option A: Install via pipx (Recommended)](#option-a-install-via-pipx-recommended)
  * [Option B: Install via pip](#option-b-install-via-pip)
  * [Option C: Install for Local Development](#option-c-install-for-local-development)
  * [CLI Configuration & Verification](#cli-configuration--verification)
* [Storage & Path Configuration](#storage--path-configuration)

---

# Section 1: VS Code Extension Setup

The **Identity Generator** extension allows developers to generate synthetic test identities directly inside the VS Code integrated terminal, with a visual preferences wizard and zero setup friction.

### Option A: Install from VS Code Marketplace

1. Open **Visual Studio Code**.
2. Open the **Extensions view** (`Ctrl+Shift+X` on Windows/Linux or `Cmd+Shift+X` on macOS).
3. In the search box, type:
   ```text
   Identity Generator
   ```
4. Click **Install**.
5. Once installed, a notification will appear welcoming you to Identity Generator.

---

### Option B: Install from Local Package (.vsix)

If you have built the `.vsix` file locally or downloaded a release asset:

#### Via Command Line:
```bash
code --install-extension vscode-extension/identity-generator-0.1.0.vsix
```

#### Via VS Code UI:
1. Open **Visual Studio Code**.
2. Press `Ctrl+Shift+X` to open the Extensions sidebar.
3. Click the three dots (`...`) in the upper-right corner of the Extensions view.
4. Select **Install from VSIX...**.
5. Browse and select `identity-generator-0.1.0.vsix`.

---

### First-Time Configuration Wizard

Upon first launch after installation, the extension prompts you to configure your preferences:

1. Click **Configure Now** on the welcome notification, or open the Command Palette (`Ctrl+Shift+P` / `Cmd+Shift+P`) and run:
   ```text
   Identity Generator: Configure Preferences
   ```
2. In the graphical settings page:
   * **Default Export Location**: Choose where generated Excel, JSON, and CSV files should be saved (e.g. your workspace or a dedicated folder).
   * **Default Fields**: Check which fields you use most frequently (`Full Name`, `Email`, `Password`, `Phone Number`).
   * **Default Quantity**: Set how many identities should be generated when `--count` is not specified (default: `1`).
   * **Default Format**: Choose your preferred output format (`Terminal`, `Excel`, `JSON`, `CSV`).
   * **Output Folder Name**: Specify the subfolder name for exported files (default: `generated-names`).
3. Click **Save Preferences**. Your preferences are persisted and synchronized with the CLI.

---

### Terminal Integration & Verification

The extension automatically exposes the `identity` command in all VS Code integrated terminals without requiring manual PATH edits:

1. Open a new integrated terminal in VS Code (`Ctrl+\`` or `Terminal > New Terminal`).
2. Run the help command:
   ```bash
   identity --help
   ```
3. Test a quick generation:
   ```bash
   identity generate
   ```
4. Open the built-in manual:
   ```bash
   identity man
   ```

---

# Section 2: Standalone CLI Setup

If you prefer using the CLI in external terminals (Command Prompt, Windows PowerShell, PowerShell 7, macOS Terminal, Linux Bash/Zsh), you can install the CLI directly on your system.

### Option A: Install via pipx (Recommended)

[`pipx`](https://pypa.github.io/pipx/) installs Python CLI applications into isolated virtual environments while making their executables globally available on your system `PATH`.

```bash
# 1. Install pipx (if not already installed)
pip install pipx
pipx ensurepath

# 2. Install Identity CLI globally from GitHub
pipx install git+https://github.com/swayamprabhu2005/Identity-CLI.git
```

To update to the latest version in the future:
```bash
pipx upgrade identity-cli
```

---

### Option B: Install via pip

You can also install the package into your active Python environment using standard `pip`:

```bash
pip install git+https://github.com/swayamprabhu2005/Identity-CLI.git
```

---

### Option C: Install for Local Development

If you have cloned the source repository:

```bash
# Clone the repository
git clone https://github.com/swayamprabhu2005/Identity-CLI.git
cd Identity-CLI

# Install in editable mode
pip install -e .
```

---

### CLI Configuration & Verification

#### 1. Verify Installation
Check the installed version:
```bash
identity --version
```
Expected output:
```text
Identity CLI v0.1.0
```

#### 2. View Current Configuration
```bash
identity config --show
```

#### 3. Customize Persistent History Directory (`--data-dir`)
By default, persistent uniqueness history (`names.txt`, `emails.txt`, `passwords.txt`, `phones.txt`) is stored in your OS AppData/local share directory. You can set a custom directory:
```bash
# Windows example:
identity config --data-dir "D:\IdentityData"

# macOS / Linux example:
identity config --data-dir "$HOME/identity_data"
```

#### 4. Customize Default File Export Location (`--location`)
Set the default folder where file-based exports (Excel, JSON, CSV) will be created:
```bash
identity config --location "D:\MyProjects\TestExports"
```

---

## 🔒 Storage & Path Configuration: Important Distinction

To ensure maximum data safety, Identity CLI maintains a strict separation between two directories:

| Flag / Option | Purpose | What It Contains | Default Location |
| :--- | :--- | :--- | :--- |
| **`--data-dir`** | Persistent Uniqueness History | `names.txt`, `emails.txt`, `passwords.txt`, `phones.txt` | `%LOCALAPPDATA%\IdentityCLI` (Windows)<br>`~/.local/share/identity_cli` (Linux/Mac) |
| **`--location`** | Target for File Exports | `generated-names/` folder holding `.xlsx`, `.json`, `.csv` | Current working directory (`./`) or user-configured path |

> [!IMPORTANT]
> `--data-dir` and `--location` do not overlap.
> * `--data-dir` is configured using `identity config --data-dir <path>` and is never used as an export target.
> * `--location` can be passed per-command (`identity generate --excel --location ./test-data`) or set as default with `identity config --location <path>`.
