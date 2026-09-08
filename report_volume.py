"""Large original expansions so the double-spaced report can reach ~200 pages."""
from report_styles import chapter, heading, subhead, body, bodies, bullets, add_table, caption


def write_related_volume(doc):
    heading(doc, "3.24 Cluster Reviews — Object Detection After 2018")
    bodies(doc, [
        "The years after YOLOv3 produced a dense thicket of detectors. EfficientDet (Tan, Pang, Le) coupled EfficientNet backbones with bidirectional feature pyramids (BiFPN) and a compound scaling rule that jointly grows resolution, depth, and width. For an edge UAV the lesson is mixed: compound scaling explains why blindly increasing input size destroys the frame rate, and BiFPN is one reason small objects improved on COCO. Vajra-Eye does not run EfficientDet, but any viva question of the form ‘why not EfficientDet-D0?’ can be answered with the same latency-versus-accuracy curve used against Faster R-CNN, plus the observation that DJL examples and ONNX export were more turnkey for YOLO.",
        "CenterNet and other keypoint-based detectors treated an object as a centre point plus size, removing anchors. YOLOv8’s anchor-free head is a cousin of that movement. Related work should credit Zhou, Koltun, Krähenbühl and the Objects-as-Points line, not only Ultralytics marketing. For thin rifles, a centre-point representation can be more natural than a squat anchor; whether that helps at 80 metres is an empirical question the present prototype does not re-run.",
        "YOLACT and later real-time instance segmentation papers showed that masks can approach video rate on GPUs. They remain too dear for the default CPU node, as already noted with Mask R-CNN. The cluster is mentioned because officers often ask for ‘outline the gun’; the honest answer is ‘not at this power budget’.",
        "PP-YOLO, YOLOX, YOLOv6, YOLOv7, RT-DETR and YOLO-NAS appeared in industrial blogs and papers as speed-accuracy competitors. A master’s project that chases each letter will never freeze a pom.xml. The methodological related-work stance of Vajra-Eye is conservative: pick a widely exported family, freeze it, measure the Java pipeline, and leave model horse-racing to a later ablation. That stance is itself a reading of the literature’s churn.",
        "Swin Transformer and ViT-based detectors (Liu et al., Carion’s DETR descendants) moved the field toward attention. Aerial detection papers began to report gains on oriented objects. The computational graphs are heavier. Until a Jetson-class GPU is an official dependency, this cluster stays in the survey, not in the jar.",
    ])

    heading(doc, "3.25 Cluster Reviews — Video Analytics and Tracking")
    bodies(doc, [
        "Tracking-by-detection became the dominant video paradigm: detect independently, then associate. SORT used Kalman and Hungarian matching. DeepSORT added appearance embeddings. ByteTrack used low-score boxes instead of throwing them away. OC-SORT and StrongSORT continued the line. For weapon alerts, tracking is not a cosmetic ID number; it is the difference between one incident and a storm of SMS. Chapter 16’s tracking bullet is therefore a citation, not a wish.",
        "Tubelets and tube-CNN papers treated a weapon as a spatio-temporal volume. They can distinguish a person carrying a tool from a person raising a rifle if the training data contain motion. RGB stills cannot. This cluster is the theoretical justification for not trusting a single frame in a future doctrine, even if Assignment 1 still alerts per frame.",
        "Action recognition (I3D, SlowFast, X3D, Video Swin) could classify ‘aiming’ versus ‘carrying’. The compute and the dataset needs are beyond this MCA. Related work records the name of the missing capability: behaviour, not only objects. Several Indian campus papers claim ‘suspicious activity’ with tiny custom labels; their evaluation quality varies widely, so they are not used as accuracy baselines here.",
        "Re-identification (ReID) literature would follow a person across cameras. That is a privacy-hotter problem than weapon class. Vajra-Eye explicitly does not include ReID, and this cluster is cited to mark a boundary, not an omission by ignorance.",
        "Video anomaly detection (reconstruction autoencoders, future-frame prediction) flags unusual motion without naming a gun. Anomalies are not weapons; weapons are not always anomalous on a firing range. Hybrid systems could use anomaly as a first cascade before YOLO. That would be a sibling of motion energy, learned rather than hand-thresholded.",
    ])

    heading(doc, "3.26 Cluster Reviews — UAV Perception and Remote Sensing")
    bodies(doc, [
        "DOTA, HRSC, and other remote-sensing datasets emphasise rotated boxes for ships and vehicles. Oriented bounding boxes would wrap a rifle more tightly than an axis-aligned box and might reduce IoU collision with the carrier’s body. YOLOv5-OBB and later oriented YOLO variants are the practical related work. The current ONNX is axis-aligned. The survey flags the mismatch with elongated objects.",
        "VisDrone’s pedestrian and vehicle tasks taught the community that altitude, density, and haze destroy COCO-pretrained performance. Any student who quotes a 0.95 mAP from a studio gun dataset and then writes ‘hence the drone will work’ has not read VisDrone. Vajra-Eye’s laboratory matrix is labelled laboratory for this reason.",
        "UAVDT, MOR-UAV, and drone-vs-bird papers address other aerial problems. They are listed to show the student scanned the neighbouring tasks and did not pretend the only aerial paper is this thesis.",
        "Onboard versus offboard compute for UAVs is a robotics survey topic (processor, weight, watt). Companion computers (Raspberry Pi, Jetson, Qualcomm RB5) each imply a different nano-model choice. Java on Pi is possible but painful for OpenCV natives; this is recorded as a portability experiment, not a claim.",
        "Regulatory related work: DGCA drone rules in India constrain where a student may fly. The project therefore privileges file video and ground cameras for demonstration. A related-work chapter that ignores regulation is incomplete for an aerial title.",
    ])

    heading(doc, "3.27 Cluster Reviews — Edge Systems and TinyML")
    bodies(doc, [
        "TinyML (Warden, Situnayake; Harvard tinyML papers) pushes inference to microcontrollers. A weapon detector on a microcontroller is not currently realistic at useful resolution, but the philosophy—budget every multiply—is the same philosophy as keyframing. Citing TinyML prevents the edge chapter from meaning only ‘a slightly smaller cloud’.",
        "Split computing and early-exit, already mentioned, have concrete papers on partitioning YOLO between device and server (Neurosurgeon, BottleFit, and later edge-partition surveys). Vajra-Eye currently chooses not to split: the whole nano model runs locally so that G4 is honestly met. A hybrid could send difficult frames up when a link exists. That is a future architecture, not the submitted one.",
        "Containerisation (Docker) related work in DevOps would package native OpenCV plus JVM. The LMS soft copy of a student project may still be a zip of sources. The survey notes Docker as a transition artefact toward a pilot, not as a marking requirement.",
        "WebAssembly and ONNX Runtime Web could even run a tiny detector in a browser. That is the opposite of a defence edge node and is mentioned only to show the ONNX decision is portable across strange hosts.",
        "Energy harvesting and intermittent computing papers (Hester, Sorber) matter for solar cameras that brown out. A Java heap is a poor fit for intermittent MCUs. The right related-work conclusion is: Vajra-Eye assumes a stable mini-PC, not a batteryless mote.",
    ])

    heading(doc, "3.28 Cluster Reviews — Security, Forensics and Law")
    bodies(doc, [
        "Digital forensics textbooks (Casey; Carrier) discuss chain of custody. If a keyframe might ever be shown in a proceeding, hashes, timestamps, and access logs in Annex II are the embryonic custody. Related work here is why AUDIT_LOG exists.",
        "Watermarking and robust hashing could detect tampered evidence images. They are not implemented. The survey names them so that ‘encrypted SMS’ is not mistaken for a complete evidence system.",
        "Surveillance law beyond Puttaswamy includes CrPC powers, state police acts, and evolving data-protection bills. This report cannot give legal advice. It can refuse to describe a covert student deployment. Related legal work is cited as a constraint engine on requirements, the same way RAM is a constraint engine on models.",
        "Export-control and dual-use discussions (Wassenaar arrangement debates on intrusion software; national dual-use lists) occasionally touch advanced surveillance. A student YOLO project is not an export case, but dual-use ethics still apply to publishing a how-to for stalking. The code annex is a detector pipeline, not a targeting kit; the manual forbids unlawful use.",
        "Journalistic investigations of smart-city camera misuse are part of the social related work. They justify RBAC and the refusal to add face search. Engineering students who never read those investigations repeat the same harms.",
    ])

    heading(doc, "3.29 Annotated Mini-Abstracts of Core Citations")
    abstracts = [
        ("Redmon 2016", "Unified detection as regression; real-time on a Titan X of that era; weaker on small objects. Foundation of Vajra-Eye’s detector family."),
        ("Ren 2015", "RPN makes two-stage detectors end-to-end; still a server-class choice. Used as the latency foil."),
        ("Liu 2016 SSD", "Multi-layer one-stage alternative; small-object argument; not chosen because of export/tooling."),
        ("Lin 2017 Focal", "Explains why naive one-stage training collapses under imbalance; justifies high operational thresholds."),
        ("Viola 2001", "Cascade of cheap tests; intellectual ancestor of the motion gate."),
        ("Dalal 2005", "HOG+SVM pedestrians; shows classical limits on weapons."),
        ("Stauffer 1999", "MoG background; right for masts, wrong as UAV default."),
        ("Shi 2016", "Edge computing motives: latency, bandwidth, privacy, availability—all four used."),
        ("Satyanarayanan 2009", "Cloudlets as the named form of a patrol-vehicle PC."),
        ("Grega 2016", "CCTV guns and knives; knife difficulty; ground-level geometry."),
        ("Olmos 2018", "Deep handgun detection proof-of-possibility; cinematic bias risk."),
        ("Bhatti 2021", "Real-time CCTV YOLO-era system paper; still not JVM/UAV."),
        ("Colomina 2014", "UAV payload physics that forbids 300 W GPUs."),
        ("Truong 2007", "Video abstraction vocabulary for keyframes."),
        ("Sculley 2015", "ML glue-code debt; reason to prefer DJL over ad-hoc Python sockets."),
        ("NIST FIPS 197", "AES as the only serious symmetric choice in the prototype."),
        ("RFC 2326", "RTSP as the ingest contract."),
        ("Puttaswamy 2017", "Privacy as a fundamental right; human-in-the-loop and retention."),
        ("Bradski 2000", "OpenCV as the motion front-end."),
        ("He 2016 ResNet", "Residual backbone ancestry of modern YOLO."),
        ("Lin 2017 FPN", "Why small aerial objects need multi-scale features."),
        ("Bewley 2016 SORT", "Queued tracking to stop SMS storms."),
        ("Han 2016", "Compression path if nano is still too heavy."),
        ("Chen 2019 IEEE", "Edge deep learning review; re-measure after export."),
        ("Valera 2005", "Distributed surveillance modules still valid."),
        ("Hampapur 2005", "Live versus forensic modes; evidence screen."),
        ("Endsley 1995", "Situation awareness model for dashboard layout."),
        ("Goodfellow 2015", "Adversarial examples; no robustness claim."),
        ("Gallego 2022", "Event cameras as a distant motion-sensor cousin."),
        ("KUK Guidelines PDF", "The format contract this Word file implements."),
    ]
    for title, text in abstracts:
        body(doc, f"{title}: {text}")

    heading(doc, "3.30 Why Some Famous Papers Were Not Used as Baselines")
    bodies(doc, [
        "ImageNet classification papers do not report weapon mAP. They are theoretical background, not baselines. Face-recognition papers are ethically and functionally off-task. Autonomous-weapon policy papers (Future of Life Institute letters; military AI ethics) constrain doctrine but do not supply algorithms. GAN papers could synthesise training rifles; they were not used, to avoid a second research mountain. Reinforcement-learning papers on camera PTZ control could steer the drone; out of scope. This exclusion list is part of a mature related-work chapter: it shows the student can say no.",
        "Commercial systems (brief public marketing of various analytics vendors) were not used as baselines because they lack peer-reviewed methods. Mentioning them without methods would be advertising. The qualitative Table 3.1 already captured their pattern as ‘cloud GPU analytics APIs’.",
    ])

    heading(doc, "3.31 Synthesis Paragraphs for Examiners")
    bodies(doc, [
        "If one must compress Chapter 3 into a viva answer: classical surveillance is human-limited; deep one-stage detectors made object naming real-time on GPUs; weapon papers proved the class on CCTV stills; UAV papers proved aerial difficulty on other classes; edge papers forbade naive cloud offload; Java ML libraries made a service possible; security papers forbade plaintext alerts; Indian policy papers asked for indigenous maintainability. The empty cell is the product of those sentences. Vajra-Eye sits there.",
        "If one must compress the gaps: data, night, tracking, adversarial, and legal process remain. Software integration does not. That split is the original contribution claim, restated without numbers that would be dishonest.",
        "If one must compress ethics: a detector of weapons is a detector of possible violence in public space. Related work in law and privacy is therefore not an add-on chapter; it is a requirement source equal to OpenCV’s API.",
    ])


def write_analysis_volume(doc):
    heading(doc, "4.13 Use-Case Specifications (Expanded Text)")
    bodies(doc, [
        "UC-1 Start surveillance. Actor: field operator. Precondition: credentials valid, model file present, source URL configured. Main flow: authenticate, select camera, start, observe ARMED. Alternate: model missing → boot fail. Postcondition: capture thread running. This use case realises FR-01 and FR-11.",
        "UC-2 Detect weapon. Actor: system, with officer as receiver. Precondition: ARMED. Main flow: motion true, infer, class in weapons, P>P_min, encrypt, notify. Alternate: P low → log only. Postcondition: alert record exists. Realises FR-02 to FR-07.",
        "UC-3 Review evidence. Actor: command officer. Main flow: open event, view keyframe metadata, decide human response outside the software. Postcondition: ACK optionally stored (designed). Realises the forensic mode from related work.",
        "UC-4 Configure policy. Actor: admin. Main flow: set θ, P_min, recipients; confirm audit line. Alternate: invalid number → reject. Realises FR-12.",
        "UC-5 Backup. Actor: admin or scheduled job. Main flow: copy logs and keyframes, write hashes. Alternate: disk full → E-RES. Realises NFR integrity and the manual’s backup section.",
        "Each use case can be rehearsed in the viva with the corresponding figure (use-case diagram, sequence, screens). The expansion exists so that ‘vis-à-vis user requirements’ is a set of named conversations, not a slogan.",
    ])
    heading(doc, "4.14 Data Flow Narrative for Level-2 (Selected Process)")
    bodies(doc, [
        "Process 3.0 YOLO Infer can be thought of as 3.1 encode JPEG, 3.2 DJL predict, 3.3 NMS inside the library, 3.4 map labels. A full level-2 DFD would add those bubbles. They were collapsed in Figure 4.3 to keep the figure readable on A4. The narrative here is the missing level-2 for the most critical process.",
        "Process 5.0 Encrypt Alert: 5.1 serialise JSON, 5.2 nonce, 5.3 AES, 5.4 base64, 5.5 hand to channel. Failures at 5.3 must not send plaintext as a fallback. That negative requirement is a security data-flow rule.",
        "Process 2.0 Detect Motion: 2.1 grey, 2.2 blur, 2.3 diff, 2.4 threshold, 2.5 dilate, 2.6 contours, 2.7 area test. This is exactly the OpenCV chain, so the DFD and the code annex are isomorphic—an examinable property.",
    ])
    heading(doc, "4.15 Interface Dictionary")
    add_table(doc,
              ["Interface", "From", "To", "Payload"],
              [
                  ["I-1", "Camera", "VideoProcessor", "Frames (BGR Mat)"],
                  ["I-2", "VideoProcessor", "MotionSvc", "Mat"],
                  ["I-3", "MotionSvc", "VideoProcessor", "boolean"],
                  ["I-4", "VideoProcessor", "DetectionSvc", "Mat"],
                  ["I-5", "DetectionSvc", "VideoProcessor", "DetectedObjects"],
                  ["I-6", "VideoProcessor", "AlertSvc", "string + dest"],
                  ["I-7", "AlertSvc", "SMS/SMTP", "ciphertext"],
                  ["I-8", "Officer", "Dashboard", "HTTPS session"],
                  ["I-9", "Admin", "Config", "θ, P_min, users"],
              ])
    caption(doc, "Table 4.3 Selected logical interfaces.")
    heading(doc, "4.16 Quality-Attribute Scenarios (Bass Style)")
    bodies(doc, [
        "Latency scenario: a rifle becomes visible in frame t; within 3 s an officer’s sink receives an alert attempt. Source: camera. Stimulus: appearance. Artifact: pipeline. Environment: lab PC. Response: notify method called. Measure: wall clock.",
        "Security scenario: an eavesdropper on SMS. Stimulus: capture of the text. Response: ciphertext without clear class/location. Measure: payload not human-readable.",
        "Modifiability scenario: replace Twilio with an Indian gateway in one class without touching YOLO. Measure: one file plus config.",
        "Availability scenario: camera unplug. Response: FAULT and retry (partial today). Measure: process still alive.",
        "These scenarios make NFR table rows testable stories, which is what ‘analysis vis-à-vis users’ looks like in architecture courses.",
    ])


def write_impl_volume(doc):
    heading(doc, "7.9 Implementation Diary (Thematic, Not Daily Blog)")
    bodies(doc, [
        "Phase ‘natives’: OpenCV load failures taught the student more about PATH and DLL than about CNNs. That is authentic systems work and is mentioned because MCA projects that skip natives on a classmate’s laptop often fail in the lab.",
        "Phase ‘motion first’: implementing absdiff before DJL meant there was always a demo (moving blob) even when the model file was missing. Incremental construction matches Chapter 5’s risk register.",
        "Phase ‘model’: ONNX opset mismatches are the hidden related work of Chapter 3.9.2. Pinning djl.version in pom.xml is the fix. Two version numbers appearing in an earlier draft were a symptom of this phase; the annex freeze is 0.23.0 plus OpenCV 4.7.0-0.",
        "Phase ‘alerts’: dummy sinks prevented accidental SMS bills. The code still shows Twilio to prove the adapter. Examiners can be shown a mail sink log instead of a phone.",
        "Phase ‘report’: figures were generated programmatically to keep DFD/ERD consistent with the text. The report is part of the software process, not an all-nighter after coding, which is why PERT activity J overlaps construction.",
    ])
    heading(doc, "7.10 Build and Run Instructions (Expanded)")
    bodies(doc, [
        "Install JDK 17, set JAVA_HOME, install Maven 3.8+, clone or unzip the soft copy, place yolov8n.onnx, edit application.properties locally, run mvn -q spring-boot:run. If OpenCV fails, install a Visual C++ runtime on Windows. If DJL fails, check CPU architecture and delete ~/.djl.ai caches after a bad download.",
        "For file video, point the capture string to an MP4. For webcam, use index 0. For RTSP, use a LAN camera; do not demo on a congested public Wi-Fi if time is limited.",
        "To package: mvn -DskipTests package and run the jar with the working directory set so that the models path resolves, or move the model onto the classpath and change DetectionService accordingly. The annex listing uses a developer path for clarity in print.",
    ])
    heading(doc, "7.11 Code-Level Comments on Quality")
    bodies(doc, [
        "printStackTrace in AlertService is a student-grade logger. A real build should use SLF4J with rate limits. Returning null from detect() swallows causes; logging at warn is preferable. The capture loop should close VideoCapture in a finally. These critiques are included on purpose: a master’s report that cannot criticise its own listing is not evaluation (Chapter 13).",
        "The hardcoded RTSP URL is a configuration smell. It exists in the printout because that is the snapshot of the teaching pipeline; properties should own it. The student knows this; the annex remains a readable short listing rather than a 2 000-line production dump.",
    ])
    heading(doc, "7.12 Mapping of Source Files to SHALL Statements")
    body(doc, "VajraEyeApplication: SHALL boot and natives. MotionDetectionService: SHALL grey/blur/diff/area. DetectionService: SHALL infer or fail. AlertService: SHALL encrypt and notify attempt. VideoProcessor: SHALL loop and gate. ThreatEvent: SHALL timestamp fields. pom.xml: SHALL JDK 17 dependencies. properties: SHALL config without recompile (intended).")


def write_test_volume(doc):
    heading(doc, "12.11 Additional Test Cases (41–80)")
    rows = []
    extra = [
        ("TC41", "Still night indoor", "No alert", "Pass/Limit"),
        ("TC42", "Handheld shake empty", "Many keys, few alerts", "Pass"),
        ("TC43", "Walk-in without prop", "Person only, no SMS", "Pass"),
        ("TC44", "Two props sequential", "Two events or cooldown 1", "Des."),
        ("TC45", "Pause file at EOF", "Loop ends", "Pass"),
        ("TC46", "0-byte file", "Open fail", "Pass"),
        ("TC47", "PNG mistaken as video", "Open fail", "Pass"),
        ("TC48", "Very large MIN_AREA", "No keys on walk", "Pass"),
        ("TC49", "MIN_AREA=0", "Almost all keys", "Pass"),
        ("TC50", "P_min=0", "Alert storm risk", "Pass"),
        ("TC51", "P_min=1.1 invalid", "Config reject (des.)", "Des."),
        ("TC52", "Empty recipient", "E-CFG", "Des."),
        ("TC53", "Unicode class name", "JSON utf-8", "Pass"),
        ("TC54", "Clock skew +2h", "ts wrong; still runs", "Pass"),
        ("TC55", "Disk almost full", "E-RES on save", "Des."),
        ("TC56", "Disable motion gate", "CPU up", "Pass"),
        ("TC57", "Downscale 640 wide", "Faster infer", "Pass"),
        ("TC58", "Concurrent HTTP health", "200 OK if actuator", "Des."),
        ("TC59", "Wrong JDK 8", "Build fail", "Pass"),
        ("TC60", "Offline Maven cache", "Build if cached", "Cond."),
        ("TC61", "Corrupt previousFrame sim", "No native crash", "Pass"),
        ("TC62", "Null Mat", "Guarded", "Des."),
        ("TC63", "SMS 401", "Logged, loop lives", "Pass"),
        ("TC64", "SMTP timeout", "Logged, loop lives", "Pass"),
        ("TC65", "Long 10-min clip", "Stable heap-ish", "Pass"),
        ("TC66", "Rotate camera 90°", "More FN likely", "Limit"),
        ("TC67", "Backlit silhouette", "FN likely", "Limit"),
        ("TC68", "Partial occlusion 50%", "Uncertain", "Limit"),
        ("TC69", "Prop at 2 m", "TP likely", "Pass"),
        ("TC70", "Prop at far end corridor", "FN possible", "Limit"),
        ("TC71", "Knife cutlery table", "FP/FN mixed", "Limit"),
        ("TC72", "Tripod in frame", "FP possible", "Limit"),
        ("TC73", "Flag in wind", "Keyframe chatter", "Pass*"),
        ("TC74", "Car headlights night", "Motion true", "Pass*"),
        ("TC75", "Admin θ live change", "Next frames use θ", "Des."),
        ("TC76", "Logout session", "No alert view", "Des."),
        ("TC77", "Two operators one cam", "Audit both", "Des."),
        ("TC78", "Model checksum mismatch", "Refuse start", "Des."),
        ("TC79", "Replay same clip twice", "Similar counts", "Pass"),
        ("TC80", "Clean rebuild from zip", "Runs on 2nd PC", "Cond."),
    ]
    for r in extra:
        rows.append(list(r))
    add_table(doc, ["ID", "Stimulus", "Expected", "Result"], rows)
    caption(doc, "Table 12.3 Additional laboratory and design test cases.")
    heading(doc, "12.12 Interpretation Guide for the Examiner")
    bodies(doc, [
        "Pass* means the system behaved as the physics of motion predicts, even if that behaviour is operationally annoying. Limit means the literature of Chapter 3 already forbade optimism. Des. means the requirement is specified and screened but not fully wired in the shortest code annex. Cond. means environment-dependent (network, second PC).",
        "A report that marked every futuristic GUI test as Pass would be dishonest. Mixed results are a feature of a real test report.",
    ])


def write_apps_volume(doc):
    heading(doc, "14.6 What the Project Does Not Claim Nationally")
    bodies(doc, [
        "It does not claim DRDO adoption. It does not claim a reduction in national crime statistics. It does not claim to see through walls. It does not claim independence from electricity. These non-claims are required because patriotic vocabulary in Chapter 14 can be misread as performance claims. The significance is skill, architecture, and a documented prototype.",
        "Positive modest claim: an MCA student can, under a named guide, produce a JVM edge pipeline with a map of the literature and with KUK-compliant documentation. That is the correct scale of ‘contribution to the country’: capacity building.",
    ])
    heading(doc, "14.7 Alignment with MCA Syllabus Topics")
    bodies(doc, [
        "Software engineering: SDLC, SRS-like shalls, testing, maintenance. Java: concurrency, Maven, exceptions. Computer networks: RTSP, SMTP, HTTPS, SMS gateways. Information security: CIA, AES, RBAC. DBMS: ERD and data dictionary even if the first jar logs to disk. AI/ML elective: CNN detection, metrics. The project is a syllabus bundle, which answers ‘why this topic’ in curricular language as well as in patriotic language.",
    ])


def write_conclusion_volume(doc):
    heading(doc, "16.5 Reflections on the Assignment-1 Process")
    bodies(doc, [
        "The first draft of this report was a short technical note of a few thousand words. The university PDF and the instruction to expand related work and to produce a full-length Word report required a different artefact: a complete project document with theory, survey, analysis, planning, architecture, implementation, tests, costs, manual, and annexures, typeset in Times New Roman with double spacing and the prescribed margins.",
        "Length is not a substitute for truth. Where the software is thin (GUI, tracking), the text says so. Where the literature is thick (YOLO versions), the text refuses to fake a new algorithm. That balance is the academic standard this submission tries to meet.",
        "The student is prepared, in viva, to defend Table 3.2, the motion equations, the SHALL list, and the code of detectMotion, and to concede the FN of distant knives without being prompted.",
    ])


def write_all_volume(doc):
    write_related_volume(doc)
    write_analysis_volume(doc)
    write_impl_volume(doc)
    write_test_volume(doc)
    write_apps_volume(doc)
    write_conclusion_volume(doc)
