"""Node-side MQTT topic helpers aligned with the hub definitions."""

from __future__ import annotations

from typing_extensions import Final


_PREFIX: Final[str] = "ECHOTRACE"
_HEALTH_TEMPLATE: Final[str] = f"{_PREFIX}/health/{{node_id}}"
_TRIGGER_TEMPLATE: Final[str] = f"{_PREFIX}/trigger/{{node_id}}"
_STATE_HUB: Final[str] = f"{_PREFIX}/state/hub"
_CONFIG_TEMPLATE: Final[str] = f"{_PREFIX}/config/{{node_id}}"
_ACK_TEMPLATE: Final[str] = f"{_PREFIX}/ack/{{node_id}}"


def health_topic(node_id: str) -> str:
    """Return the health topic for the provided node identifier."""
    return _HEALTH_TEMPLATE.format(node_id=node_id)


def trigger_topic(node_id: str) -> str:
    """Return the trigger topic for the provided node identifier."""
    return _TRIGGER_TEMPLATE.format(node_id=node_id)


def hub_state_topic() -> str:
    """Return the topic where the hub publishes state updates."""
    return _STATE_HUB


def node_config_topic(node_id: str) -> str:
    """Return the configuration topic for this node."""
    return _CONFIG_TEMPLATE.format(node_id=node_id)


def node_ack_topic(node_id: str) -> str:
    """Return the acknowledgement topic for this node."""
    return _ACK_TEMPLATE.format(node_id=node_id)


__all__ = [
    "health_topic",
    "trigger_topic",
    "hub_state_topic",
    "node_config_topic",
    "node_ack_topic",
]
