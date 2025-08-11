"""
World-class tests for operational.expectation
"""
from domain_repository.operational.expectation import Expectation

def test_expectation_creation():
    e = Expectation(name="Test Expectation")
    assert e.name == "Test Expectation"
    assert hasattr(e, "id")
    assert e.metamodel_type == "Expectation"
