"""MQTT topic helpers used across EchoTrace components."""

from __future__ import annotations

from typing_extensions import Final


_PREFIX: Final[str] = "ECHOTRACE"
_HEALTH_TEMPLATE: Final[str] = f"{_PREFIX}/health/{{node_id}}"
_TRIGGER_TEMPLATE: Final[str] = f"{_PREFIX}/trigger/{{node_id}}"
_STATE_HUB: Final[str] = f"{_PREFIX}/state/hub"
_CONFIG_TEMPLATE: Final[str] = f"{_PREFIX}/config/{{node_id}}"
_ACK_TEMPLATE: Final[str] = f"{_PREFIX}/ack/{{node_id}}"
_HEALTH_WILDCARD: Final[str] = f"{_PREFIX}/health/+"
_TRIGGER_WILDCARD: Final[str] = f"{_PREFIX}/trigger/+"
_ACK_WILDCARD: Final[str] = f"{_PREFIX}/ack/+"


def health_topic(node_id: str) -> str:
    """Return the health topic for a given node identifier."""
    return _HEALTH_TEMPLATE.format(node_id=node_id)


def trigger_topic(node_id: str) -> str:
    """Return the trigger topic for a given node identifier."""
    return _TRIGGER_TEMPLATE.format(node_id=node_id)


def hub_state_topic() -> str:
    """Return the topic used for publishing hub state updates."""
    return _STATE_HUB


def node_config_topic(node_id: str) -> str:
    """Return the configuration topic for a specific node."""
    return _CONFIG_TEMPLATE.format(node_id=node_id)


def node_ack_topic(node_id: str) -> str:
    """Return the acknowledgement topic for a specific node."""
    return _ACK_TEMPLATE.format(node_id=node_id)


def health_wildcard() -> str:
    """Return the wildcard subscription topic for node health."""
    return _HEALTH_WILDCARD


def trigger_wildcard() -> str:
    """Return the wildcard subscription topic for node triggers."""
    return _TRIGGER_WILDCARD


def ack_wildcard() -> str:
    """Return the wildcard subscription topic for node acknowledgements."""
    return _ACK_WILDCARD


__all__ = [
    "health_topic",
    "trigger_topic",
    "hub_state_topic",
    "node_config_topic",
    "node_ack_topic",
    "health_wildcard",
    "trigger_wildcard",
    "ack_wildcard",
]
