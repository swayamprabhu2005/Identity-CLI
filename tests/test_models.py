"""Tests for data models."""

import json
from identity_cli.models import Identity


def test_identity_without_phone() -> None:
    identity = Identity(
        name="Ethan Brooks",
        email="ethan.brooks482@example.com",
        password="V!7qL@92xK#p",
    )
    d = identity.to_dict()
    assert d == {
        "name": "Ethan Brooks",
        "email": "ethan.brooks482@example.com",
        "password": "V!7qL@92xK#p",
    }
    assert "phone" not in d

    parsed = json.loads(identity.to_json())
    assert parsed["name"] == "Ethan Brooks"
    assert "phone" not in parsed


def test_identity_with_phone() -> None:
    identity = Identity(
        name="Maya Richardson",
        email="maya.richardson731@example.com",
        password="pQ8!xR2#Lm91",
        phone="+1 202-555-0103",
    )
    d = identity.to_dict()
    assert d["phone"] == "+1 202-555-0103"

    parsed = json.loads(identity.to_json())
    assert parsed["phone"] == "+1 202-555-0103"
