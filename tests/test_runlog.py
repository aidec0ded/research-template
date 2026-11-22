import json
from pathlib import Path

from research_template.runlog import finish_run, start_run


def test_run_records_config_and_metrics(tmp_path: Path) -> None:
    run_dir = start_run("smoke", {"lr": 0.1}, seed=7, root=tmp_path)
    finish_run(run_dir, {"accuracy": 0.9})
    meta = json.loads((run_dir / "config.json").read_text())
    assert meta["seed"] == 7 and meta["config"] == {"lr": 0.1}
    assert json.loads((run_dir / "metrics.json").read_text()) == {"accuracy": 0.9}