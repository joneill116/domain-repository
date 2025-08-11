"""
World-class tests for operational.workflow
"""
from domain_repository.operational.workflow import Workflow

def test_workflow_creation():
    w = Workflow(name="Test Workflow")
    assert w.name == "Test Workflow"
    assert hasattr(w, "id")
    assert w.metamodel_type == "Workflow"
