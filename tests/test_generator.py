"""Tests for synthetic identity generator."""

import string
import pytest
from identity_cli.generator import (
    IdentityGenerator,
    SAFE_DOMAINS,
    GenerationError,
    MAX_BATCH_SIZE,
)
from identity_cli.models import Identity
from identity_cli.storage import HistoryData, StorageManager


def test_password_generation() -> None:
    gen = IdentityGenerator()
    pwd = gen.generate_password(length=14)

    assert len(pwd) == 14
    assert any(c.isupper() for c in pwd)
    assert any(c.islower() for c in pwd)
    assert any(c.isdigit() for c in pwd)
    assert any(c in "!@#$%^&*_-+" for c in pwd)


def test_name_generation_and_uniqueness() -> None:
    history = HistoryData()
    history.names.add("ethan brooks")

    gen = IdentityGenerator(history=history)
    # Generate 20 names and ensure none match Ethan Brooks
    names = [gen.generate_name() for _ in range(20)]
    for n in names:
        assert n.lower() != "ethan brooks"


def test_first_last_name_reuse_allowed() -> None:
    # Full name uniqueness allows sharing first or last name
    history = HistoryData()
    history.names.add("john carter")

    assert history.contains_name("John Carter")
    # "John Williams" and "Michael Carter" are allowed because combination is different
    assert not history.contains_name("John Williams")
    assert not history.contains_name("Michael Carter")


def test_email_generation_safe_domains() -> None:
    history = HistoryData()
    history.emails.add("ethan.brooks100@example.com")

    gen = IdentityGenerator(history=history)
    for _ in range(20):
        email = gen.generate_email("Ethan Brooks")
        domain = email.split("@")[1]
        assert domain in SAFE_DOMAINS
        assert email.lower() != "ethan.brooks100@example.com"


def test_phone_generation_reserved_range() -> None:
    history = HistoryData()
    gen = IdentityGenerator(history=history)

    phone = gen.generate_phone()
    # Should start with +1, contain 555-01, and match reserved range
    assert phone.startswith("+1 ")
    assert "-555-01" in phone


def test_batch_generation_uniqueness(storage: StorageManager) -> None:
    gen = IdentityGenerator(storage=storage)
    batch = gen.generate_batch(count=50, include_phone=True)

    assert len(batch) == 50

    names = [i.name.lower() for i in batch]
    emails = [i.email.lower() for i in batch]
    phones = [i.phone for i in batch if i.phone]

    # Mutual uniqueness in batch
    assert len(names) == len(set(names))
    assert len(emails) == len(set(emails))
    assert len(phones) == len(set(phones))


def test_batch_size_validation() -> None:
    gen = IdentityGenerator()
    with pytest.raises(ValueError, match="Count must be greater than 0"):
        gen.generate_batch(0)

    with pytest.raises(ValueError, match=f"Maximum batch size is {MAX_BATCH_SIZE:,}"):
        gen.generate_batch(MAX_BATCH_SIZE + 1)


def test_persistent_uniqueness_across_executions(storage: StorageManager) -> None:
    """Simulate execution 1, saving identities, then running execution 2 with fresh generator."""
    # Execution 1
    gen1 = IdentityGenerator(storage=storage)
    first_batch = gen1.generate_batch(count=10, include_phone=True)
    storage.append_batch(first_batch)

    first_names = {i.name.lower() for i in first_batch}
    first_emails = {i.email.lower() for i in first_batch}
    first_phones = {i.phone for i in first_batch if i.phone}

    # Execution 2 (fresh generator, fresh storage loader, same directory)
    fresh_storage = StorageManager(storage.base_dir)
    gen2 = IdentityGenerator(storage=fresh_storage)
    second_batch = gen2.generate_batch(count=15, include_phone=True)

    # Verify no collisions between execution 1 and execution 2
    for identity in second_batch:
        assert identity.name.lower() not in first_names
        assert identity.email.lower() not in first_emails
        if identity.phone:
            assert identity.phone not in first_phones
