"""Chapters 1 and 4-6: introduction, analysis, planning, architecture."""
from report_styles import chapter, heading, subhead, body, bodies, bullets, add_figure, add_table, caption, add_code_lines


def write_intro(doc):
    chapter(doc, "CHAPTER 1")
    body(doc, "INTRODUCTION", indent=False)

    heading(doc, "1.1 Background of the Study")
    bodies(doc, [
        "Surveillance is older than electronics. Watchtowers, sentries, and patrols are information systems in human form. Electronics multiplied the eyes and did not automatically multiply the understanding. A camera records; a person interprets; a delay grows between the two. The twenty-first century added cheap sensors, cheap aircraft, and cheap compute, and thereby created a new imbalance: more pixels than people to watch them.",
        "Artificial intelligence, specifically visual object detection, offers a way to restore balance by converting pixels into named events. The conversion is imperfect. Models confuse objects, fail in fog, and inherit the biases of their training sets. An MCA project cannot abolish those imperfections. It can, however, wrap a detector in an engineering system that is fast enough, small enough, and accountable enough to be studied, criticised, and later improved.",
        "Vajra-Eye is that wrapping. The Sanskrit word vajra denotes a thunderbolt and a diamond—speed and hardness. The project uses the name as a reminder of the design goals: a quick local decision and a robust software artefact. The eye is the camera. The intelligence is a Java service that refuses to look equally hard at every empty frame.",
        "Kurukshetra University requires MCA third-semester candidates to submit a project report based on work done during the project period, including software development and a soft copy on the LMS. This report is written to those rules: prescribed front matter, synopsis heads, main-report heads (objectives, theory, problem, analysis, PERT, module logic, methodology, hardware/software, maintenance, cost-benefit, life cycle, ERD/DFD, screens, testing, code, user manual), and annexures.",
    ])

    heading(doc, "1.2 Evolution of Surveillance Practice")
    bodies(doc, [
        "Analogue CCTV of the 1980s and 1990s produced tapes and, later, digital video recorders. The product was footage for after-the-fact inquiry. The 2000s brought IP cameras and centralised video management systems. The 2010s brought commercial analytics and, after 2014, deep detectors that could name objects rather than only flag motion. The 2020s brought cheap quadcopters in civilian airspace, including airspace that security agencies must watch.",
        "Each generation left a residue of unsolved work. Centralised analytics assumed generous networks. Deep detectors assumed generous GPUs. UAV video assumed a pilot staring at a phone. Vajra-Eye is situated after these generations: it assumes a constrained network, a constrained GPU (sometimes none), and a pilot who cannot stare forever.",
        "The evolution also includes law. Recording public space is regulated; automated classification of people and objects is more sensitive still. A 2026 academic system must therefore be designed with access control and audit from the first class diagram, not as a sticker added after the viva.",
    ])

    heading(doc, "1.3 Need for Intelligent Aerial Surveillance in India")
    bodies(doc, [
        "India’s land borders are long, terrain is mixed, and manpower, however dedicated, is finite. Public events in cities concentrate risk. Critical infrastructure—power, transport, campuses, courts—requires perimeters that are watched without turning every citizen into a suspect. Drones already fly for mapping, journalism, and leisure; the same airframes can carry a camera for lawful security tasks if the software is responsible.",
        "Imported turnkey analytics create vendor lock-in and data-residency anxiety. An MCA project cannot replace a national procurement. It can show that a student team, using open frameworks, can assemble a pipeline whose source is readable by Indian engineers. That demonstration is the civic need this topic serves, in addition to the technical need of detecting a visible weapon in a moving view.",
        "Rural connectivity further motivates edge design. A hill post may have a camera and a solar-charged computer with only intermittent 4G. If intelligence lives only in a metro data centre, the hill post is blind whenever the backhaul dies—the exact moment at which local awareness is most valuable.",
    ])

    heading(doc, "1.4 Project Overview")
    bodies(doc, [
        "Vajra-Eye is an intelligent surveillance middleware designed to identify unauthorised handheld weapons such as guns, rifles, grenades, and knives from aerial or elevated video feeds. Unlike traditional CCTV analytics, it is written to tolerate the erratic motion of drone-mounted cameras and the low-power constraints of field-deployed edge hardware.",
        "The system functions as an autonomous digital sentry. It analyses live or recorded video, spends deep-learning compute only on motion-rich keyframes, and alerts authorities when a detection passes a confidence gate. Encrypted payloads and a Spring Boot command layer complete the path from pixel to officer.",
        "The software is organised as a Maven project: VajraEyeApplication, MotionDetectionService, DetectionService, AlertService, VideoProcessor, and ThreatEvent. A YOLOv8n ONNX graph sits in resources. Configuration lives in application.properties. This overview is expanded into architecture, process logic, and code annexures in later chapters.",
    ])
    add_figure(doc, "layered_arch.png", "Figure 2.1 Logical layer stack of Vajra-Eye (preview; architecture is detailed in Chapter 6).")

    heading(doc, "1.5 Problem Statement and Definition of the Problem")
    bodies(doc, [
        "Definition of the problem (university head): Design and implement a software system that (a) ingests video from a drone-like or CCTV source, (b) detects visible handheld weapons without sending every frame to a cloud GPU, (c) notifies authorised persons through protected channels in a few seconds, and (d) is documented with the SDLC artefacts required for MCA Project Work.",
        "Elaboration: Manual monitoring is inefficient and prone to fatigue. Four-kilometre-range 4K downlinks are impractical on thin links. Pure cloud inference adds round-trip delay and outage risk. Pure Python notebooks are not packaged services. Pure detectors without security leak sensitive evidence. The problem is the conjunction of these failures, not any one of them alone.",
        "Stakeholders: field operator, command officer, system administrator, and (indirectly) the public whose safety is the justification and whose privacy is the constraint. Success is measured by pipeline completeness, latency, responsible false-alarm behaviour, and report compliance—not by a marketing mAP number.",
    ])

    heading(doc, "1.6 Why this Topic was Chosen")
    bodies(doc, [
        "The topic matches the university instruction that project topics be based on the syllabus or on industry need in sync with the course. Computer networks, Java, software engineering, and emerging AI electives all appear in an MCA curriculum. Weapon-aware aerial analytics is an industry need discussed in public safety forums. The combination is therefore in-scope.",
        "Personal academic interest also played a role: the student wished to learn how a neural model is hosted, not only how it is trained. DJL was selected as a learning vehicle that few classmates use, reducing the chance of a duplicated mini-project and increasing the chance of genuine debugging experience.",
        "Ethical caution accompanied the choice. The project will not be used to target individuals in the student laboratory. Test videos are to be recorded in controlled scenes or selected from lawful public research sources. The report uses schematic screens, not doxxing imagery.",
    ])

    heading(doc, "1.7 Objectives of the Project")
    bodies(doc, [
        "The primary objectives, restated in examination form, are as follows.",
    ])
    bullets(doc, [
        "To develop a Java-based real-time inference engine suitable for edge deployment.",
        "To implement YOLOv8 object detection using Deep Java Library and an ONNX model.",
        "To reduce computational and power overhead through temporal frame differencing and motion-based keyframing.",
        "To generate encrypted alerts and to notify authorised users by email and/or SMS.",
        "To keep end-to-end detection-and-alert latency of the order of a few seconds in the laboratory (target: less than three seconds on the reference PC for a keyframe that contains a clear object).",
        "To produce university-compliant design artefacts: DFD, ERD, PERT, screens, tests, data dictionary, and user manual.",
        "To survey related work in enough depth that design choices are cited rather than improvised.",
    ])

    heading(doc, "1.8 Scope and Limitations of Scope")
    bodies(doc, [
        "In scope: RGB video; visible weapons present in the model’s label set; single-node edge processing; Spring APIs; laboratory tests; documentation. Optional thermal input is a future interface, not a current sensor. Multi-drone swarming is out of scope. Automatic weapon discharge, face identification for policing, and covert interception are ethically and legally out of scope.",
        "The project does not claim to replace human commanders. It claims to draft an attention signal. That limitation of scope is also a safety feature.",
    ])

    heading(doc, "1.9 Expected Contribution")
    bodies(doc, [
        "The contribution is a reference architecture and a running prototype for JVM-based edge weapon alerting with motion scheduling and cryptographic notification. Secondary contributions are a long original literature map and a complete MCA report template instantiated on a modern AI topic.",
        "If the software is later taken up by an organisation, the organisation must re-train models on lawful data, commission security audits, and obtain legal advice. Those steps are contributions of that organisation, not of this dissertation.",
    ])

    heading(doc, "1.10 Organisation of the Report")
    bodies(doc, [
        "Chapter 2 presents theory. Chapter 3 surveys related work in unusual depth because that was identified as a weakness of the draft submission. Chapter 4 analyses users and data flows. Chapter 5 plans time with PERT and Gantt. Chapter 6 describes architecture and module logic. Chapter 7 records methodology, hardware, and implementation. Chapter 8 details keyframing. Chapter 9 details security. Chapter 10 presents screens. Chapter 11 estimates cost and benefit. Chapter 12 reports tests. Chapter 13 discusses maintenance. Chapter 14 discusses applications. Chapter 15 is the operational manual. Chapter 16 concludes. Annexures hold the data dictionary, guide details, code, and bibliography.",
        "Page specification throughout follows the university note: A4, left 3.0 cm, right 2.0 cm, top and bottom 2.54 cm, Times New Roman 12-point body with double spacing and justified alignment, 14-point underlined paragraph headings, 20-point centred chapter headings, Courier New 10-point code, and page numbers at the bottom centre.",
    ])


def write_analysis(doc):
    chapter(doc, "CHAPTER 4")
    body(doc, "SYSTEM ANALYSIS AND DESIGN VIS-À-VIS USER REQUIREMENTS", indent=False)

    heading(doc, "4.1 Introduction to Analysis")
    bodies(doc, [
        "System analysis translates the problem statement into users, use cases, data flows, and constraints. Design vis-à-vis user requirements means that every major component is traceable to a user need rather than to a fashionable library. This chapter performs that tracing.",
        "The analysis methods used are: stakeholder interviews with the student playing the roles of operator, officer, and administrator (typical of an academic project without a live client); use-case modelling; structured DFD; ER modelling; and a quality-attribute workshop in miniature (latency, security, deployability).",
    ])

    heading(doc, "4.2 Feasibility Study")
    subhead(doc, "4.2.1 Technical feasibility")
    body(doc, "Java 17, OpenCV bindings, DJL, and YOLOv8n ONNX are all publicly available. A 16 GB RAM PC can run the nano model at a useful rate if frames are gated. Technical feasibility is therefore high for a prototype. Feasibility of a weather-proof, night-proof, court-proof product is a different question and is rated only medium without new data and hardware.")
    subhead(doc, "4.2.2 Operational feasibility")
    body(doc, "Operators already understand cameras and SMS. A dashboard that shows camera status and alerts matches existing command-post habits. Operational feasibility is high if false alarms are kept in check. If every passing iron rod triggers SMS, operators will disable the system; hence the high confidence threshold.")
    subhead(doc, "4.2.3 Economic feasibility")
    body(doc, "Software is open source. Hardware is a common PC plus a camera. SMS has a per-message cost. Compared with a commercial analytics licence, the academic stack is economically feasible. A national rollout’s true cost is training, maintenance, and false-alarm labour, discussed in Chapter 11.")
    subhead(doc, "4.2.4 Legal and ethical feasibility")
    body(doc, "Academic development is feasible. Field use requires lawful authority, privacy impact assessment, and data-retention rules. The project is feasible as a university submission; it is not self-authorising as a public deployment.")
    subhead(doc, "4.2.5 Schedule feasibility")
    body(doc, "A twenty-week plan with parallel literature and coding is feasible for Assignment-1 documentation of design plus a working core. Full field trials are not claimed inside that calendar.")

    heading(doc, "4.3 User Classes and Characteristics")
    bodies(doc, [
        "Field operator: starts and stops capture, checks that the RTSP URL is alive, may carry the edge node. Not expected to tune neural networks.",
        "Command officer: receives alerts, views keyframes, decides human response. Needs clarity and low false-alarm load.",
        "Administrator: sets thresholds, users, backup, and keys. Needs auditability.",
        "Developer/maintainer: the student now, an IT cell later. Needs readable modules and a Maven build.",
    ])
    add_figure(doc, "use_case.png", "Figure 4.1 Use-case diagram (conceptual).")

    heading(doc, "4.4 Functional Requirements")
    add_table(doc,
              ["ID", "Requirement", "Source user"],
              [
                  ["FR-01", "Ingest RTSP or file video frames", "Operator"],
                  ["FR-02", "Detect motion and select keyframes", "System"],
                  ["FR-03", "Run weapon detector on keyframes", "Officer"],
                  ["FR-04", "Filter by class and confidence", "Admin"],
                  ["FR-05", "Encrypt alert payload", "Admin"],
                  ["FR-06", "Send SMS and/or email", "Officer"],
                  ["FR-07", "Store event metadata and keyframe path", "Officer"],
                  ["FR-08", "Authenticate dashboard users", "Admin"],
                  ["FR-09", "Show live status and last detections", "Officer"],
                  ["FR-10", "Export audit log", "Admin"],
                  ["FR-11", "Fail visibly if model file missing", "Operator"],
                  ["FR-12", "Allow threshold configuration", "Admin"],
              ])
    caption(doc, "Table 4.1 Selected functional requirements.")

    heading(doc, "4.5 Non-Functional Requirements")
    add_table(doc,
              ["ID", "Quality attribute", "Target (prototype)"],
              [
                  ["NFR-01", "Latency (keyframe to notify start)", "< 3 s on reference PC"],
                  ["NFR-02", "Availability of capture loop", "Restart on camera loss"],
                  ["NFR-03", "Confidentiality of alerts", "AES; TLS on HTTP"],
                  ["NFR-04", "Integrity of logs", "Append-only audit records"],
                  ["NFR-05", "Portability", "Windows/Linux JVM"],
                  ["NFR-06", "Maintainability", "Layered Maven modules"],
                  ["NFR-07", "Resource use", "~45% CPU reduction vs all-frame"],
                  ["NFR-08", "Usability", "Schematic screens learnable in 30 min"],
              ])
    caption(doc, "Table 4.2 Non-functional requirements.")

    heading(doc, "4.6 Requirement Traceability (Narrative)")
    bodies(doc, [
        "FR-01 traces to VideoProcessor and OpenCV VideoCapture. FR-02 traces to MotionDetectionService. FR-03 traces to DetectionService. FR-04 is a policy in the process loop. FR-05/06 trace to AlertService. FR-07 traces to ThreatEvent persistence (model now; table later). FR-08/09/10 trace to the command layer described in screens. NFR-01 is tested in Chapter 12. This narrative is the vis-à-vis: users asked for timely, secret, low-noise alerts; modules exist to match.",
        "Untraced fashionable features (face galleries, social-media scraping) were rejected because no user class in Section 4.3 requested them and because they inflate ethical risk.",
    ])

    heading(doc, "4.7 Process Description and Data Flow")
    bodies(doc, [
        "The university asks that the process of the whole software system be mentioned in brief and supported by DFDs. At context level, the system is a single process exchanging video with cameras, alerts with officers, and configuration with administrators.",
    ])
    add_figure(doc, "dfd_level0.png", "Figure 4.2 Context-level DFD (Level 0).")
    bodies(doc, [
        "Level-1 decomposes ingest, motion, inference, scoring, encryption, and notify-log. Data stores hold frames briefly, models, alerts, and audit trails. This is a logical DFD: it does not freeze the physical choice of SQL versus files.",
    ])
    add_figure(doc, "dfd_level1.png", "Figure 4.3 Level-1 data flow diagram.")

    heading(doc, "4.8 Entity Relationship Design")
    bodies(doc, [
        "Although the prototype may persist with files and logs, a normalised ERD is required for life-cycle completeness and for any future database. Core entities are USER, CAMERA, THREAT_EVENT, KEYFRAME, ALERT, and AUDIT_LOG. Cardinality: one camera produces many events; one event may produce many alerts (SMS and email); one event may store one or more keyframes; users generate audit rows.",
    ])
    add_figure(doc, "erd.png", "Figure 4.4 Entity relationship diagram.")

    heading(doc, "4.9 Object-Oriented View")
    bodies(doc, [
        "Classes follow services rather than a heavy domain model, which is appropriate for a streaming pipeline. VideoProcessor orchestrates; the three services hide OpenCV, DJL, and Twilio/crypto respectively; ThreatEvent is a plain data carrier. This keeps Spring’s dependency injection aligned with the single-responsibility principle.",
    ])
    add_figure(doc, "class_diagram.png", "Figure 4.5 Core class collaboration.")

    heading(doc, "4.10 Alternative Designs Considered")
    bodies(doc, [
        "Alternative A: Python FastAPI plus Ultralytics native. Rejected for packaging and for the pedagogical goal of JVM inference. Alternative B: all frames to a cloud GPU. Rejected for NFR bandwidth and outage. Alternative C: classical HOG only. Rejected for aerial robustness. Alternative D: two-stage Faster R-CNN on server. Rejected for edge latency. The chosen design is therefore a reasoned remainder, not the first idea in the editor.",
        "Interface alternative: a thick desktop JavaFX client versus a thin web dashboard. The report’s screens are web-like because officers already live in browsers. Implementation may expose REST first and a full GUI later without changing the detection core.",
    ])

    heading(doc, "4.11 Assumptions, Dependencies and Constraints")
    bullets(doc, [
        "Assumption: a weapon that matters is at least partly visible in RGB.",
        "Assumption: the operator can supply a working RTSP URL or a file path.",
        "Dependency: Maven Central (or a mirrored repo) for libraries.",
        "Dependency: validity of the ONNX model file.",
        "Constraint: no classified data in the student repository.",
        "Constraint: SMS credentials must not be committed in clear form to public git.",
        "Constraint: double-spaced report length is large; figures are schematic.",
    ])

    heading(doc, "4.12 Summary of Chapter 4")
    body(doc, "Analysis established feasibility, users, numbered requirements, DFDs, ERD, class view, and rejected alternatives. Planning of time and critical path follows.")


def write_planning(doc):
    chapter(doc, "CHAPTER 5")
    body(doc, "SYSTEM PLANNING (PERT CHART)", indent=False)

    heading(doc, "5.1 Planning Objectives")
    bodies(doc, [
        "University format requires system planning with a PERT chart. PERT (Programme Evaluation and Review Technique) models tasks as a network of precedence with optimistic, most-likely, and pessimistic durations. For a student project the numbers are estimates, but the discipline of listing tasks and finding a critical path is real.",
        "Planning also produces a Gantt chart for calendar communication and an SDLC choice so that implementation does not proceed as unstructured hacking.",
    ])

    heading(doc, "5.2 Work Breakdown Structure")
    add_table(doc,
              ["Id", "Activity", "o", "m", "p", "te=(o+4m+p)/6"],
              [
                  ["A", "Topic freeze and synopsis", "1", "2", "3", "2.0"],
                  ["B", "Literature survey (extended)", "3", "5", "8", "5.2"],
                  ["C", "Requirement & DFD/ERD", "2", "3", "5", "3.2"],
                  ["D", "Architecture and UI schematics", "2", "3", "4", "3.0"],
                  ["E", "Motion pipeline coding", "2", "4", "6", "4.0"],
                  ["F", "DJL/YOLO integration", "3", "5", "8", "5.2"],
                  ["G", "Alert crypto & notify", "1", "3", "5", "3.0"],
                  ["H", "Dashboard/API", "2", "3", "5", "3.2"],
                  ["I", "Testing and tuning", "2", "3", "5", "3.2"],
                  ["J", "Report writing (200 pp. target)", "3", "5", "7", "5.0"],
              ])
    caption(doc, "Table 5.1 Work-breakdown with PERT expected times in weeks (illustrative).")
    body(doc, "Expected times are in student-weeks of part-time effort, not exclusive calendar weeks. Some activities overlap, as the Gantt chart shows. The literature survey was deliberately lengthened relative to a typical mini-project because Assignment 1 demanded a deeper related-work section.")

    heading(doc, "5.3 Precedence and Critical Path")
    bodies(doc, [
        "A must precede C. B may run parallel to A after topic freeze. C precedes D. D precedes E and F. E and F join at G. G and H join at I. I precedes J’s final freeze, though J starts earlier. An illustrative critical path is A–C–D–F–G–I–J, driven by the YOLO integration uncertainty (wide o–p spread on F).",
        "Slack exists on pure documentation tasks early, but Assignment-1 submission date removes that slack: the report must be frozen even if a future build improves mAP. PERT is therefore used as a risk tool: the pessimistic eight weeks on F warns the student not to switch models weekly.",
    ])
    add_figure(doc, "pert.png", "Figure 5.1 Simplified PERT network (time in weeks on arrows).")
    add_figure(doc, "gantt.png", "Figure 5.2 Project Gantt chart (20-week plan).")

    heading(doc, "5.4 Resource Planning")
    bodies(doc, [
        "Human resource: one student, part-time, with guide review cycles. Compute resource: one laptop. Information resource: papers listed in Chapter 3. Communication resource: guide meetings and LMS submission. No paid annotators are budgeted; that absence is a risk to dataset quality and is accepted for the degree prototype.",
    ])

    heading(doc, "5.5 SDLC Model Adopted")
    bodies(doc, [
        "A pure one-pass waterfall would delay coding until the 200-page report was imagined in full, which is unrealistic. A chaotic agile without documents would violate university format. The adopted model is iterative waterfall: each cycle revisits analysis-design-code-test while the document accumulates. Prototypes of motion detection were allowed to fail early.",
    ])
    add_figure(doc, "sdlc.png", "Figure 5.3 Iterative SDLC adopted for Vajra-Eye.")

    heading(doc, "5.6 Risk Register (Planning View)")
    add_table(doc,
              ["Risk", "Likelihood", "Impact", "Mitigation"],
              [
                  ["ONNX/DJL version clash", "Medium", "High", "Pin versions in pom.xml"],
                  ["RTSP unstable", "High", "Medium", "File-video fallback"],
                  ["False SMS storm", "Medium", "High", "Threshold 0.85 + cooldown"],
                  ["Guide time scarce", "Medium", "Medium", "Written queries, frozen TOC"],
                  ["Overlength report", "High", "Low", "Styles per KUK; structured ch."],
                  ["Credential leak", "Low", "High", "placeholders in repo"],
              ])

    heading(doc, "5.7 Summary of Chapter 5")
    body(doc, "Planning produced a WBS, PERT expected times, a critical path dominated by model integration, a Gantt overlap of writing and coding, an iterative SDLC, and a short risk register. Architecture can now be specified with the knowledge of what must be built first.")


def write_architecture(doc):
    chapter(doc, "CHAPTER 6")
    body(doc, "SYSTEM ARCHITECTURE AND PROCESS LOGIC OF EACH MODULE", indent=False)

    heading(doc, "6.1 Overall Architecture")
    bodies(doc, [
        "Vajra-Eye uses a three-layer architecture: perception, processing, and command. Perception is the drone or camera and any ingest adapter. Processing is the Java edge service that performs motion tests and neural inference. Command is Spring Boot’s dashboard, APIs, and notification adapters. The layers communicate with small messages, not with raw video, once a threat is scored.",
        "This separation allows a camera to be replaced without touching AES, and allows Twilio to be replaced with an Indian SMS gateway without touching YOLO. That is the operational meaning of modularity.",
    ])
    add_figure(doc, "architecture.png", "Figure 6.1 Layered architecture of Vajra-Eye.")
    add_figure(doc, "deployment.png", "Figure 6.2 Deployment view.")

    heading(doc, "6.2 Backend: Java Spring Boot")
    bodies(doc, [
        "Spring Boot is the orchestration framework. It owns process lifetime, configuration injection, and (in a fuller build) REST controllers and WebSocket relays of overlays. Security context—authentication of officers—belongs here rather than inside OpenCV.",
        "Key responsibilities include REST for telemetry and configuration, WebSocket for low-latency overlay if a UI is connected, and a security filter chain. Even if Assignment-1 demonstration emphasises the capture thread, the architecture keeps Spring as the backbone so that the project is a service, not a single main() loop with no future.",
    ])

    heading(doc, "6.3 Inference Engine: Deep Java Library")
    bodies(doc, [
        "DJL loads the ONNX graph, supplies Image and DetectedObjects types, and uses ONNX Runtime as the engine. Cross-framework compatibility is the point: the model may be trained in Python once, then frozen. High performance on the JVM is ‘near native’ relative to a poorly written JNI loop, not magic faster than TensorRT. Edge optimisation comes from choosing yolov8n and from not calling the predictor on every frame.",
    ])

    heading(doc, "6.4 Process Logic of Each Module")
    subhead(doc, "6.4.1 VajraEyeApplication")
    body(doc, "Loads OpenCV native binaries in a static block and launches Spring. Process logic: if OpenCV fails to load, the process must abort with a clear log; silent continuation would produce null Mats and mysterious crashes later.")
    subhead(doc, "6.4.2 VideoProcessor")
    bodies(doc, [
        "Opens VideoCapture on an RTSP URL or file. Loops until the stream ends. For each frame, calls motion detection; on true, calls detection; on high-probability weapon class, calls alert. Runs on a background thread started from @PostConstruct so that Spring’s web thread pool is not blocked.",
        "Failure logic: if read() fails, the loop should back off and retry rather than spin a hot CPU. The listing in the annex shows the happy path; the maintenance chapter describes the retry policy as an improvement.",
    ])
    add_figure(doc, "sequence.png", "Figure 6.3 Sequence — weapon detection and alert.")
    add_figure(doc, "state_model.png", "Figure 6.4 Camera node state model.")

    subhead(doc, "6.4.3 MotionDetectionService")
    body(doc, "Converts BGR to grey, Gaussian-blurs, stores previous grey, absdiff, thresholds, dilates, finds contours, and returns whether any contour area exceeds MIN_AREA. First frame always returns false. This logic is the adaptive keyframe gate.")
    subhead(doc, "6.4.4 DetectionService")
    body(doc, "On start, builds DJL Criteria with ONNX engine and model path. On detect(), encodes Mat to JPEG bytes, wraps as DJL Image, and predicts. Exceptions return null so that the capture loop survives a single bad frame. Production code should log the exception with rate limiting.")
    subhead(doc, "6.4.5 AlertService")
    body(doc, "Encrypts a message and sends SMS via Twilio in the illustrative listing. Email is an alternative adapter. Keys must move to a secret store before any real deployment. Cooldown logic (not in the shortest listing) should suppress duplicate SMS for the same camera within N seconds.")
    subhead(doc, "6.4.6 ThreatEvent")
    body(doc, "Holds weaponType, confidence, location, timestamp. It is the domain seed for the ERD’s THREAT_EVENT table.")

    heading(doc, "6.5 Technology Stack Summary")
    add_table(doc,
              ["Component", "Technology"],
              [
                  ["Language", "Java 17"],
                  ["Backend", "Spring Boot"],
                  ["AI", "DJL + ONNX Runtime"],
                  ["Detector", "YOLOv8n"],
                  ["Video", "OpenCV 4.x"],
                  ["Build", "Maven"],
                  ["IPC/API", "REST, WebSocket"],
                  ["Security", "AES, TLS, RBAC (designed)"],
                  ["Notify", "SMTP / Twilio"],
              ])
    caption(doc, "Table 6.1 Technology stack.")

    heading(doc, "6.6 Quality Attributes in Architectural Form")
    bodies(doc, [
        "Latency: keep inference off the WebFlux/MVC threads; gate frames. Security: encrypt payload independently of transport. Modifiability: swap AlertService gateway. Testability: services are beans. Availability: isolate native OpenCV crashes from the Spring actuator if possible (process supervisor at OS level).",
        "These tactics are textbook Bass/Kazman moves applied to a vision service. They belong in an MCA architecture chapter so that ‘we used Spring’ is not an empty sentence.",
    ])

    heading(doc, "6.7 Summary of Chapter 6")
    body(doc, "Architecture is layered, deployed as field node plus command host plus notify cloud, sequenced as capture-motion-detect-alert, and modularised into six primary types. The next chapter records how that architecture was implemented and on which hardware.")
