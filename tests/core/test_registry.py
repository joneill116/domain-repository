"""
World-class tests for core.registry
"""
import pytest
from domain_repository.core.registry import MetamodelRegistry
from domain_repository.core.base import BaseMetamodel, MetamodelType
from uuid import uuid4

class DummyMetamodel(BaseMetamodel):
    metamodel_type = MetamodelType.COMPONENT

registry = MetamodelRegistry()
registry.register_metamodel_class(DummyMetamodel)

def test_create_and_register_instance():
    instance = registry.create_instance(MetamodelType.COMPONENT, name="X")
    assert isinstance(instance, DummyMetamodel)
    registry.register_instance(instance)
    assert registry.get_entity(instance.id) == instance
