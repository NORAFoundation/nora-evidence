from __future__ import annotations
from datetime import datetime, timezone
from enum import Enum
from typing import List, Optional, Set
from pydantic import BaseModel, Field

class DataClassification(str, Enum):
    PUBLIC = "public"
    CONFIDENTIAL = "confidential"
    RESTRICTED = "restricted"

class AccessGrant(BaseModel):
    grant_id: str
    principal_id: str
    allowed_data_classes: Set[DataClassification] = Field(default_factory=set)
    expires_at: Optional[datetime] = None

class AcquisitionEnvelope(BaseModel):
    envelope_id: str
    artifact_id: str
    classification: DataClassification = DataClassification.PUBLIC
    owner_id: str
    access_policy_id: str

class AccessPolicy(BaseModel):
    policy_id: str
    name: str
    allowed_roles: Set[str] = Field(default_factory=set)

    def is_authorized(self, principal_id: str, role: str, classification: DataClassification) -> bool:
        if classification == DataClassification.PUBLIC:
            return True
        return role in self.allowed_roles
