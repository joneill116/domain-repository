# [DEPRECATED] Please see the root-level README.md for all documentation and usage. This file is intentionally left blank.

This package provides a world-class, extensible foundation for modeling, linking, and managing all operational domain concepts—workflows, components, expectations, protocols—using a polymorphic, registry-based, and JSON-LD native approach.

## Key Features
- **Polymorphic Base Classes:** All metamodels inherit from a common, extensible base for consistency and code reuse.
- **Type-Safe Relationships:** Explicit, validated relationships between metamodels (e.g., workflows contain components, components implement protocols).
- **Registry Pattern:** Central registry for all metamodels, supporting dynamic discovery, validation, and querying.
- **JSON-LD Serialization:** All metamodels and relationships are natively serializable to JSON-LD for semantic interoperability.
- **Service Layer:** High-level API for creating, linking, and querying metamodels and their relationships.

## Architecture Overview

```
┌──────────────────────────────┐
│   Polymorphic Metamodels     │
└─────────────┬────────────────┘
              │
              ▼
┌──────────────────────────────┐
│   Registry & Relationships   │
└─────────────┬────────────────┘
              │
              ▼
┌──────────────────────────────┐
│   Service Layer (API)        │
└─────────────┬────────────────┘
              │
              ▼
┌──────────────────────────────┐
│   Metadata Registry Svc      │
└──────────────────────────────┘
```

## Core Modules
- `core/`: Base classes, relationship manager, registry
- `operational/`: Workflow, Component, Expectation, Protocol metamodels
- `services/`: Polymorphic service for high-level operations

## Example: Creating and Linking Metamodels

```python
from domain_repository import polymorphic_service, MetamodelType

# Create protocol and expectation with semantic annotations
protocol = polymorphic_service.create_protocol(
    name="REST API Protocol",
    specification_url="https://restfulapi.net/",
    semantic_tags=["api", "rest"],
    ontology_mappings={"skos:exactMatch": "https://schema.org/WebAPI"},
    external_references=["https://schema.org/WebAPI"],
    constraints=[{"property": "specification_url", "pattern": "^https?://"}]
)
expectation = polymorphic_service.create_expectation(
    name="Data Quality",
    validation_rules=["non_null_check"],
    semantic_tags=["quality", "validation"],
    ontology_mappings={"skos:exactMatch": "https://schema.org/PropertyValue"}
)

## Example: Relationship-Centric Linking

# Create component, protocol, and expectation (no direct references)
component = polymorphic_service.create_component(
    name="Acquisition",
    semantic_tags=["acquisition", "data"],
    ontology_mappings={"skos:broader": "https://schema.org/Action"}
)
protocol = polymorphic_service.create_protocol(
    name="REST API Protocol",
    specification_url="https://restfulapi.net/",
    semantic_tags=["api", "rest"]
)
expectation = polymorphic_service.create_expectation(
    name="Data Quality",
    validation_rules=["non_null_check"],
    semantic_tags=["quality", "validation"]
)

# Create workflow (no component_ids field)
workflow = polymorphic_service.create_workflow(
    name="Data Pipeline",
    semantic_tags=["pipeline", "workflow"]
)

# Link entities via explicit relationships
polymorphic_service.create_relationship(
    source_id=workflow.id,
    target_id=component.id,
    relationship_type="contains"
)
polymorphic_service.create_relationship(
    source_id=component.id,
    target_id=protocol.id,
    relationship_type="implements"
)
polymorphic_service.create_relationship(
    source_id=component.id,
    target_id=expectation.id,
    relationship_type="fulfills"
)

# Serialize to JSON-LD
print(polymorphic_service.export_complete_jsonld_graph())
```

## Demo
See `examples/polymorphic_architecture_demo.py` for a full demonstration of the new architecture.

## Extending the System
- Add new metamodels by subclassing the base classes in `core/`.
- Register new relationship types in the relationship manager.
- Use the service layer for all high-level operations and validation.
- All entity connections are managed via explicit Relationship objects—never direct fields.

## Notes
- All metamodels are blueprints, not concrete instances.
- Relationships are explicit, type-safe, and validated.
- The registry enables dynamic discovery, validation, and graph export.
- Ontology/semantic fields and provenance (PROV-O) are first-class citizens.
- All JSON-LD and API payloads reflect the decoupled, relationship-centric model.

## Migration Note
If upgrading from a previous version, remove all direct reference fields (e.g., `component_ids`, `protocol_id`, `expectation_id`) from your code and use explicit relationships instead.

## Validation Checklist (World-Class Ontology Review)
- [x] All entity connections are explicit relationships
- [x] Ontology/semantic fields and provenance are present
- [x] SHACL/OWL constraints supported
- [x] JSON-LD serialization for all entities and relationships
- [x] Registry and relationship manager are central to all operations
