"""
build_portfolio.py
Generates individual deep-dive project pages and updates index.html for piksliviksi.github.io
"""
import os
import json

SYSTEMS = [
    {
        "id": "01",
        "slug": "huginn",
        "name": "HUGINN",
        "domain": "Alternative PNT",
        "role": "Autonomous GPS-Denied UAV Navigation & Sensor Fusion System",
        "platform": "Jetson AGX Orin / Raspberry Pi Zero 2W / Pixhawk (PX4 / ArduPilot)",
        "protocol": "MAVLink (VISION_POSITION_ESTIMATE) / DVB-T2 / LTE",
        "classification": "SOVEREIGN DEFENSE SPECIFICATION",
        "status": None,
        "primary_image": "huginn2.jpg",
        "secondary_image": None,
        "thumbnail_labels": [
            "GPS-Denied UAV Navigation Core",
            "DVB-T2 Broadcast Tower Pseudoranges (Airspy Mini)",
            "Terrestrial LTE Cell Tower Triangulation",
            "TERCOM Terrain Contour Elevation Matching",
            "DSMAC Optical Scene-Matching Area Correlation",
            "Direct QGC-Simulator SITL/HITL Compatibility",
            "8-State Extended Kalman Filter (EKF) FusionEngine",
            "PX4/ArduPilot EKF2 Injection via VISION_POSITION_ESTIMATE"
        ],
        "summary": "HUGINN is an autonomous navigation system for tactical unmanned aerial vehicles (fixed-wing and hybrid VTOL) operating in contested, GPS-denied environments. By synthesizing terrestrial signals of opportunity (DVB-T2 and LTE), radar/optical terrain contour matching, and visual scene correlation, HUGINN maintains sub-meter to tens-of-meters localization when GPS is jammed or spoofed.",
        "what_it_does": [
            "Maintains high-confidence 3D position, velocity, and attitude estimates during total GNSS outages, jamming, or deceptive satellite spoofing attacks.",
            "Replaces traditional satellite positioning by dynamically harvesting ambient terrestrial radio frequency broadcasts and physical ground topology.",
            "Injects real-time synthetic position updates directly into PX4 or ArduPilot autopilot flight computers, ensuring flight stability, mission continuation, and return-to-base capabilities.",
            "Integrates seamless failover finite state machines (FSM) that continuously monitor GNSS signal health and switch to alternative PNT sources without human intervention.",
            "Supports both tactical fixed-wing high-endurance cruising and VTOL quad-plane launch/recovery profiles."
        ],
        "how_it_works": [
            "**DVB-T2 Signals of Opportunity (SoOP)**: Uses an Airspy Mini SDR to intercept terrestrial digital television signals from Levira broadcast towers. Implements the MUSIC (Multiple Signal Classification) super-resolution algorithm, phase-locked loops (PLL), and Gauss-Newton non-linear solvers to measure pseudoranges from transmitter towers with known coordinates.",
            "**Cellular Triangulation**: Taps ambient LTE base stations, harvesting Cell IDs (CID) and measuring signal metrics (RSRP/RSSI) against an offline geocoded tower database to provide robust coarse positioning constraints.",
            "**TERCOM (Terrain Contour Matching)**: Samples surface elevation clearance beneath the aircraft and matches elevation profiles against pre-loaded high-resolution Digital Elevation Models (DEM) via sliding-window normalized cross-correlation.",
            "**DSMAC (Digital Scene-Matching Area Correlation)**: Downward-looking optical cameras track ground landmarks, comparing real-time frames with georeferenced satellite imagery to eliminate cumulative inertial drift.",
            "**8-State EKF FusionEngine**: An 8-state Extended Kalman Filter fuses RF pseudoranges, cell multilateration, TERCOM fixes, and DSMAC optical vectors into a single unified navigation solution.",
            "**Autopilot Telemetry Bridge**: Bridges fused estimates into MAVLink `VISION_POSITION_ESTIMATE` messages streamed at 20-50 Hz into PX4 or ArduPilot EKF2 state estimators, transparently keeping the drone on mission."
        ],
        "hardware_specs": [
            {"component": "Navigation Computer", "spec": "NVIDIA Jetson AGX Orin (64GB, 275 TOPS) for neural DSMAC vision & terrain correlation; or Raspberry Pi Zero 2W for low-SWaP lightweight deployments"},
            {"component": "RF Frontend Receiver", "spec": "Airspy Mini SDR (high-dynamic range frontend tuned for DVB-T2 UHF 470–862 MHz and GSM/LTE 800–1800 MHz)"},
            {"component": "GNSS Subsystem", "spec": "Septentrio mosaic-X5 multi-constellation RTK GNSS receiver with AIM+ anti-jamming/anti-spoofing; secondary u-blox backup"},
            {"component": "Autopilot Flight Controller", "spec": "Pixhawk 6X / Cube Orange running PX4 or ArduPilot firmware"},
            {"component": "IMU / Bridge Firmware", "spec": "NodeMCU ESP8266 high-rate serial/SPI hardware bridge"},
            {"component": "Airframe Platform", "spec": "Composite tactical fixed-wing / VTOL airframe with forward tractor prop and 4-motor VTOL quad-lift booms"}
        ],
        "software_specs": [
            {"layer": "Operating System", "detail": "Ubuntu 22.04 LTS (Jetson Linux BSP) / Kali Linux ARM64 (Pi Zero 2W)"},
            {"layer": "DSP & RF Processing", "detail": "Custom C++ / Python signal processing pipeline using NumPy, SciPy, and pyadi-iio"},
            {"layer": "GCS & Control", "detail": "Custom QGroundControl build with HUGINN custom status bar and emergency GPS-OFF buttons"},
            {"layer": "Web Management API", "detail": "Lightweight Flask server hosting real-time map UI, telemetry visualizer, and REST endpoints (port 8080)"}
        ],
        "tags": ["Alternative PNT", "GPS-Denied", "DVB-T2", "TERCOM", "DSMAC", "PX4 EKF2", "Jetson Orin", "Airspy Mini", "Autonomous UAV"]
    },
    {
        "id": "02",
        "slug": "crow",
        "name": "CROW",
        "domain": "RF & EW",
        "role": "Ground-Based Mobile Passive Radar System",
        "platform": "Tactical Vehicle Mount / Mobile Mast / Ruggedized Workstation",
        "protocol": "Phase-Coherent IQ Streaming / High-Speed Gigabit Optical Link",
        "classification": "SOVEREIGN DEFENSE SPECIFICATION",
        "status": "PROTOTYPE VALIDATED",
        "primary_image": "CROW.jpg",
        "secondary_image": None,
        "thumbnail_labels": [
            "Ground-Based Passive Radar System",
            "Ambient Emitter Reception (Signals of Opportunity)",
            "Reflection Detecting & Tracking (Target Echoes)",
            "No-Transmission Stealth (Zero Electromagnetic Signature)",
            "Bistatic Radar Processing (Multi-path Cancellation & Coherent Integration)",
            "Target Classification (Doppler Signature & Emitter ID Identification)",
            "Ground Station Mobile Deployment (Tactical 4x4 / Mast)"
        ],
        "summary": "CROW is a ground-based passive radar surveillance system engineered for covert detection, tracking, and classification of aerial and surface targets. By exploiting ambient civilian and commercial RF signals of opportunity without emitting radiation, CROW operates in complete electromagnetic silence, rendering it undetectable to enemy electronic support measures (ESM) and immune to anti-radiation missiles.",
        "what_it_does": [
            "Detects and tracks airborne targets (including low-RCS drones, fixed-wing aircraft, and cruise missiles) without transmitting any RF signals.",
            "Eliminates the vulnerability of conventional active radar stations, which act as immediate beacons for hostile anti-radiation missiles and electronic jamming.",
            "Operates covertly from mobile tactical vehicles (such as 4x4 light tactical vehicles) or rapidly deployable ground masts.",
            "Classifies detected targets based on micro-Doppler signatures, propeller blade modulations, and jet engine turbine echo characteristics.",
            "Fuses multi-static reflection data across multiple transmitter baselines to calculate 3D Cartesian coordinates and heading vectors."
        ],
        "how_it_works": [
            "**Ambient Illuminators of Opportunity**: Exploits non-cooperative ambient broadcasts such as commercial FM radio (88–108 MHz), digital television (DVB-T/DVB-T2), and 4G/5G cellular base stations as illumination sources.",
            "**Reference & Surveillance Channels**: Utilizes dual phase-coherent RF receiver channels. The Reference Channel (`REFERENCE RX`) uses a dedicated directional antenna aimed at the transmitter to capture direct line-of-sight signals. The Surveillance Channel uses a phased array directed at the surveillance airspace to intercept weak target reflections.",
            "**Extensive Clutter & Direct-Path Cancellation**: Employs an Adaptive Extensive Cancellation Algorithm (ECA) to cancel the high-power direct path signal and stationary ground clutter from the surveillance channel without suppressing target echoes.",
            "**Cross-Ambiguity Function (CAF)**: Cross-correlates the cleaned surveillance signal with time-delayed, Doppler-shifted replicas of the reference signal over coherent processing intervals (CPI) to yield 2D Range-Doppler matrices.",
            "**CFAR Target Extraction & Kinematic Tracking**: Constant False Alarm Rate (CFAR) detectors extract target energy peaks, while multi-hypothesis tracking (MHT) algorithms triangulate targets across multiple emitter baselines to generate continuous tracks."
        ],
        "hardware_specs": [
            {"component": "Antenna Array Suite", "spec": "Dual-polarized wideband planar surveillance array with automated pan-tilt pedestal; high-gain directional reference horn/yagi"},
            {"component": "Receiver Frontend", "spec": "Multi-channel phase-coherent Software Defined Radio (SDR) with shared local oscillator (LO) and 14-bit ADC resolution"},
            {"component": "Clock Discipline", "spec": "High-stability Oven-Controlled Crystal Oscillator (OCXO) / GPS-disciplined Rubidium frequency standard"},
            {"component": "DSP Processing Unit", "spec": "Ruggedized 19-inch 4U server chassis equipped with dual NVIDIA RTX GPUs for real-time CUDA Cross-Ambiguity DSP acceleration"},
            {"component": "Tactical Deployment", "spec": "Pneumatic telescopic mast mounted on all-terrain military vehicle with shock-isolated electronic server rack"}
        ],
        "software_specs": [
            {"layer": "Signal Processing Core", "detail": "C++ / CUDA accelerated Cross-Ambiguity Function (CAF) and Wiener filtering pipeline"},
            {"layer": "Tracking & Fusion", "detail": "Multisite Kalman filtering and Track-Before-Detect (TBD) algorithms"},
            {"layer": "Tactical UI & C2 Link", "detail": "Real-time Range-Doppler heatmaps, PPI radar display, and STANAG/ATAK CoT integration"}
        ],
        "tags": ["Passive Radar", "Bistatic Radar", "RF & EW", "Counter-UAS", "Doppler Tracking", "Zero-Emission", "Signals of Opportunity"]
    },
    {
        "id": "03",
        "slug": "fruitfly",
        "name": "Fruitfly",
        "domain": "Autonomy & Sim",
        "role": "Bio-Inspired Neuromorphic Autopilot",
        "platform": "Custom FPV Racing Airframe / Neuromorphic SBC / Unity SIM",
        "protocol": "Lock-step UDP Physics Bridge / Betaflight Serial Telemetry",
        "classification": "EXPERIMENTAL RESEARCH SPECIFICATION",
        "status": "SIM & LAB PROTOTYPE",
        "primary_image": "13_fruitfly.jpg",
        "secondary_image": None,
        "thumbnail_labels": [
            "Experimental Bio-Inspired Autopilot",
            "Digitized Fruit Fly Brain Control (Connectome-driven flight)",
            "Adapting Insect Neural Pathways & Reflexes",
            "High-Speed Navigation & Obstacle Avoidance Without Heavy Computing",
            "Neural Flow Analysis & Real-time Spiking Activity",
            "High-Speed Flight Data & Sub-Millisecond Closed-Loop Control"
        ],
        "summary": "Fruitfly is an experimental neuromorphic flight control system that flies racing drones using a biological spiking model of the Drosophila melanogaster male central nervous system (MaleCNS v1.0). By leveraging actual biological connectome wiring rather than traditional multi-layer deep neural networks, Fruitfly achieves ultra-fast visual navigation and obstacle avoidance with microwatt computational overhead.",
        "what_it_does": [
            "Demonstrates autonomous agile drone flight through racing gate courses governed by a digitized insect connectome.",
            "Eliminates heavy matrix-multiplication deep learning models, replacing them with event-driven leaky integrate-and-fire (LIF) biological neural circuits.",
            "Replicates the compound-eye optical reflexes that allow flies to navigate complex obstacles at high speed without GPS, LiDAR, or complex SLAM algorithms.",
            "Provides a complete hardware and simulation testbed for neuromorphic robotics, bridging biological connectomics with embedded UAV flight controllers."
        ],
        "how_it_works": [
            "**Compound Eye Optical Frontend**: Two lateral virtual compound-eye cameras (64x48 grayscale) emulate fly ommatidia. Visual feeds pass through elementary motion detectors (EMD) and Reichardt correlators tuned for optic flow, looming dilation, and dark-object detection.",
            "**Poisson Spike Ingestion**: Motion vectors are converted into Poisson spike trains injected into specific connectome visual neurons: Horizontal System (HS/H2), Vertical System (VS), looming detectors (LPLC2/LC4), and small object trackers (LC10/11/15/18).",
            "**Biological Connectome Model**: Simulates the neural circuit extracted from Janelia FlyEM's MaleCNS v1.0 dataset. Synapse counts, transmitter polarity (excitatory vs. inhibitory), and network topology are completely preserved from biology without artificial neural retraining.",
            "**Spiking LIF Dynamics**: Runs a leaky integrate-and-fire simulation (0.5 ms discrete time-steps) across visual interneurons, descending neurons, and wing motor neurons.",
            "**DAgger Linear Readout**: A minimal linear readout layer trained via DAgger imitation learning maps descending motor neuron firing rates into real-time drone stick commands (pitch, roll, yaw, altitude hold)."
        ],
        "hardware_specs": [
            {"component": "Airframe", "spec": "3-inch to 5-inch lightweight carbon-fiber racing quadcopter with high-aspect motor geometry"},
            {"component": "Vision Sensor", "spec": "Twin low-latency monochrome optical flow sensors with ultra-wide angle fish-eye microlenses"},
            {"component": "Compute Engine", "spec": "Embedded neuromorphic processor / Raspberry Pi Zero 2W / Jetson Nano companion board"},
            {"component": "Flight Controller", "spec": "STM32F4/F7 MCU running Betaflight / custom Angle-mode firmware with high-speed serial stick injection"},
            {"component": "Propulsion", "spec": "High-kV brushless outrunner motors delivering >5:1 thrust-to-weight ratio for sub-millisecond reaction times"}
        ],
        "software_specs": [
            {"layer": "Connectome Database", "detail": "Janelia FlyEM neuPrint API (male-cns:v1.0 dataset)"},
            {"layer": "Neural Simulation", "detail": "Event-driven NumPy LIF network running biological neuron parameters (Shiu et al. Nature 2024)"},
            {"layer": "Simulation Environment", "detail": "Custom UnityFPVDroneSimulator with C# FlyBrain lock-step UDP bridge"}
        ],
        "tags": ["Neuromorphic", "Bio-Inspired", "Autonomy", "Connectome", "FPV Drone", "Spiking Neural Network", "Robotics"]
    },
    {
        "id": "04",
        "slug": "tmsi-sensor",
        "name": "TMSI-sensor",
        "domain": "RF & EW",
        "role": "Airborne Passive Cellular & RF Reconnaissance Sensor",
        "platform": "Raspberry Pi Zero 2W / RTL-SDR / Micro-UAV Payload",
        "protocol": "GSM Paging Decode / LTE Uplink / Kismet Remote Capture",
        "classification": "SOVEREIGN DEFENSE SPECIFICATION",
        "status": "FIELD OPERATIONAL",
        "primary_image": "TMSI.jpg",
        "secondary_image": None,
        "thumbnail_labels": [
            "Airborne Passive RF Capture",
            "Cellular Signal TMSI / IMSI Extraction",
            "Wi-Fi & Bluetooth Probe Sniffing",
            "GPS Coordinate Enriched Telemetry",
            "Real-Time LTE Uplink to Ground Station Kismet",
            "Sub-250g Ultralight Aerial Scout Payload (160g total)"
        ],
        "summary": "TMSI-sensor is an ultra-lightweight (160g) airborne signals intelligence (SIGINT) payload designed for sub-250g reconnaissance drones. Operating completely passively without localized RF emissions, it intercepts cellular paging identities (TMSI/IMSI), Wi-Fi probe requests, and Bluetooth advertisements, geolocates targets with onboard GPS, and streams live intelligence over LTE to a ground command post.",
        "what_it_does": [
            "Intercepts cellular identifiers (TMSI/IMSI) from mobile handsets downlinked from commercial cell towers without active interrogator transmissions.",
            "Captures Wi-Fi 802.11 probe requests and MAC addresses, uncovering historical Wi-Fi network associations of individuals on the ground.",
            "Logs Bluetooth Low Energy (BLE) advertisements and peripheral devices to detect tactical radios, smartphones, and wearable electronic devices.",
            "Tags every intercepted RF packet with high-precision GPS coordinates, altitude, and timestamps.",
            "Transmits structured surveillance feeds over an onboard 4G/LTE cellular link back to a centralized Kismet tactical GIS server."
        ],
        "how_it_works": [
            "**Passive GSM Monitoring**: An RTL-SDR V3 Pro receiver tunes to local cellular downlink frequencies (GSM900 / GSM850) using `gr-gsm`. It passively decodes CCCH/PCH paging channel packets, extracting subscriber Temporary Mobile Subscriber Identities (TMSI) and IMSIs.",
            "**Pluto/Fishball Fast Downlink Path**: Includes an experimental fast RF scanning path on ADALM-Pluto/Fishball (`pluto_gsm_scan.py`) to rank high-activity cellular carriers across large geographic areas.",
            "**Wi-Fi & BLE Interception**: Puts the Raspberry Pi's onboard Broadcom chip into 802.11 raw monitor mode to sniff probe frames. A secondary USB Bluetooth 5.0 dongle captures BLE advertising beacons.",
            "**GPS Georeferencing**: A dedicated daemon (`pi-reporter.py`) continuously reads NMEA sentences from an onboard u-blox GPS receiver via UART, tagging each signal intercept with coordinates.",
            "**LTE Ground Relay**: Streams enriched device observations through a 4G USB cellular modem directly into a remote Kismet server (`kismet-ingest.py`), updating the common tactical operating picture."
        ],
        "hardware_specs": [
            {"component": "Host Compute", "spec": "Raspberry Pi Zero 2W (quad-core 64-bit ARM Cortex-A53 @ 1.0 GHz, 512MB RAM) running Kali Linux ARM64"},
            {"component": "SDR Tuner", "spec": "RTL-SDR Blog V3 Pro with 0.5 PPM TCXO (tunable 500 kHz to 1.7 GHz); optional ADALM-Pluto / Fishball 7020"},
            {"component": "GNSS Module", "spec": "u-blox NEO-M8N GPS receiver with active patch antenna connected via UART (GPIO 14/15)"},
            {"component": "Telemetry Uplink", "spec": "Industrial USB 4G/LTE Cat-4 cellular modem (wwan0 interface)"},
            {"component": "Wireless Dongle", "spec": "USB Bluetooth 4.0/5.0 CSR8510 dongle for dedicated BLE scanning"},
            {"component": "SWaP Profile", "spec": "Total payload weight: ~160g including powered micro-OTG hub, antennas, and 3D-printed enclosure; power draw < 6W"}
        ],
        "software_specs": [
            {"layer": "Operating System", "detail": "Kali Linux ARM64 (headless optimized, read-only root overlay)"},
            {"layer": "SIGINT Stack", "detail": "gr-gsm, simple_IMSI-catcher, GNU Radio flowgraphs, Kismet remote capture daemons"},
            {"layer": "Ground Server", "detail": "Dockerized Kismet server, Python ingest pipeline, and real-time mapping UI"}
        ],
        "tags": ["SIGINT", "Passive RF", "TMSI", "IMSI", "Cellular", "Raspberry Pi", "Kismet", "LTE Uplink", "RF & EW"]
    },
    {
        "id": "05",
        "slug": "plutosky",
        "name": "PlutoSky",
        "domain": "RF & EW",
        "role": "Counter-UAS SDR Detector & Tactical RF Jammer",
        "platform": "ADALM-Pluto SDR / Fishball 7020 / Tactical Field Terminal",
        "protocol": "Direct RF Synthesizer / Swept Spectrum Analysis",
        "classification": "SOVEREIGN DEFENSE SPECIFICATION",
        "status": "FIELD TESTED",
        "primary_image": "Plutosky.jpg",
        "secondary_image": None,
        "thumbnail_labels": [
            "PlutoSky SDR: Tactical Airspace Awareness",
            "FPV Drone Detection & Video Carrier Monitoring",
            "ELRS / Crossfire Control Link Monitoring",
            "Targeted RF Jamming & Frequency Hopping Disruption",
            "Multi-Band Coverage (868/915 MHz, 2.4 GHz, 5.8 GHz)",
            "Field Portable High-Mobility C-UAS Kit"
        ],
        "summary": "PlutoSky is a portable Software-Defined Radio (SDR) counter-UAS platform engineered to detect, monitor, and suppress First-Person View (FPV) kamikaze drones and commercial UAVs. Operating across 868 MHz, 915 MHz, 2.4 GHz, and 5.8 GHz, PlutoSky provides tactical infantry and vehicle crews with rapid airspace alerting and targeted RF suppression capabilities.",
        "what_it_does": [
            "Detects incoming FPV strike drones by monitoring their frequency-hopping control links and analog video downlinks in real time.",
            "Decodes and tracks ExpressLRS (ELRS) and TBS Crossfire telemetry packets, identifying transmission hops and signal strength.",
            "Alerts operators with visual waterfall plots and acoustic alarms upon detecting analog 5.8 GHz FPV video carrier emissions.",
            "Executes surgical, selective RF suppression against hostile control links to trigger drone failsafes, emergency landings, or control loss.",
            "Operates as a lightweight man-portable soldier kit or vehicle-mounted tactical protective bubble."
        ],
        "how_it_works": [
            "**Fast Swept Spectrum Analysis**: Employs the wideband Analog Devices AD9363/AD9361 transceiver to sweep tactical drone bands at up to several gigahertz per second.",
            "**Protocol Fingerprinting**: Demodulates LoRa and FSK modulation frames specific to ExpressLRS and Crossfire links. Measures packet transmission intervals, chirp bandwidths, and pseudo-random hop sequences.",
            "**Analog Video Carrier Detection**: Scans 5.8 GHz video bands (Raceband, FatShark, Band A/B/E) for the characteristic carrier shape and sync pulses of analog video transmitters (VTX).",
            "**Selective Counter-Transmission**: When hostile signals are identified, PlutoSky synthesizes precision reactive jamming waveforms (such as narrow-band noise, fast linear sweeps, or barrage noise) targeted exactly at the drone's operational hop channels, preserving friendly spectrum outside the engagement band."
        ],
        "hardware_specs": [
            {"component": "SDR Core", "spec": "Analog Devices ADALM-Pluto rev C / Fishball 7020 (Xilinx Zynq-7020 FPGA + dual ARM Cortex-A9 + AD9363/AD9361 RF frontend)"},
            {"component": "Frequency Reference", "spec": "FOX924B 0.5 PPM high-stability Temperature Compensated Crystal Oscillator (TCXO)"},
            {"component": "RF Amplification", "spec": "Solid-state wideband RF power amplifier modules with fast PIN diode RX/TX switching"},
            {"component": "Antennas", "spec": "High-gain multi-band directional patch arrays and wideband collinear omnidirectional antennas"},
            {"component": "Chassis", "spec": "Milled aluminum thermal enclosure with transparent tactical acrylic cover, SMA/N-type bulkheads, and military shock bumpers"}
        ],
        "software_specs": [
            {"layer": "Firmware", "detail": "Custom Linux buildroot / ADI IIO firmware on Zynq FPGA"},
            {"layer": "DSP & Control Engine", "detail": "pyadi-iio, GNU Radio, and custom Python spectral classifier daemons"},
            {"layer": "User Interface", "detail": "High-contrast tactical dark GUI with real-time waterfall display, channel heatmaps, and audio alerts"}
        ],
        "tags": ["Counter-UAS", "FPV Denial", "ExpressLRS", "SDR", "Electronic Warfare", "RF & EW", "ADALM-Pluto"]
    },
    {
        "id": "06",
        "slug": "spoofgrid",
        "name": "SpoofGrid",
        "domain": "RF & EW",
        "role": "Tactical GNSS Jamming & Spoofing Evaluation Suite",
        "platform": "ADALM-Pluto + HackRF One / Faraday Cage Testbed",
        "protocol": "FastAPI Web Console / pyadi-iio / gnss-sdr-sim / WebSocket",
        "classification": "CONTROLLED LABORATORY TESTBED",
        "status": "OPERATIONAL RANGE BENCH",
        "primary_image": "Spoofgrid.jpg",
        "secondary_image": None,
        "thumbnail_labels": [
            "SpoofGrid EW Suite: GNSS Interference Simulation",
            "Jamming Noise Waveform Synthesis (CW, Chirp, Gaussian, Pulse)",
            "Jamming Vector Analysis Across 13 GNSS Bands",
            "Spoofed Coords vs Ground Truth Error Visualization",
            "Navigation Resilience Assessment & Receiver Hardening",
            "Cage-Only Authorization Safety Gate & Watchdog Auto-Kill"
        ],
        "summary": "SpoofGrid is a cage-only GNSS electronic warfare testbench and resilience evaluation platform. Powered by a FastAPI control console and dual independent SDRs, SpoofGrid executes 9 distinct electronic attack vectors across 13 satellite navigation bands to stress-test military and commercial GNSS receivers (u-blox F9P/F9R, Septentrio Mosaic-X5) and validate anti-spoofing algorithms.",
        "what_it_does": [
            "Evaluates how GNSS receivers and drone autopilots behave under complex, coordinated electronic warfare attacks.",
            "Generates repeatable, laboratory-grade satellite spoofing vectors (static position, moving trajectory, ephemeris tampering, progressive pull-off drift).",
            "Simulates broadband and narrowband jamming waveforms across GPS, Galileo, BeiDou, and GLONASS constellations.",
            "Tests and benchmarks anti-spoofing detection daemons (such as DragonSync spoof_detector.py) against live hardware.",
            "Enforces strict cage-only safety interlocks, requiring digital tickets and hardware TCXO verification before any SDR radiation can occur."
        ],
        "how_it_works": [
            "**Dual-SDR Architecture**: Simultaneously controls two SDRs with independent process locks: HackRF One for high-bandwidth wideband vectors and ADALM-Pluto for precision multi-band transmission via `pyadi-iio`.",
            "**Comprehensive Attack Catalog**: Supports 9 attack specifications: `spoof_static` (Tier-0 fixed-point spoofing), `spoof_trajectory` (Tier-1 moving spoof along custom paths), `spoof_replay` (meaconing record-and-playback), `spoof_ephemeris` (RINEX BRDC ephemeris tampering), `spoof_pullin_drift` (gradual pull-off from true coordinates), and 4 jamming modes (`jam_cw`, `jam_sweep`, `jam_noise`, `jam_pulse`).",
            "**Full GNSS Constellation Coverage**: Synthesizes signals across 13 satellite navigation bands: GPS L1/L2/L5, Galileo E1/E5a/E5b/E6, BeiDou B1I/B1C/B2a/B3I, and GLONASS L1/L2.",
            "**FastAPI Web Dashboard**: Exposes a real-time web interface (127.0.0.1:8090) featuring Leaflet interactive mapping, Chart.js error plots, xterm.js live logging, and an instant hard kill-switch."
        ],
        "hardware_specs": [
            {"component": "Wideband Transmitter", "spec": "HackRF One with FOX924B TCXO (~15 dBm output, 20 MHz bandwidth, all 13 bands)"},
            {"component": "Precision Transmitter", "spec": "ADALM-Pluto / PlutoSky with TCXO (~7 dBm output, up to 56 MHz bandwidth)"},
            {"component": "Devices Under Test (DUT)", "spec": "u-blox ZED-F9P / F9R inertial GNSS modules, Septentrio mosaic-X5, ArduPilot / Cube Orange"},
            {"component": "Test Enclosure", "spec": "Certified RF-shielded enclosure (Faraday cage) with calibrated step-attenuators and RF combiner network"},
            {"component": "Host Workstation", "spec": "x86-64 Linux workstation running Python 3.11, pyadi-iio, and FastAPI"}
        ],
        "software_specs": [
            {"layer": "Backend Engine", "detail": "FastAPI, Uvicorn, WebSockets, Python subprocess supervisor"},
            {"layer": "Simulation Tools", "detail": "gnss-sdr-sim, pyadi-iio, custom ephemeris modifier scripts"},
            {"layer": "Frontend", "detail": "Vanilla JavaScript, Leaflet GIS, Chart.js, xterm.js"}
        ],
        "tags": ["GNSS Spoofing", "Electronic Warfare", "GPS Jamming", "SDR", "FastAPI", "Faraday Testbed", "RF & EW"]
    },
    {
        "id": "07",
        "slug": "gsm-navi",
        "name": "GSM-NAVI",
        "domain": "Alternative PNT",
        "role": "Terrestrial Cellular Multi-Mast Navigation System",
        "platform": "Embedded ARM Controller / Industrial Cellular Frontend",
        "protocol": "Downlink Cell Broadcast Sniffing / Offline Geodetic Trilateration",
        "classification": "SOVEREIGN DEFENSE SPECIFICATION",
        "status": "FIELD VALIDATED",
        "primary_image": "GSM_NAVi.jpg",
        "secondary_image": None,
        "thumbnail_labels": [
            "GSM-NAVI Unit: Terrestrial Navigation Active",
            "Cell ID (CID) & Multi-Mast Signal Strength (RSSI/RSRP)",
            "Autonomous Navigation Backup When GPS is Degraded or Denied",
            "Resilient Positioning & Multilateration Fix",
            "Offline Geocoded Base Station Registry (Estonia, Nordic & Eastern Europe)",
            "Rugged Vehicle & Airframe Mountable Form Factor"
        ],
        "summary": "GSM-NAVI is a terrestrial positioning unit that derives accurate geographic coordinates exclusively from ambient cellular base stations. Designed to keep vehicles, vessels, and unmanned systems on course when satellite navigation is jammed or spoofed, GSM-NAVI operates completely passively by cross-referencing visible tower signals against an offline geocoded base station database.",
        "what_it_does": [
            "Provides reliable ground and aerial navigation backup when GNSS signals are degraded, jammed, or spoofed.",
            "Operates without emitting radio signals, eliminating the risk of electronic detection or counter-battery locating.",
            "Cross-references ambient base station broadcast telemetry against pre-compiled regional cell tower databases (including Estonia, Nordic, and Eastern Europe via RUcell).",
            "Calculates continuous position fixes and estimated error ellipses without requiring cellular network connectivity or data subscription SIM cards."
        ],
        "how_it_works": [
            "**Passive Broadcast Ingestion**: Scans cellular downlink channels across 2G, 3G, 4G, and LTE bands. Decodes broadcast system information blocks containing Cell ID (CID), Local Area Code (LAC), Mobile Network Code (MNC), and Mobile Country Code (MCC).",
            "**Signal Strength Profiling**: Gathers multi-tower signal parameters including Received Signal Strength Indicator (RSSI), Reference Signal Received Power (RSRP), and Reference Signal Received Quality (RSRQ) from multiple neighboring masts simultaneously.",
            "**Offline Geodetic Database Lookup**: Queries an onboard, compressed spatial SQLite database storing millions of pre-surveyed cellular mast locations, heights, and antenna radiation patterns.",
            "**Weighted Multilateration Algorithm**: Applies an iterative non-linear weighted least-squares solver incorporating empirical RF propagation path-loss models (Hata/Okumura) to derive a position fix and bounding uncertainty ellipse."
        ],
        "hardware_specs": [
            {"component": "Cellular Radio Frontend", "spec": "Quectel / Telit industrial multi-band cellular module with diagnostic raw-scan AT firmware"},
            {"component": "Embedded Controller", "spec": "Raspberry Pi Compute Module 4 / Cortex-M7 embedded controller"},
            {"component": "Antenna", "spec": "Multi-band wideband omnidirectional low-profile puck antenna with high out-of-band rejection"},
            {"component": "Interfaces", "spec": "Dual isolated CAN bus (UAVCAN / DroneCAN) and RS-422/UART serial ports"},
            {"component": "Enclosure", "spec": "IP67-rated CNC aluminum chassis with MIL-STD-810H vibration and thermal hardening"}
        ],
        "software_specs": [
            {"layer": "Database", "detail": "Spatialite / SQLite embedded geocoded tower registry with R-tree spatial indexing"},
            {"layer": "Solver", "detail": "C++ non-linear multilateration engine with Levenberg-Marquardt optimization"},
            {"layer": "Autopilot Link", "detail": "DroneCAN / NMEA output sentence streaming at 5-10 Hz"}
        ],
        "tags": ["Alternative PNT", "Cellular Navigation", "GSM-NAVI", "GPS-Denied", "Trilateration", "EW Resilient"]
    },
    {
        "id": "08",
        "slug": "qgc-simulator",
        "name": "QGC-Simulator",
        "domain": "Autonomy & Sim",
        "role": "HUGINN Tactical Flight & Hardware-in-the-Loop Simulator",
        "platform": "Liquid-Cooled Workstation / HOTAS Tactical Command Console",
        "protocol": "MAVLink UDP / PX4 SITL / PowerShell Test Automation",
        "classification": "DEVELOPMENT & REHEARSAL SUITE",
        "status": "OPERATIONAL",
        "primary_image": "QGC.jpg",
        "secondary_image": None,
        "thumbnail_labels": [
            "QGC-Simulator: HUGINN Flight Sim",
            "High-Fidelity Virtual Deployment Test & Mission Rehearsal",
            "Deep QGroundControl Protocol Integration",
            "Dynamic Payload Behavior & Sensor Disruption Emulation",
            "Full Control Parameters & Aerodynamic Verification",
            "Tactical Operator Console with Dual HOTAS Flight Controls & Triple Displays"
        ],
        "summary": "QGC-Simulator is a high-fidelity flight simulation and mission validation environment engineered specifically for the HUGINN UAV platform and PX4 autonomous autopilots. Featuring deep QGroundControl integration and a physical tactical command console, QGC-Simulator enables flight crews to virtually rehearse missions, validate payload behaviors, and stress-test autonomous failover logic under simulated electronic warfare conditions.",
        "what_it_does": [
            "Rehearses complex UAV mission profiles in realistic virtual airspace before live physical deployments.",
            "Validates autonomous flight modes, waypoint routing, geofence constraints, and return-to-launch procedures.",
            "Injects severe simulated flight disruptions: GPS jamming, spoofed trajectories, sensor loss, and extreme atmospheric turbulence.",
            "Integrates physical tactical ground control stations with dual HOTAS flight sticks, rudder pedals, and multi-monitor instrument dashboards.",
            "Executes automated end-to-end regression test scripts via PowerShell (`Start-HuginnSimulation.ps1`)."
        ],
        "how_it_works": [
            "**PX4 Software-In-The-Loop (SITL)**: Executes the complete PX4 autopilot flight firmware within an isolated simulation container, modeling realistic 6-DOF aerodynamics for fixed-wing, multirotor, and hybrid VTOL platforms.",
            "**Custom QGroundControl UI**: Links via high-speed MAVLink UDP routing to custom QGroundControl builds equipped with custom HUGINN telemetry indicators, Alt-PNT status displays, and simulated GPS-kill toggles.",
            "**Sensor & Electronic Warfare Injection**: Dynamically injects simulated DVB-T2 radio tower pseudoranges, cell mast signal strengths, terrain elevation profiles, and synthetic camera feeds to evaluate how the HUGINN FusionEngine responds to GNSS loss.",
            "**Automated Simulation Runner**: Orchestrates complete multi-vehicle simulation runs using PowerShell scripts that handle network port binding, process lifecycles, and telemetry recording."
        ],
        "hardware_specs": [
            {"component": "Simulation Workstation", "spec": "High-performance liquid-cooled multi-GPU workstation running Ubuntu Linux and Windows 11 Pro"},
            {"component": "Operator Command Console", "spec": "Three high-resolution tactical flight displays mounted on an aluminum extrusion rig with carbon-fiber fascia"},
            {"component": "Flight Controls", "spec": "Dual military-grade HOTAS throttle-and-stick controls with programmable switches and rudder controls"},
            {"component": "Hardware-in-the-Loop Link", "spec": "USB-to-CAN / Serial hardware adapters connecting physical Pixhawk flight controllers to simulation buses"}
        ],
        "software_specs": [
            {"layer": "Autopilot Stack", "detail": "PX4 Autopilot v1.14+ SITL, jMAVSim, and Gazebo Classic / Ignition physics"},
            {"layer": "Ground Control Station", "detail": "Custom Qt5/QML QGroundControl with HUGINN action panels"},
            {"layer": "Automation", "detail": "PowerShell 7 orchestration framework with automated telemetry logging"}
        ],
        "tags": ["Simulation", "SITL", "HITL", "QGroundControl", "PX4", "MAVLink", "Autonomy & Sim", "HUGINN Companion"]
    },
    {
        "id": "09",
        "slug": "isr-master",
        "name": "ISR_master",
        "domain": "C4ISR & Recon",
        "role": "Tactical Gimbal Control & Central Management Pipeline",
        "platform": "Ruggedized 19-inch Server / Toughbook / Pan-Tilt Gimbal",
        "protocol": "RS-232 / RS-485 / MAVLink v2 / MJPEG / Cursor-on-Target",
        "classification": "SOVEREIGN DEFENSE SPECIFICATION",
        "status": "FIELD DEPLOYED (v5.2+)",
        "primary_image": "ISR_master.jpg",
        "secondary_image": None,
        "thumbnail_labels": [
            "ISR_MASTER: Central Management Pipeline",
            "Multi-Source Sensor Aggregation & Video Processing",
            "Electro-Optical / Infrared (EO/IR) Gimbal Control & Laser Rangefinder",
            "Automated Target Handoff & Georeferencing",
            "Multi-Source ISR Data Classification & NATO SALUTE Reporting",
            "Direct ATAK Cursor-on-Target (CoT) Dissemination"
        ],
        "summary": "ISR_master is a central intelligence, surveillance, and reconnaissance (ISR) mission management pipeline and video telemetry engine. Designed for airborne observation platforms and tactical ground stations, it controls stabilized dual EO/IR gimbals and laser rangefinders, renders real-time heads-up displays (HUD), computes terrain-aware georeferencing, and disseminates targets directly to ATAK and command headquarters.",
        "what_it_does": [
            "Controls stabilized airborne and ground gimbals via serial (RS-232/RS-485) and MAVLink protocols.",
            "Streams low-latency visible-light (EO) and thermal infrared (IR) video feeds with tactical HUD overlays.",
            "Calculates high-precision ground intersection coordinates (MGRS, UTM, Lat/Lon) of targets in crosshairs using digital elevation heightmaps.",
            "Captures intelligence still frames, annotates images, and compiles standardized NATO SALUTE reconnaissance reports.",
            "Broadcasts Cursor-on-Target (CoT) XML packets to the Android Team Awareness Kit (ATAK) network for immediate fire-support handoff."
        ],
        "how_it_works": [
            "**Dual Gimbal Drivers**: Implements native drivers for the ERDI/DYT POD80 gimbal (`EB 90` frame format over serial/TCP) and the NextVision Colibri 2 gimbal (MAVLink v2 Gimbal Manager protocol over UDP). Controls pan, tilt, zoom, camera switching, and laser rangefinder firing.",
            "**Tactical Video HUD**: A Flask and OpenCV video pipeline ingests MJPEG/RTSP streams, superimposing an aviator HUD with pitch/roll ladders, heading tapes (in degrees or mils: 0–6400 mil), and military DTG clocks.",
            "**Terrain Elevation Georeferencing**: Combines aircraft GPS coordinates, barometric altitude, and gimbal pan/tilt/zoom angles with GeoTIFF heightmaps (`rasterio`, `pyproj`). Traces the optical line of sight to terrain intersections, outputting instant MGRS coordinates.",
            "**SALUTE & ATAK Integration**: A built-in report generator compiles Size, Activity, Location, Unit, Time, and Equipment (SALUTE) briefs into encrypted PDFs, while simultaneously publishing Cursor-on-Target (CoT) target markers to ATAK."
        ],
        "hardware_specs": [
            {"component": "Supported Gimbals", "spec": "ERDI/DYT POD80 / EDU80 dual EO/IR with Laser Rangefinder (RS-232/RS-485/TCP); NextVision Colibri 2 MAVLink gimbal"},
            {"component": "Tactical Workstation", "spec": "Panasonic Toughbook 55 / Dell Rugged 5430; 19-inch 4U vehicle server rack with fiber-optic video inputs"},
            {"component": "Video Capture", "spec": "High-definition HDMI/SDI to USB 3.0 hardware video grabber and low-latency COFDM digital receivers"},
            {"component": "Networking", "spec": "Gigabit Ethernet, RS-422 serial interfaces, and MAVLink telemetry radio links"}
        ],
        "software_specs": [
            {"layer": "Backend Engine", "detail": "Python 3.11, Flask server, OpenCV, PySerial, PyMAVLink, Rasterio, MGRS, ReportLab"},
            {"layer": "Frontend", "detail": "Modern responsive dark HUD UI with keyboard navigation, d-pad controls, and canvas image annotation"},
            {"layer": "Interoperability", "detail": "Cursor-on-Target (CoT) XML over UDP multicast (port 4242) for native ATAK/WinTAK integration"}
        ],
        "tags": ["ISR", "C4ISR & Recon", "Gimbal Control", "POD80", "Colibri 2", "EO/IR", "ATAK", "Cursor-on-Target", "SALUTE"]
    },
    {
        "id": "10",
        "slug": "c4isr-sentinel",
        "name": "C4ISR SENTINEL",
        "domain": "C4ISR & Recon",
        "role": "Command & Control Fusion Hub & Battlefield Operating System",
        "platform": "Modular Edge Server Cube / Firehawk FCS Mobile Android",
        "protocol": "Multi-Stream Data Protocol (MSDP) / ZeroMQ / WebSockets / CoT",
        "classification": "SOVEREIGN DEFENSE SPECIFICATION",
        "status": "OPERATIONAL (v5+)",
        "primary_image": "C4ISR.jpg",
        "secondary_image": None,
        "thumbnail_labels": [
            "C4ISR SENTINEL Command Hub",
            "Multi-Source Aggregated Battlefield Data Fusion",
            "Automated Friendly & Hostile Unit Tracking",
            "Shared Common Operating Picture (COP) Situational Awareness",
            "Tactical Units Online via Zero-Trust Tactical Mesh Networks",
            "32-Module Clean Service Architecture & Firehawk Mobile FCS"
        ],
        "summary": "C4ISR SENTINEL is an enterprise-grade tactical command, control, and intelligence fusion hub built on a 32-module decoupled microservice architecture. It ingests multi-source battlefield telemetry—including drone video streams, radar tracks, acoustic detections, and blue-force feeds—synthesizing them into a real-time Common Operating Picture (COP) deployed across edge command servers and forward mobile tablets.",
        "what_it_does": [
            "Aggregates heterogeneous battlefield sensor feeds and operational telemetry into a synchronized tactical command picture.",
            "Tracks friendly and hostile unit positions in real time using standardized NATO military symbology (MIL-STD-2525 / APP-6).",
            "Integrates seamlessly with forward observers using the Firehawk Mobile FCS Android application for drone steering and target coordinates.",
            "Distributes low-latency video and tactical data across intermittent, bandwidth-constrained tactical mesh radio networks.",
            "Maintains situational awareness and operational command capability under contested electronic warfare environments."
        ],
        "how_it_works": [
            "**32-Module Decoupled Architecture**: Designed around a clean master architecture separating shippable applications (NestJS API backend, Firehawk mobile client, web C2), shared packages (MGRS, SIDC, protocol adapters), and tactical UI components.",
            "**Multi-Stream Data Protocol (MSDP)**: Ingests high-bandwidth telemetry over ZeroMQ, WebSockets, and UDP multicast, guaranteeing message ordering and resilience over low-bandwidth tactical mesh radios (Silvus, TrellisWare, DTC).",
            "**Tactical Brutalism UI Language**: Implements high-contrast, distraction-free visual design specifically optimized for readability on ruggedized screens under direct sunlight or night-vision goggle (NVG) conditions.",
            "**ATAK & NATO Adapter Layer**: Converts proprietary drone and sensor payloads into standard Cursor-on-Target (CoT) and STANAG 4609 compliant metadata feeds for multinational joint-force interoperability."
        ],
        "hardware_specs": [
            {"component": "Command Server Hub", "spec": "Modular ruggedized edge server cube with multi-core Intel Xeon/AMD EPYC processors, 64GB ECC RAM, and redundant power"},
            {"component": "Forward Mobile Tablets", "spec": "Samsung Galaxy Tab Active4 Pro tactical tablets with MIL-STD-810H and IP68 hardening"},
            {"component": "Networking Backbone", "spec": "Managed Gigabit Ethernet switch with multi-mode 10GbE SFP+ optical uplinks and tactical MANET radios"},
            {"component": "Storage Subsystem", "spec": "Encrypted NVMe RAID array for real-time mission telemetry and video recording archive"}
        ],
        "software_specs": [
            {"layer": "Backend Engine", "detail": "NestJS TypeScript enterprise backend, PostgreSQL / PostGIS spatial database, Redis queue"},
            {"layer": "Mobile Client", "detail": "Capacitor + React tactical mobile application (Firehawk FCS) with native Android bridge"},
            {"layer": "Deployment", "detail": "Docker Compose / Kubernetes edge containers with zero-trust local network policies"}
        ],
        "tags": ["C4ISR", "C2 Platform", "Sentinel", "Tactical Mesh", "Firehawk FCS", "ATAK", "Common Operating Picture"]
    },
    {
        "id": "11",
        "slug": "aetherstack",
        "name": "aetherstack",
        "domain": "AI & OSINT",
        "role": "Multi-Model Privacy-Governed LLM Control Plane",
        "platform": "Local GPU Rig (CUDA/ROCm/Metal/Vulkan) / VS Code Extension",
        "protocol": "LiteLLM Gateway / Redis Vector Cache / Open WebUI",
        "classification": "COMMERCIAL & DEFENSE SPECIFICATION",
        "status": "PUBLIC RELEASED & MARKETPLACE VERIFIED",
        "primary_image": "Aether.jpg",
        "secondary_image": None,
        "thumbnail_labels": [
            "AetherStack LLM: Privacy-First Multi-Model Orchestration",
            "Strict Data Governance & Local Air-Gapped Processing Controls",
            "Built-In GDPR Compliance & Sovereign Machine Boundaries",
            "Multi-Model Consensus & Disagreement Detection",
            "Local Ollama GPU Engine with Cloud Fallback & Failover",
            "Unified VS Code Extension & Team Control Plane"
        ],
        "summary": "AetherStack is a multi-model AI orchestration control plane and VS Code extension that consolidates multiple AI models into a single unified reasoning interface. Built for high-security engineering teams and defense contractors, AetherStack automates multi-model consensus, enforces air-gapped data governance, and prevents proprietary source code from leaking to public cloud APIs.",
        "what_it_does": [
            "Collapses disparate AI subscriptions and models into a single chat window, eliminating the need to copy-paste context across tools.",
            "Queries an ordered group of AI models simultaneously, synthesizing their answers and highlighting points of disagreement to catch subtle code bugs and hallucinations.",
            "Enforces strict air-gapped local execution on private hardware, guaranteeing that sensitive code and proprietary models never leave the local network.",
            "Automatically manages API key failover, seamlessly switching to backup providers or local GPU models when cloud rate limits are reached.",
            "Maintains persistent project memory across developer sessions without context window bloat."
        ],
        "how_it_works": [
            "**Multi-Model Synthesis & Disagreement Detection**: Instead of relying on a single model's overconfident answer, AetherStack queries multiple models in parallel (such as a local Ollama model + external frontier models). It parses disagreements and returns a synthesized consensus report.",
            "**Dynamic Task Routing**: Automatically routes user queries to the optimal specialist mode (`/research`, `/plan`, `/code`, `/test`, `/bugfix`), matching the complexity of the task with the ideal model architecture.",
            "**Sovereign Local Mode**: Runs local open-weights LLMs via Ollama, utilizing hardware acceleration across NVIDIA CUDA, AMD ROCm, Apple Silicon Metal, and Vulkan backends.",
            "**Multi-Key & Failover Management**: Supports simultaneous personal and organizational API keys. When session or token quotas are depleted, the gateway automatically falls back to secondary keys or local offline models without disrupting workflow."
        ],
        "hardware_specs": [
            {"component": "Host Workstation", "spec": "Workstations running Windows 11, macOS (Apple Silicon M-series), or Ubuntu Linux"},
            {"component": "GPU Acceleration", "spec": "NVIDIA RTX 4090 / A100 (CUDA), AMD Radeon 7900XTX (ROCm), Apple M1/M2/M3/M4 Max (Metal), or Vulkan compute"},
            {"component": "Local Storage", "spec": "High-speed NVMe SSD hosting local quantized weights (GGUF 4-bit / 8-bit)"}
        ],
        "software_specs": [
            {"layer": "Control Plane", "detail": "LiteLLM gateway proxy, Redis vector cache, and Open WebUI container stack"},
            {"layer": "Client Integration", "detail": "Published VS Code extension (Marketplace verified) with integrated chat view"},
            {"layer": "Local Inference", "detail": "Ollama local inference runtime supporting Llama 3, Qwen, DeepSeek, and Mistral"}
        ],
        "tags": ["AI Orchestration", "LLM", "Privacy", "VS Code Extension", "Ollama", "Multi-Model", "AI & OSINT"]
    },
    {
        "id": "12",
        "slug": "o-cehtp",
        "name": "O-CEHTP",
        "domain": "AI & OSINT",
        "role": "Hardened OSINT Cyber Intelligence & Investigation Platform",
        "platform": "Sandboxed Container Host / Analyst Multi-Screen Operations Board",
        "protocol": "Hardened Chromium Sandbox / GraphQL / Tor / Neo4j",
        "classification": "SOVEREIGN DEFENSE SPECIFICATION",
        "status": "ARCHITECTURE VALIDATED & TESTED",
        "primary_image": "OCEHTP.jpg",
        "secondary_image": None,
        "thumbnail_labels": [
            "O-CEHTP OSINT Investigation Platform",
            "Encrypted Evidence Locker & Cryptographic Chain-of-Custody",
            "Isolated Sandboxing (Built-in Hardened Virtual Browser)",
            "Active Cyber Defense & Modular Open-Source Plugins",
            "AI-Driven Entity Extraction & Cross-Registry Data Federation",
            "Multi-Screen Operations Board & Dark Web Investigation Room"
        ],
        "summary": "O-CEHTP is a sovereign cyber intelligence and open-source intelligence (OSINT) investigation platform. Built around a tripartite architecture—an isolated sandbox browser, an autonomous AI research agent, and a data federation engine—O-CEHTP automates the collection, cross-referencing, and preservation of digital evidence from surface, deep, and dark web sources.",
        "what_it_does": [
            "Automates digital intelligence gathering for cybercrime investigators, AML/KYC compliance teams, and national security analysts.",
            "Executes anonymous, isolated browsing sessions across the clear web and dark web without leaving browser fingerprint traces.",
            "Employs autonomous AI agents to parse raw webpages, social networks, and leaked databases to extract interconnected entities.",
            "Cross-references individuals and corporations against offshore registries, business databases, and crypto transaction ledgers.",
            "Generates cryptographically sealed, tamper-proof evidentiary case files that maintain court-admissible chain of custody."
        ],
        "how_it_works": [
            "**Isolated Sandbox Browser**: Features an embedded, disposable browser container (Chromium sandbox/Playwright) running in an isolated network namespace with Tor/I2P routing, isolating investigators from malware and tracking pixels.",
            "**Autonomous Intelligence Agent**: AI agents autonomously follow investigative leads, parse document dumps, perform reverse image searches, and extract identifiers (names, IBANs, crypto wallets, email addresses, phone numbers).",
            "**Data Federation Lake**: Simultaneously queries commercial intelligence databases, company registries, breach repositories, and blockchain ledgers via a unified API gateway.",
            "**Visual Operations Board**: Visualizes entities, financial transactions, and communication links on interactive 2D/3D graph networks, speeding up pattern recognition in complex criminal networks.",
            "**Encrypted Evidence Locker**: Hashes all collected artifacts (SHA-256) and stores them in an immutable, encrypted database with detailed audit logs to satisfy evidentiary standards."
        ],
        "hardware_specs": [
            {"component": "Analyst Workstation", "spec": "Multi-monitor tactical console with hardware-isolated network adapters and biometric authentication"},
            {"component": "Server Infrastructure", "spec": "Dedicated server running hardened Linux kernel (SELinux/AppArmor) hosting containerized services"},
            {"component": "Secure Storage", "spec": "FIPS 140-2 validated self-encrypting NVMe storage array hosting PostgreSQL and Neo4j graph databases"}
        ],
        "software_specs": [
            {"layer": "Browser Engine", "detail": "Hardened Chromium container with Playwright automation and anti-fingerprinting patches"},
            {"layer": "Graph & Federation", "detail": "Neo4j graph database, PostgreSQL, GraphQL API gateway"},
            {"layer": "Frontend", "detail": "Vite + TypeScript SPA with interactive entity canvas and real-time agent chat"}
        ],
        "tags": ["OSINT", "Cyber Defense", "Intelligence", "Sandbox Browser", "Graph Database", "AI Agent", "AI & OSINT"]
    },
    {
        "id": "13",
        "slug": "kratt",
        "name": "KRATT",
        "domain": "AI & OSINT",
        "role": "Autonomous Quantitative Intelligence & Execution Engine",
        "platform": "Compact Industrial Edge PC / Time-Series Database Rig",
        "protocol": "WebSocket Tick Streaming / Air-Gapped Accounting Boundary",
        "classification": "PROPRIETARY TRADING ARCHITECTURE",
        "status": "OPERATIONAL (NEXT ARCHITECTURE)",
        "primary_image": "KRATT.jpg",
        "secondary_image": None,
        "thumbnail_labels": [
            "KRATT Market Intel: Cryptocurrency & Equities Intelligence",
            "Real-Time Asset Momentum & Multi-Indicator Anomaly Scoring",
            "Equity Sentiment & Social Signal Extraction Pipelines",
            "Trade Insights & Automated Quantitative Execution Modeling",
            "Sovereign Local Ledger Accounting (FTMO / Prop Challenge Boundary)",
            "Air-Gapped Architecture Free from SaaS Dependencies"
        ],
        "summary": "KRATT is a sovereign quantitative market intelligence and algorithmic trading engine designed for cryptocurrencies and equities. Featuring strict architectural isolation between quote ingestion, execution policy, and ledger accounting, KRATT analyzes order books and sentiment streams to detect market anomalies and manage automated prop-firm challenges.",
        "what_it_does": [
            "Processes high-frequency market data to identify short-term momentum shifts and statistical price anomalies.",
            "Extracts sentiment velocity from social and financial media feeds, predicting narrative-driven price movements.",
            "Enforces strict risk management protocols, maximum drawdown limits, and challenge parameters (such as FTMO rules).",
            "Maintains a decoupled ledger boundary that prevents simulation, challenge, and live capital accounts from cross-contaminating.",
            "Executes trades autonomously without relying on third-party cloud SaaS infrastructure."
        ],
        "how_it_works": [
            "**Market Data Streaming**: Ingests real-time Level 2 order books and tick transactions via direct low-latency WebSocket connections to major exchanges.",
            "**Multi-Indicator Anomaly Scoring**: Computes statistical indicators (order flow imbalance, volume-weighted momentum, volatility compression) in real time to generate quantitative scores.",
            "**LLM Policy & Sentiment Filter**: Evaluates qualitative macro context and news feeds using an onboard LLM policy skeleton to verify whether market anomalies align with current market sentiment.",
            "**Decoupled Ledger Architecture**: Employs a strict architectural boundary (`kratt_next`) that completely isolates market data providers, strategy generators, and execution ledgers. FTMO challenge accounts operate within an isolated watchdog pipeline with autonomous circuit-breakers."
        ],
        "hardware_specs": [
            {"component": "Compute Node", "spec": "Fanless industrial edge mini-PC with Intel Core i7 / AMD Ryzen processor and dual low-latency Gigabit Ethernet"},
            {"component": "Storage", "spec": "High-endurance PCIe 4.0 NVMe SSD storing high-frequency tick databases and local ledger logs"},
            {"component": "Display Station", "spec": "Ultra-wide multi-panel financial workstation running real-time order-book heatmaps and risk dials"}
        ],
        "software_specs": [
            {"layer": "Core Engine", "detail": "Python 3.11 with FastAPI, NumPy, Pandas, and asynchronous WebSockets"},
            {"layer": "Database", "detail": "SQLite with WAL mode / DuckDB for high-throughput time-series tick logging"},
            {"layer": "Risk Watchdog", "detail": "Autonomous rule-enforcement daemon monitoring equity drawdowns at millisecond resolution"}
        ],
        "tags": ["Quantitative Finance", "Market Intelligence", "AI/ML", "Algorithmic Trading", "Risk Engine", "AI & OSINT"]
    }
]

def generate_project_page(sys_data, prev_sys, next_sys):
    specs_html = "".join([
        f"""<div class="border-hairline p-4 bg-mono-900/60">
              <span class="text-accent-orange font-mono text-xs block mb-1 font-semibold">{spec['component']}</span>
              <span class="text-mono-200 text-xs font-sans leading-relaxed">{spec['spec']}</span>
            </div>"""
        for spec in sys_data["hardware_specs"]
    ])

    sw_html = "".join([
        f"""<div class="border-hairline p-4 bg-mono-900/60">
              <span class="text-accent-cyan font-mono text-xs block mb-1 font-semibold">{sw['layer']}</span>
              <span class="text-mono-200 text-xs font-sans leading-relaxed">{sw['detail']}</span>
            </div>"""
        for sw in sys_data["software_specs"]
    ])

    what_html = "".join([
        f"""<li class="flex items-start space-x-3 text-xs sm:text-sm text-mono-200 leading-relaxed font-sans">
              <span class="text-accent-orange font-mono select-none font-bold mt-0.5">■</span>
              <span>{item}</span>
            </li>"""
        for item in sys_data["what_it_does"]
    ])

    how_html = "".join([
        f"""<li class="flex items-start space-x-3 text-xs sm:text-sm text-mono-200 leading-relaxed font-sans">
              <span class="text-accent-cyan font-mono select-none font-bold mt-0.5">▶</span>
              <div>{item}</div>
            </li>"""
        for item in sys_data["how_it_works"]
    ])

    labels_html = "".join([
        f"""<span class="px-2.5 py-1 bg-mono-950 border border-mono-700 text-mono-300 font-mono text-[11px] inline-flex items-center space-x-1.5">
              <span class="w-1.5 h-1.5 bg-accent-orange"></span>
              <span>{label}</span>
            </span>"""
        for label in sys_data["thumbnail_labels"]
    ])

    tags_html = "".join([
        f"""<span class="px-2 py-0.5 border border-mono-800 text-mono-400 text-[10px] font-mono bg-mono-950">{tag}</span>"""
        for tag in sys_data["tags"]
    ])

    secondary_img_html = ""
    if sys_data.get("secondary_image"):
        secondary_img_html = f"""
        <div class="border-hairline bg-mono-900/40 p-4 mt-6">
          <img src="../images/{sys_data['secondary_image']}" alt="{sys_data['name']} Architectural Blueprint" 
               class="w-full h-auto border-hairline" />
        </div>
        """

    page_html = f"""<!DOCTYPE html>
<html lang="en" class="dark">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{sys_data['name']} // {sys_data['role']} - piksliviksi</title>
  
  <!-- Tailwind CSS Engine -->
  <script src="https://cdn.tailwindcss.com"></script>
  
  <!-- Fonts: Inter & JetBrains Mono -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">

  <script>
    tailwind.config = {{
      darkMode: 'class',
      theme: {{
        extend: {{
          fontFamily: {{
            sans: ['Inter', '-apple-system', 'BlinkMacSystemFont', 'Segoe UI', 'Roboto', 'sans-serif'],
            mono: ['JetBrains Mono', 'ui-monospace', 'SFMono-Regular', 'Menlo', 'monospace'],
          }},
          colors: {{
            mono: {{
              950: '#07080a',
              900: '#0c0e12',
              850: '#111419',
              800: '#181c23',
              700: '#232832',
              600: '#343b49',
              500: '#525b6c',
              400: '#7e889b',
              300: '#b1b8c5',
              200: '#dce0e7',
              100: '#f1f3f7',
              50: '#fafbfd'
            }},
            accent: {{
              amber: '#f59e0b',
              orange: '#f97316',
              cyan: '#0ea5e9',
              emerald: '#10b981',
              zinc: '#e4e4e7'
            }}
          }}
        }}
      }}
    }}
  </script>

  <style>
    * {{ border-radius: 0px !important; }}
    body {{
      background-color: #08090c;
      color: #d1d5db;
      font-family: 'Inter', sans-serif;
      -webkit-font-smoothing: antialiased;
    }}
    .blueprint-grid {{
      background-image: linear-gradient(to right, rgba(255, 255, 255, 0.02) 1px, transparent 1px),
                        linear-gradient(to bottom, rgba(255, 255, 255, 0.02) 1px, transparent 1px);
      background-size: 32px 32px;
    }}
    .border-hairline {{ border: 1px solid #1c2028; }}
    .border-hairline-t {{ border-top: 1px solid #1c2028; }}
    .border-hairline-b {{ border-bottom: 1px solid #1c2028; }}
    .border-hairline-l {{ border-left: 1px solid #1c2028; }}
    .border-hairline-r {{ border-right: 1px solid #1c2028; }}
    ::-webkit-scrollbar {{ width: 5px; height: 5px; }}
    ::-webkit-scrollbar-track {{ background: #08090c; }}
    ::-webkit-scrollbar-thumb {{ background: #232832; }}
  </style>
</head>

<body class="blueprint-grid min-h-screen flex flex-col selection:bg-zinc-800 selection:text-white">

  <!-- Top Header Navigation -->
  <header class="border-hairline-b bg-mono-950/95 sticky top-0 z-30 backdrop-blur-sm">
    <div class="max-w-[1400px] mx-auto px-4 sm:px-6 lg:px-8">
      <div class="h-14 flex items-center justify-between gap-4">
        
        <!-- Breadcrumb & Identity -->
        <div class="flex items-center space-x-3 text-xs font-mono">
          <a href="../index.html" class="flex items-center space-x-2 text-white font-semibold uppercase hover:text-accent-orange transition-colors">
            <span class="w-2.5 h-2.5 bg-accent-orange inline-block"></span>
            <span>piksliviksi</span>
          </a>
          <span class="text-mono-600">/</span>
          <a href="../index.html" class="text-mono-400 hover:text-white uppercase transition">Catalog</a>
          <span class="text-mono-600">/</span>
          <span class="text-accent-orange font-semibold">{sys_data['id']}_{sys_data['slug'].upper()}</span>
        </div>

        <!-- Back to Catalog Link -->
        <div class="flex items-center space-x-4 font-mono text-xs">
          <a href="../index.html" class="inline-flex items-center space-x-1.5 px-3 py-1.5 border border-mono-700 hover:border-mono-400 text-mono-200 hover:text-white bg-mono-900 transition text-xs font-mono">
            <span>←</span>
            <span>BACK TO CATALOG</span>
          </a>
        </div>
      </div>
    </div>
  </header>

  <main class="max-w-[1400px] mx-auto px-4 sm:px-6 lg:px-8 py-8 flex-grow w-full">
    
    <!-- Top System Identification Banner -->
    <div class="border-hairline bg-mono-900/60 p-6 sm:p-8 mb-8">
      <div class="flex flex-wrap items-center justify-between gap-4 border-hairline-b pb-4 mb-6">
        <div class="flex items-center space-x-3 font-mono text-xs">
          <span class="px-2 py-0.5 bg-accent-orange text-black font-bold">SYS_{sys_data['id']}</span>
          <span class="px-2 py-0.5 border border-mono-700 bg-mono-950 text-mono-300 uppercase">{sys_data['domain']}</span>
          <span class="px-2 py-0.5 border border-emerald-900/50 bg-emerald-950/20 text-emerald-400 uppercase text-[10px]">{sys_data['status']}</span>
        </div>
        <div class="font-mono text-xs text-mono-500 uppercase tracking-widest hidden sm:block">
          {sys_data['classification']}
        </div>
      </div>

      <div class="max-w-4xl">
        <h1 class="text-3xl sm:text-4xl lg:text-5xl font-semibold text-white tracking-tight font-sans mb-2">
          {sys_data['name']}
        </h1>
        <div class="text-sm sm:text-base font-mono text-accent-orange mb-4">
          {sys_data['role']}
        </div>
        <p class="text-mono-300 text-sm sm:text-base leading-relaxed font-sans mb-6">
          {sys_data['summary']}
        </p>

        <!-- Fast Specs Telemetry Strip -->
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3 font-mono text-xs pt-4 border-hairline-t">
          <div>
            <span class="text-mono-500 uppercase block text-[10px]">Operating Platform</span>
            <span class="text-mono-200">{sys_data['platform']}</span>
          </div>
          <div>
            <span class="text-mono-500 uppercase block text-[10px]">Telemetry & Protocol</span>
            <span class="text-mono-200">{sys_data['protocol']}</span>
          </div>
          <div>
            <span class="text-mono-500 uppercase block text-[10px]">Access & Repository</span>
            <span class="text-mono-400">Proprietary / Private Defense Repo</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Blueprint & Visual Architecture Showcase -->
    <section class="border-hairline bg-mono-900/40 p-6 sm:p-8 mb-8">
      <div class="flex items-center justify-between border-hairline-b pb-4 mb-6">
        <div class="flex items-center space-x-2 text-mono-300 font-mono text-xs uppercase tracking-widest">
          <span class="w-2.5 h-2.5 bg-accent-orange inline-block"></span>
          <span>Technical Architecture Blueprint & Schematic</span>
        </div>
        <span class="font-mono text-[11px] text-mono-500">CLICK IMAGE TO ENLARGE</span>
      </div>

      <!-- Main Thumbnail Blueprint -->
      <div class="relative group bg-mono-950 border-hairline overflow-hidden cursor-pointer" onclick="openModal('../images/{sys_data['primary_image']}')">
        <img src="../images/{sys_data['primary_image']}" alt="{sys_data['name']} Architectural Blueprint" 
             class="w-full h-auto object-cover group-hover:scale-[1.01] transition-transform duration-300" />
        <div class="absolute bottom-3 right-3 px-3 py-1.5 bg-mono-950/90 border border-mono-700 text-mono-200 font-mono text-xs flex items-center space-x-1.5 opacity-90 group-hover:opacity-100 transition">
          <svg class="w-3.5 h-3.5 text-accent-orange" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0zM10 7v3m0 0v3m0-3h3m-3 0H7"></path>
          </svg>
          <span>INSPECT HIGH-RES SCHEMATIC</span>
        </div>
      </div>

      <!-- Blueprint Extraction Tags -->
      <div class="mt-6 border-hairline-t pt-4">
        <div class="text-mono-500 font-mono text-[10px] uppercase tracking-wider mb-2.5">
          Verified Blueprint Capabilities & Callouts:
        </div>
        <div class="flex flex-wrap gap-2">
          {labels_html}
        </div>
      </div>

      {secondary_img_html}
    </section>

    <!-- Deep Technical Information Sections (2-Column Grid) -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
      
      <!-- Column 1: What It Does -->
      <section class="border-hairline bg-mono-900/50 p-6 sm:p-8">
        <div class="flex items-center space-x-2 text-mono-300 font-mono text-xs uppercase tracking-widest border-hairline-b pb-3 mb-6">
          <span class="w-2 h-2 bg-accent-orange inline-block"></span>
          <span>Operational Capabilities // What It Does</span>
        </div>
        <ul class="space-y-4">
          {what_html}
        </ul>
      </section>

      <!-- Column 2: How It Works -->
      <section class="border-hairline bg-mono-900/50 p-6 sm:p-8">
        <div class="flex items-center space-x-2 text-mono-300 font-mono text-xs uppercase tracking-widest border-hairline-b pb-3 mb-6">
          <span class="w-2 h-2 bg-accent-cyan inline-block"></span>
          <span>Technical Architecture // How It Works</span>
        </div>
        <ul class="space-y-4">
          {how_html}
        </ul>
      </section>
    </div>

    <!-- Hardware & Software Specs (2-Column Grid) -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
      
      <!-- Hardware Suite -->
      <section class="border-hairline bg-mono-900/50 p-6 sm:p-8">
        <div class="flex items-center space-x-2 text-mono-300 font-mono text-xs uppercase tracking-widest border-hairline-b pb-3 mb-6">
          <span class="w-2 h-2 bg-accent-orange inline-block"></span>
          <span>Hardware & Sensor Suite Specifications</span>
        </div>
        <div class="grid grid-cols-1 gap-3">
          {specs_html}
        </div>
      </section>

      <!-- Software & Protocols -->
      <section class="border-hairline bg-mono-900/50 p-6 sm:p-8">
        <div class="flex items-center space-x-2 text-mono-300 font-mono text-xs uppercase tracking-widest border-hairline-b pb-3 mb-6">
          <span class="w-2 h-2 bg-accent-cyan inline-block"></span>
          <span>Software Stack & Telemetry Protocols</span>
        </div>
        <div class="grid grid-cols-1 gap-3">
          {sw_html}
        </div>
      </section>
    </div>

    <!-- Bottom Navigation Bar (Prev / Next) -->
    <nav class="border-hairline bg-mono-950 p-4 sm:p-6 flex flex-col sm:flex-row items-center justify-between gap-4 font-mono text-xs">
      <a href="{prev_sys['slug']}.html" class="inline-flex items-center space-x-2 text-mono-400 hover:text-white transition">
        <span>←</span>
        <span>PREVIOUS: {prev_sys['name']} (#{prev_sys['id']})</span>
      </a>

      <a href="../index.html" class="px-4 py-2 border border-mono-700 bg-mono-900 text-mono-200 hover:text-white hover:border-mono-400 transition">
        CATALOG OVERVIEW
      </a>

      <a href="{next_sys['slug']}.html" class="inline-flex items-center space-x-2 text-mono-400 hover:text-white transition">
        <span>NEXT: {next_sys['name']} (#{next_sys['id']})</span>
        <span>→</span>
      </a>
    </nav>
  </main>

  <!-- Fullscreen Image Inspection Modal -->
  <div id="image-modal" class="fixed inset-0 z-50 bg-black/90 backdrop-blur-md hidden items-center justify-center p-4" onclick="closeModal()">
    <div class="relative max-w-7xl max-h-[95vh] w-full flex flex-col items-center" onclick="event.stopPropagation()">
      <div class="w-full flex items-center justify-between pb-3 text-mono-400 font-mono text-xs">
        <span id="modal-title">{sys_data['name']} Blueprint Inspection</span>
        <button onclick="closeModal()" class="px-3 py-1 border border-mono-700 hover:border-white text-white bg-mono-900">
          CLOSE [ESC]
        </button>
      </div>
      <img id="modal-img" src="" alt="High resolution preview" class="max-h-[85vh] w-auto object-contain border-hairline shadow-2xl" />
    </div>
  </div>

  <!-- Minimalist Footer -->
  <footer class="border-hairline-t bg-mono-950 font-mono text-xs text-mono-500 mt-auto">
    <div class="max-w-[1400px] mx-auto px-4 sm:px-6 lg:px-8 py-6 flex flex-col sm:flex-row items-center justify-between gap-4">
      <div class="flex items-center space-x-3">
        <span class="w-1.5 h-1.5 bg-mono-600 inline-block"></span>
        <span class="text-mono-400">AUTHOR: piksliviksi</span>
        <span class="text-mono-700">|</span>
        <span>DEFENSE, EW &amp; AUTONOMOUS SYSTEMS</span>
      </div>
      <div>
        <a href="https://github.com/piksliviksi" target="_blank" class="hover:text-mono-300 transition">github.com/piksliviksi</a>
      </div>
    </div>
  </footer>

  <script>
    function openModal(src) {{
      document.getElementById('modal-img').src = src;
      const modal = document.getElementById('image-modal');
      modal.classList.remove('hidden');
      modal.classList.add('flex');
      document.body.classList.add('overflow-hidden');
    }}

    function closeModal() {{
      const modal = document.getElementById('image-modal');
      modal.classList.add('hidden');
      modal.classList.remove('flex');
      document.body.classList.remove('overflow-hidden');
    }}

    window.addEventListener('keydown', (e) => {{
      if (e.key === 'Escape') closeModal();
    }});
  </script>
</body>
</html>
"""
    return page_html

def main():
    projects_dir = os.path.join(os.path.dirname(__file__), "projects")
    os.makedirs(projects_dir, exist_ok=True)

    n = len(SYSTEMS)
    for i, sys_data in enumerate(SYSTEMS):
        prev_sys = SYSTEMS[(i - 1) % n]
        next_sys = SYSTEMS[(i + 1) % n]
        page_content = generate_project_page(sys_data, prev_sys, next_sys)
        file_path = os.path.join(projects_dir, f"{sys_data['slug']}.html")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(page_content)
        print(f"Generated: {file_path}")

    print("All 13 project pages successfully generated!")

if __name__ == "__main__":
    main()
