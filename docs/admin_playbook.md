# Admin Playbook

This playbook outlines daily routines, accessibility management, troubleshooting, and maintenance tasks for EchoTrace – Whispering Objects.

## Daily Start-Up Checklist

1. **Inspect hardware** – Ensure all Raspberry Pi nodes, sensors, speakers, and power supplies are connected and free of strain.
2. **Power on** – Apply power to the hub (Raspberry Pi 4/5) and individual nodes (Pi Zero 2 W). LEDs on the nodes should glow faintly within 60 seconds.
3. **Verify network** – Confirm the local Wi-Fi or wired network is active. The hub unit must run the Mosquitto MQTT broker.
4. **Check dashboard health** – From a staff tablet or workstation on the same network, visit `http://<hub-ip>:8080/` and log in with the administrator credentials.
5. **Review analytics badge** – Confirm all nodes report heartbeats (Overview → Nodes panel). Address missing nodes before opening to visitors.

## Setting the Tone for the Day

- **Select a content pack** – Navigate to **Content** → choose the desired pack. The hub pushes fragment metadata to all nodes.
- **Choose accessibility mode** – In **Accessibility**, apply presets as needed (e.g., sensory-friendly mornings, hard-of-hearing tours). Verify the confirmation banner.
- **Test a whisper** – Approach each node to ensure audio, LED, and optional haptic responses fire correctly.

## During Public Hours

- Monitor the dashboard occasionally; the **Analytics** tab lists recent events and trigger counts. Spikes may indicate a popular object or repeated false triggers.
- Use the **Nodes** tab to push targeted adjustments (e.g., lower volume on a busy node) or log a planned restart.
- If accessibility needs change (quiet hour, mobility group), reapply presets or set per-node overrides without restarting hardware.

## Troubleshooting

| Symptom | Action |
|---------|--------|
| Node missing from heartbeats | Check power, sensor cables, then reboot the Pi Zero. In **Nodes**, use “Push Config” with a minimal payload to wake the MQTT client. |
| Audio distorted or silent | Confirm speaker connections and that the fragment file exists in the content pack. Push an accessibility override with a gentler volume or reload the content pack. |
| Mystery object never unlocks | Verify the `required_fragments_to_unlock` setting in `hub/config.yaml`. Confirm four unique nodes (by ID) triggered in the analytics table. |
| Dashboard inaccessible | Make sure the hub service is running (`sudo systemctl status echotrace-hub`). Check Mosquitto service status if hub logs show connection errors. |
| Excess triggers without visitors | The VL53 sensor may see reflections. Adjust the node’s proximity thresholds via per-node override or reposition the sensor to avoid glossy surfaces. |

## Accessibility Suite

- **Global toggles** – Captions, high contrast theme, sensory-friendly pacing (slower audio, lower volume), safety limiter, quiet hours (list of `HH:MM-HH:MM` ranges such as `"20:00-09:00"` that dim LEDs and lower volume automatically).
- **Presets** – Hard of hearing (captions, limiter), Low vision (captions, high contrast), Sensory friendly (lower volume/pace, limiter), Mobility aware (extra mobility buffer before playback).
- **Per-node overrides** – Adjust LED behaviour (`visual_pulse`, `proximity_glow`), haptic pacing (`repeat`, `pace`), mobility buffer, and per-node volume. Overrides persist in `hub/accessibility_profiles.yaml` and reapply on boot.

## Maintenance Schedule

- **Weekly** – Export analytics CSV for review; archive to secure storage. Inspect cabling and sensor mounts.
- **Monthly** – Update content packs or rotate to new narratives. Review system packages (`sudo apt update && sudo apt upgrade`) on all Pis. Check available disk space on the hub.
- **Quarterly** – Back up the repository (`/opt/echotrace`) and content packs to external storage. Test UPS or power conditioning equipment if present.

## Backup and Restore

1. Stop services: `sudo systemctl stop echotrace-hub echotrace-node` on each device.
2. Copy `/opt/echotrace` (hub) or `/opt/echotrace-node` (node) to an external drive.
3. Restore by copying the directories back, reinstalling Python dependencies (`pip install -r requirements.txt`), and re-enabling services.

## Security & Privacy

- Change administrator credentials regularly (`ECHOTRACE_ADMIN_USER`, `ECHOTRACE_ADMIN_PASS`).
- Keep the hub on a private museum VLAN with no external internet exposure.
- Do not ingest visitor identifiers; transcripts are static and audio playback is one-way.

By following this playbook, facilitators can keep EchoTrace responsive, inclusive, and ready for iterative interpretation with museum audiences.
