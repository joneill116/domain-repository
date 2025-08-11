"""
World-class tests for operational.protocol
"""
from domain_repository.operational.protocol import Protocol

def test_protocol_creation():
    p = Protocol(name="Test Protocol")
    assert p.name == "Test Protocol"
    assert hasattr(p, "id")
    assert p.metamodel_type == "Protocol"
