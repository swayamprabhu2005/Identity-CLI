"""Synthetic identity generator with persistent uniqueness guarantees."""

import re
import secrets
import string
from typing import List, Optional

from faker import Faker

from identity_cli.models import Identity
from identity_cli.storage import HistoryData, StorageManager

# Reserved test domains for synthetic data (RFC 2606 / RFC 6761)
SAFE_DOMAINS = ["example.com", "example.org", "example.net"]

# Reserved fictional/test area codes and exchanges (555-0100 through 555-0199)
RESERVED_AREA_CODES = [
    "202", "212", "312", "415", "503", "617", "702", "818", "917", "206",
    "303", "404", "512", "602", "713", "801", "858", "901", "919", "972"
]

SPECIAL_CHARACTERS = "!@#$%^&*_-+"
MAX_BATCH_SIZE = 10000
MAX_ATTEMPTS = 500


class GenerationError(Exception):
    """Raised when unique synthetic identity cannot be generated."""
    pass


class IdentityGenerator:
    """Generates synthetic identities ensuring persistent and batch uniqueness."""

    def __init__(
        self,
        storage: Optional[StorageManager] = None,
        history: Optional[HistoryData] = None,
        locale: str = "en_US"
    ):
        self.storage = storage
        self.faker = Faker(locale)
        self._sys_random = secrets.SystemRandom()

        if history is not None:
            self.history = history
        elif self.storage is not None:
            self.history = self.storage.load_history()
        else:
            self.history = HistoryData()

    def generate_password(self, length: int = 12) -> str:
        """Generate a strong random password using Python's secrets module."""
        if length < 8:
            length = 12

        # Ensure at least one from each category
        password_chars = [
            secrets.choice(string.ascii_lowercase),
            secrets.choice(string.ascii_uppercase),
            secrets.choice(string.digits),
            secrets.choice(SPECIAL_CHARACTERS),
        ]

        all_chars = string.ascii_letters + string.digits + SPECIAL_CHARACTERS
        for _ in range(length - 4):
            password_chars.append(secrets.choice(all_chars))

        # Secure shuffle
        self._sys_random.shuffle(password_chars)
        return "".join(password_chars)

    def generate_name(self) -> str:
        """Generate a unique full name not present in history."""
        for _ in range(MAX_ATTEMPTS):
            first = self.faker.first_name()
            last = self.faker.last_name()
            candidate = f"{first} {last}"
            if not self.history.contains_name(candidate):
                return candidate

        raise GenerationError(
            f"Unable to find a unique name after {MAX_ATTEMPTS} attempts."
        )

    def generate_email(self, name: str) -> str:
        """Generate a unique synthetic email using safe example domains."""
        # Sanitize name for email local-part
        parts = re.split(r"\s+", name.strip().lower())
        if len(parts) >= 2:
            clean_first = re.sub(r"[^a-z0-9]", "", parts[0])
            clean_last = re.sub(r"[^a-z0-9]", "", parts[-1])
            base_local = f"{clean_first}.{clean_last}"
        else:
            base_local = re.sub(r"[^a-z0-9]", "", name.strip().lower()) or "user"

        for _ in range(MAX_ATTEMPTS):
            domain = secrets.choice(SAFE_DOMAINS)
            # Add random numeric suffix e.g. 100-9999 for high entropy realism
            suffix = secrets.randbelow(9900) + 100
            candidate = f"{base_local}{suffix}@{domain}"
            if not self.history.contains_email(candidate):
                return candidate

        raise GenerationError(
            f"Unable to find a unique email after {MAX_ATTEMPTS} attempts."
        )

    def generate_phone(self) -> str:
        """Generate a unique phone number in the reserved 555-0100..0199 test range."""
        for _ in range(MAX_ATTEMPTS):
            area = secrets.choice(RESERVED_AREA_CODES)
            # 555-0100 through 555-0199 are reserved test numbers in NANP
            subscriber = secrets.randbelow(100)
            candidate = f"+1 {area}-555-01{subscriber:02d}"
            if not self.history.contains_phone(candidate):
                return candidate

        raise GenerationError(
            f"Unable to find a unique phone after {MAX_ATTEMPTS} attempts."
        )

    def generate_identity(self, include_phone: bool = False) -> Identity:
        """Generate a single unique identity and register it in working history."""
        name = self.generate_name()
        email = self.generate_email(name)
        password = self.generate_password()
        phone = self.generate_phone() if include_phone else None

        identity = Identity(
            name=name,
            email=email,
            password=password,
            phone=phone,
        )
        self.history.add(identity)
        return identity

    def generate_batch(self, count: int, include_phone: bool = False) -> List[Identity]:
        """Generate a batch of unique identities.

        Validates count and guarantees uniqueness across persistent history
        and within the generated batch.
        """
        if count < 1:
            raise ValueError("Count must be greater than 0.")
        if count > MAX_BATCH_SIZE:
            raise ValueError(f"Maximum batch size is {MAX_BATCH_SIZE:,}.")

        batch: List[Identity] = []
        for _ in range(count):
            identity = self.generate_identity(include_phone=include_phone)
            batch.append(identity)

        return batch
