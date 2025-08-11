"""
World-class tests for operational.component
"""
from domain_repository.operational.component import Component

def test_component_creation():
    c = Component(name="Test Component")
    assert c.name == "Test Component"
    assert hasattr(c, "id")
    assert c.metamodel_type == "Component"
