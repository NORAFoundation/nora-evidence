# Architecture

## Invariants

1. The public repository contains reusable technology, not private Matter data.
2. Every important output has an inspectable basis appropriate to this project's domain.
3. Authorization is evaluated before data is exposed to retrieval/tool/model paths where applicable.
4. Model output is a transformation, not a source of truth.
5. Unknown and disputed states are valid outputs.
6. Tests/evals use synthetic or redistributable fixtures.
7. Migration provenance is explicit.

## Target-specific architecture

Core object model:
- Artifact: immutable/native bytes or structured source object.
- SourceOccurrence: where/when/how an artifact was acquired or appeared.
- AcquisitionEvent: connector/account/external ID/version/checkpoint metadata.
- Locator: exact round-trippable reference into an artifact/occurrence.
- Transformation: deterministic or model-assisted derivative with lineage.
- BasisEdge: support/contradict/qualify/derive relationships.
- SourceGenealogy: duplicate/propagation/independent-origin relationships.
- CustodyEvent: append-only handling/export events.
- AttestationAdapter: optional protocol bridge; never the evidence database.

## Extension points

Connector adapters, locator codecs, transformation processors, custody backends, Canon adapter, export adapters.

## Compatibility

Public contracts should be versioned and provider-neutral where practical.

## Architecture decisions

Record consequential changes under `docs/decisions/`.
