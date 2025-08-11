"""
World-class tests for core.base
"""
import pytest
from domain_repository.core.base import BaseMetamodel, MetamodelType
from uuid import UUID

def test_basemetamodel_fields():
    m = BaseMetamodel(
        id=UUID(int=0),
        name="Test",
        description="desc",
        semantic_tags=["tag1"],
        ontology_mappings={"skos:exactMatch": "uri"},
        external_references=["uri"],
    )
    assert m.name == "Test"
    assert isinstance(m.id, UUID)
    assert m.semantic_tags == ["tag1"]
    assert m.ontology_mappings["skos:exactMatch"] == "uri"
    assert m.external_references == ["uri"]
