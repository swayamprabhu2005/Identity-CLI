# Identity Generator for VS Code

**A polished developer utility that enables you to generate unique, synthetic mock test identities directly from your VS Code integrated terminal.**

---

## ⚡ The Integrated Terminal Experience

Once installed, Identity Generator gives you a first-time configuration screen to set your preferences. Afterward, you simply work from the **VS Code integrated terminal**:

```bash
identity generate
```

No Command Palette browsing every time you need mock data. Just type and generate!

---

## ✨ Features

- 🛠️ **Terminal-First Workflow**: Run `identity generate` directly inside any integrated terminal in VS Code.
- ⚙️ **One-Time Configuration**: Set your preferred export location, default fields, quantity, and formats once.
- 🎯 **Flexible Fields**: Generate only the fields you need (`--fields name`, `--fields email,password`, etc.).
- 📊 **Multiple Output Formats**: Display immediately in the terminal, or export to clean **Excel (.xlsx)**, **JSON**, or **CSV** spreadsheets.
- 📁 **Organized File Generation**: Automatically creates a `generated-names/` folder in your project or storage location.
- 📖 **Built-in Manual**: Instant reference documentation available anytime with `identity man`.
- 🔁 **Guaranteed Local Uniqueness**: Never get duplicate identities across sessions.

---

## 🚀 Quick Usage Examples

Inside your VS Code terminal:

```bash
# Generate 1 identity to terminal (default)
identity generate

# Generate 5 identities
identity generate --count 5

# Generate only names
identity generate --fields name

# Generate names and emails
identity generate --fields name,email

# Export to JSON
identity generate --format json

# Export to Excel
identity generate --format excel

# Target current project directory
identity generate --location .

# Full combined command
identity generate --count 100 --fields name,email --format excel --location ./test-data

# Open full CLI manual
identity man
```

---

## ⚙️ Configuration & Preferences

To reopen preferences anytime:
1. Open the Command Palette (`Ctrl+Shift+P` / `Cmd+Shift+P`).
2. Type and select **`Identity Generator: Configure Preferences`**.

### Configurable Settings:
- **Default Location**: Directory where exported files are saved (e.g. `D:\IdentityData`).
- **Default Fields**: Full Name, Email Address, Secure Password, Reserved Phone.
- **Default Quantity**: Initial count (defaults to `1`).
- **Default Format**: `terminal`, `excel`, `json`, or `csv`.
- **Folder Name**: Automatic subfolder name (defaults to `generated-names`).

---

## 📄 License

This extension is licensed under the [MIT License](LICENSE).
