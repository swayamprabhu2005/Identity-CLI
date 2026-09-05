# Contributing to Identity CLI

Thank you for your interest in contributing to **Identity CLI**!

## Development Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/identity-cli.git
   cd identity-cli
   ```

2. **Create and activate a virtual environment**:
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

3. **Install the package in editable mode with development dependencies**:
   ```powershell
   pip install -e ".[dev]"
   ```

4. **Run the test suite**:
   ```powershell
   pytest
   ```

## Code Guidelines

- Adhere to PEP 8 standards and maintain clean type annotations.
- Keep the application simple, focused, and free of unnecessary dependencies.
- Ensure all persistent uniqueness guarantees remain intact across all test cases.
- Add tests for any new options, subcommands, or modifications.
- Ensure all generated data remains purely synthetic and local to the user's machine.
