import pytest
from nora_evidence.access import AccessGrant, AccessPolicy, AcquisitionEnvelope, DataClassification

def test_access_policy_authorization():
    policy = AccessPolicy(
        policy_id="POL-001",
        name="Auditor Access Policy",
        allowed_roles={"auditor", "admin"}
    )
    
    assert policy.is_authorized("user-1", "auditor", DataClassification.CONFIDENTIAL) is True
    assert policy.is_authorized("user-2", "guest", DataClassification.CONFIDENTIAL) is False
    assert policy.is_authorized("user-2", "guest", DataClassification.PUBLIC) is True
