# Workflow domain model with polymorphic base
from pydantic import Field
from typing import Optional, List, Dict, Any
from uuid import UUID
from ..core.base import ExecutableMetamodel, MetamodelType


class Workflow(ExecutableMetamodel):
    """
    JSON-LD compatible Workflow metamodel with polymorphic behavior.

    Represents the structure of a Workflow type for the metadata registry.
    This is a metamodel (a blueprint), not a concrete workflow instance.

    Ontology/semantic features:
    - semantic_tags: List of SKOS or domain-specific tags
    - ontology_mappings: Dict of ontology URIs (e.g., skos:exactMatch, rdfs:subClassOf)
    - external_references: List of URIs to standards or docs
    - constraints: List of SHACL-like or custom validation rules
    - parent_id: Optional parent metamodel for inheritance
    """

    metamodel_type = MetamodelType.WORKFLOW

    # No direct reference fields; all relationships are managed via Relationship objects.
    def get_related_entity_ids(self) -> dict:
        return {}
    pass
