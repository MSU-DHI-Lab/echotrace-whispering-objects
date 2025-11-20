# Accessibility Guide

EchoTrace’s Accessibility Suite ensures that different sensory, cognitive, and mobility needs are supported without compromising privacy.

## Principles

- **Multiple modalities** – Every fragment is available as audio, haptic pulse (optional), LED lighting, and QR transcript.
- **Configurable environment** – Staff can adjust global settings or per-node overrides in seconds, letting them tailor the experience to scheduled programs or spontaneous visitor needs.
- **No tracking of individuals** – Adjustments affect environmental output only; no user accounts or recordings are created.

## Global Settings

Accessible via the dashboard’s **Accessibility** tab:

- **Captions** – Highlights transcript availability in the UI; QR codes remain active regardless of toggle.
- **High contrast** – Applies a bold contrast theme to the dashboard for facilitators or visitors using shared screens.
- **Sensory-friendly mode** – Lowers default volume, slows pacing, and sets gentle LED glow to reduce overstimulation.
- **Safety limiter** – Caps maximum audio volume across nodes (enabled by default).
- **Mobility buffer** – Adds a delay (in milliseconds) before audio triggers, useful for visitors using mobility devices.
- **Quiet hours** – List of time ranges in `HH:MM-HH:MM` (e.g., `"18:00-09:00"`) which dim LEDs, pause visual pulses, and reduce volume during calm periods.

## Presets

- **Hard of Hearing** – Captions + safety limiter emphasised.
- **Low Vision** – High contrast dashboard and guaranteed captions.
- **Sensory Friendly** – Sensory-friendly mode with strict limiter and calmer LEDs.
- **Mobility Aware** – Adds a 1000 ms mobility buffer to all nodes.

Presets can be layered with manual adjustments. Applying a preset updates `hub/accessibility_profiles.yaml` and pushes new runtime configuration to each node.

## Per-Node Overrides

Staff can highlight specific narratives or accommodate visitors at a particular station by overriding:

- `visual_pulse` – Blink LED rather than steady glow during story playback.
- `proximity_glow` – Enable/disable ambient glow to reduce distraction.
- `mobility_buffer_ms` – Extra delay before audio plays (0–60,000 ms).
- `repeat` – Number of automatic replays (0–2) for visitors who want more processing time.
- `pace` – Playback rate (0.85–1.15) for nuanced comprehension (applies directly when fragments are packaged as WAV files; other formats fall back to default speed).
- `safety_limiter` – Relax or enforce the limiter locally.
- `volume` – Optional per-node volume cap (0.0–1.0) when fine control is needed.

Overrides persist across reboots and deploy instantly via MQTT.

## Transcripts & QR Codes

Each transcript includes a short contextual paragraph, reflective prompt, and accessibility note. Print the corresponding QR codes near objects at a reachable height. For tactile labels, include braille or large-print cues indicating that audio is available nearby.

## Haptics & Sensory Management

- Haptics default to ON but can be disabled by removing the transistor or unchecking `visual_pulse`/`proximity_glow` for calmer feedback.
- Sensory-friendly mode automatically reduces LED intensity and audio volume, benefiting visitors with sensory processing differences.
- Quiet hours bring the installation into a calm state for meditation sessions, after-hours tours, or rest periods.

By adjusting these controls dynamically, facilitators ensure Whispering Objects remains inclusive while preserving its collaborative storytelling intent.
