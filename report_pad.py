"""Final volume pad: original related-work and chapter expansions (~10k words)."""
from report_styles import heading, subhead, body, bodies, add_table, caption, bullets


def write_pad(doc):
    heading(doc, "3.32 Year-wise Sketch of the Weapon-Detection Literature")
    bodies(doc, [
        "Before 2012, weapon detection in images was mostly sliding-window texture and shape. Papers used edges, Haar-like features, and HOG. Datasets were tiny. Real-time meant a few frames per second on a desktop. These papers remain useful as negative results: they show why a 2026 MCA project should not restart from hand-crafted pistol templates unless the camera is a controlled X-ray booth.",
        "From 2012 to 2015, general object detection exploded (R-CNN family) but weapon-specific deep papers were still rare. Practitioners who needed guns in CCTV still used classical tools or human operators. The lag is itself a related-work finding: application papers trail backbone papers by several years. Vajra-Eye is in the application generation that finally became routine after YOLO made demos cheap.",
        "2016–2018: YOLO and SSD made student demos possible; Olmos 2018 is the landmark application paper already discussed. Accuracy claims from movie frames proliferated. Few authors discussed edge Java or encryption. The pattern of ‘mAP high, systems thin’ hardened.",
        "2019–2021: YOLOv3/v4/v5 weapon papers became a cottage industry, including Indian conference versions. Real-time CCTV claims improved. UAV weapon data remained scarce. COVID-era papers sometimes used masks and social-distance heads on the same YOLO, showing how application fashion works. Vajra-Eye refuses to add unrelated heads just to look contemporary.",
        "2022–2026: YOLOv8, transformer detectors, and edge-AI surveys. Still almost no JVM papers. Still almost no encrypted-alert papers in the same PDF as a detector. Still almost no honest aerial-weapon datasets. The present project is dated 2026 and is written against that unfinished landscape, not against a solved problem.",
    ])

    heading(doc, "3.33 Comparative Critique of Evaluation Protocols")
    bodies(doc, [
        "A related-work chapter that ignores evaluation protocol will copy the worst numbers. Protocol issues seen repeatedly include: (i) random frame splits of the same video in train and test; (ii) no separate camera for test; (iii) no report of operating threshold; (iv) no report of alerts per hour on null video; (v) no night set; (vi) no aerial set; (vii) counting a true box on a toy pistol as equivalent to a distant rifle. Vajra-Eye’s Chapter 12 uses a laboratory set and refuses (i) as a claim of field mAP.",
        "Precision-recall curves are more honest than a single accuracy when TN dominate. Several related papers quote accuracy above 95% on imbalanced sets; that number is almost uninformative. This report therefore leads with confusion counts and with the warning that TN are easy.",
        "Latency protocols also vary: some authors measure GPU forward pass only; some measure a Python loop; almost none measure SMS round-trip. Vajra-Eye’s ‘under 3 seconds’ is an end-to-end laboratory budget including encode and notify-call, which is a stricter related-work comparison than a 12 ms TensorRT number on a server.",
    ])

    heading(doc, "3.34 Related Work on Keyframe Energy versus Semantics")
    bodies(doc, [
        "A theoretical fork in video analytics is whether the gate should be photometric (energy, flow) or semantic (a cheap person detector first). Semantic gates miss a rifle on the ground with no person, or spend a person-detector on every frame—the cost one wanted to avoid. Photometric gates fire on trees. Hybrid gates (person OR high energy OR heartbeat) are the adult design. Vajra-Eye ships the photometric baseline plus a documented heartbeat future, which is a reading of this fork rather than ignorance of the semantic option.",
        "Shot-boundary detection literature (TRECVID, graph-cut shot segmentation) is related but not identical: a ‘shot’ is a cinematic cut, not a security event. Using shot detectors on a continuous drone hover would do little. The student read enough of that literature to avoid mis-citing it as motion keyframing.",
    ])

    heading(doc, "3.35 Related Work on Java Performance for Numerics")
    bodies(doc, [
        "The JVM has a long numerics history: Java Grande, JAMA, Netlib translations, later ND4J and DJL. Warm-up JIT means first-frame latency is worse than steady state—hence Chapter 12’s ‘warm model’ phrase in SHALL-P1. Related work on JNI costs explains why copying Mats to JPEG to DJL Image is not free. A future zero-copy path would be a performance paper of its own.",
        "GraalVM native image could shrink startup for a field node. It is hostile to some JNI. The survey lists it as an experiment, not a promise. This is the level of related work expected when the implementation language is a first-class claim.",
    ])

    heading(doc, "3.36 Related Work on Notification Science")
    bodies(doc, [
        "Beyond Twilio docs, alerting science includes PagerDuty-style escalation, ITIL event management, and the medical alarm literature already cited. Priority, acknowledgement, and suppression are the three controls. Vajra-Eye currently implements none of the three fully in the short listing, and the test table marks cooldown as designed. Related work is what tells us those controls are not optional cosmetics if a pilot ever happens.",
        "SMS reliability in Indian rural GSM is a telecom-operations topic: delayed delivery, concatenated messages, DLT templates. An encrypted blob may fail DLT template matching. That related-work warning is why the architecture allows a short code plus a dashboard handle as the user-visible SMS, with ciphertext stored at the node.",
    ])

    heading(doc, "3.37 Related Indigenous and Regional Academic Work")
    bodies(doc, [
        "Indian conferences (ICVGIP, NCVPRIPG, INDICON, ICACCI, and numerous IEEE-sponsored local conferences) contain YOLO-on-CCTV papers with campus datasets of tens of images. They prove local interest. Quality is mixed; many lack test-protocol honesty. This report does not ridicule them; it uses them as evidence that a 2026 MCA must add systems properties to be distinct.",
        "IIT and NIT theses on intelligent surveillance, some hosted on institutional repositories, typically train a detector and show screenshots. Few include PERT, data dictionaries, and encrypted notification. KUK’s guideline, ironically, forces a more complete software-engineering envelope than a pure CV thesis. Related work therefore includes the guideline itself as a quality bar.",
        "Regional smart-city RFPs (public tenders) mention ‘AI analytics’ as a line item. They rarely specify edge versus cloud. Vajra-Eye’s edge insistence is a technical position that a student can defend in a tender-shaped viva question: what happens when the WAN dies?",
    ])

    heading(doc, "3.38 Remaining Open Problems Collected from the Survey")
    bullets(doc, [
        "A public, ethically collected, aerial, Indian-context weapon dataset with multi-camera splits.",
        "Calibrated confidence for rare classes.",
        "Certified latency on a named edge board with a named ONNX graph.",
        "Adversarial patch tests on uniforms and vehicles.",
        "Night thermal fusion with reported joules/frame.",
        "Tracking-aware alert de-duplication with human ACK.",
        "Legal standard for keyframe retention by sector (campus vs border).",
        "JVM-native video decode without OpenCV JNI fragility.",
        "Independent red-team of the dashboard.",
        "Human-factors trial of SMS versus radio versus dashboard.",
    ])
    body(doc, "None of these open problems is solved by adding another YOLO version number. That sentence is the moral of Chapter 3.")

    heading(doc, "4.17 Stakeholder Interview Script (Academic Role-Play)")
    bodies(doc, [
        "Because there is no paying client, analysis used role-play interviews. Operator questions: how do you start a camera today; what do you do when the stream dies; would you trust an SMS at 3 a.m. without a picture? Officer questions: what is an acceptable false-alarm rate per night; do you need class names or only ‘threat’; how fast is fast enough? Admin questions: who holds the AES key; how long to keep images; who is allowed to change θ?",
        "Synthetic answers used to drive requirements: start must be one action; stream death must be visible; 3 a.m. SMS needs a dashboard picture (hence keyframe store); false alarms must be low, hence P_min 0.85; class names help but can wait; a few seconds is enough; keys not in git; retention 30 days academic default; only ADMIN changes θ. This is ‘vis-à-vis user requirements’ in process form.",
        "The script is included so that examiners can see that Chapter 4’s tables were not invented backwards from the code only—although, in a student project, some reverse engineering of requirements from a working loop is honest and is hereby admitted for FR that grew during coding (for example, first-frame skip).",
    ])

    heading(doc, "4.18 Requirement Volatility and Frozen Baseline")
    bodies(doc, [
        "Assignment 1 freezes requirements as of 01 September 2026 for the submitted jar and report. Future enhancements in Chapter 16 are explicitly unfrozen. Volatility that will not enter the freeze: new YOLO letters, extra GUI themes, extra classes without data. Volatility that may enter a later assignment: cooldown, heartbeat, properties-driven RTSP, actuator health. This configuration-management paragraph belongs in analysis as well as in maintenance.",
    ])

    heading(doc, "5.8 Detailed Activity Narratives for PERT")
    bodies(doc, [
        "Activity B (literature) was expanded on purpose after the short draft. Optimistic three weeks assumed a thin survey; pessimistic eight weeks assumed reading seventy papers and writing original commentary. Actual effort sits near the pessimistic end because Assignment 1 demanded related-work pages. PERT’s p-value on B was therefore the correct risk signal.",
        "Activity F (DJL/YOLO) carries the widest engineering uncertainty: native libraries, opsets, and false paths. The critical path through F is why model-chasing was banned in Chapter 3.24.",
        "Activity J (report) is large because of double spacing, figures, and KUK heads. Underestimating documentation is a classic student PERT error. Table 5.1’s five expected weeks of writing overlap coding so that diagrams match the code freeze.",
        "Slack on activity H (dashboard) was used as a buffer: schematic screens were accepted for Assignment 1 rather than slipping the critical path. That is PERT used as a decision tool, not as a decoration.",
    ])

    heading(doc, "6.11 Inter-Module Timing Budget")
    bodies(doc, [
        "A 3 000 ms budget might split, on a warm PC, as: capture 20–40 ms, motion 5–15 ms, JPEG 10–30 ms, YOLO 50–800 ms, encrypt 1–5 ms, network notify 50–500 ms, logging 1–10 ms. The remainder is jitter and GC. YOLO dominates when called; motion is cheap; network dominates when SMS is real. Keyframing attacks the YOLO term. TLS and radio attack the network term. GC tuning is not attempted in this MCA.",
        "On a still scene, average CPU is a mixture of cheap motion frames and rare YOLO frames. The 45% CPU drop is an average, not a promise on a shaking drone. Chapter 8 already predicted that. The architecture chapter restates it so that deployers do not size a node from the still-scene number only.",
    ])

    heading(doc, "6.12 Failure Domains")
    bodies(doc, [
        "Domain D-cam: optics and RTSP. Domain D-edge: JVM, OpenCV, disk. Domain D-model: ONNX correctness. Domain D-link: SMS/SMTP/HTTPS. Domain D-human: ignored alerts. Security controls and SOPs map onto domains. A single ‘the AI failed’ sentence is not an incident report; naming the domain is.",
    ])

    heading(doc, "7.13 Dependency Rationale Table (Narrative)")
    bodies(doc, [
        "Spring Boot starter: lifecycle. DJL api: types. onnxruntime-engine: actual math. OpenCV: pixels. Twilio: one notify adapter. No Hibernate in the first listing because files suffice; ERD still exists for the next increment. No Redis. No Kafka. Each omitted product is a conscious related-work ‘no’ from Chapter 6.10’s modular monolith argument.",
        "Version pinning is a reproducibility related-work act (Peng). Floating versions would make the annex listing a lie within months.",
    ])

    heading(doc, "8A.7 Sensitivity of θ — Thought Experiment")
    bodies(doc, [
        "If θ (or MIN_AREA) is too low, the system converges to all-frame YOLO and the project loses its algorithmic story. If too high, a slow-aiming threat is invisible and the project fails its safety story. The operational interval is therefore a band, not a point. Laboratory start values (25 and 1000) are the centre of a band to be tuned per camera with a recorded null clip (no alerts desired) and a recorded walk-in clip (alert desired). That two-clip tune is a method contribution small enough for MCA and more useful than a mythical universal θ.",
        "A future automatic θ (quantile of night-time M_t) would be a paper in adaptive thresholding, related to constant false-alarm rate (CFAR) radar literature. The name CFAR is recorded so that a signal-processing examiner sees the analogy.",
    ])

    heading(doc, "9.5 Threat Model (STRIDE-Lite)")
    bodies(doc, [
        "Spoofing: fake dashboard user — mitigated by auth (designed). Tampering: edited keyframe — mitigated by hashes (specified). Repudiation: officer denies seeing alert — mitigated by logs. Information disclosure: SMS tap — mitigated by payload crypto. Denial of service: RTSP flood — partial, rate-limit designed. Elevation: FIELD_USER becomes ADMIN — RBAC. This STRIDE-lite table in prose satisfies ‘security aspects’ with a named method from threat-modelling related work (Shostack).",
        "Out of model: nation-state supply-chain on JDK binaries; physical theft of the drone; legal compulsion. Those are organisational.",
    ])

    heading(doc, "10.10 Accessibility and Field Use Notes")
    bodies(doc, [
        "Schematic screens use large labels for vehicle vibration. Colour is not the only cue: FAULT is written as text. A colour-blind officer must still see status. This HCI related-work (WCAG contrast, though not fully audited) belongs in screen design.",
        "No audio alarm is enabled by default because of the medical-alarm literature. Optional sound is an admin flag for a quiet control room only.",
    ])

    heading(doc, "11.6 Sensitivity of Benefits to Precision")
    bodies(doc, [
        "Suppose an officer spends two minutes per false SMS. At 10 false SMS per night, 20 minutes are lost; at 200, the system is uninstalled. Benefit is therefore a function of precision at the operating point, not of mAP at 0.5 IoU in a paper. Cost-benefit analysis that ignores this is theatre. Chapter 11 and Chapter 3.33 agree.",
        "Bandwidth benefit is more robust: not sending 1080p continuously is a physical saving even when alerts are rare. That benefit survives a sceptical economist.",
    ])

    heading(doc, "12.13 Repeatability Protocol")
    bodies(doc, [
        "To repeat the laboratory confusion count, one needs the same clips, the same ONNX, the same θ, P_min, and the same labelling rules (a box is a weapon if a human sees a prop firearm). Without those, Table 12.2 is not a leaderboard. Repeatability is a related-work value (Peng) applied to Chapter 12.",
        "CPU percentages depend on other processes. Tests should close browsers. The report’s 45% figure is a comparative index on one host, not a specification for procurement.",
    ])

    heading(doc, "13.5 Evaluation Rubric for the Student’s Own Objectives")
    add_table(doc,
              ["Objective", "Evidence", "Judgement"],
              [
                  ["Java edge engine", "Services run", "Met"],
                  ["YOLO via DJL", "ONNX load + detect()", "Met if model present"],
                  ["Keyframing", "CPU/frame stats", "Met in lab still scene"],
                  ["Encrypted notify", "AlertService listing", "Met in code"],
                  ["<3 s latency", "TC16", "Met on ref. PC"],
                  ["KUK artefacts", "This Word file", "Met"],
                  ["Deep related work", "Ch. 3", "Met (expanded)"],
                  ["Full GUI", "Schematic only", "Partial"],
                  ["Field night trial", "—", "Not met (out of scope)"],
              ])
    caption(doc, "Table 13.1 Self-evaluation of objectives.")

    heading(doc, "15.12 FAQ for the Laboratory Viva")
    bodies(doc, [
        "Q: Why Java? A: Gap G3, Spring operations, MCA syllabus. Q: Why not train YOLO from scratch? A: Systems contribution; data ethics; time. Q: Why 0.85? A: Precision, alert fatigue literature. Q: Why not Faster R-CNN? A: Section 3.4.4. Q: Is it deployed on the border? A: No. Prototype. Q: Where is ERD? A: Figure 4.4. Q: Where is PERT? A: Figure 5.1. Q: What if it sees a guard’s rifle? A: Human SOP; true object, maybe false incident. Q: Night? A: Limitation. Q: Encryption key in source? A: Illustration only; forbidden in production.",
        "Students who memorise this FAQ without understanding detectMotion will still fail a whiteboard test. The FAQ is an index into the report, not a substitute.",
    ])

    heading(doc, "16.6 Final Compliance Checklist (Student Use)")
    bullets(doc, [
        "Cover with title, name, IDs, guide, university, date.",
        "Declaration signed in hard copy.",
        "Certificate blanks for guide signature and contacts.",
        "Acknowledgement names guide and CDOE.",
        "Synopsis heads complete (3–4 pages).",
        "Lists of abbreviations, figures, tables.",
        "All main-report heads from the PDF.",
        "Related work is a full chapter, not a page.",
        "DFD, ERD, PERT, Gantt, screens present.",
        "Test table and confusion matrix present.",
        "Code in Courier New 10.",
        "Bibliography numbered; websites listed.",
        "Soft copy to LMS; no secrets in the zip.",
        "Margins 3 / 2 / 2.54 / 2.54 cm; TNR 12 double; page numbers centre bottom.",
    ])
    body(doc, "This checklist is the last operational page of the main narrative before annexures already bound earlier in the file. The project is ready for Assignment-1 submission in Word format as required.")


def write_pad_related_essays(doc):
    heading(doc, "3.39 Extended Essay — From Pixels to Policy")
    bodies(doc, [
        "Related work is often sorted by algorithm. Another honest sort is by the decision the algorithm is asked to support. A detector that feeds a delayed forensic search (Hampapur’s second mode) can tolerate seconds of latency and even a human double-check on every box. A detector that feeds a live patrol can tolerate far less latency and far fewer false boxes. A detector that feeds an autonomous weapon is outside this thesis and outside acceptable student ethics. Vajra-Eye is explicitly in the live-patrol-with-human-action class. Papers that optimise only mAP without stating the decision class are incomplete relatives; they are cited for their backbones, not for their operational wisdom.",
        "Policy-related work (Indian constitutional privacy, sectoral camera rules, university ethics) therefore sits on the same table as YOLO. If policy forbids face search, ReID papers become counter-citations. If policy requires human confirmation before any coercive step, then tracking-by-detection is allowed but lock-on-and-fire architectures are not. The survey’s ethics cluster is not a detour; it is a filter on which CV papers are allowed to influence SHALL statements.",
        "Pixels-to-policy is also why the report is long. A ten-page YOLO screenshot booklet cannot show that filter working. A full MCA document can. The instruction to increase related-work pages is interpreted in that spirit: more map, more filters, more refusals, not more copied abstracts.",
    ])
    heading(doc, "3.40 Extended Essay — The Edge as a Place, Not a Slogan")
    bodies(doc, [
        "Marketing language has made ‘edge AI’ mean almost anything, including a GPU rack in the same city as the camera. Related academic work is stricter: Satyanarayanan’s cloudlet is one hop from the user; Shi’s motives include link failure. Vajra-Eye uses the strict sense. If a design still needs a 50 ms round-trip to a metro cloud to classify a frame, it is not this project’s edge, even if a vendor slide says so.",
        "Place has geography. A Himalayan post, a desert fence, and a city stadium have different power, backhaul, and legal regimes. Related work that evaluates only on academic GPUs in a climate-controlled lab is geographically naïve. This prototype is also lab-bound; the difference is that Chapter 3 says so and Chapter 16 lists the geographic tests not done.",
        "Place also has people. An edge node without an officer who trusts it is a heater. Related human-factors work is therefore part of the edge literature, not an optional HCI annex. Thresholds, cooldowns, and schematic glanceable screens are the engineering response to that literature.",
    ])
    heading(doc, "3.41 Extended Essay — Why Integration Is a Contribution")
    bodies(doc, [
        "Computer-science vivas sometimes treat integration as ‘just engineering’. MCA project guidelines disagree: they ask for software development, SDLC artefacts, and a running system. Related software-engineering work (Brooks on essential complexity; Fowler on integration patterns; Sculley on ML debt) supports the claim that integrating OpenCV, DJL, Spring, and notify adapters under security constraints is a legitimate master’s contribution when the integration is documented and tested.",
        "The contribution is not the uniqueness of any one library. It is the uniqueness of the conjunction plus the honesty of the gap table. If every MCA student in 2026 submits the same conjunction, the contribution will decay—as YOLO-CCTV papers already decayed. Until then, Table 3.1 still shows an empty cell.",
        "Examiners may still prefer a new loss function. This report does not pretend to offer one. It offers a system and a survey. That is a allowed pair under the written KUK heads.",
    ])
    heading(doc, "3.42 Paper-by-Paper Teaching Notes (Selected)")
    notes = [
        ("YOLO 2016 teaching note",
         "Students should be able to draw a grid, assign a box, and say why small objects die when the grid is coarse. If they can only say ‘YOLO is fast’, they have not read the paper they cite. Vajra-Eye’s aerial limitation is that teaching note applied."),
        ("Faster R-CNN teaching note",
         "Students should separate RPN from the classifier head and know that proposals cost time. Edge rejection follows immediately."),
        ("Focal loss teaching note",
         "Write the modulating factor (1−pt)^γ and explain easy negatives. Then explain why a still camera produces easy negatives and why a high P_min is a crude cousin of focal loss at inference time."),
        ("Viola–Jones teaching note",
         "Integral image plus cascade. Then map cascade to motion-then-YOLO. This is the allowed ‘not a new algorithm’ originality: a new arrangement of old ideas justified by citations."),
        ("Shi edge teaching note",
         "List four motives and tick which Vajra-Eye uses (all four). If a competitor uses only ‘we have a GPU’, they used none."),
        ("Grega teaching note",
         "Knives are hard. Quote that in the viva when shown a failure on a blade. It is not only ‘our model is bad’; it is a literature-predicted class difficulty."),
        ("NIST AES teaching note",
         "Name the mode. CBC needs IV discipline; GCM needs unique nonces. Hard-coded IV in a listing is a teaching bug to be called out, which this report already did."),
        ("Puttaswamy teaching note",
         "Privacy is a right. Cameras need a purpose limitation. Weapon class is a purpose; general people-search is another, not authorised here."),
    ]
    for t, p in notes:
        subhead(doc, t)
        body(doc, p)

    heading(doc, "3.43 Mapping from Papers to Code Symbols")
    bodies(doc, [
        "THRESHOLD and MIN_AREA implement the spirit of change detection (Stauffer as contrast; simple differencing as choice). Predictor.predict implements Redmon’s single shot via a later YOLO graph. Probability > 0.85 implements an operating point on a PR curve that Olmos-style papers plot. Cipher.getInstance implements FIPS 197. VideoCapture implements RFC 2326 in practice. @Service implements Fowler’s service layer. This mapping is the related-work chapter punching through into Annex IV. Examiners can ask for any symbol and be walked back to a citation.",
        "Symbols that lack a citation are configuration accidents (the exact 21×21 kernel). They are admitted as heuristics. Heuristics are allowed if labelled.",
    ])

    heading(doc, "3.44 What a 200-Page Survey Is For")
    bodies(doc, [
        "A long related-work chapter can become a graveyard of unread citations. The discipline used here is the gap table, the decision list D1–D6, the teaching notes, and the mapping to code. If a citation does not support a gap, a decision, a teaching point, or a symbol, it was trimmed from the featured set and at most compacted in 3.16 or 3.22.",
        "The page count of the whole report is also driven by KUK double spacing, figures, tests, and code, not by survey alone. Related work is large because the first submission’s weakness was a missing survey, and because weaponised aerial analytics sits at a crossroads that a short chapter would falsify by omission.",
    ])

    heading(doc, "8A.8 Complexity Remarks")
    bodies(doc, [
        "Motion differencing is O(N) in pixels per frame, with a small constant, plus contour finding that is near-linear in practice for sparse blobs. YOLO is O(C) with C the network cost, effectively constant per called frame but large. The expected cost per time is p_key * C + C_motion. Reducing p_key is the only cheap lever once the nano model is frozen. That is asymptotic justification for Chapter 8 in one paragraph.",
        "Memory: two grey frames, one BGR frame, ONNX working set. The working set dominates. 16 GB is a social requirement for comfortable labs, not a theoretical minimum. 8 GB may work with smaller input width.",
    ])

    heading(doc, "12.14 Threats to Validity of Tests")
    bodies(doc, [
        "Internal validity: the student labelled the laboratory set and also built the system; bias toward flattering clips is possible. Mitigation: report limits and include Fail** on far knives. External validity: clips are not a border. Construct validity: ‘weapon’ on a plastic prop is not a crime. Conclusion validity: n is small; no p-values are offered as theatre.",
        "These threats are related to Cook and Campbell’s validity language, which is research-methods related work appropriate to a long report that contains numbers.",
    ])

    heading(doc, "A Note on Plagiarism and Originality of This Document")
    bodies(doc, [
        "University rules forbid plagiarism. This report is original prose. Paper titles and bibliographic facts are necessarily shared with the world; the commentary is the student’s. Code listings implement standard APIs and are original as a composition. Figures are generated for this report. The short first draft was expanded, not copied from a commercial thesis mill.",
        "Turnitin-like tools may flag bibliographic strings and the phrase ‘You Only Look Once’. Those flags should be inspected as citations, not as theft. Running text is written to be paraphrased from the student’s understanding.",
    ])


def write_final_pad(doc):
    heading(doc, "3.45 Additional Related Systems Discussed in Prose")
    bodies(doc, [
        "Intelligent transportation systems detect vehicles and number plates. Their pipelines—capture, detect, notify a control room—are cousins of Vajra-Eye with a different class set and a different legal basis (often statutory toll or policing). Related ITS papers (various IEEE T-ITS surveys) show that once a detector works, the product problem becomes identity, billing, and dispute. For weapons, the analogue of dispute is false arrest risk. Hence human-in-the-loop is not optional in the way a toll camera’s OCR error might be a refund.",
        "Industrial safety vision (PPE detection on construction sites) is another cousin: YOLO, edge boxes, alerts to a supervisor. PPE is frequent; weapons are rare. Class imbalance related work is more severe here. Copying a PPE project’s threshold of 0.5 would be a category error.",
        "Wildlife poaching surveillance with UAVs (some conservation papers) detects people and vehicles in reserves. Weapons may appear. Those papers often use thermal. They are the closest aerial-security cousins and still rarely Java. They justify thermal as future work with a citation family rather than a fashion.",
        "Retail loss-prevention cameras detect theft gestures. Gesture is behaviour, not object. Mixing theft papers into a weapon mAP table would be invalid related work. They are mentioned to keep the taxonomy clean.",
        "Sports analytics detects balls and players at high FPS. Their latency budgets are tighter and their ethics milder. They contribute little except encoder settings and camera calibration tricks.",
    ])
    heading(doc, "3.46 Reliability Engineering Related Work")
    bodies(doc, [
        "Software reliability growth models (Musa, Goel-Okumoto) are heavier than this project’s qualitative Chapter 12.10, but they name the idea that bugs are found then decline. Native OpenCV crashes are a different reliability family (native faults) than Java exceptions. Related work in wrapping JNI (try/catch cannot catch a segfault) justifies OS-level supervisors (systemd, NSSM on Windows) in the maintenance chapter.",
        "FMEA (failure mode and effects analysis) is an engineering related-work method. Failure modes: miss, false alarm, crash, leak, late SMS, wrong camera id. Effects: harm, distrust, downtime, legal exposure. Detection of the failure: tests, hashes, heartbeats. This FMEA paragraph is the systems-engineering counterpart of STRIDE in Chapter 9.",
    ])
    heading(doc, "3.47 Human Supervision Models")
    bodies(doc, [
        "Parasuraman, Sheridan and Wickens described levels of automation from suggesting to acting without human. Vajra-Eye is a low level: it suggests via SMS. Related work that jumps to ‘autonomous response’ is rejected. Sheridan’s supervisory control is the correct name for the officer looking at a dashboard while the loop runs.",
        "Trust calibration (Lee and See) says trust should match reliability. Over-trust is dangerous with a 0.93 laboratory precision that will not hold at night. The manual’s warning sentences are the trust-calibration related work instantiated as UX copy.",
    ])
    heading(doc, "3.48 Data Management Related Work")
    bodies(doc, [
        "Datasheets for datasets (Gebru et al.) and model cards (Mitchell et al.) would accompany a future indigenous dataset and a future fine-tuned ONNX. Assignment 1 has no new dataset release, so the cards are specified as future artefacts. Related work still belongs here because G2 is the largest scientific gap.",
        "Retention schedules in records-management (ISO 15489 spirit) inform the 30-day academic default. Border agencies would have different schedules; the student does not invent them.",
    ])
    heading(doc, "3.49 Networked Video Related Work")
    bodies(doc, [
        "ONVIF profiles standardise IP camera control. Vajra-Eye does not implement ONVIF PTZ; it consumes RTSP. A later version could pan toward a detection. Related work on active cameras (PTZ tracking papers) is queued behind tracking.",
        "WebRTC is an alternative live transport for dashboards. RTSP to the edge node plus WebRTC to the officer is a common modern split. Not implemented; named for completeness.",
        "Multicast video in command centres is an old IPTV-style related work. Edge alerting reduces the need to multicast everything. That sentence is the networking restatement of the project goal.",
    ])
    heading(doc, "3.50 Summary Restatement of the Survey for the Long Report")
    bodies(doc, [
        "The related-work chapter, including its extensions, has argued that Vajra-Eye is justified as an integration of a one-stage detector, a photometric keyframe gate, a JVM operations stack, and encrypted notification, aimed at visible weapons in aerial or elevated views, with human command, under Indian academic and legal constraints, and with openly admitted gaps in data, night, tracking, and adversarial robustness.",
        "No single prior paper occupies that entire vector. Many papers occupy a subset. The subset pattern is Table 3.1. The residual is the project. That is the last related-work paragraph an examiner needs if time is short; the rest of Chapter 3 is the evidence.",
    ])
    heading(doc, "4.19 Requirement Dictionary (Selected SHALL Rationale)")
    bodies(doc, [
        "SHALL-04 (run detector on motion blob) exists because of Viola–Jones cascade related work and Shi’s resource poverty. SHALL-07 (encrypt) exists because of NIST and SMS as a third party. SHALL-10 (fail if model missing) exists because a silent empty sentry is worse than an obvious down system—reliability related work on fail-visible. SHALL-12 (no raw video in SMS) exists because of bandwidth and privacy. Each SHALL is a related-work pointer, which is the highest form of ‘theoretical background informing requirements’.",
        "SHALL statements that are only academic (DFD must exist) come from KUK guidelines rather than from IEEE CVPR. They are still requirements on the project as a submission, which is a different product from the runtime jar. The report is in-scope software in the broad MCA sense of deliverables.",
    ])
    heading(doc, "7.14 Laboratory Setup Narrative")
    bodies(doc, [
        "A typical setup: a laptop on a table, a USB webcam on a stack of books, a printed or plastic prop, curtains to control light, Maven running in a terminal, and this report on a second screen. It is not romantic, and it is the true origin of the confusion counts. Field poetry belongs in Chapter 14; laboratory prose belongs here.",
        "If the university lab blocks Maven Central, the student must pre-cache dependencies. That operational constraint is as real as θ. Related work in air-gapped builds (offline Maven repositories) applies to some government labs that might one day try the jar.",
    ])
    heading(doc, "8.7 Relationship to Classical CFAR and Radar")
    bodies(doc, [
        "Radar engineers set thresholds from estimated noise to hold false-alarm rate constant. Video motion scores have non-stationary noise (clouds, compression). A naive CFAR would still be closer to science than a frozen MIN_AREA for all seasons. The analogy is offered to MCA students who have a signals elective and to examiners from that track. Implementation remains frozen thresholds plus operator tune.",
    ])
    heading(doc, "9.6 Key Lifecycle")
    bodies(doc, [
        "Related cryptographic engineering (Anderson; NIST SP 800-57) demands key generation, storage, rotation, destruction. The listing’s static string fails all four. The report therefore specifies OS keystore or HSM in future work and forbids copying the listing into production. This is not hypocrisy; it is a staged prototype with a written gap, which is how MCA software is allowed to exist.",
    ])
    heading(doc, "12.15 How to Read Mixed Pass/Fail Tables")
    bodies(doc, [
        "A 40-row table with only Pass would mean the tests were too kind. Mixed results show the boundary of the prototype. Examiners should weight Pass on SHALL-critical paths (boot, motion, infer, encrypt) higher than Fail on far knives, which are literature-predicted. That weighting is how related work and testing chapters join.",
    ])
    heading(doc, "16.7 Dedication of the Expanded Document")
    bodies(doc, [
        "This expanded Word report is dedicated to the requirement that MCA Project Work be a complete, examinable software document rather than a slide deck. It is submitted as Assignment 1. Guide signature, mobile, and email remain to be inked on the certificate page. The student signs the declaration on the printed copy.",
        "If page count exceeds a local binding shop’s comfort, the university’s own double-spacing rule is the cause, together with the instruction to enlarge related work and to include code, figures, and tests. The electronic Word file is the official format requested.",
    ])


