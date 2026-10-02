"""Data models for Identity CLI."""

from dataclasses import dataclass
import json
from typing import Any, Dict, Optional


@dataclass(frozen=True)
class Identity:
    """Represents a generated synthetic identity with optionally selected fields."""

    name: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    phone: Optional[str] = None

    def to_dict(self, selected_fields: Optional[list[str]] = None) -> Dict[str, Any]:
        """Convert the identity to a dictionary.

        If selected_fields is provided, strictly only include those fields.
        Otherwise, only include non-None attributes.
        """
        if selected_fields is not None:
            data: Dict[str, Any] = {}
            for field in selected_fields:
                val = getattr(self, field, None)
                if val is not None:
                    data[field] = val
            return data

        data = {}
        if self.name is not None:
            data["name"] = self.name
        if self.email is not None:
            data["email"] = self.email
        if self.password is not None:
            data["password"] = self.password
        if self.phone is not None:
            data["phone"] = self.phone
        return data

    def to_json(self, indent: Optional[int] = 2, selected_fields: Optional[list[str]] = None) -> str:
        """Serialize the identity to a JSON formatted string."""
        return json.dumps(self.to_dict(selected_fields=selected_fields), indent=indent)
