"""Pytest configuration for scaffold tests."""

from __future__ import annotations

import sys
import types
from typing import Generator

import pytest


@pytest.fixture(autouse=True)
def mock_hardware_modules() -> Generator[None, None, None]:
    """Provide lightweight stand-ins for hardware-specific libraries."""
    created_modules: list[str] = []

    if "gpiozero" not in sys.modules:
        gpiozero = types.ModuleType("gpiozero")

        class _PWMLED:  # type: ignore[no-redef]
            """Mock PWM LED for testing without hardware."""

            def __init__(self, pin: int, frequency: int | None = None) -> None:
                """Initialise the mock LED on the specified pin."""
                self.pin = pin
                self.frequency = frequency
                self.value = 0.0

            def blink(self, on_time: float, off_time: float) -> None:
                self.value = 0.5

            def off(self) -> None:
                self.value = 0.0

            def close(self) -> None:
                self.value = 0.0

        class _DigitalOutputDevice:  # type: ignore[no-redef]
            """Mock digital output device for testing without hardware."""

            def __init__(self, pin: int, active_high: bool = True) -> None:
                """Initialise the mock device on the specified pin."""
                self.pin = pin
                self.active_high = active_high
                self.state = False

            def blink(
                self,
                on_time: float,
                off_time: float,
                n: int | None = None,
            ) -> None:
                """Simulate a blink pattern."""
                del n  # Unused parameter
                self.state = True

            def on(self) -> None:
                self.state = True

            def off(self) -> None:
                self.state = False

            def close(self) -> None:
                self.off()

        gpiozero.PWMLED = _PWMLED  # type: ignore[attr-defined]
        gpiozero.DigitalOutputDevice = _DigitalOutputDevice  # type: ignore[attr-defined]
        sys.modules["gpiozero"] = gpiozero
        created_modules.append("gpiozero")

    if "pygame" not in sys.modules:
        pygame = types.ModuleType("pygame")

        class _Music:
            """Mock music mixer for testing without pygame."""

            def __init__(self) -> None:
                """Initialise the mock music mixer."""
                self.volume = 1.0

            def load(self, path: str) -> None:
                """Record the loaded audio path."""
                self.last_loaded = path

            def play(self, loops: int = 0) -> None:
                """Simulate playback with the specified loop count."""
                self.is_playing = loops

            def stop(self) -> None:
                self.is_playing = 0

            def set_volume(self, value: float) -> None:
                self.volume = value

        class _Mixer:
            def __init__(self) -> None:
                self._init = False
                self.music = _Music()

            def init(self) -> None:
                self._init = True

            def get_init(self) -> bool:
                return self._init

            def quit(self) -> None:
                self._init = False

        pygame.mixer = _Mixer()  # type: ignore[attr-defined]
        sys.modules["pygame"] = pygame
        sys.modules["pygame.mixer"] = pygame.mixer  # type: ignore[assignment]
        created_modules.append("pygame")
        created_modules.append("pygame.mixer")

    try:
        yield
    finally:
        for module_name in created_modules:
            sys.modules.pop(module_name, None)
