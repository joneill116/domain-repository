"""
World-class tests for core.relationships
"""
import pytest
from domain_repository.core.relationships import Relationship, RelationshipType
from uuid import uuid4

def test_relationship_creation():
    rel = Relationship(
        source_id=uuid4(),
        target_id=uuid4(),
        relationship_type=RelationshipType.CONTAINS
    )
    assert rel.relationship_type == RelationshipType.CONTAINS
    assert rel.source_id != rel.target_id
    assert rel.id is not None
