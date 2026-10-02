"""Excel export functionality for Identity CLI using openpyxl."""

from pathlib import Path
from typing import List, Optional

from identity_cli.exports import export_to_excel, get_safe_export_path
from identity_cli.models import Identity


def get_unique_export_path(exports_dir: Path) -> Path:
    """Generate a collision-safe filename for the Excel export.

    Maintains backward compatibility with older tests while using clean identities.xlsx naming.
    """
    return get_safe_export_path(exports_dir, base_name="identities", ext="xlsx")


__all__ = ["export_to_excel", "get_unique_export_path"]

