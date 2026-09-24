"""MC-Question and AnswerStore Classes."""

import json
from pathlib import Path

import ipywidgets as widgets


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
        self.data = self._load()  # frisch laden -> fremde Änderungen mitnehmen
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
    """A multiple-choice question. Reads/writes its subtree in the store."""

    def __init__(
        self,
        store: AnswerStore,
        chapter: str,
        q_key: str,
        options: dict[str, str],
    ) -> None:
        # options: {internal_key: display_text}
        self.store = store
        self.chapter = chapter
        self.q_key = q_key
        self.options = options
        self.checkboxes: dict[str, widgets.Checkbox] = {}  # internal_key -> Checkbox
        self._build()

    def _build(self) -> None:
        for opt_key, text in self.options.items():
            cb = widgets.Checkbox(
                value=self.store.get(self.chapter, self.q_key, opt_key),
                description=text,
                indent=False,
                style={"description_width": "initial"},
                layout=widgets.Layout(width="auto"),
            )

            # Late-binding fix: pin opt_key as a default argument
            def on_change(change, ok=opt_key):
                self.store.set(self.chapter, self.q_key, ok, change["new"])

            cb.observe(on_change, names="value")
            self.checkboxes[opt_key] = cb

    def show(self):
        return widgets.VBox(list(self.checkboxes.values()))
