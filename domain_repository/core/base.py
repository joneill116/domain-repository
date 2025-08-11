# Core base classes for polymorphic design
from abc import ABC, abstractmethod
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, ClassVar
from uuid import UUID, uuid4
from datetime import datetime
from enum import Enum


class MetamodelType(str, Enum):
    """Enumeration of all supported metamodel types."""

    WORKFLOW = "Workflow"
    COMPONENT = "Component"
    EXPECTATION = "Expectation"
    PROTOCOL = "Protocol"


class BaseMetamodel(BaseModel, ABC):
    """
    Abstract base class for all metamodels.
    Provides common fields, JSON-LD serialization, and polymorphic behavior.
    """

    # Common fields across all metamodels
    id: UUID = Field(default_factory=uuid4)
    name: str = Field(..., description="Human-readable name")
    description: Optional[str] = Field(None, description="Optional description")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    # Ontology/semantic enhancements
    semantic_tags: Optional[list[str]] = Field(
        default=None, description="Semantic tags or keywords (e.g., SKOS concepts)"
    )
    ontology_mappings: Optional[dict[str, str]] = Field(
        default=None,
        description="Mappings to external ontologies (e.g., skos:exactMatch, rdfs:subClassOf)",
    )
    external_references: Optional[list[str]] = Field(
        default=None, description="URIs to external standards or documentation"
    )
    constraints: Optional[list[dict[str, Any]]] = Field(
        default=None, description="SHACL-like or custom validation rules"
    )
    parent_id: Optional[UUID] = Field(
        default=None,
        description="Optional parent metamodel for explicit inheritance/subtyping",
    )

    # Metamodel-specific configuration
    metamodel_type: ClassVar[MetamodelType]
    jsonld_context: ClassVar[str] = "https://schema.org"

    @property
    def __jsonld__(self) -> Dict[str, Any]:
        """
        Generate JSON-LD representation with common base structure,
        semantic annotations, and metamodel-specific extensions.
        References: schema.org, SKOS, SHACL, PROV-O
        """
        base_jsonld = {
            "@context": self.jsonld_context,
            "@type": self.metamodel_type.value,
            "id": str(self.id),
            "name": self.name,
            "description": self.description,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "semantic_tags": self.semantic_tags,
            "ontology_mappings": self.ontology_mappings,
            "external_references": self.external_references,
            "constraints": self.constraints,
            "parent_id": str(self.parent_id) if self.parent_id else None,
        }

        # Allow subclasses to extend the JSON-LD representation
        extensions = self._get_jsonld_extensions()
        base_jsonld.update(extensions)

        return base_jsonld

    @abstractmethod
    def _get_jsonld_extensions(self) -> Dict[str, Any]:
        """
        Return metamodel-specific extensions to the base JSON-LD structure.
        Must be implemented by each concrete metamodel.
        """
        pass

    @abstractmethod
    def get_related_entity_ids(self) -> Dict[str, Optional[UUID]]:
        """
        Return UUIDs of related entities for relationship mapping.
        Must be implemented by each concrete metamodel.
        """
        pass

    def validate_relationships(self, registry_service) -> bool:
        """
        Validate that all related entity IDs exist in the registry.
        Generic validation that works across all metamodels.
        """
        related_ids = self.get_related_entity_ids()
        for relation_type, entity_id in related_ids.items():
            if entity_id is not None:
                if not registry_service.entity_exists(entity_id):
                    raise ValueError(
                        f"Related {relation_type} with ID {entity_id} not found"
                    )
        return True


class VersionableMetamodel(BaseMetamodel):
    """
    Extended base class for metamodels that support versioning.
    """

    version: str = Field(default="1.0.0", description="Semantic version")
    is_deprecated: bool = Field(
        default=False, description="Whether this version is deprecated"
    )

    def _get_jsonld_extensions(self) -> Dict[str, Any]:
        extensions = super()._get_jsonld_extensions()
        extensions.update(
            {
                "version": self.version,
                "is_deprecated": self.is_deprecated,
            }
        )
        return extensions


class ExecutableMetamodel(BaseMetamodel):
    """
    Base class for metamodels that can be executed or instantiated.
    """

    is_active: bool = Field(
        default=True, description="Whether this metamodel is active"
    )
    execution_context: Optional[Dict[str, Any]] = Field(
        default=None, description="Context for execution"
    )

    def _get_jsonld_extensions(self) -> Dict[str, Any]:
        extensions = super()._get_jsonld_extensions()
        extensions.update(
            {
                "is_active": self.is_active,
                "execution_context": self.execution_context,
            }
        )
        return extensions
