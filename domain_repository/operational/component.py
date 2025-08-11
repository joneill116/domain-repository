# Component domain model with polymorphic base
from pydantic import Field
from typing import Optional, Dict, Any
from uuid import UUID
from ..core.base import ExecutableMetamodel, MetamodelType


class Component(ExecutableMetamodel):
    """
    JSON-LD compatible Component metamodel with polymorphic behavior.

    Ontology/semantic features:
    - semantic_tags: List of SKOS or domain-specific tags
    - ontology_mappings: Dict of ontology URIs (e.g., skos:exactMatch, rdfs:subClassOf)
    - external_references: List of URIs to standards or docs
    - constraints: List of SHACL-like or custom validation rules
    - parent_id: Optional parent metamodel for inheritance
    """

    metamodel_type = MetamodelType.COMPONENT

    # No direct reference fields; all relationships are managed via Relationship objects.
    pass
