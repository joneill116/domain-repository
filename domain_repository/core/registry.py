# Metamodel factory and registry for polymorphic instantiation
from typing import Dict, Type, Optional, List, Any
from uuid import UUID
from .base import BaseMetamodel, MetamodelType
from .relationships import RelationshipManager


class MetamodelRegistry:
    """Registry for metamodel types and instances with polymorphic support."""

    def __init__(self):
        self.metamodel_classes: Dict[MetamodelType, Type[BaseMetamodel]] = {}
        self.instances: Dict[UUID, BaseMetamodel] = {}
        self.relationship_manager = RelationshipManager()
        self.type_index: Dict[MetamodelType, List[UUID]] = {}

    def register_metamodel_class(self, metamodel_class: Type[BaseMetamodel]) -> None:
        """Register a metamodel class for polymorphic instantiation."""
        if not hasattr(metamodel_class, "metamodel_type"):
            raise ValueError(
                f"Metamodel class {metamodel_class} must define metamodel_type"
            )

        self.metamodel_classes[metamodel_class.metamodel_type] = metamodel_class

        if metamodel_class.metamodel_type not in self.type_index:
            self.type_index[metamodel_class.metamodel_type] = []

    def create_instance(self, metamodel_type: MetamodelType, **kwargs) -> BaseMetamodel:
        """Polymorphically create an instance of the specified metamodel type."""
        if metamodel_type not in self.metamodel_classes:
            raise ValueError(f"Metamodel type {metamodel_type} not registered")

        metamodel_class = self.metamodel_classes[metamodel_type]
        instance = metamodel_class(**kwargs)

        return instance

    def register_instance(self, instance: BaseMetamodel) -> None:
        """Register a metamodel instance."""
        self.instances[instance.id] = instance

        if instance.metamodel_type not in self.type_index:
            self.type_index[instance.metamodel_type] = []

        self.type_index[instance.metamodel_type].append(instance.id)

    def get_entity(self, entity_id: UUID) -> Optional[BaseMetamodel]:
        """Get a metamodel instance by ID."""
        return self.instances.get(entity_id)

    def entity_exists(self, entity_id: UUID) -> bool:
        """Check if an entity exists in the registry."""
        return entity_id in self.instances

    def get_instances_by_type(
        self, metamodel_type: MetamodelType
    ) -> List[BaseMetamodel]:
        """Get all instances of a specific metamodel type."""
        instance_ids = self.type_index.get(metamodel_type, [])
        return [self.instances[iid] for iid in instance_ids if iid in self.instances]

    def validate_all_relationships(self) -> bool:
        """Validate all relationships in the registry."""
        for instance in self.instances.values():
            try:
                instance.validate_relationships(self)
            except ValueError as e:
                raise ValueError(
                    f"Validation failed for {instance.name} ({instance.id}): {e}"
                )

        return True

    def export_jsonld_graph(self) -> Dict[str, Any]:
        """Export the entire registry as a JSON-LD graph."""
        entities = []

        # Export all metamodel instances
        for instance in self.instances.values():
            entities.append(instance.__jsonld__)

        # Export all relationships
        for relationship in self.relationship_manager.relationships.values():
            entities.append(relationship.__jsonld__)

        return {"@context": "https://schema.org", "@type": "Graph", "@graph": entities}

    def get_statistics(self) -> Dict[str, Any]:
        """Get registry statistics."""
        stats = {
            "total_instances": len(self.instances),
            "total_relationships": len(self.relationship_manager.relationships),
            "instances_by_type": {},
        }

        for metamodel_type in MetamodelType:
            count = len(self.type_index.get(metamodel_type, []))
            stats["instances_by_type"][metamodel_type.value] = count

        return stats


# Global registry instance
registry = MetamodelRegistry()
