# Contributing to Identity CLI

Thank you for your interest in contributing to **Identity CLI**! We welcome contributions, bug reports, feature suggestions, and documentation improvements.

---

## 📋 Code of Conduct

We are committed to providing a welcoming, inclusive, and harassment-free environment for everyone. Please be respectful and constructive in all communications.

---

## 🛠️ Setting Up Your Development Environment

### Prerequisites
* **Python**: Version 3.10 or higher
* **Node.js**: Version 18.0.0 or higher (for the VS Code extension)
* **Git**: Installed and configured on your system

### 1. Clone the Repository
```bash
git clone https://github.com/swayamprabhu2005/Identity-CLI.git
cd Identity-CLI
```

### 2. Set Up Python Virtual Environment
```bash
# Create a virtual environment
python -m venv .venv

# Activate the virtual environment
# Windows (PowerShell):
.venv\Scripts\Activate.ps1
# Windows (Command Prompt):
.venv\Scripts\activate.bat
# Linux / macOS:
source .venv/bin/activate

# Install the package in editable mode with development dependencies
pip install -e ".[dev]"
```

### 3. Set Up VS Code Extension (Optional)
If you are developing or testing the VS Code extension:
```bash
cd vscode-extension
npm install
npm run compile
cd ..
```

---

## 🧪 Running Tests

We maintain comprehensive automated tests covering the CLI, generator, models, storage, and exports.

Run the test suite using pytest:
```bash
# Set PYTHONPATH to src and run tests
# Windows (PowerShell):
$env:PYTHONPATH="src"; pytest -v

# Linux / macOS / Bash:
PYTHONPATH=src pytest -v
```

All 43 tests must pass before opening a Pull Request.

---

## 🌿 Development Guidelines

1. **Synthetic Data Only**: All generated test data must remain synthetic and test-safe.
   * Domains must use RFC-reserved test domains (`example.com`, `example.org`, `example.net`).
   * Phone numbers must use fictional test ranges (`555-0100` through `555-0199`).
   * Passwords must use cryptographically secure generation (`secrets` module).
2. **Offline First**: Never add external network calls or remote telemetry. The tool must run 100% locally and offline.
3. **Strict Separation of Storage**:
   * `--data-dir` is strictly for persistent history text files (`names.txt`, `emails.txt`, `passwords.txt`, `phones.txt`).
   * `--location` is strictly for file-based exports (`.xlsx`, `.json`, `.csv` inside `generated-names/`).
4. **Code Quality**: Follow PEP 8 guidelines and include type annotations.

---

## 🚀 Submitting a Pull Request (PR)

1. Create a descriptive feature branch from `main`:
   ```bash
   git checkout -b feature/my-new-feature
   ```
2. Make your changes and write automated tests for any new functionality.
3. Run the full test suite and verify that all tests pass.
4. Commit your changes with clear, descriptive commit messages:
   ```bash
   git commit -m "feat: add support for custom phone prefixes"
   ```
5. Push to your fork and submit a Pull Request to the `main` branch.
6. Provide a concise summary of the changes and link any related issues.

---

## 💬 Questions & Support

If you have questions or run into issues:
* Open an issue on GitHub: [Issues](https://github.com/swayamprabhu2005/Identity-CLI/issues)
* Review our [Usage Guide](USAGE_GUIDE.md) and [Setup Guide](SETUP_GUIDE.md).
