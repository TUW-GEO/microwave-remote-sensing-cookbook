"""MC-Question and AnswerStore Classes."""

import json
from pathlib import Path


class AnswerStore:
    """Saves and Loads answers from json store."""

    def __init__(self, path: str | Path) -> None:  # noqa: D107
        self.path = Path(path)
        self.data = self._load()

    def _load(self) -> dict:
        if not self.path.exists():
            return {}
        return json.loads(self.path.read_text())

    def _save(self) -> None:
        self.path.write_text(json.dumps(self.data, indent=2, sort_keys=True))

    def set(self, chapter: str, q_key: str, answer_option: str, value: bool) -> None:  # noqa: D102, FBT001
        self.data.setdefault(chapter, {}).setdefault(q_key, {})[answer_option] = value
        self._save()

    def get(  # noqa: D102
        self,
        chapter: str,
        q_key: str,
        answer_options: str,
        default: bool = False,  # noqa: FBT001, FBT002
    ) -> bool:
        return self.data.get(chapter, {}).get(q_key, {}).get(answer_options, default)


class MCQuestion:
    """Creates MC-Questions with Checkboxes."""

    def __init__(  # noqa: D107
        self,
        store: AnswerStore,
        chapter: str,
        q_key: str,
        answer_options: dict[str, str],
    ) -> None:
        raise NotImplementedError

    def _build_question(self) -> None:
        raise NotImplementedError

    def show_question(self) -> None:  # noqa: D102
        raise NotImplementedError
