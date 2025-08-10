# Example Metamodels for Operational Domain

This document provides example definitions for workflow, component, protocol, and expectation metamodels. These examples illustrate how to use the abstract models in the `operational` folder to define types for registration in the metadata-registry-svc.

---

## Example: Data Processing Workflow Metamodel

```python
from operational.workflow import Workflow
from uuid import uuid4

# Example component UUIDs (would be registered separately)
acquisition_component_id = uuid4()
transformation_component_id = uuid4()

workflow_metamodel = Workflow(
    name="Data Processing Workflow",
    description="A workflow for processing raw data through acquisition and transformation steps.",
    component_ids=[acquisition_component_id, transformation_component_id]
)
print(workflow_metamodel.__jsonld__)
```

---

## Example: Acquisition Component Metamodel

```python
from operational.component import Component
from uuid import uuid4

protocol_id = uuid4()  # Example protocol UUID

acquisition_component = Component(
    name="Acquisition Component",
    description="Component responsible for acquiring data from source systems.",
    protocol_id=protocol_id
)
print(acquisition_component.__jsonld__)
```

---


## Example: Protocol Metamodel (Business Protocol)

```python
from operational.protocol import Protocol

protocol = Protocol(
    name="Send to Analyst on Failure",
    description="If an expectation fails on a component, notify an analyst for review."
)
print(protocol.__jsonld__)
```

---

## Example: Expectation Metamodel

```python
from operational.expectation import Expectation

expectation = Expectation(
    name="Row Count Expectation",
    description="Expectation that checks if the row count meets a minimum threshold."
)
print(expectation.__jsonld__)
```