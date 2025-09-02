class MockDispatcher:
    def dispatch(self, intent: str) -> None:
        print(f"[ACTION] {intent}")
