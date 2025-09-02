import re


class RegexParser:
    def __init__(self, commands: dict[str, dict[str, list[str]]]) -> None:
        self.commands = {}
        for intent, patterns in commands.items():
            sub_patterns = patterns.get("patterns", [])
            full_pattern = "|".join(sub_patterns)
            self.commands[intent] = f"({full_pattern})"
        print(self.commands)

    def parse(self, text: str) -> str | None:
        for intent, pattern in self.commands.items():
            if re.search(pattern, text):
                return intent
        return None
