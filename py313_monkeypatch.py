import sys
import types


def monkeypatch() -> None:
    audioop_stub = types.ModuleType("audioop")
    sys.modules["audioop"] = audioop_stub