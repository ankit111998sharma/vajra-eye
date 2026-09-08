"""Chapters 7-11: implementation, keyframing, security, screens, cost."""
from report_styles import chapter, heading, subhead, body, bodies, bullets, add_figure, add_table, caption, add_code_lines


def write_implementation(doc):
    chapter(doc, "CHAPTER 7")
    body(doc, "METHODOLOGY, SYSTEM IMPLEMENTATION AND HARDWARE/SOFTWARE", indent=False)

    heading(doc, "7.1 Methodology Adopted")
    bodies(doc, [
        "Methodology here means the combination of SDLC iteration (Chapter 5), computer-vision pipeline design (Chapter 8), and Java implementation practice. Requirements were frozen enough to code, then tests revealed threshold mistakes, then thresholds returned to the admin manual. Models were not trained from scratch in this submission; a pre-trained YOLOv8n was exported to ONNX. That is a valid MCA methodology when the learning outcome is systems integration, provided the report does not pretend that training from scratch occurred.",
        "Coding standards: Java 17, Maven, package com.vajra, services annotated with @Service, configuration via application.properties, no secrets in source. Illustrative keys in listings are fake and must be replaced.",
        "Configuration management: pom.xml pins DJL and OpenCV versions. The report records two nearby version numbers that appeared during drafting (0.23 and 0.25 style coordinates); the annex listing is the reference snapshot for compilation.",
    ])

    heading(doc, "7.2 Detailed Life Cycle of the Project")
    bodies(doc, [
        "The university asks for a detailed life cycle including ERD, DFD, screens, process, testing method, test report, and code sheet. Those artefacts are distributed across Chapters 4, 10, 12 and Annexure IV. This section narrates the life cycle in time.",
        "Inception: topic Vajra-Eye, guide consent, synopsis heads. Elaboration: literature (Chapter 3), DFD/ERD, risk that DJL would not load ONNX. Construction: motion service first (because it needs no model file), then DetectionService, then AlertService, then the loop. Transition: laboratory tests, schematic screens, this report. The cycle is allowed to spin once more after examiner comments.",
    ])

    heading(doc, "7.3 Hardware Used")
    add_table(doc,
              ["Component", "Specification"],
              [
                  ["Processor", "Intel i7 / edge-class CPU"],
                  ["RAM", "16 GB"],
                  ["OS", "Windows 10/11 or Linux 64-bit"],
                  ["Java", "JDK 17"],
                  ["Video input", "Recorded files and live RTSP"],
                  ["Model", "YOLOv8n ONNX"],
                  ["Optional", "USB webcam for bench demo"],
              ])
    caption(doc, "Table 7.1 Hardware used in the laboratory.")
    body(doc, "Field hardware may be a rugged mini-PC. Drones used in a future trial remain the camera source; this project does not claim to have built an airframe.")

    heading(doc, "7.4 Software Used")
    bodies(doc, [
        "JDK 17, Apache Maven, Spring Boot starter, DJL API, DJL ONNX Runtime engine, org.openpnp OpenCV, Twilio SDK (optional), a mail starter for SMTP, Git for local history if used, and Microsoft Word for this report. Python with matplotlib was used only to generate report figures, not as the runtime of Vajra-Eye.",
        "IDE choice is free: IntelliJ IDEA, Eclipse, or VS Code with Java packs. The build must succeed from mvn -q -DskipTests package on a clean machine with native OpenCV loaded.",
    ])

    heading(doc, "7.5 Project Structure")
    add_code_lines(doc, """Vajra-Eye/
├── pom.xml
├── src/main/java/com/vajra/
│   ├── VajraEyeApplication.java
│   ├── service/
│   │   ├── MotionDetectionService.java
│   │   ├── DetectionService.java
│   │   ├── AlertService.java
│   │   └── VideoProcessor.java
│   └── model/
│       └── ThreatEvent.java
├── src/main/resources/
│   ├── application.properties
│   └── models/
│       └── yolov8n.onnx
└── src/test/java/   (unit tests)""")

    heading(doc, "7.6 Implementation Notes by Stage")
    subhead(doc, "7.6.1 Native library loading")
    body(doc, "OpenCV native libraries are the most common cause of ‘it works on my machine’ failure. nu.pattern.OpenCV.loadShared() is used in the application class. Linux servers may additionally need GTK-free OpenCV builds if running headless.")
    subhead(doc, "7.6.2 Frame acquisition")
    body(doc, "VideoCapture can open device index 0, a file path, or rtsp://user:pass@host:554/path. Credentials in URLs are a secret; the annex uses a placeholder host. Buffering latency in IP cameras can dominate model latency; operators should prefer sub-second GOP settings on the camera when possible.")
    subhead(doc, "7.6.3 Inference session")
    body(doc, "Creating a Predictor per frame is simple and slow. A production optimisation is a long-lived predictor with synchronisation. The annex listing uses try-with-resources per call for safety in a student build. Chapter 16 lists pooling as future work.")
    subhead(doc, "7.6.4 Notification")
    body(doc, "Twilio is one of many SMS vendors. An Indian deployment may require DLT-registered templates. Email is easier in the laboratory using a college SMTP or a dummy sink. The architecture treats both as AlertChannel implementations even if the first listing inlines Twilio.")

    heading(doc, "7.7 Resources and Limitations (Guideline Head)")
    bodies(doc, [
        "Resources: hardware in Table 7.1, open-source software, public papers, guide time, and the student’s labour. Data from a live defence organisation is not used (write NA for classified industry data; the annex data dictionary still describes intended fields).",
        "Limitations relative to a comprehensive national system: no radar, no thermal in the current path, no swarm, no certified HSM, no 24×7 NOC, limited classes, and laboratory rather than monsoon-night evaluation. These limits are honest and required by the university’s ‘limitations of the proposed system’ instruction.",
    ])

    heading(doc, "7.8 Summary of Chapter 7")
    body(doc, "Methodology is iterative integration of a frozen detector into Java services. Hardware is a common PC. Software is Maven/Spring/DJL/OpenCV. Life-cycle artefacts live in neighbouring chapters. The distinctive algorithm—motion keyframing—is next.")


def write_motion(doc):
    chapter(doc, "CHAPTER 8")
    body(doc, "MOTION-BASED KEYFRAMING AND DETECTION PIPELINE", indent=False)

    heading(doc, "8.1 Concept of Adaptive Keyframe Extraction")
    bodies(doc, [
        "Continuous processing of every frame is computationally expensive, particularly when a drone camera shakes and most frames contain no new object. Vajra-Eye evaluates temporal variation and forwards only frames with significant motion to YOLOv8. Static frames are skipped. Resources are spent when the world might have changed.",
        "Adaptive does not mean unsupervised learning of θ in the current build. It means the decision is data-dependent: the same code may skip 70% of frames in a still courtyard and skip far fewer during a patrol with constant ego-motion. Operators then raise θ or add a future homography stage.",
    ])
    add_figure(doc, "pipeline.png", "Figure 8.1 Detection pipeline flow.")

    heading(doc, "8.2 Mathematical Model")
    bodies(doc, [
        "Let F_t be the current greyscale blurred frame and F_{t-1} the previous. The absolute difference is D_t = |F_t − F_{t-1}|. A motion score M_t may be the sum of D_t over pixels, or a function of contour areas after thresholding D_t. If M_t > θ (or if a blob area > A_min), the frame is a keyframe and is sent to the detector.",
        "In the implementation, THRESHOLD = 25 on the 8-bit difference image and MIN_AREA = 1000 pixels are the practical counterparts of θ and A_min. They are not universal constants; they are starting points for a 1080p-ish laboratory camera. A 4K frame would need a larger area, or the image should be downscaled before the motion stage—which is also a recommended speed tactic.",
        "Let 1_key(t) be 1 if the frame is a keyframe. The expected compute saving versus all-frame inference is 1 − E[1_key]. Laboratory observation in Chapter 12 reports a saving of the order of 70% frames and 45% CPU under a moderately still scene. A continuously panning drone will show a smaller saving; that is predicted by the model, not a contradiction of it.",
    ])
    add_figure(doc, "motion_keyframe.png", "Figure 8.2 Adaptive keyframe selection (M_t > θ).")

    heading(doc, "8.3 Advantages of Motion-Based Processing")
    bullets(doc, [
        "Reduced computational load: fewer YOLO calls.",
        "Lower power: relevant to battery nodes.",
        "Improved real-time behaviour: queue does not grow with empty frames.",
        "Bandwidth optimisation: alerts and keyframes, not full video, on the uplink.",
        "Scalability: more cameras per CPU if each is mostly idle.",
    ])
    bodies(doc, [
        "Disadvantages, which related work also predicts: global illumination changes fire the gate; ego-motion fires the gate; very slow aiming of a weapon may stay under θ. The operational answer is not to abandon the gate but to pair it with periodic heartbeat inference (for example one YOLO call every N seconds even if still) in a future revision so that a static armed sentry is not invisible.",
    ])

    heading(doc, "8.4 Pipeline Logic (End to End)")
    bodies(doc, [
        "Capture; motion; keyframe decision; YOLO; class/confidence filter; encrypt; notify; log. Each arrow is a possible test seam. The process involved, in university language, is this pipeline plus the human process of responding to an SMS, which is outside software but inside the operational manual.",
    ])

    heading(doc, "8.5 Parameters and Tuning Guidance")
    add_table(doc,
              ["Parameter", "Typical start", "If too many keyframes", "If missed motion"],
              [
                  ["Gaussian k", "21×21", "increase slightly", "decrease"],
                  ["Binary θ", "25", "increase", "decrease"],
                  ["MIN_AREA", "1000", "increase", "decrease"],
                  ["YOLO P_min", "0.85", "increase", "decrease (more FP)"],
                  ["Heartbeat N", "off", "n/a", "enable 1/N s"],
              ])

    heading(doc, "8.6 Summary of Chapter 8")
    body(doc, "Keyframing is the main algorithmic originality of the integration. It is classical vision used as a scheduler for a modern detector. Security of what happens after a positive detection is the next chapter.")


def write_security(doc):
    chapter(doc, "CHAPTER 9")
    body(doc, "ALERTING, SECURITY MECHANISM AND CONTROLS", indent=False)

    heading(doc, "9.1 Encrypted Alert Generation")
    bodies(doc, [
        "A structured alert contains timestamp, class, confidence, and camera identifier. The payload is encrypted before it is handed to SMS or mail. AES-GCM is recommended; the teaching listing also shows AES-CBC. IVs/nonces must be unique. Hard-coded keys in source are unacceptable outside a classroom illustration.",
        "The point of payload encryption, even when TLS exists, is defence in depth: SMS gateways and mail servers are third parties. A ciphertext in a text message is less informative to an interceptor than the sentence ‘Rifle at tower 4’.",
    ])
    add_figure(doc, "security_layers.png", "Figure 9.1 Defence-in-depth security layers.")

    heading(doc, "9.2 Notification System")
    bodies(doc, [
        "Email uses Spring Mail or a Java mail client. SMS uses an HTTP API such as Twilio. Redundancy is the requirement: if SMS DLT fails, mail may still arrive. The message body for a real deployment should be a short code plus a handle to the dashboard, not a full classified dump.",
        "Alert fatigue controls: cooldown per camera, maximum N alerts per hour, and a maintenance mode that silences SMS while still logging. These controls are specified for the product even if the shortest code path sends every detection.",
    ])

    heading(doc, "9.3 Data Security, Access Rights, Backup and Controls")
    bodies(doc, [
        "University manuals ask for security aspects, access rights, backup, and controls. Access rights: roles FIELD_USER, CMD_OFFICER, ADMIN. FIELD_USER starts capture. CMD_OFFICER views alerts and keyframes. ADMIN sets thresholds, users, and backup policy. Least privilege applies.",
        "Backup: encrypted alert logs and keyframe files are copied daily to an offline disk; hashes (SHA-256) of files are stored in AUDIT_LOG. Retention: academic default 30 days unless law requires more or less. Destruction: overwrite then delete.",
        "Controls: TLS for HTTP, password hashing (prefer Argon2/bcrypt), lockout after repeated failures, time-synchronised logs, and change management for pom.xml and model files (a swapped ONNX is a security event).",
    ])
    add_table(doc,
              ["Threat", "Control"],
              [
                  ["Eavesdropped SMS", "Payload AES; short codes"],
                  ["Stolen laptop", "Disk encryption; hashed passwords"],
                  ["Rogue insider", "RBAC + audit"],
                  ["Model tampering", "Checksum of ONNX at boot"],
                  ["Alert replay", "Timestamp + nonce in payload"],
                  ["DoS by fake RTSP", "Auth on config API; rate limit"],
              ])
    caption(doc, "Table 9.1 Security controls mapped to threats.")

    heading(doc, "9.4 Summary of Chapter 9")
    body(doc, "Security is layered: node, transport, payload, audit. Notification is multi-channel. Access rights and backup complete the operational story that the user manual will repeat in procedural language.")


def write_screens(doc):
    chapter(doc, "CHAPTER 10")
    body(doc, "INPUT AND OUTPUT SCREEN DESIGN", indent=False)

    heading(doc, "10.1 Design Principles")
    bodies(doc, [
        "Screens are designed for glanceability. An officer under stress should see camera identity, threat class, confidence, and time without hunting. Colour: navy for chrome, red for live threat, grey for idle. The figures are schematic layouts for the report, not marketing screenshots of a classified UI.",
        "Input screens collect credentials, RTSP URLs, and thresholds. Output screens show detections, evidence, and logs. Error states (camera down, model missing) must be first-class screens, not stack traces.",
    ])

    heading(doc, "10.2 Login")
    add_figure(doc, "screen_login.png", "Figure 10.1 Operator login (schematic).")
    body(doc, "Inputs: username, password, optional role display after auth. Output: session cookie or JWT. Failures: unknown user, wrong password, locked account. No detailed error that helps an attacker enumerate users in a hardened build (generic ‘invalid credentials’).")

    heading(doc, "10.3 Live Dashboard")
    add_figure(doc, "screen_dashboard.png", "Figure 10.2 Live surveillance dashboard (schematic).")
    body(doc, "Output: camera list, ARMED/IDLE/FAULT state, adaptive FPS, last motion time. Input: start/stop. This is the operator’s home screen.")

    heading(doc, "10.4 Alert Console")
    add_figure(doc, "screen_alert.png", "Figure 10.3 Threat alert console (schematic).")
    body(doc, "Output: class, confidence, channel status (SMS sent/failed). Input: acknowledge button (future) so that alert fatigue can be measured.")

    heading(doc, "10.5 Evidence Review")
    add_figure(doc, "screen_review.png", "Figure 10.4 Keyframe evidence review (schematic).")
    body(doc, "Output: keyframe thumbnail path, motion score, event id. This screen is the forensic half of the IBM-style dual mode discussed in related work.")

    heading(doc, "10.6 Admin Policy")
    add_figure(doc, "screen_admin.png", "Figure 10.5 Admin policy panel (schematic).")
    body(doc, "Inputs: θ, minimum YOLO probability, recipient list. Changes are audit-logged.")

    heading(doc, "10.7 Audit Viewer")
    add_figure(doc, "screen_logs.png", "Figure 10.6 Audit log viewer (schematic).")
    body(doc, "Output: user, action, hash check. Read-only for CMD_OFFICER; export for ADMIN.")

    heading(doc, "10.8 Input/Output Data Formats")
    bodies(doc, [
        "Input video: RTSP or MP4. Input config: properties file or admin form. Output alert JSON (then ciphertext): {cameraId, class, confidence, ts}. Output logs: CSV/JSON lines. These formats are the practical I/O specification for testers.",
    ])

    heading(doc, "10.9 Summary of Chapter 10")
    body(doc, "Six schematic screens cover login, live ops, alerts, evidence, policy, and audit. They implement the use cases of Chapter 4 in visual form.")


def write_cost(doc):
    chapter(doc, "CHAPTER 11")
    body(doc, "COST AND BENEFIT ANALYSIS", indent=False)

    heading(doc, "11.1 Purpose")
    bodies(doc, [
        "University format requires cost and benefit analysis. For a student prototype the rupee figures are illustrative, not a tender. The point is to show that the student can think like a systems analyst: people and false alarms cost more than Maven.",
    ])

    heading(doc, "11.2 Cost Elements")
    add_table(doc,
              ["Element", "Academic prototype (INR)", "One-site pilot (INR, order)"],
              [
                  ["PC / mini PC", "Already owned / 40,000", "60,000–1,20,000"],
                  ["Camera / drone time", "Lab webcam / 0", "Hired UAV as per policy"],
                  ["Software licences", "0 (open source)", "0–support contract"],
                  ["SMS pack", "0–500", "2,000–10,000 / year"],
                  ["Student labour", "Course effort", "n/a"],
                  ["Training officers", "n/a", "20,000–50,000"],
                  ["Annual maintenance", "n/a", "15–20% of hardware"],
              ])
    caption(doc, "Table 11.1 Cost elements (illustrative INR, not a quotation).")

    heading(doc, "11.3 Benefits")
    bodies(doc, [
        "Quantifiable (pilot hypothesis): reduced hours of unaided watching; reduced uplink GB; faster notice of a visible weapon. Not quantified here: lives and property, because such claims would be speculative in an MCA report.",
        "Qualitative: indigenous maintainability, audit trail, learning value for the student and for a future IT cell. Bandwidth saving from keyframing is a real technical benefit even when rupees are not booked.",
        "Cost of false positives: each false SMS consumes officer attention and, eventually, trust. A ‘cheap’ detector with 30% precision is economically expensive. This is why θ and P_min are economic instruments, not only mathematical ones.",
    ])

    heading(doc, "11.4 Break-even Narrative")
    body(doc, "A single commercial analytics camera licence can cost more per year than the academic stack. A pilot that replaces even a fraction of unused recorded footage with a few true alerts can justify a mini-PC. Break-even fails if the system is switched off due to noise. Therefore testing (next chapter) is part of the economic argument.")

    heading(doc, "11.5 Summary of Chapter 11")
    body(doc, "Costs are dominated by hardware and people, not by YOLO. Benefits are attention and bandwidth. False alarms are a cost. Evaluation must therefore measure precision, not only the joy of a bounding box.")
