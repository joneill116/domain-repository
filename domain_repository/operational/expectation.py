# Great Expectations-inspired Expectation models with SHACL/OWL/PROV-O support
from pydantic import Field, BaseModel
from typing import Optional, Dict, Any, List
from uuid import UUID
from ..core.base import VersionableMetamodel, MetamodelType


class Expectation(VersionableMetamodel):
    """
    Represents a single expectation (e.g., column values must not be null).
    Supports SHACL/OWL constraints and PROV-O provenance.
    """

    metamodel_type = MetamodelType.EXPECTATION
    expectation_type: str = Field(
        ...,
        description="Type of expectation (e.g., expect_column_values_to_not_be_null)",
    )
    kwargs: Dict[str, Any] = Field(
        default_factory=dict, description="Parameters for the expectation"
    )
    shacl_constraints: Optional[List[Dict[str, Any]]] = Field(
        default=None, description="SHACL constraints for this expectation"
    )
    owl_axioms: Optional[List[str]] = Field(
        default=None, description="OWL axioms for this expectation"
    )
    prov: Optional[Dict[str, Any]] = Field(
        default=None, description="PROV-O provenance metadata"
    )

    def _get_jsonld_extensions(self) -> Dict[str, Any]:
        extensions = super()._get_jsonld_extensions()
        extensions.update(
            {
                "expectation_type": self.expectation_type,
                "kwargs": self.kwargs,
                "shacl_constraints": self.shacl_constraints,
                "owl_axioms": self.owl_axioms,
                "prov": self.prov,
            }
        )
        return extensions

    # No direct reference fields; all relationships are managed via Relationship objects.
    def get_related_entity_ids(self) -> dict:
        return {}
    pass


class ExpectationSuite(VersionableMetamodel):
    """
    Represents a reusable, composable suite of expectations.
    Supports SHACL/OWL constraints and PROV-O provenance.
    """

    metamodel_type = MetamodelType.EXPECTATION
    shacl_constraints: Optional[List[Dict[str, Any]]] = Field(
        default=None, description="SHACL constraints for this suite"
    )
    owl_axioms: Optional[List[str]] = Field(
        default=None, description="OWL axioms for this suite"
    )
    prov: Optional[Dict[str, Any]] = Field(
        default=None, description="PROV-O provenance metadata"
    )

    # No direct reference fields; all relationships are managed via Relationship objects.
    # Expectation membership is managed via explicit Relationship objects.
    def _get_jsonld_extensions(self) -> Dict[str, Any]:
        extensions = super()._get_jsonld_extensions()
        extensions.update(
            {
                "shacl_constraints": self.shacl_constraints,
                "owl_axioms": self.owl_axioms,
                "prov": self.prov,
            }
        )
        return extensions


class ExpectationResult(BaseModel):
    """
    Represents the result of evaluating an expectation.
    Includes PROV-O provenance.
    """

    # No direct reference fields; all relationships are managed via Relationship objects.
    # The expectation this result is for is linked via a Relationship object.
    success: bool
    result_details: Dict[str, Any] = Field(default_factory=dict)
    evaluated_at: Optional[str] = None  # ISO timestamp
    prov: Optional[Dict[str, Any]] = Field(
        default=None, description="PROV-O provenance metadata"
    )
