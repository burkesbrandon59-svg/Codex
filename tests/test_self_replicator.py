from pathlib import Path

from agent_loop.self_replicator import KnowledgeBase, SelfReplicationLoop


def test_distillation_and_blueprint(tmp_path: Path) -> None:
    kb = KnowledgeBase(tmp_path)
    loop = SelfReplicationLoop(kb)

    kb.add_observation("p1", "event-a", "do A", 0.9)
    kb.add_observation("p2", "event-b", "do B", 0.4)

    lessons = loop.distill_lessons(min_confidence=0.6)
    assert len(lessons) == 1
    assert "do A" in lessons[0].rule

    blueprint = loop.create_blueprint("child")
    assert blueprint["name"] == "child"
    assert blueprint["safety"]["autonomous_spread"] is False
    assert (tmp_path / "child_blueprint.json").exists()
