"""Tests for persistent storage manager."""

from pathlib import Path
from identity_cli.models import Identity
from identity_cli.storage import HistoryData, StorageManager


def test_storage_initialization_and_empty(storage: StorageManager) -> None:
    history = storage.load_history()
    assert isinstance(history, HistoryData)
    assert len(history.names) == 0
    assert len(history.emails) == 0
    assert len(history.phones) == 0

    stats = storage.get_stats()
    assert stats["stored_names"] == 0
    assert stats["stored_emails"] == 0
    assert stats["stored_passwords"] == 0
    assert stats["stored_phones"] == 0
    assert stats["total_identities"] == 0


def test_append_batch_and_persistence(storage: StorageManager) -> None:
    identities = [
        Identity(
            name="Ethan Brooks",
            email="ethan.brooks482@example.com",
            password="V!7qL@92xK#p",
            phone=None,
        ),
        Identity(
            name="Maya Richardson",
            email="maya.richardson731@example.com",
            password="pQ8!xR2#Lm91",
            phone="+1 202-555-0103",
        ),
    ]

    storage.append_batch(identities)

    # Check files exist
    assert storage.names_file.exists()
    assert storage.emails_file.exists()
    assert storage.passwords_file.exists()
    assert storage.phones_file.exists()

    # Verify line counts and content
    stats = storage.get_stats()
    assert stats["stored_names"] == 2
    assert stats["stored_emails"] == 2
    assert stats["stored_passwords"] == 2
    assert stats["stored_phones"] == 1  # Only 1 had phone
    assert stats["total_identities"] == 2

    # Verify history loading in a fresh StorageManager instance
    fresh_storage = StorageManager(storage.base_dir)
    loaded_history = fresh_storage.load_history()

    # Case-insensitive checks
    assert loaded_history.contains_name("Ethan Brooks")
    assert loaded_history.contains_name("ethan brooks")
    assert loaded_history.contains_name("MAYA RICHARDSON")
    assert not loaded_history.contains_name("Sarah Mitchell")

    assert loaded_history.contains_email("ethan.brooks482@example.com")
    assert loaded_history.contains_email("ETHAN.BROOKS482@EXAMPLE.COM")
    assert not loaded_history.contains_email("other@example.com")

    assert loaded_history.contains_phone("+1 202-555-0103")
    assert not loaded_history.contains_phone("+1 202-555-0199")


def test_append_empty_batch(storage: StorageManager) -> None:
    storage.append_batch([])
    stats = storage.get_stats()
    assert stats["stored_names"] == 0
