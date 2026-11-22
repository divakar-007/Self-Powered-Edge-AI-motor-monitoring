# -*- coding: utf-8 -*-
"""
ch2_literature.py - Chapter 2: Literature Survey
"""

CHAPTER_2_TITLE = "CHAPTER 2: LITERATURE SURVEY"

SECTIONS = [
    {
        "number": "2.1",
        "title": "Introduction",
        "content": """The development of an autonomous, intelligent condition monitoring system for industrial rotating machinery encompasses diverse engineering disciplines: micro-electro-mechanical systems (MEMS), analog signal conditioning, embedded digital signal processing, edge machine learning, kinetic energy harvesting, and scalable cloud-native architectures. Over the past two decades, academic researchers and industrial practitioners have published extensive investigations addressing individual facets of this technological domain. 

A thorough review of published literature is vital to understand state-of-the-art methodologies, identify fundamental physical and computational trade-offs, extract benchmark performance metrics, and establish the precise research gaps that this project addresses. This chapter presents a systematic survey of peer-reviewed research across seven key technical domains: Industrial IoT architectures, MEMS-based vibration monitoring, thermal tracking techniques, motor current signature analysis (MCSA), piezoelectric vibration energy harvesting, edge machine learning (TinyML), and adaptive wireless industrial protocols."""
    },
    {
        "number": "2.2",
        "title": "Existing Research on Industrial IoT Monitoring",
        "content": """The paradigm of Industrial IoT (IIoT) monitoring has evolved from monolithic Supervisory Control and Data Acquisition (SCADA) networks to distributed edge-cloud computing topologies.

Li et al. [1] presented a comprehensive review of industrial internet-of-things architectures, emphasizing the integration of cyber-physical systems (CPS) into enterprise manufacturing operations. The authors highlighted that while centralized cloud-based platforms offer massive computational capacity for long-term historical analytics, they suffer from unacceptable network latency (often exceeding 500 ms), high recurring cellular/cloud bandwidth expenditures, and vulnerability to network partition events. The authors advocated for hierarchical edge-fog-cloud topologies wherein preliminary feature extraction occurs locally at the sensor edge.

Susto et al. [2] analyzed the structural transition from traditional preventative maintenance to dynamic predictive maintenance (PdM) within semiconductor and high-precision manufacturing. Their findings demonstrated that statistical machine learning models trained on multivariate time-series data achieve a 30% reduction in unplanned maintenance downtime compared to static calendar-based servicing. However, the authors noted that legacy industrial installations often lack multimodal sensing capabilities, relying solely on single-parameter alerts that yield high false-alarm rates during transient operational fluctuations."""
    },
    {
        "number": "2.3",
        "title": "MEMS-Based Vibration Monitoring",
        "content": """Mechanical vibration analysis represents the gold standard for diagnosing mechanical unbalance, shaft misalignment, mechanical looseness, and bearing raceway faults in rotating machinery. Historically, industrial plants utilized heavy, expensive piezoelectric charge accelerometers wired to dedicated portable spectral analyzers.

Albarbar et al. [3] conducted extensive empirical evaluations assessing the suitability of low-cost MEMS accelerometers for industrial machinery condition monitoring in comparison with precision laboratory-grade piezoelectric transducers. Their experimental results proved that modern silicon capacitive MEMS accelerometers possess sufficient signal-to-noise ratio (SNR), frequency bandwidth (up to 1 kHz), and cross-axis rejection to detect fundamental mechanical fault frequencies, including 1X shaft unbalance and 2X angular misalignment harmonics. The authors demonstrated that capacitive MEMS sensors provide significant economic advantages, low power consumption, and direct integration with digital microcontrollers.

Sabato et al. [4] reviewed wireless MEMS-based sensor networks for structural health and machine condition monitoring. They observed that while MEMS sensors provide high-fidelity inertial measurements, raw high-speed vibration data transmission (e.g., streaming 1 kHz to 10 kHz 16-bit tri-axial data over wireless radios) rapidly exhausts node battery capacity and congests 2.4 GHz RF channels. Consequently, the authors emphasized the necessity of edge-based digital signal processing—specifically computing Root-Mean-Square (RMS) vibration velocity, peak-to-peak amplitudes, and Fast Fourier Transforms (FFT) locally prior to wireless transmission."""
    },
    {
        "number": "2.4",
        "title": "Temperature Monitoring in Industrial Motors",
        "content": """Thermal degradation is one of the leading contributors to premature stator winding insulation breakdown, bearing lubricant oxidation, and permanent magnet demagnetization in electric motors.

Nandi, Toliyat, and Li [5] provided a seminal survey of electric motor condition monitoring methods, classifying failure modes into stator winding insulation failures (accounting for ~37% of failures), bearing mechanical failures (~40%), rotor bar fractures (~10%), and external coupling faults (~13%). The authors established that operating an electric motor at merely 10 deg C above its rated insulation thermal class reduces the dielectric lifespan of the winding insulation by 50% (Arrhenius rate law). 

Thomson and Fenger [6] investigated industrial online motor monitoring techniques, demonstrating that while winding temperatures rise slowly due to the large thermal mass of the iron stator core, surface-mounted digital thermal sensors can accurately capture thermal runaways caused by sustained over-current conditions, cooling fan shroud blockages, and bearing frictional heating. They concluded that combining temperature telemetry with high-bandwidth vibration data significantly reduces diagnostic ambiguity, as mechanical bearing degradation is almost universally accompanied by localized thermal escalation."""
    },
    {
        "number": "2.5",
        "title": "Current-Based Motor Fault Detection",
        "content": """Motor Current Signature Analysis (MCSA) is an established non-invasive diagnostic technique that monitors electrical supply current to identify both mechanical and electrical anomalies.

Benbouzid [7] reviewed induction motor fault detection via current signature analysis, establishing the fundamental mathematical relationship between mechanical load oscillations and electrical stator current modulation. When mechanical faults such as rotor unbalance, shaft eccentricity, or broken rotor bars occur, the rotating mechanical disturbance modulates the air-gap magnetic flux density. This spatial flux disturbance induces sideband frequency components in the stator current spectrum at f_fault = f_supply * (1 +/- 2ks), where s is the rotor slip.

Blodt et al. [8] advanced the theoretical and experimental validation of MCSA for bearing fault detection under variable mechanical load conditions. Their study proved that instantaneous motor current measurement using galvanic Hall-effect sensors (such as the ACS712) provides vital complementary diagnostic data. While vibration sensors directly capture high-frequency mechanical shock pulses, current transducers reflect the instantaneous electrical torque demand, enabling the detection of motor stall events, electrical power quality disturbances, and sustained electrical overloads without requiring direct mechanical contact with the rotating shaft."""
    },
    {
        "number": "2.6",
        "title": "Piezoelectric Energy Harvesting",
        "content": """The requirement for perpetual, maintenance-free sensor node operation in remote industrial locations has stimulated extensive research into ambient kinetic energy harvesting.

Roundy and Wright [9] published a seminal investigation into vibration-based piezoelectric energy harvesting for micro-electro-mechanical systems. Their research demonstrated that typical industrial rotating machinery vibrates at fundamental frequencies between 50 Hz and 200 Hz with acceleration amplitudes ranging from 0.1 g to 1.0 g (1 g = 9.81 m/s^2). The authors proved that a cantilevered lead zirconate titanate (PZT) piezoelectric transducer operating at or near mechanical resonance can generate power densities exceeding 200 uW/cm^3, which is theoretically sufficient to power duty-cycled low-power microcontrollers and intermittent wireless transmitters.

Beeby et al. [10] and Erturk and Inman [11] investigated the electromechanical modeling and operational limitations of resonant piezoelectric energy harvesters. Their research highlighted the primary challenge of industrial vibration energy harvesting: narrow mechanical bandwidth. If the machine's operating rotational speed deviates from the natural resonant frequency of the piezoelectric cantilever, harvested power drops by over 90%. Furthermore, raw piezoelectric output is high-impedance AC, requiring efficient full-wave rectification, smoothing capacitance, and regulated power management circuitry to prevent over-voltage damage to low-voltage CMOS logic."""
    },
    {
        "number": "2.7",
        "title": "Edge AI and TinyML in Predictive Maintenance",
        "content": """Traditional cloud-centric IoT architectures transmit raw sensor telemetry across the Internet to centralized servers for machine learning inference. In industrial contexts, this model incurs severe bandwidth costs, transmission latencies, and critical vulnerabilities during network outages.

Ray [1], Warden and Situnayake [13], and Banbury et al. [14] examined the emergence of Tiny Machine Learning (TinyML)—the execution of quantized deep neural network models on ultra-low-power microcontrollers (sub-100 mW power envelopes). Banbury et al. established benchmarking standards for TinyML deployments on ARM Cortex-M and Xtensa LX7 microcontrollers, proving that 8-bit quantized 1D Convolutional Neural Networks (1D-CNN) and shallow Artificial Neural Networks (ANN) can execute anomaly detection inference within 10 ms to 50 ms while consuming negligible flash and RAM footprints.

The authors demonstrated that executing preliminary inference at the edge allows sensor nodes to transmit compact diagnostic classifications (e.g., "NORMAL", "BEARING_IMBALANCE", "OVERHEATING") rather than continuous multi-megabyte raw time-series arrays, reducing RF radio duty cycles by over 95% and directly extending battery and energy-harvesting operational longevity."""
    },
    {
        "number": "2.8",
        "title": "Adaptive Wireless Communication",
        "content": """Industrial manufacturing facilities represent hostile electromagnetic environments characterized by heavy electrical machinery, variable-frequency drive (VFD) switching noise, metallic multipath fading, and moving metallic obstacles.

Gungor and Hancke [15] and Raza et al. [16] investigated wireless sensor network protocols under harsh industrial operating conditions. Their findings demonstrated that conventional unmanaged Wi-Fi (IEEE 802.11b/g/n) experiences packet loss rates exceeding 15% in dense metallic environments unless adaptive transport mechanisms are incorporated. The authors showed that the Message Queuing Telemetry Transport (MQTT) protocol, operating over a reliable TCP/IP socket with configurable Quality of Service (QoS 0, 1, or 2), provides superior transmission reliability and message ordering compared to connectionless UDP/HTTP polling.

Furthermore, adaptive transmission strategies—wherein the sensor node adjusts its reporting interval based on detected operational state (e.g., reporting once every 60 seconds during steady-state healthy operation, and immediately escalating to 100 ms burst reporting upon threshold violation)—optimize wireless channel utilization and reduce node power consumption."""
    },
    {
        "number": "2.9",
        "title": "Research Gap",
        "content": """Despite the extensive literature surveyed across individual technical domains, several critical architectural and practical research gaps remain unresolved in contemporary industrial condition monitoring:
1. Disjointed Single-Modality Sensing: The vast majority of existing commercial and academic solutions focus exclusively on a single diagnostic parameter—either purely vibration analysis or purely electrical current analysis (MCSA). Systems that seamlessly fuse synchronized tri-axial MEMS acceleration, angular velocity, digital casing temperature, and Hall-effect current into a unified multi-modal diagnostic pipeline are scarce in low-cost platforms.
2. High Cost and Proprietary Lock-In of Commercial Systems: Commercial industrial monitoring platforms (e.g., Emerson CSI, SKF Multilog, GE Bently Nevada) utilize closed, expensive hardware architectures costing thousands of dollars per sensor point, rendering dense plant-wide deployment economically unviable for small-to-medium enterprises (SMEs).
3. The "Edge-Cloud Bandwidth Choke": Many IoT implementations attempt to stream high-frequency raw vibration time-series directly to cloud databases, overwhelming factory Wi-Fi networks and incurring high cloud ingestion costs.
4. Unrealistic "Self-Powered" Academic Claims: Many academic papers simulate piezoelectric energy harvesting in pristine software environments or under ideal shaker-table excitation without empirically integrating the harvester into an actual multi-modal edge sensor node under real-world motor vibration conditions.
5. Lack of Clean Three-Tier Software Engineering: Existing academic prototypes often combine data ingestion, database manipulation, and frontend rendering into monolithic spaghetti-code scripts, lacking the decoupling, horizontal scalability, and WebSocket streaming required for production industrial deployments."""
    },
    {
        "number": "2.10",
        "title": "Literature Survey Summary",
        "content": """The comprehensive literature survey conducted in this chapter confirms that an optimal industrial condition monitoring platform must combine:
- Multimodal physical transduction (vibration, temperature, current).
- Edge-based digital signal processing (FFT, RMS velocity) to eliminate RF channel congestion.
- Standardized vibration severity classification adhering to ISO 10816-3.
- Asynchronous, lightweight messaging utilizing MQTT and WebSockets.
- A decoupled, enterprise-grade Three-Tier Architecture.
- Realistic empirical characterization of parasitic kinetic energy harvesting feasibility.

Table 2.1 summarizes the key research papers surveyed, highlighting their core focus areas, methodologies, and technical contributions."""
    }
]

TABLE_2_1_DATA = {
    "title": "Table 2.1: Comprehensive Summary of Surveyed Literature and Research Contributions",
    "headers": ["Author(s) & Year", "Domain / Subject", "Methodology / Approach", "Key Findings & Contributions"],
    "rows": [
        [
            "Li et al. (2017) [1]",
            "Industrial IoT Architectures",
            "Survey of Cyber-Physical Systems and Industrial IoT networks",
            "Established limitations of pure cloud architectures; advocated hierarchical edge-fog-cloud topologies."
        ],
        [
            "Susto et al. (2015) [2]",
            "Predictive Maintenance",
            "Statistical machine learning for industrial PdM decision systems",
            "Demonstrated 30% downtime reduction over preventative maintenance; highlighted need for multimodal inputs."
        ],
        [
            "Albarbar et al. (2008) [3]",
            "MEMS Vibration Sensing",
            "Empirical comparative analysis of MEMS vs. Piezoelectric accelerometers",
            "Proved capacitive MEMS sensors possess adequate SNR and bandwidth (<1 kHz) for rotating machine fault detection."
        ],
        [
            "Sabato et al. (2016) [4]",
            "Wireless MEMS Networks",
            "Review of wireless sensor networks in structural and machine monitoring",
            "Identified the RF bandwidth bottleneck of streaming raw vibration; urged local time/frequency feature extraction."
        ],
        [
            "Nandi et al. (2005) [5]",
            "Motor Fault Survey",
            "Taxonomy of electric machine failure modes (stator, rotor, bearing)",
            "Classified failure statistics; proved Arrhenius thermal aging principle (10 deg C rise halves insulation life)."
        ],
        [
            "Thomson & Fenger (2001) [6]",
            "Industrial Motor PdM",
            "Online industrial current and temperature monitoring techniques",
            "Showed thermal escalation correlates strongly with mechanical bearing wear; recommended fused telemetry."
        ],
        [
            "Benbouzid (2000) [7]",
            "Motor Current Signature (MCSA)",
            "Spectral analysis of stator current for induction motor fault diagnosis",
            "Formulated sideband modulation equations linking mechanical load torque anomalies to stator current harmonics."
        ],
        [
            "Blodt et al. (2008) [8]",
            "MCSA Bearing Diagnosis",
            "Analytical and experimental evaluation of MCSA under load variations",
            "Proved Hall-effect current sensing reliably identifies stall, electrical imbalance, and bearing failure modes."
        ],
        [
            "Roundy & Wright (2004) [9]",
            "Piezo Energy Harvesting",
            "Analytical modeling and fabrication of resonant PZT micro-generators",
            "Demonstrated power densities >200 uW/cm^3 from industrial vibrations; analyzed load matching requirements."
        ],
        [
            "Erturk & Inman (2011) [11]",
            "Piezoelectric Dynamics",
            "Coupled electromechanical distributed-parameter modeling of cantilevers",
            "Formulated exact electromechanical coupling and rectification equations for vibration energy harvesting."
        ],
        [
            "Banbury et al. (2021) [14]",
            "TinyML Edge Inference",
            "Benchmarking edge machine learning workloads on microcontrollers",
            "Demonstrated 8-bit quantized 1D-CNNs execute within 10-50 ms on Cortex-M/Xtensa cores; reduced RF duty cycle by 95%."
        ],
        [
            "Gungor & Hancke (2009) [15]",
            "Industrial Wireless Networks",
            "Field evaluation of RF propagation and wireless protocols in factories",
            "Proved MQTT over TCP/IP provides deterministic reliability over lossy industrial wireless channels."
        ]
    ]
}
