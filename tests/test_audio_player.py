"""Tests for the AudioPlayer pacing helpers."""

from __future__ import annotations

import wave
from pathlib import Path

from pi_nodes.audio_player import AudioPlayer


def _write_wav(path: Path) -> None:
    with wave.open(str(path), "wb") as handle:
        handle.setnchannels(1)
        handle.setsampwidth(2)
        handle.setframerate(44100)
        handle.writeframes(b"\x00\x00" * 100)


def test_make_paced_copy_creates_and_cleans(tmp_path: Path) -> None:
    """A paced copy should be created for WAVs and cleaned when requested."""
    wav_path = tmp_path / "clip.wav"
    _write_wav(wav_path)

    player = AudioPlayer()
    player.load(wav_path)

    paced = player._make_paced_copy(0.9)
    assert paced is not None
    assert paced.exists()

    AudioPlayer.cleanup_temp_file(paced)
    assert not paced.exists()


def test_make_paced_copy_ignored_for_non_wav(tmp_path: Path) -> None:
    """Non-WAV assets should not attempt to create paced copies."""
    mp3_path = tmp_path / "clip.mp3"
    mp3_path.write_bytes(b"dummy")

    player = AudioPlayer()
    player.load(mp3_path)

    assert player._make_paced_copy(0.9) is None
