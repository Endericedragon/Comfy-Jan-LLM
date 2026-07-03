from pathlib import Path
from typing import Dict


class MarkdownWatcher:
    def __init__(self, path_to_watch: Path | str) -> None:
        if isinstance(path_to_watch, str):
            self.path = Path(path_to_watch)
        else:
            self.path = path_to_watch

    def inspect(self) -> Dict[str, Path]:
        return {each.name: each for each in self.path.glob("*.md")}


if __name__ == "__main__":
    watcher = MarkdownWatcher(Path(__file__).parent / "default_prompts")
    for file in watcher.inspect():
        print(file)
