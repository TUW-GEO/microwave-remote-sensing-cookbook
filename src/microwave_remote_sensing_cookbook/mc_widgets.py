"""MC-Question and AnswerStore Classes."""

import Path


class AnswerStore:
    """Saves and Loads answers from json.store."""

    def __init__(self, path: str | Path) -> None:  # noqa: D107
        raise NotImplementedError

    def _load_answer(self) -> dict:
        raise NotImplementedError

    def _save_answer(self) -> None:
        raise NotImplementedError
