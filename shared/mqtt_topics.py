"""MQTT topic helpers used across EchoTrace hub and node components.

This module defines a single source of truth for all MQTT topic patterns
used in the EchoTrace system. Both the hub and pi_nodes packages should
import from this module to ensure consistent topic naming.
"""

from __future__ import annotations

from typing_extensions import Final


PREFIX: Final[str] = "ECHOTRACE"

_HEALTH_TEMPLATE: Final[str] = f"{PREFIX}/health/{{node_id}}"
_TRIGGER_TEMPLATE: Final[str] = f"{PREFIX}/trigger/{{node_id}}"
_STATE_HUB: Final[str] = f"{PREFIX}/state/hub"
_CONFIG_TEMPLATE: Final[str] = f"{PREFIX}/config/{{node_id}}"
_ACK_TEMPLATE: Final[str] = f"{PREFIX}/ack/{{node_id}}"

_HEALTH_WILDCARD: Final[str] = f"{PREFIX}/health/+"
_TRIGGER_WILDCARD: Final[str] = f"{PREFIX}/trigger/+"
_ACK_WILDCARD: Final[str] = f"{PREFIX}/ack/+"


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
    "PREFIX",
    "ack_wildcard",
    "health_topic",
    "health_wildcard",
    "hub_state_topic",
    "node_ack_topic",
    "node_config_topic",
    "trigger_topic",
    "trigger_wildcard",
]
