# EchoTrace: Whispering Objects

EchoTrace is an interactive storytelling installation designed for museums, galleries, and cultural heritage sites. It transforms objects into whispering narrators that share fragments of a larger story when visitors come near. Each “whisper node” uses a Raspberry Pi, a distance sensor, an LED, and a speaker to respond to movement and create a multisensory experience of curiosity and discovery.

As visitors explore, they hear pieces of a hidden story scattered among several artifacts. When enough fragments have been heard, a “mystery object” plays a final chapter that connects the pieces into a shared conclusion. Every step and pause becomes part of the interpretive process. Visitors learn through movement, listening, and reflection.

For museum staff, EchoTrace is designed to be easy to manage and adaptable to different exhibitions. It includes a browser-based dashboard for adjusting accessibility settings, calibrating sensors, loading new stories, and reviewing engagement data. The system runs entirely on a local network, without requiring internet access. EchoTrace demonstrates how physical computing and inclusive design can deepen engagement and learning in informal museum settings.

## Features

- **Distributed architecture (hub and nodes)**  
  The system includes a central “hub” Raspberry Pi and five “node” devices: four whispering objects and one mystery object. The hub manages coordination, content, and analytics, while each node handles sensing and playback. Communication uses **MQTT (Message Queuing Telemetry Transport)**, a lightweight messaging protocol common in Internet of Things systems. MQTT allows reliable communication across the local network even without internet access.

- **Proximity-responsive storytelling**  
  Each node uses a **VL53L1X time-of-flight sensor** to detect distance. At a distance, the object emits a faint whisper. As a visitor approaches, the story becomes clear and audible. This shifting soundscape connects movement and interpretation, making space and curiosity part of the learning experience.

- **Narrative unlock system**  
  The hub tracks which story fragments have played. When a configurable number of unique fragments have been heard, the hub signals the mystery object to play the final chapter. This encourages collaboration, since no single visitor can hear the entire story alone.

- **Accessibility and inclusion**  
  EchoTrace can be adapted to visitor needs. Features include captions and transcripts via QR codes, multilingual content in English, French, and Spanish, adjustable sound and light levels, high-contrast visual options, and sensory-friendly settings. Presets make it easy for staff to enable profiles such as “hard of hearing,” “low vision,” “sensory-friendly,” or “mobility-aware.”

- **Modular content packs**  
  Story content is stored in modular packs that contain YAML metadata, MP3 or WAV audio files, and multilingual HTML transcripts. Staff can replace or edit packs without programming. This makes the system reusable across exhibitions and adaptable to different stories and collections.

- **Offline analytics**  
  All visitor interactions are logged locally as CSV files on the hub. The dashboard summarizes engagement data such as number of triggers and completion rate. No personal information is collected, keeping data management simple and ethical.

## Visitor Interactions

1. **Attraction: the call of the whisper**  
   Faint sounds and soft light draw visitors closer. Each object seems alive and quietly invites approach.

2. **Embodied listening: movement as participation**  
   As a visitor approaches, the whisper becomes clear. The LED brightens, and optional haptic feedback adds a tactile rhythm. The visitor’s motion becomes part of the story experience.

3. **Interpretation through exploration**  
   Each object tells only a fragment. Visitors compare what they have heard, revisit objects, and scan QR codes for transcripts. The story becomes a puzzle to piece together.

4. **Shared discovery and the mystery reveal**  
   After enough fragments have been triggered—by one visitor or several—the mystery object plays the final chapter. The group experiences the conclusion together.

5. **Reflection and return**  
   Visitors often return to earlier objects to re-listen. This reflection deepens understanding and highlights how movement and curiosity shape interpretation.

## Admin Dashboard Highlights

The admin dashboard provides clear, real-time control over the installation. It is designed for museum staff and requires no programming knowledge. Each section offers visual feedback, simple controls, and instant updates through MQTT communication.

1. **Overview**  
   Displays the current content pack, node status, and progress toward the story’s conclusion. Administrators can pause or restart the experience and monitor system health.

2. **Nodes**  
   Lists all active nodes with their names, roles, and signal strength. Each entry includes quick tools to test LEDs, audio playback, and sensors. Administrators can push new settings or restart nodes remotely.

3. **Accessibility**  
   Lets staff enable captions, adjust brightness or volume, and switch between accessibility presets. Settings can be applied globally or per node. All updates take effect immediately.

4. **Content Management**  
   Allows staff to upload or activate new content packs, check language availability, and print new QR labels for transcripts. Metadata and audio links are displayed for verification before deployment.

5. **Calibration**  
   Shows live sensor readings and threshold distances. Staff can adjust placement or sensitivity while viewing real-time feedback to ensure smooth performance in the gallery space.

6. **Analytics**  
   Displays engagement statistics such as number of interactions, completion rates, and average time between triggers. CSV data can be exported for evaluation and reporting. The dashboard provides insights into how visitors are engaging without tracking individuals.

## Hardware Checklist

| Role | Core Hardware |
|------|----------------|
| Hub | Raspberry Pi 4 or 5, 32 GB microSD, Mosquitto MQTT broker, Flask dashboard |
| Whisper Nodes (×4) | Raspberry Pi Zero 2 W, VL53L1X sensor, LED + resistor, small amplifier + speaker, optional haptic motor |
| Mystery Node (×1) | Same as whisper node with finale audio content |
| Fabrication | 3D-printed bezels or LED holders (STL), laser-cut panels (DXF), mounting hardware |

See `docs/hardware_setup.md` for detailed wiring, installation, and maintenance instructions.

## Content Packs

- Stored under `content-packs/<pack-name>/` with YAML metadata, audio files, and HTML transcripts.  
- Each pack defines node roles, languages, and file mappings.  
- Transcripts are served locally at `/transcripts/<pack>/<filename>.html` and can be linked with QR codes.  
- See `docs/content_pack_guide.md` for authoring and localization details.

## Accessibility Suite

- Global toggles for captions, high-contrast mode, sensory-friendly playback, volume limits, mobility buffers, and quiet hours.  
- Presets for hearing, vision, sensory, and mobility support.  
- Per-node overrides for brightness, playback speed, repetition, and volume.  
- Accessibility profiles are saved in YAML and applied instantly through MQTT.

## Analytics and Privacy

- Logged events include `heartbeat_received`, `fragment_triggered`, `narrative_unlocked`, `config_push_ok`, `config_push_timeout`, and `admin_action`.  
- Dashboard summaries display counts, rates, and timing averages without collecting identifying data.  
- Data remain local to the hub unless exported by an administrator for evaluation.

## Educational and Learning Goals

- **Constructivist learning through storytelling**  
  Visitors build understanding by gathering and connecting story fragments. Each interaction becomes an act of investigation, mirroring how learning in museums often happens through exploration and curiosity.

- **Embodied cognition and spatial learning**  
  Movement is part of how visitors make sense of information. The sensors and light or sound feedback connect motion, perception, and interpretation, showing how physical engagement supports learning.

- **Collaborative and social learning**  
  No single visitor can hear the whole story alone. The design encourages sharing, discussion, and cooperative discovery, reflecting how people learn through social interaction.

- **Inclusive and multimodal participation**  
  Audio, light, vibration, and text work together so visitors with different sensory or linguistic backgrounds can participate. Accessibility features model Universal Design for Learning principles in a museum setting.

- **Reflection and metacognition**  
  The final mystery object encourages visitors to think about how they formed meaning. Revisiting earlier fragments promotes awareness of their own interpretive process.

## Quick Start (Development)

To set up a local development environment:

1. Create a virtual environment and install dependencies (runtime + tooling):
   ```
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt -r requirements-dev.txt
   ```
   The `make install` target performs the same steps.
2. Run the full verification suite:
   ```
   ruff check .
   mypy .
   pytest
   ```
   The Makefile provides shortcuts: `make lint`, `make typecheck`, `make test`, or `make verify` to run all three.
3. Run the hub and node services in mock mode for testing:
   - `make run-hub` starts the dashboard and listener in development mode.  
   - `make run-node` starts a mocked node service loop using test hardware mocks.

## Deployment Steps (Production)

1. Install the repository to `/opt/echotrace` on the hub and `/opt/echotrace-node` on each node.  
2. Create Python virtual environments and install dependencies.  
3. Configure environment variables in `/etc/default/echotrace` such as `ECHOTRACE_ADMIN_USER` and `ECHOTRACE_ADMIN_PASS`.  
4. Copy systemd unit files (`system/hub.service`, `system/node.service`), adjust paths, then enable them:
   ```
   sudo systemctl enable --now hub.service
   sudo systemctl enable --now node.service
   ```
5. Add content packs under `content-packs/`, verify audio paths, and select the active pack from the dashboard.

## License

Released under the MIT License. See `LICENSE` for details.
