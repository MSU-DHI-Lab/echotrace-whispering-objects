"""Proximity sensor abstraction for EchoTrace nodes."""

from __future__ import annotations

import logging
from typing import Iterable, Optional

LOGGER = logging.getLogger(__name__)

try:  # pragma: no cover - executed only on hardware
    import board
    import busio
    import adafruit_vl53l1x
except ImportError:  # pragma: no cover - executed in development environments
    board = None  # type: ignore[assignment]
    busio = None  # type: ignore[assignment]
    adafruit_vl53l1x = None  # type: ignore[assignment]


class ProximitySensor:
    """Read distance measurements from a VL53L1X sensor with graceful fallback."""

    def __init__(self, i2c_bus: Optional[int] = None, address: Optional[int] = None) -> None:
        self._fallback_distance = 900
        self._sensor = None

        if board is None or busio is None or adafruit_vl53l1x is None:
            LOGGER.info("VL53L1X dependencies unavailable; using fallback distances.")
            return

        try:  # pragma: no cover - requires hardware
            if i2c_bus is not None:
                i2c = busio.I2C(board.SCL, board.SDA, frequency=400000)
            else:
                i2c = busio.I2C(board.SCL, board.SDA)
            self._sensor = adafruit_vl53l1x.VL53L1X(i2c, address=address)
            self._sensor.distance_mode = 1  # short range for museum settings
            self._sensor.timing_budget = 33
            LOGGER.info("VL53L1X sensor initialised successfully.")
        except Exception as exc:  # pragma: no cover - requires hardware
            self._sensor = None
            LOGGER.warning("Failed to initialise VL53L1X sensor: %s", exc)

    @property
    def status(self) -> str:
        """Return the current status of the sensor."""
        if self._sensor is not None:
            return "hardware"
        return "fallback"

    def read_distance_mm(self) -> Optional[int]:
        """Return the measured distance in millimetres or a fallback value."""
        if self._sensor is None:
            return self._fallback_distance
        try:  # pragma: no cover - requires hardware
            distance = self._sensor.distance
            if distance is None:
                return None
            return int(distance)
        except Exception as exc:
            LOGGER.debug("Error reading distance: %s", exc)
            return None


class MockProximitySensor(ProximitySensor):
    """Simple mockable proximity sensor used in tests."""

    def __init__(self, distances: Optional[Iterable[int | None]] = None) -> None:
        super().__init__()
        self._distances = list(distances or [900])
        self._index = 0

    def read_distance_mm(self) -> Optional[int]:
        if not self._distances:
            return None
        result = self._distances[min(self._index, len(self._distances) - 1)]
        self._index += 1
        return result


__all__ = ["ProximitySensor", "MockProximitySensor"]
