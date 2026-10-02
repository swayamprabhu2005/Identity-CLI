"""Persistent plain-text storage for Identity CLI."""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Set

from identity_cli.models import Identity


@dataclass
class HistoryData:
    """Holds in-memory sets of historical values for quick uniqueness checks."""

    names: Set[str] = field(default_factory=set)
    emails: Set[str] = field(default_factory=set)
    phones: Set[str] = field(default_factory=set)

    def contains_name(self, name: str) -> bool:
        """Check if a full name exists (case-insensitive)."""
        return name.strip().lower() in self.names

    def contains_email(self, email: str) -> bool:
        """Check if an email exists (case-insensitive)."""
        return email.strip().lower() in self.emails

    def contains_phone(self, phone: str) -> bool:
        """Check if a phone number exists."""
        return phone.strip() in self.phones

    def add(self, identity: Identity) -> None:
        """Add an identity's attributes to history sets."""
        if identity.name:
            self.names.add(identity.name.strip().lower())
        if identity.email:
            self.emails.add(identity.email.strip().lower())
        if identity.phone:
            self.phones.add(identity.phone.strip())


class StorageManager:
    """Manages reading, writing, and statistics for persistent identity files."""

    def __init__(self, base_dir: Path):
        self.base_dir = Path(base_dir)
        self.data_dir = self.base_dir / "data"
        self.exports_dir = self.base_dir / "exports"

        self.names_file = self.data_dir / "names.txt"
        self.emails_file = self.data_dir / "emails.txt"
        self.passwords_file = self.data_dir / "passwords.txt"
        self.phones_file = self.data_dir / "phones.txt"

    def ensure_directories(self) -> None:
        """Ensure data and exports directories exist."""
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.exports_dir.mkdir(parents=True, exist_ok=True)

    def _read_lines(self, file_path: Path) -> List[str]:
        """Read non-empty stripped lines from a UTF-8 text file."""
        if not file_path.exists():
            return []
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return [line.strip() for line in f if line.strip()]
        except OSError:
            return []

    def load_history(self) -> HistoryData:
        """Load persistent history into memory for uniqueness checks."""
        self.ensure_directories()
        names = {name.lower() for name in self._read_lines(self.names_file)}
        emails = {email.lower() for email in self._read_lines(self.emails_file)}
        phones = set(self._read_lines(self.phones_file))
        return HistoryData(names=names, emails=emails, phones=phones)

    def append_batch(self, identities: List[Identity]) -> None:
        """Atomically append a batch of identities to persistent TXT files."""
        if not identities:
            return

        self.ensure_directories()

        names_to_write = [i.name.strip() for i in identities if i.name]
        emails_to_write = [i.email.strip() for i in identities if i.email]
        passwords_to_write = [i.password.strip() for i in identities if i.password]
        phones_to_write = [i.phone.strip() for i in identities if i.phone]

        # Prepare string payloads
        names_content = ("\n".join(names_to_write) + "\n") if names_to_write else ""
        emails_content = ("\n".join(emails_to_write) + "\n") if emails_to_write else ""
        passwords_content = ("\n".join(passwords_to_write) + "\n") if passwords_to_write else ""
        phones_content = ("\n".join(phones_to_write) + "\n") if phones_to_write else ""

        # Write sequentially to persistent files
        if names_content:
            with open(self.names_file, "a", encoding="utf-8") as f:
                f.write(names_content)

        if emails_content:
            with open(self.emails_file, "a", encoding="utf-8") as f:
                f.write(emails_content)

        if passwords_content:
            with open(self.passwords_file, "a", encoding="utf-8") as f:
                f.write(passwords_content)

        if phones_content:
            with open(self.phones_file, "a", encoding="utf-8") as f:
                f.write(phones_content)

    def get_stats(self) -> Dict[str, int]:
        """Return counts of stored names, emails, passwords, and phones."""
        names_count = len(self._read_lines(self.names_file))
        emails_count = len(self._read_lines(self.emails_file))
        passwords_count = len(self._read_lines(self.passwords_file))
        phones_count = len(self._read_lines(self.phones_file))

        return {
            "stored_names": names_count,
            "stored_emails": emails_count,
            "stored_passwords": passwords_count,
            "stored_phones": phones_count,
            "total_identities": max(names_count, emails_count, passwords_count, phones_count),
        }
