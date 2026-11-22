"""Record each experiment run: config, seed and commit in, metrics out."""

import json
import platform
import random
import subprocess
import time
from pathlib import Path
from typing import Any


def git_sha() -> str:
    try:
        out = subprocess.run(
            ["git", "rev-parse", "--short", "HEAD"],
            capture_output=True, text=True, check=True,
        )
        return out.stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        return "unknown"


def start_run(name: str, config: dict[str, Any], seed: int,
              root: Path = Path("results")) -> Path:
    random.seed(seed)  # seed numpy / torch too in projects that use them
    run_dir = root / f"{time.strftime('%Y%m%d-%H%M%S')}-{name}"
    run_dir.mkdir(parents=True)
    meta = {"name": name, "seed": seed, "git_sha": git_sha(),
            "python": platform.python_version(), "config": config}
    (run_dir / "config.json").write_text(json.dumps(meta, indent=2))
    return run_dir


def finish_run(run_dir: Path, metrics: dict[str, Any]) -> None:
    (run_dir / "metrics.json").write_text(json.dumps(metrics, indent=2))