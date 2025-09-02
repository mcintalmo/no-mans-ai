import logging

from dispatchers.lua_socket import LuaSocketDispatcher
from dispatchers.mock import MockDispatcher
from intents.regex_parser import RegexParser
from stt.vosk_engine import VoskSTT
from utils.config_loader import load_config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def build_dispatcher(config: dict) -> MockDispatcher | LuaSocketDispatcher:
    engine = config["dispatcher"]["engine"]
    if engine == "lua_socket":
        s = config["dispatcher"].get("lua_socket", {})
        return LuaSocketDispatcher(
            host=s.get("host", "0.0.0.0"),
            port=int(s.get("port", 8765)),
            connect_timeout=float(s.get("connect_timeout", 2.0)),
            send_timeout=float(s.get("send_timeout", 2.0)),
        )
    # fallback
    return MockDispatcher()


def main() -> None:
    # Load config
    config = load_config("config.yaml")

    # Initialize components
    stt_engine = VoskSTT(model_path=config["stt"]["model_path"])
    parser = RegexParser(commands=config["commands"])
    dispatcher = build_dispatcher(config)

    logger.info("No-Man's AI is listening...")

    for transcript in stt_engine.listen():
        logger.info(f"[STT] {transcript}")
        intent = parser.parse(transcript)
        if intent:
            dispatcher.dispatch(intent)
        else:
            logger.info("[Parser] No match")


if __name__ == "__main__":
    main()
