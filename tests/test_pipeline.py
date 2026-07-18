import importlib
import sys

import pytest


@pytest.fixture
def pipeline_module(tmp_path, monkeypatch):
    """Import the pipeline module with storage dirs redirected into a temp path."""
    base = tmp_path / "data_warehouse"
    logs = tmp_path / "logs"
    reports = tmp_path / "reports"
    for d in (base, logs, reports):
        d.mkdir(parents=True, exist_ok=True)

    # Ensure a clean import so module-level dir setup runs first.
    sys.modules.pop("data_ingestion_pipeline", None)
    mod = importlib.import_module("data_ingestion_pipeline")
    monkeypatch.setattr(mod, "BASE_DATA_DIR", str(base))
    monkeypatch.setattr(mod, "LOG_DIR", str(logs))
    monkeypatch.setattr(mod, "REPORT_DIR", str(reports))
    return mod


def test_hash_is_deterministic_and_content_sensitive(pipeline_module):
    monitor = pipeline_module.DataPipelineMonitor()
    h1 = monitor.get_content_hash(b"hello")
    h2 = monitor.get_content_hash(b"hello")
    h3 = monitor.get_content_hash(b"world")
    assert h1 == h2
    assert h1 != h3
    # SHA-256 hex digests are 64 characters long.
    assert len(h1) == 64


def test_save_writes_versioned_and_latest(pipeline_module):
    import os
    monitor = pipeline_module.DataPipelineMonitor()
    monitor.save_file_with_versioning("world_bank", "demo", b"col\n1\n")

    repo_path = os.path.join(pipeline_module.BASE_DATA_DIR, "world_bank", "demo")
    files = os.listdir(repo_path)
    assert "latest.csv" in files
    assert any(f.startswith("v_") and f.endswith(".csv") for f in files)
    assert len(monitor.execution_summary["successful_downloads"]) == 1


def test_save_skips_when_content_unchanged(pipeline_module):
    monitor = pipeline_module.DataPipelineMonitor()
    monitor.save_file_with_versioning("world_bank", "demo", b"same")
    monitor.save_file_with_versioning("world_bank", "demo", b"same")

    assert len(monitor.execution_summary["successful_downloads"]) == 1
    assert len(monitor.execution_summary["skipped_no_changes"]) == 1


def test_track_failure_records_error(pipeline_module):
    monitor = pipeline_module.DataPipelineMonitor()
    monitor.track_failure("who_gho", "demo", "boom")
    failures = monitor.execution_summary["failed_downloads"]
    assert len(failures) == 1
    assert failures[0]["error"] == "boom"
    assert failures[0]["dataset"] == "demo"
