# Enhanced relationship management system
from typing import Dict, List, Optional, Set, Type, Union, Any
from uuid import UUID, uuid4
from enum import Enum
from pydantic import BaseModel, Field
from .base import BaseMetamodel


class RelationshipType(str, Enum):
    """Types of relationships between metamodels."""

    CONTAINS = "contains"  # Workflow contains Components
    IMPLEMENTS = "implements"  # Component implements Protocol
    EXPECTS = "expects"  # Component expects Expectations
    DEPENDS_ON = "depends_on"  # Generic dependency
    COMPOSED_OF = "composed_of"  # Composition relationship
    EXTENDS = "extends"  # Inheritance/extension


class Relationship(BaseModel):
    """Represents a typed relationship between metamodels."""

    id: UUID = Field(default_factory=uuid4)
    source_id: UUID = Field(..., description="Source entity UUID")
    target_id: UUID = Field(..., description="Target entity UUID")
    relationship_type: RelationshipType
    metadata: Optional[Dict[str, Any]] = Field(
        default=None, description="Additional relationship metadata"
    )

    @property
    def __jsonld__(self):
        return {
            "@context": "https://schema.org",
            "@type": "Relationship",
            "id": str(self.id),
            "source": str(self.source_id),
            "target": str(self.target_id),
            "relationshipType": self.relationship_type.value,
            "metadata": self.metadata,
        }


class RelationshipManager:
    """Manages relationships between metamodels with type safety and validation."""

    def __init__(self):
        self.relationships: Dict[UUID, Relationship] = {}
        self.source_index: Dict[UUID, Set[UUID]] = {}  # source_id -> relationship_ids
        self.target_index: Dict[UUID, Set[UUID]] = {}  # target_id -> relationship_ids
        self.type_index: Dict[RelationshipType, Set[UUID]] = (
            {}
        )  # type -> relationship_ids

    def add_relationship(self, relationship: Relationship) -> None:
        """Add a relationship with proper indexing."""
        self.relationships[relationship.id] = relationship

        # Update indexes
        if relationship.source_id not in self.source_index:
            self.source_index[relationship.source_id] = set()
        self.source_index[relationship.source_id].add(relationship.id)

        if relationship.target_id not in self.target_index:
            self.target_index[relationship.target_id] = set()
        self.target_index[relationship.target_id].add(relationship.id)

        if relationship.relationship_type not in self.type_index:
            self.type_index[relationship.relationship_type] = set()
        self.type_index[relationship.relationship_type].add(relationship.id)

    def get_relationships_from(
        self, source_id: UUID, relationship_type: Optional[RelationshipType] = None
    ) -> List[Relationship]:
        """Get all relationships originating from a source entity."""
        relationship_ids = self.source_index.get(source_id, set())
        relationships = [self.relationships[rid] for rid in relationship_ids]

        if relationship_type:
            relationships = [
                r for r in relationships if r.relationship_type == relationship_type
            ]

        return relationships

    def get_relationships_to(
        self, target_id: UUID, relationship_type: Optional[RelationshipType] = None
    ) -> List[Relationship]:
        """Get all relationships targeting an entity."""
        relationship_ids = self.target_index.get(target_id, set())
        relationships = [self.relationships[rid] for rid in relationship_ids]

        if relationship_type:
            relationships = [
                r for r in relationships if r.relationship_type == relationship_type
            ]

        return relationships

    def validate_relationship_constraints(
        self, relationship: Relationship, metamodel_registry
    ) -> bool:
        """Validate that a relationship makes sense given metamodel types."""
        source_entity = metamodel_registry.get_entity(relationship.source_id)
        target_entity = metamodel_registry.get_entity(relationship.target_id)

        if not source_entity or not target_entity:
            raise ValueError("Both source and target entities must exist")

        # Define valid relationship patterns
        valid_patterns = {
            RelationshipType.CONTAINS: {
                ("Workflow", "Component"),
                ("Component", "Expectation"),
            },
            RelationshipType.IMPLEMENTS: {
                ("Component", "Protocol"),
            },
            RelationshipType.EXPECTS: {
                ("Component", "Expectation"),
            },
        }

        source_type = source_entity.metamodel_type.value
        target_type = target_entity.metamodel_type.value

        if relationship.relationship_type in valid_patterns:
            pattern = (source_type, target_type)
            if pattern not in valid_patterns[relationship.relationship_type]:
                raise ValueError(
                    f"Invalid relationship: {source_type} cannot {relationship.relationship_type.value} {target_type}"
                )

        return True
