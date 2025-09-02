import json
import logging
import queue
from collections.abc import Generator
from typing import Any, NoReturn

import sounddevice as sd
from vosk import KaldiRecognizer, Model

logger = logging.getLogger(__name__)


class VoskSTT:
    def __init__(self, model_path: str) -> None:
        logger.info(f"Loading Vosk model from {model_path}")
        self.model = Model(model_path)
        self.queue: queue.Queue[bytes] = queue.Queue()

    def _callback(
        self,
        indata: bytes,
        frames: int,
        time,
        status: sd.CallbackFlags,
    ) -> None:
        if status:
            logger.info(status)
        self.queue.put(bytes(indata))

    def listen(self) -> Generator[Any, Any, NoReturn]:
        with sd.RawInputStream(
            samplerate=16000,
            blocksize=8000,
            dtype="int16",
            channels=1,
            callback=self._callback,
        ):
            rec = KaldiRecognizer(self.model, 16000)
            while True:
                data = self.queue.get()
                if rec.AcceptWaveform(data):
                    result = json.loads(rec.Result())
                    text = result.get("text", "").strip().lower()
                    if text:
                        yield text
