"""Safe process-level self-replication via shared knowledge artifacts.

This module does NOT clone or spread executable agents autonomously.
Instead, it implements a controlled loop where each process can:
1) record observations,
2) distill stable lessons,
3) publish a versioned blueprint,
4) let future processes bootstrap from that blueprint.
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from datetime import datetime, timezone
import json
from pathlib import Path
from typing import Iterable, List


@dataclass
class Observation:
    source_process: str
    event: str
    insight: str
    confidence: float
    timestamp: str


@dataclass
class Lesson:
    rule: str
    rationale: str
    confidence: float


class KnowledgeBase:
    """Stores process observations and distilled lessons in plain JSON files."""

    def __init__(self, root: Path) -> None:
        self.root = root
        self.root.mkdir(parents=True, exist_ok=True)
        self.observations_path = self.root / "observations.jsonl"
        self.lessons_path = self.root / "lessons.json"

    def add_observation(self, source_process: str, event: str, insight: str, confidence: float) -> Observation:
        obs = Observation(
            source_process=source_process,
            event=event,
            insight=insight,
            confidence=max(0.0, min(1.0, confidence)),
            timestamp=datetime.now(timezone.utc).isoformat(),
        )
        with self.observations_path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(asdict(obs), ensure_ascii=False) + "\n")
        return obs

    def read_observations(self) -> List[Observation]:
        if not self.observations_path.exists():
            return []
        data: List[Observation] = []
        with self.observations_path.open("r", encoding="utf-8") as f:
            for line in f:
                raw = json.loads(line)
                data.append(Observation(**raw))
        return data

    def write_lessons(self, lessons: Iterable[Lesson]) -> None:
        payload = [asdict(lesson) for lesson in lessons]
        with self.lessons_path.open("w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2, ensure_ascii=False)

    def read_lessons(self) -> List[Lesson]:
        if not self.lessons_path.exists():
            return []
        with self.lessons_path.open("r", encoding="utf-8") as f:
            raw = json.load(f)
        return [Lesson(**item) for item in raw]


class SelfReplicationLoop:
    """Generates reusable 'offspring configurations' from distilled lessons."""

    def __init__(self, kb: KnowledgeBase) -> None:
        self.kb = kb

    def distill_lessons(self, min_confidence: float = 0.6) -> List[Lesson]:
        observations = self.kb.read_observations()
        lessons: List[Lesson] = []
        for obs in observations:
            if obs.confidence < min_confidence:
                continue
            lessons.append(
                Lesson(
                    rule=f"When '{obs.event}', apply: {obs.insight}",
                    rationale=f"Observed in process '{obs.source_process}'",
                    confidence=obs.confidence,
                )
            )
        self.kb.write_lessons(lessons)
        return lessons

    def create_blueprint(self, process_name: str) -> dict:
        """Creates a versioned, portable blueprint another process can load."""
        lessons = self.kb.read_lessons()
        blueprint = {
            "name": process_name,
            "version": "1.0.0",
            "created_at": datetime.now(timezone.utc).isoformat(),
            "boot_instructions": [lesson.rule for lesson in lessons],
            "safety": {
                "autonomous_spread": False,
                "requires_human_trigger": True,
                "auditable_artifacts": True,
            },
        }
        out = self.kb.root / f"{process_name}_blueprint.json"
        with out.open("w", encoding="utf-8") as f:
            json.dump(blueprint, f, indent=2, ensure_ascii=False)
        return blueprint


def demo() -> None:
    """Small demonstration of the learning + replication loop."""
    kb = KnowledgeBase(Path("runtime_knowledge"))
    loop = SelfReplicationLoop(kb)

    kb.add_observation(
        source_process="worker-1",
        event="failing-check",
        insight="run unit tests before creating commit",
        confidence=0.95,
    )
    kb.add_observation(
        source_process="worker-2",
        event="ambiguous-request",
        insight="ship minimal safe implementation with clear assumptions",
        confidence=0.88,
    )

    loop.distill_lessons()
    blueprint = loop.create_blueprint("offspring-agent")
    print(json.dumps(blueprint, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    demo()
