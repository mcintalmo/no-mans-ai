import json
import logging
import socket
import threading
import time
from typing import Any

logger = logging.getLogger(__name__)


class LuaSocketDispatcher:
    """
    Sends newline-delimited JSON commands to a local TCP server (Lua bridge).
    Intended message format:
      {"intent": "launch", "args": {"speed": "boost"}, "timestamp": 1725140000.12, "source": "nms_copilot"}
    """

    def __init__(
        self,
        host: str = "0.0.0.0",
        port: int = 8765,
        connect_timeout: float = 2.0,
        send_timeout: float = 2.0,
        auto_reconnect: bool = True,
    ) -> None:
        self.host = host
        self.port = port
        self.connect_timeout = connect_timeout
        self.send_timeout = send_timeout
        self.auto_reconnect = auto_reconnect

        self._sock: socket.socket | None = None
        self._lock = threading.Lock()

        self._connect()

    def _connect(self) -> None:
        self._close()
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(self.connect_timeout)
        try:
            s.connect((self.host, self.port))
            s.settimeout(self.send_timeout)
            # Disable Nagle to reduce latency for small messages
            try:
                s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
            except Exception:
                pass
            self._sock = s
            logger.info(f"[LuaSocket] Connected to {self.host}:{self.port}")
        except Exception as e:
            self._sock = None
            logger.exception(f"[LuaSocket] Connect failed: {e}")

    def _close(self) -> None:
        if self._sock:
            try:
                self._sock.close()
            except Exception:
                pass
            finally:
                self._sock = None

    def _send_json_line(self, message: dict[str, Any]) -> bool:
        data = (json.dumps(message, separators=(",", ":")) + "\n").encode(
            "utf-8"
        )
        with self._lock:
            if not self._sock:
                if not self.auto_reconnect:
                    return False
                self._connect()
                if not self._sock:
                    return False
            try:
                self._sock.sendall(data)
                return True
            except Exception as e:
                logger.exception(f"[LuaSocket] Send failed: {e}")
                # Try one reconnect attempt
                self._connect()
                if not self._sock:
                    return False
                try:
                    self._sock.sendall(data)
                    return True
                except Exception as e2:
                    logger.exception(f"[LuaSocket] Resend failed: {e2}")
                    return False

    def dispatch(
        self,
        intent: str,
        args: dict[str, Any] | None = None,
    ) -> None:
        """
        Dispatch an intent with optional args to the Lua bridge.
        Signature is compatible with simple dispatchers that only use `intent`.
        """
        payload = {
            "intent": intent,
            "args": args or {},
            "timestamp": time.time(),
            "source": "nms_copilot",
        }
        ok = self._send_json_line(payload)
        if ok:
            logger.info(f"[ACTION→Lua] {intent} {args or ''}")
        else:
            logger.warning(f"[LuaSocket] Failed to deliver intent: {intent}")

    def close(self) -> None:
        self._close()
