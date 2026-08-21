import pytest
from nora_evidence.custody import CustodyChain, CustodyRecord, FileCustodyStore
from nora_evidence.store import LocalEvidenceStore


def test_custody_chain_append_and_verification():
    chain = CustodyChain(artifact_id="art_100")
    r1 = chain.append("rec_1", "ingested", "user_alice")
    r2 = chain.append("rec_2", "sealed", "user_bob")

    assert len(chain.records) == 2
    assert r1.previous_hash == "GENESIS_0000000000000000000000000000000000000000000000000000000000000000"
    assert r2.previous_hash == r1.record_hash
    assert chain.verify_chain() is True


def test_sqlite_custody_store_persistence(tmp_path):
    db_file = str(tmp_path / "evidence.db")
    store = LocalEvidenceStore(db_file)

    chain = CustodyChain(artifact_id="art_200")
    r1 = chain.append("rec_1", "ingested", "sys_ingest")
    r2 = chain.append("rec_2", "annotated", "user_charlie")

    store.insert_custody_record(r1)
    store.insert_custody_record(r2)
    store.close()

    # Re-open database file to simulate restart readback
    restarted_store = LocalEvidenceStore(db_file)
    fetched_chain = restarted_store.fetch_custody_chain("art_200")
    assert len(fetched_chain.records) == 2
    assert fetched_chain.records[0].record_id == "rec_1"
    assert fetched_chain.records[1].previous_hash == fetched_chain.records[0].record_hash
    assert fetched_chain.verify_chain() is True
    restarted_store.close()


def test_file_custody_store_persistence(tmp_path):
    storage_file = tmp_path / "custody.json"
    file_store = FileCustodyStore(storage_file)

    chain = file_store.get_chain("art_300")
    chain.append("rec_10", "ingested", "sys_ingest")
    chain.append("rec_11", "sealed", "sys_seal")
    file_store.save_chain(chain)

    # Re-instantiate FileCustodyStore from disk file to verify restart readback
    restarted_file_store = FileCustodyStore(storage_file)
    readback_chain = restarted_file_store.get_chain("art_300")
    assert len(readback_chain.records) == 2
    assert readback_chain.verify_chain() is True
