"""Audio playback helpers for EchoTrace node devices."""

from __future__ import annotations

import os
import tempfile
import wave
import logging
from pathlib import Path
from threading import Lock
from typing import Optional

try:  # pragma: no cover - executed when pygame is available
    from pygame import mixer
except ImportError:  # pragma: no cover - executed in test/mock environments
    mixer = None  # type: ignore[assignment]


LOGGER = logging.getLogger(__name__)


class AudioPlayer:
    """Provide a thin wrapper around pygame.mixer with safety limiting."""

    def __init__(self) -> None:
        self._loaded_path: Optional[Path] = None
        self._temp_audio: Optional[Path] = None
        self._temp_lock = Lock()
        self._safety_limit: float = 1.0
        self._mixer_available = mixer is not None
        if self._mixer_available and not mixer.get_init():  # type: ignore[union-attr]
            try:
                mixer.init()  # type: ignore[union-attr]
                LOGGER.info("pygame.mixer initialised for audio playback.")
            except Exception as exc:  # pragma: no cover
                LOGGER.warning("Failed to initialise pygame.mixer: %s", exc)
                self._mixer_available = False

    def load(self, path: Path) -> None:
        """Store the path to the audio file to be played later."""
        self._cleanup_temp_audio()
        self._loaded_path = path
        LOGGER.debug("Audio fragment ready: %s", path)

    def set_safety_limit(self, limit: float) -> None:
        """Set the maximum volume permitted for safety policies."""
        self._safety_limit = max(0.0, min(1.0, limit))

    def set_volume(self, value_0_to_1: float) -> None:
        """Adjust output volume if the mixer is present, respecting the safety limit."""
        requested = max(0.0, min(1.0, value_0_to_1))
        effective = min(requested, self._safety_limit)
        if not self._mixer_available or mixer is None:
            LOGGER.debug("Volume request %.2f ignored; mixer unavailable.", effective)
            return
        mixer.music.set_volume(effective)  # type: ignore[union-attr]
        LOGGER.debug("Volume set to %.2f (requested %.2f).", effective, requested)

    def play(self, loop: bool = False, pace: float = 1.0, repeat: int = 0) -> None:
        """
        Start playback for the loaded clip if supported.

        The repeat parameter maps to pygame's loop count while still supporting a loop flag.
        """
        if self._loaded_path is None:
            LOGGER.warning("No audio loaded; play() ignored.")
            return
        if not self._mixer_available or mixer is None:
            LOGGER.info("Play request for %s ignored; mixer unavailable.", self._loaded_path)
            return
        target = self._select_playback_source(pace)
        temp_source = self._temp_audio if self._temp_audio and target == self._temp_audio else None
        loops = repeat if repeat > 0 else (-1 if loop else 0)
        try:
            mixer.music.load(str(target))  # type: ignore[union-attr]
            mixer.music.play(loops)  # type: ignore[union-attr]
            LOGGER.debug(
                "Playback started for %s (loops=%s pace=%.2f).",
                target,
                loops,
                pace,
            )
        except Exception as exc:  # pragma: no cover
            LOGGER.error("Failed to play audio %s: %s", self._loaded_path, exc)
        finally:
            if temp_source is not None:
                self._cleanup_temp_audio()

    def stop(self) -> None:
        """Stop playback when supported."""
        if not self._mixer_available or mixer is None:
            LOGGER.debug("Stop request ignored; mixer unavailable.")
            return
        mixer.music.stop()  # type: ignore[union-attr]

    def _select_playback_source(self, pace: float) -> Path:
        """Return the audio path to use, transforming it when pace changes."""
        if self._loaded_path is None:
            raise RuntimeError("Audio fragment not loaded.")
        if not self._mixer_available or abs(pace - 1.0) < 0.02:
            return self._loaded_path
        paced = self._make_paced_copy(pace)
        if paced is None:
            return self._loaded_path
        return paced

    def _make_paced_copy(self, pace: float) -> Optional[Path]:
        """Create a temporary WAV with modified sample rate to adjust playback."""
        assert self._loaded_path is not None
        if self._loaded_path.suffix.lower() != ".wav":
            LOGGER.debug(
                "Playback pace adjustments require WAV assets; using original clip %s.",
                self._loaded_path,
            )
            return None
        self._cleanup_temp_audio()
        fd, temp_name = tempfile.mkstemp(prefix="echotrace_paced_", suffix=".wav")
        os.close(fd)
        temp_path = Path(temp_name)
        try:
            with wave.open(str(self._loaded_path), "rb") as source:
                params = source.getparams()
                frames = source.readframes(params.nframes)
            with wave.open(str(temp_path), "wb") as dest:
                new_rate = max(500, int(params.framerate * pace))
                dest.setnchannels(params.nchannels)
                dest.setsampwidth(params.sampwidth)
                dest.setframerate(new_rate)
                dest.writeframes(frames)
        except (OSError, wave.Error) as exc:
            LOGGER.warning("Unable to prepare paced audio for %s: %s", self._loaded_path, exc)
            temp_path.unlink(missing_ok=True)
            return None
        with self._temp_lock:
            self._temp_audio = temp_path
        return temp_path

    def _cleanup_temp_audio(self) -> None:
        """Remove any generated paced audio clip."""
        with self._temp_lock:
            if self._temp_audio is None:
                return
            target = self._temp_audio
            self._temp_audio = None
        try:
            target.unlink(missing_ok=True)
        except OSError:
            LOGGER.debug("Failed to remove temporary paced audio %s", target)

    def __del__(self) -> None:  # pragma: no cover - best-effort cleanup
        self._cleanup_temp_audio()


__all__ = ["AudioPlayer"]
