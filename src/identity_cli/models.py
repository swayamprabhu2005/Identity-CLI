"""Data models for Identity CLI."""

from dataclasses import dataclass
import json
from typing import Any, Dict, Optional


@dataclass(frozen=True)
class Identity:
    """Represents a generated synthetic identity."""

    name: str
    email: str
    password: str
    phone: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert the identity to a dictionary.

        Excludes phone if not set, maintaining clean JSON output.
        """
        data: Dict[str, Any] = {
            "name": self.name,
            "email": self.email,
            "password": self.password,
        }
        if self.phone is not None:
            data["phone"] = self.phone
        return data

    def to_json(self, indent: Optional[int] = 2) -> str:
        """Serialize the identity to a JSON formatted string."""
        return json.dumps(self.to_dict(), indent=indent)
