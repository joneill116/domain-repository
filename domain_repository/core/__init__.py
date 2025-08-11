# Core package for polymorphic metamodel architecture
from .base import (
    BaseMetamodel,
    VersionableMetamodel,
    ExecutableMetamodel,
    MetamodelType,
)
from .relationships import Relationship, RelationshipType, RelationshipManager
from .registry import MetamodelRegistry, registry

__all__ = [
    "BaseMetamodel",
    "VersionableMetamodel",
    "ExecutableMetamodel",
    "MetamodelType",
    "Relationship",
    "RelationshipType",
    "RelationshipManager",
    "MetamodelRegistry",
    "registry",
]
