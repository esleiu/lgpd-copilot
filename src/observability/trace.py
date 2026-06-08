from __future__ import annotations

import json
import time
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any


@dataclass
class TraceEvent:
    name: str
    payload: dict[str, Any]
    timestamp: float


class JsonlTracer:
    def __init__(self, path: str | Path = "data/cache/trace.jsonl") -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def log(self, name: str, **payload: Any) -> None:
        event = TraceEvent(name=name, payload=payload, timestamp=time.time())
        with self.path.open("a", encoding="utf-8") as file:
            file.write(json.dumps(asdict(event), ensure_ascii=False) + "\n")
