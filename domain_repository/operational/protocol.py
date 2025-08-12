# Business Protocol model (loosely coupled to expectations/suites, with SHACL/OWL/PROV-O)
from pydantic import Field
from typing import Optional, Dict, Any, List
from uuid import UUID
from ..core.base import VersionableMetamodel, MetamodelType


class Protocol(VersionableMetamodel):
    """
    Represents a business policy/action triggered when an expectation or suite is breached.
    Supports SHACL/OWL constraints and PROV-O provenance.
    """

    metamodel_type = MetamodelType.PROTOCOL
    name: str
    description: Optional[str] = None
    # No direct reference fields; all relationships are managed via Relationship objects.
    def get_related_entity_ids(self) -> dict:
        return {}
    pass
