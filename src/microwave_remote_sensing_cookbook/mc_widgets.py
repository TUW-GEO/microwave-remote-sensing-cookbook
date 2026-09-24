"""MC-Question and AnswerStore Classes."""

from pathlib import Path


class AnswerStore:
    """Saves and Loads answers from json store."""

    def __init__(self, path: str | Path) -> None:  # noqa: D107
        raise NotImplementedError

    def _load(self) -> dict:
        raise NotImplementedError

    def _save(self) -> None:
        raise NotImplementedError

    def set_answer(self, chapter: str, q_key: str, option: str, value: bool) -> None:  # noqa: D102, FBT001
        raise NotImplementedError

    def get_answer(  # noqa: D102
        self,
        chapter: str,
        q_key: str,
        option: str,
        default: bool = False,  # noqa: FBT001, FBT002
    ) -> bool:
        raise NotImplementedError


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
