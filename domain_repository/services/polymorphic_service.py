# Enhanced polymorphic service for metadata registry
from typing import Dict, List, Optional, Type, Any
from uuid import UUID
from domain_repository.core import (
    MetamodelRegistry,
    registry,
    MetamodelType,
    RelationshipType,
    Relationship,
)
from domain_repository.operational.workflow import Workflow
from domain_repository.operational.component import Component
from domain_repository.operational.protocol import Protocol
from domain_repository.operational.expectation import Expectation


class PolymorphicMetadataService:
    """
    Enhanced service that leverages polymorphic behavior for clean,
    coherent workflow, component, expectation, and protocol management.
    """

    def __init__(self, metamodel_registry: Optional[MetamodelRegistry] = None):
        self.registry = metamodel_registry or registry

        # Register all metamodel classes
        self._register_metamodel_classes()

    def _register_metamodel_classes(self):
        """Register all available metamodel classes for polymorphic instantiation."""
        self.registry.register_metamodel_class(Workflow)
        self.registry.register_metamodel_class(Component)
        self.registry.register_metamodel_class(Protocol)
        self.registry.register_metamodel_class(Expectation)

    def create_metamodel(self, metamodel_type: MetamodelType, **kwargs) -> Any:
        """
        Polymorphically create and register a metamodel instance.
        Returns the created instance.
        """
        instance = self.registry.create_instance(metamodel_type, **kwargs)
        self.registry.register_instance(instance)
        return instance

    def create_workflow(self, name: str, description: str = None, **kwargs) -> Workflow:
        """Create a workflow metamodel with enhanced features."""
        return self.create_metamodel(
            MetamodelType.WORKFLOW, name=name, description=description, **kwargs
        )

    def create_component(
        self,
        name: str,
        description: str = None,
        protocol_id: Optional[UUID] = None,
        expectation_id: Optional[UUID] = None,
        **kwargs,
    ) -> Component:
        """Create a component metamodel with relationship validation."""
        # Validate relationships exist if provided
        if protocol_id and not self.registry.entity_exists(protocol_id):
            raise ValueError(f"Protocol with ID {protocol_id} does not exist")
        if expectation_id and not self.registry.entity_exists(expectation_id):
            raise ValueError(f"Expectation with ID {expectation_id} does not exist")

        return self.create_metamodel(
            MetamodelType.COMPONENT,
            name=name,
            description=description,
            protocol_id=protocol_id,
            expectation_id=expectation_id,
            **kwargs,
        )

    def create_protocol(
        self,
        name: str,
        description: str = None,
        version: str = "1.0.0",
        specification_url: str = None,
        **kwargs,
    ) -> Protocol:
        """Create a protocol metamodel with versioning support."""
        return self.create_metamodel(
            MetamodelType.PROTOCOL,
            name=name,
            description=description,
            version=version,
            specification_url=specification_url,
            **kwargs,
        )

    def create_expectation(
        self,
        name: str,
        description: str = None,
        version: str = "1.0.0",
        validation_rules: List[str] = None,
        severity: str = "medium",
        **kwargs,
    ) -> Expectation:
        """Create an expectation metamodel with validation rules."""
        return self.create_metamodel(
            MetamodelType.EXPECTATION,
            name=name,
            description=description,
            version=version,
            validation_rules=validation_rules or [],
            severity=severity,
            **kwargs,
        )

    def add_component_to_workflow(self, workflow_id: UUID, component_id: UUID) -> None:
        """Add a component to a workflow with relationship tracking."""
        workflow = self.registry.get_entity(workflow_id)
        if not workflow or workflow.metamodel_type != MetamodelType.WORKFLOW:
            raise ValueError(f"Workflow with ID {workflow_id} not found")

        component = self.registry.get_entity(component_id)
        if not component or component.metamodel_type != MetamodelType.COMPONENT:
            raise ValueError(f"Component with ID {component_id} not found")

        # Add to workflow
        workflow.add_component(component_id)

        # Create explicit relationship
        relationship = Relationship(
            source_id=workflow_id,
            target_id=component_id,
            relationship_type=RelationshipType.CONTAINS,
            metadata={"added_via": "workflow_service"},
        )

        self.registry.relationship_manager.add_relationship(relationship)

    def get_workflow_components(self, workflow_id: UUID) -> List[Component]:
        """Get all components in a workflow."""
        workflow = self.registry.get_entity(workflow_id)
        if not workflow or workflow.metamodel_type != MetamodelType.WORKFLOW:
            raise ValueError(f"Workflow with ID {workflow_id} not found")

        components = []
        for component_id in workflow.component_ids:
            component = self.registry.get_entity(component_id)
            if component and component.metamodel_type == MetamodelType.COMPONENT:
                components.append(component)

        return components

    def get_polymorphic_statistics(self) -> Dict[str, Any]:
        """Get comprehensive statistics about the metamodel registry."""
        base_stats = self.registry.get_statistics()

        # Add relationship statistics
        relationship_stats = {}
        for rel_type in RelationshipType:
            count = len(
                [
                    r
                    for r in self.registry.relationship_manager.relationships.values()
                    if r.relationship_type == rel_type
                ]
            )
            relationship_stats[rel_type.value] = count

        base_stats["relationships_by_type"] = relationship_stats

        return base_stats

    def export_complete_jsonld_graph(self) -> Dict[str, Any]:
        """Export the complete metamodel graph as JSON-LD."""
        return self.registry.export_jsonld_graph()

    def validate_entire_system(self) -> bool:
        """Validate all metamodels and relationships in the system."""
        try:
            # Validate all individual metamodel relationships
            self.registry.validate_all_relationships()

            # Validate all explicit relationships
            for (
                relationship
            ) in self.registry.relationship_manager.relationships.values():
                self.registry.relationship_manager.validate_relationship_constraints(
                    relationship, self.registry
                )

            return True
        except ValueError as e:
            raise ValueError(f"System validation failed: {e}")


# Global service instance
polymorphic_service = PolymorphicMetadataService()
