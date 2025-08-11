# Domain Repository Package with Polymorphic Architecture
"""
Enhanced domain repository with polymorphic metamodel architecture for
workflow, component, expectation, and protocol management.

This package provides:
- Polymorphic base classes for all metamodels
- Type-safe relationship management
- JSON-LD serialization with semantic interoperability
- Registry-based metamodel instantiation and validation
- Clean, coherent architecture for ontology evolution
"""

from .operational.workflow import Workflow
from .operational.component import Component
from .operational.protocol import Protocol
from .operational.expectation import Expectation

from .core import (
    BaseMetamodel,
    VersionableMetamodel,
    ExecutableMetamodel,
    MetamodelType,
    Relationship,
    RelationshipType,
    RelationshipManager,
    MetamodelRegistry,
    registry,
)

from .services import PolymorphicMetadataService, polymorphic_service

__version__ = "0.2.0"

__all__ = [
    # Operational metamodels
    "Workflow",
    "Component",
    "Protocol",
    "Expectation",
    # Core polymorphic architecture
    "BaseMetamodel",
    "VersionableMetamodel",
    "ExecutableMetamodel",
    "MetamodelType",
    "Relationship",
    "RelationshipType",
    "RelationshipManager",
    "MetamodelRegistry",
    "registry",
    # Services
    "PolymorphicMetadataService",
    "polymorphic_service",
]
