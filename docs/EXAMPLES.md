# Relationship-Centric Example Metamodels for Operational Domain

This document provides example definitions for workflow, component, protocol, and expectation metamodels using the relationship-centric, ontology-driven design. All connections are managed via explicit Relationship objects and the service layer.

---

## Example: Data Processing Workflow, Components, Protocol, and Expectation

```python
from domain_repository.services import polymorphic_service

# Create protocol, expectation, and component (no direct references)
protocol = polymorphic_service.create_protocol(
    name="Send to Analyst on Failure",
    description="If an expectation fails on a component, notify an analyst for review.",
    semantic_tags=["notification", "escalation"]
)
expectation = polymorphic_service.create_expectation(
    name="Row Count Expectation",
    description="Checks if the row count meets a minimum threshold.",
    semantic_tags=["quality", "row_count"]
)
component = polymorphic_service.create_component(
    name="Acquisition Component",
    description="Component responsible for acquiring data from source systems.",
    semantic_tags=["acquisition", "data"]
)

# Create workflow (no component_ids field)
workflow = polymorphic_service.create_workflow(
    name="Data Processing Workflow",
    description="A workflow for processing raw data through acquisition and transformation steps.",
    semantic_tags=["workflow", "data_processing"]
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

---

## Notes
- All entity connections are managed via explicit Relationship objects—never direct fields.
- Ontology/semantic fields and provenance are first-class citizens.
- All JSON-LD and API payloads reflect the decoupled, relationship-centric model.