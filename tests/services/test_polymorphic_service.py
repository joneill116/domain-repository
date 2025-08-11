"""
World-class tests for services.polymorphic_service
"""
import pytest
from domain_repository.services.polymorphic_service import PolymorphicService
from domain_repository.operational.component import Component
from domain_repository.operational.workflow import Workflow
from domain_repository.operational.protocol import Protocol
from domain_repository.operational.expectation import Expectation

def test_polymorphic_service_create_and_link():
    service = PolymorphicService()
    w = service.create_workflow(name="W")
    c = service.create_component(name="C")
    p = service.create_protocol(name="P")
    e = service.create_expectation(name="E")
    # Link via relationships
    rel1 = service.create_relationship(source_id=w.id, target_id=c.id, relationship_type="contains")
    rel2 = service.create_relationship(source_id=c.id, target_id=p.id, relationship_type="implements")
    rel3 = service.create_relationship(source_id=c.id, target_id=e.id, relationship_type="fulfills")
    assert rel1.source_id == w.id and rel1.target_id == c.id
    assert rel2.source_id == c.id and rel2.target_id == p.id
    assert rel3.source_id == c.id and rel3.target_id == e.id
    # Export JSON-LD
    graph = service.export_complete_jsonld_graph()
    assert isinstance(graph, dict)
