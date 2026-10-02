# Change Log

All notable changes to the "Identity Generator" extension will be documented in this file.

## [0.1.1] - 2026-10-02

### Added
- Self-contained bundling of `identity_cli` Python modules directly inside the extension.
- Automatic dependency verification and resolution (`faker`, `openpyxl`, `rich`, `typer`) for clean zero-setup installations.
- Terminal launchers automatically detect bundled internal Python modules without requiring manual `pip install`.

## [0.1.0] - 2026-10-02

### Added
- First-time setup wizard for configuring default location, default fields, quantity, and format.
- Integrated terminal support via dynamic environment PATH injection.
- Commands: `Identity Generator: Configure Preferences`, `Identity Generator: Open Documentation (Manual)`, and `Identity Generator: Open Integrated Terminal`.
- Full synchronization with shared local CLI `config.json`.
- Direct support for `identity generate` and `identity man` in VS Code terminals.
