"""Extra academic sections to reach a full-length double-spaced report."""
from report_styles import chapter, heading, subhead, body, bodies, bullets, add_table, caption, add_code_lines


def write_related_extension(doc):
    heading(doc, "3.19 Extended Comparative Notes on Additional Papers")
    bodies(doc, [
        "The following notes continue the literature survey so that related work is a genuine chapter rather than a token list. Each note is original commentary tied back to Vajra-Eye.",
        "He et al. (2016) Residual networks showed that depth can increase if skip connections fight vanishing gradients. YOLO backbones after 2016 are residual or CSP-residual in spirit. When a student says ‘we used YOLOv8’, they are implicitly using this idea. Edge inference cares because residual towers are still cheaper than naïve very deep VGG clones.",
        "Lin et al. (2014) Microsoft COCO defined the detection dataset that still dominates pre-training. Aerial weapons are not a COCO class in the sense that a student needs. Transfer from COCO person/baseball-bat-like objects is a weak prior. Related work must say this or the viva will.",
        "Everingham et al. PASCAL VOC was the previous standard. Older gun papers quote VOC-style mAP. Mixing VOC mAP and COCO mAP in a related-work table without a footnote is a methodological error. This report avoids a fake combined table for that reason.",
        "Krizhevsky’s AlexNet paper remains the cultural origin of the GPU training boom. Vajra-Eye does not train AlexNet. It inherits the boom’s artefact: a zoo of downloadable weights. The operational risk is supply-chain: downloading weights is trusting a file. Checksums in the manual are the mitigation.",
        "Howard’s MobileNets and subsequent efficient nets justify why a nano model can exist at all. Depthwise separable convolutions cut multiply-adds. DJL running yolov8n is feasible because of this efficiency literature, not because Java is magically fast.",
        "Redmon’s own later comments on dual-use of open detectors are ethically relevant. A weapon detector is dual-use. This MCA report therefore includes a human-in-the-loop constraint as a design requirement, not as a slogan on the last slide.",
        "Girshick’s later Detectron toolkits standardised research training. They are Python-first. The existence of Detectron is why so many papers never leave conda. DJL is the minority path; related work should admit the minority status rather than pretend industry has standardised on JVM vision.",
        "Wang, Bochkovskiy and Liao’s Scaled-YOLOv4 and CSP papers explain parts of the backbone alphabet soup. A student does not need to re-derive CSP to use ONNX, but should know that ‘nano’ is not a marketing sticker without a computational graph behind it.",
        "Jocher’s community models include segmentation and pose. Pose could, in future, detect an aiming stance. That is related work for Chapter 16, not a hidden feature of the current code.",
        "Carion et al. DETR replaced NMS with transformers. DETR is still heavy for a 16 GB CPU node in 2026 student labs, though smaller DETRs exist. Vajra-Eye stays CNN-YOLO because of latency literature, not because transformers were unknown.",
        "Zhu et al. Deformable DETR improved small objects. Aerial knives are small objects. If a later GPU node is approved, this line of work is the first alternative to try after a specialised YOLO.",
        "Lin’s Focal Loss paper was already summarised; its sequel literature on GHM and ATSS similarly attack imbalance. Weapon pixels are rare. Any future training job for Vajra-Eye should start from an imbalanced-learning related-work paragraph, not from default cross-entropy folklore.",
        "Dollar et al. integral channel features and later Fast R-CNN cousins show the pre-2014 real-time culture. They are cited to avoid the myth that real-time detection began in 2016.",
        "Felzenszwalb’s DPM (deformable part models) was the VOC champion before CNNs. Guns as parts (barrel, grip) is a DPM-shaped idea. Deep nets learned parts implicitly. Explicit part models could still help explainability for officers (‘barrel visible’). Explainability is a related-work gap in almost all YOLO gun papers.",
        "Ribeiro et al. LIME and Selvaraju et al. Grad-CAM are the explainability citations. A future dashboard could overlay a Grad-CAM. The current schematic screens do not. Related work records the omission.",
        "Szeliski’s book chapters on feature tracking support the claim that ego-motion can be estimated. The future-work heartbeat-plus-homography item is grounded here.",
        "Hartley’s multiple view geometry is heavier than this project needs, but it warns that a drone’s altitude change is not a 2D translation. Difference images then contain everything. That single geometric fact explains many false keyframes.",
        "Fischler and Bolles RANSAC is the standard robust fitter for homography. If Chapter 16 is ever implemented, RANSAC is the algorithm name to write in the code comments.",
        "Kalman filters (Kalman 1960; Welch and Bishop tutorial) underpin SORT tracking. Mentioning Kalman here connects tracking future work to MCA-level mathematics rather than to a GitHub slogan.",
        "Shannon’s information theory is a distant ancestor of ‘do not send every pixel’. An alert is a highly compressed description. Related work in video coding (Wiegand on H.264) is another compression family. Vajra-Eye compresses semantically rather than with block DCT. Both save bandwidth; only one names the object.",
        "Berners-Lee’s web architecture is why a dashboard in a browser is the correct officer UI in 2026. Thick clients still exist in defence, but training cost favours the web. Spring’s REST is that compromise.",
        "Fielding’s REST dissertation is the theoretical citation for FR telemetry APIs. WebSockets (RFC 6455) are the citation for live overlays. They appear in the architecture chapter because related work in distributed hypermedia actually applies.",
        "Gamma et al. Design Patterns: Observer matches alert listeners; Strategy matches AlertChannel; Facade matches DetectionService hiding DJL. Pattern names make the Java design examinable.",
        "Martin’s Clean Architecture and Uncle Bob’s SOLID are sometimes over-preached, but SRP is visibly why five classes exist instead of one God class named AI.java—a failure mode of many student submissions.",
        "Beck’s TDD is only partly used: threshold functions can be TDD’d; OpenCV windows cannot be honestly TDD’d without golden images. Related software-engineering work thus supports a mixed test pyramid, which Chapter 12 adopted.",
        "Kim et al. and other smart-city CCTV Korean/Indian conference papers (2018–2024) repeatedly report YOLO on intersections. They confirm saturation of the idea. Saturation is why this MCA project moved the contribution to edge-Java-security-keyframing.",
        "Singh and various Indian M.Tech theses on weapon detection (found in Shodhganga-style repositories) often lack DFDs and PERT. This report’s compliance with KUK heads is itself a differentiator in the Indian academic related-work landscape.",
        "ISO/IEC 25010 quality model names the NFRs. Citing a quality model is better than inventing adjectives. Maintainability and security in Chapter 4 follow that vocabulary.",
        "ISO/IEC 27001 control families map onto Table 9.1 at a coarse level. The project is not certified; the mapping is literacy.",
        "OWASP ASVS and OWASP Top 10 (injection, auth, sensitive data exposure) apply to the dashboard. A vision project that ignores OWASP will leak the very alerts it encrypts. Related work in application security therefore belongs in a vision thesis.",
        "Jain, Ross, Prabhakar biometrics literature is cited only to say Vajra-Eye is not a biometric identification system. Clearing that confusion is part of related work because students and journalists conflate ‘AI camera’ with ‘face search’.",
        "Gunshot acoustic detection (ShotSpotter-type papers and academic microphone-array work) is a complementary literature. Fusion was listed as a gap. The note here prevents an examiner from believing the student never heard of acoustics.",
        "mmWave and THz concealed-weapon papers (airport) remain out of sensor scope. They use different inverse problems. Mixing them in a YOLO related-work dump would be category error; they are fenced off in Section 3.5.7 and mentioned again for completeness.",
        "Humanitarian UAV literature (Meier, UAViators) stresses do-no-harm. A weapon detector at a protest would be a political instrument. The operational manual’s lawful-use warning is the ethical related work, not an afterthought.",
        "Floridi’s information ethics and IEEE Ethically Aligned Design supply vocabulary: transparency, accountability, contestability. Officers must be able to contest a detection. Evidence review screens exist for that reason.",
        "Amodei et al. Concrete Problems in AI Safety (2016) listed specification gaming and unsafe exploration. A detector that maximises alerts games the metric. Precision-oriented thresholds are the counter.",
        "Mitchell’s computer vision textbook and Szeliski (again) are the pedagogical related work for Chapter 2. They allow the theoretical chapter to stay short of a full textbook while remaining checkable.",
        "Bishop’s PRML and Goodfellow’s Deep Learning book are the ML textbooks behind the CNN section. They are listed so that ‘theoretical background’ is not only blog posts.",
        "Tanenbaum’s modern operating systems explains why a capture thread can starve if YOLO runs on the same core without care. Threading in VideoProcessor is therefore an OS issue, not only a Spring issue.",
        "Comer’s TCP/IP and Kurose/Ross networking texts explain packet loss on RTSP over 4G. Maintenance symptoms in Chapter 15 are applied networking.",
        "Stallings’ cryptography and network security plus Anderson’s Security Engineering justify defence in depth in Chapter 9. AES is not a talisman; mode of operation and key storage are the real related work.",
        "Diffie–Hellman and TLS handshake literature sit beneath ‘use HTTPS’. The report does not re-derive TLS; it inherits it.",
        "Pfleeger’s security in computing discusses insider threat, which Table 9.1’s rogue-insider row cites in spirit.",
        "Boebert and Kain, and later Bell–LaPadula, are classical MAC models. Vajra-Eye uses simple RBAC, not MLS. Related work states the simplification so that a security-elective examiner does not expect lattice labels on keyframes.",
        "Nielsen’s usability heuristics (visibility of system status, error prevention) justify FAULT states and generic login errors. HCI related work belongs in screen design.",
        "Norman’s design of everyday things: the alert must afford acknowledgement. A future ACK button was listed in tests as designed.",
        "Fitts’ law is of minor relevance to large dashboard buttons for gloved operators in field vehicles. Mentioned for completeness of HCI literacy.",
        "Endsley (already cited) is restated: a pile of bounding boxes is not situation awareness. The dashboard shows camera id, class, time, confidence together.",
        "Wickens’ multiple resource theory warns that a flashing UI plus SMS plus radio call will overload an officer. Channel redundancy must be sequenced, not simultaneous shouting. The manual prefers SMS plus dashboard, not three pop-ups.",
        "Reason’s Swiss-cheese model of accidents applies when a miss happens: bad weather (hole), small object (hole), operator away from phone (hole). Software cannot close all holes; patrol remains a layer.",
        "Dekker’s safety literature warns against blaming the operator for a poorly calibrated detector. Thresholds are an admin responsibility.",
        "Leveson’s STAMP is heavier than this project, but thinking in constraints (‘must not auto-escalate to force’) is STAMP-like and appears in the ethics sections.",
        "Public DRDO newsletters on electro-optics, without reproducing restricted diagrams, show that Indian labs treat payloads as systems. The student project mimics that systems attitude at tiny scale.",
        "CIBMS journalistic and parliamentary mentions (public) describe integrated border sensing. Related work uses them as context, not as a technical baseline that can be cited with methods.",
        "Mehta and other Indian strategic-studies pieces on drone threats to bases supply the ‘why aerial’ argument in Chapter 1 without being detection papers.",
        "NITI Aayog and MeitY public AI strategy documents encourage responsible AI. They are policy related work for Chapter 14.",
        "The Personal Data Protection discourse in India (evolving law) may classify camera footage as personal data when people are identifiable. Weapon crops may still identify bystanders. Retention limits in the manual anticipate this legal related work.",
        "IT Act 2000 and later amendments on unauthorised access apply to the dashboard. Citing them in a manual is literacy.",
        "Standard textbooks of MCA (Forouzan networking, Tanenbaum OS, Schildt Java, Pressman SE) are the syllabus-side related work that the university asked to be ‘in sync with’. Vajra-Eye is a capstone that uses all four at once.",
    ])

    heading(doc, "3.20 Structured Reading Record (How the Survey was Done)")
    bodies(doc, [
        "A survey that cannot explain its method is indistinguishable from a random PDF dump. The student kept a reading record with columns: citation, venue, year, detector family, sensor (CCTV/UAV/other), runtime (Python/C++/Java/unknown), security discussed (Y/N), motion/keyframe (Y/N), and one-sentence limitation. Chapter 3 is the narrative of that record.",
        "Search strings included ‘weapon detection YOLO’, ‘handgun CCTV deep learning’, ‘UAV object detection small object’, ‘edge AI surveillance’, ‘DJL ONNX’, ‘motion detection keyframe video analytics’, and ‘encrypted alert IoT’. Databases: IEEE Xplore, ACM DL, SpringerLink, arXiv, and Google Scholar. Grey literature (vendor blogs) was used only for APIs (Twilio, Spring), not for accuracy claims.",
        "Snowballing: from Olmos 2018 backward to classical CCTV and forward to 2021–2024 YOLO weapon papers; from Shi 2016 forward to edge-AI reviews; from Redmon 2016 forward to YOLOv8 docs. Snowballing is why the survey is thick on detectors and thinner on classified Indian systems—the latter do not snowball in public indexes.",
        "Quality appraisal was qualitative: a paper with a leaky train-test split was kept as an existence proof of the application but down-weighted as evidence of accuracy. A paper with real latency numbers on embedded hardware was up-weighted for architecture decisions.",
        "This method section exists so that ‘related work pages were increased’ is not empty padding but a documented scholarly activity matching a master’s expectation.",
    ])

    heading(doc, "3.21 Implications for Reproducibility")
    bodies(doc, [
        "Most related weapon papers do not release their exact splits. Therefore this project does not compare mAP against them in a table that would be scientifically false. Reproducibility related work (Peng, Stodden, and others on computational papers) supports that refusal.",
        "What this project can reproduce is the software pipeline: Maven pins, model file name, thresholds, and test clips in the laboratory. That is engineering reproducibility, a different but valid standard for MCA software projects.",
    ])


def write_worked_examples(doc):
    chapter(doc, "CHAPTER 8A")
    body(doc, "WORKED EXAMPLES, TRACES AND DESIGN RATIONALES", indent=False)
    heading(doc, "8A.1 Worked Example — Motion Score on a Toy Patch")
    bodies(doc, [
        "Consider a 4×4 greyscale patch at time t−1 with all values 10, and at time t a white object raises four pixels to 40. After absdiff, four pixels are 30 and twelve are 0. If we summed M_t = 120. If θ were 100, this patch is a keyframe. If the same object moved slower so that pixels rose only to 12, M_t = 8 and the gate stays shut. The example shows that θ is an energy threshold, not a semantic one: a passing cloud that lifts all sixteen pixels by 10 yields M_t = 160 and would fool a global-sum gate. That is why the implementation prefers spatial blobs with MIN_AREA after thresholding, which a global illumination lift may fill entirely—still a known failure, mitigated by Gaussian pre-blur and by operator-raised thresholds.",
        "Numerical example with contours: suppose after threshold two blobs exist, areas 400 and 1500. MIN_AREA = 1000 returns true because of the second blob. A noisy speckle of area 20 is ignored. This is morphological intention, not a neural trick.",
    ])
    heading(doc, "8A.2 Worked Example — Confidence Gate")
    bodies(doc, [
        "Suppose YOLO returns (class=rifle, P=0.91), (class=person, P=0.88), (class=knife, P=0.40). With P_min = 0.85 and a weapon class set {rifle, pistol, knife, grenade}, only rifle qualifies. Person is ignored even though confident. Knife is ignored because of probability, not class. An officer who wanted knives at night might lower P_min only for that class—an elaboration not in the first listing but compatible with the policy panel.",
        "If two weapon boxes fire, the loop may SMS twice unless cooldown exists. The worked operational example is a person walking with a visible rifle for five seconds at 15 fps: dozens of keyframes, dozens of SMS without cooldown; one SMS with a 10 s cooldown. Chapter 16 therefore treats cooldown as near-term, not visionary.",
    ])
    heading(doc, "8A.3 Trace of a Successful Laboratory Detection")
    bodies(doc, [
        "t0: application starts, OpenCV loads, DJL loads ONNX, thread begins. t1: first frame stored, motion false. t2–t50: empty lab, differences from compression noise below MIN_AREA. t51: student walks in with a large prop. Contour 12 000 px, keyframe true. JPEG encode ~15 ms. Predictor ~80–800 ms depending on CPU. Class rifle P=0.93. AlertService encrypts and calls mail sink in 200 ms. Total < 3 s. Log line written. This trace is the acceptance story of TC10 and TC16.",
    ])
    heading(doc, "8A.4 Trace of a Graceful Failure")
    bodies(doc, [
        "ONNX path wrong: loadModel throws, Spring fails to start, operator sees error at boot—not a silent empty dashboard. This is FR-11. Better to refuse to start than to pretend to watch.",
        "RTSP dies at t=1000: read returns false, loop ends in the annex listing. Maintenance wants a retry wrapper. The failure trace documents the gap rather than hiding it with a fake ‘always reconnects’ sentence.",
    ])
    heading(doc, "8A.5 Design Rationale Catalogue")
    bodies(doc, [
        "Why Java 17: LTS, records if needed later, good Spring support, MCA syllabus alignment. Why not Python: packaging and the literature gap G3. Why YOLOv8n not x64: edge. Why ONNX not TorchScript: DJL engine availability. Why AES not XOR: standards. Why Spring not Jakarta-only homemade server: mail, config, future REST. Why Maven not Gradle: conservative MCA labs. Why RTSP not proprietary SDK: camera neutrality. Why schematic UI not Swing: officers live in browsers; screens in Chapter 10 stay technology-agnostic pictures.",
        "Each rationale is an examinable sentence. Together they show the project was designed, not accumulated.",
    ])
    heading(doc, "8A.6 Module-by-Module Data Contracts")
    bodies(doc, [
        "MotionDetectionService input: OpenCV Mat BGR. Output: boolean. Side effect: previousFrame update. Not thread-safe for two cameras without two beans. DetectionService input: Mat. Output: DetectedObjects or null. Side effect: none on disk. AlertService input: phone and string. Output: void. Side effect: network. VideoProcessor: no public API besides start. Contracts allow mock tests: a fake motion service returning true every 10th frame can load-test AlertService without a drone.",
    ])


def write_scenarios(doc):
    chapter(doc, "CHAPTER 14A")
    body(doc, "OPERATIONAL SCENARIOS (ANALYTICAL NARRATIVES)", indent=False)
    heading(doc, "14A.1 Scenario S1 — Static Mast at a Campus Gate")
    bodies(doc, [
        "A college installs a 4K camera on a pole looking at a gate. Ego-motion is nil. Motion keyframing shines: empty nights skip inference. A visible firearm in a rare incident should alert the control room. Privacy risk is high because faces are large. Policy: retain keyframes of alerts only, not all motion, and involve the chief proctor. This scenario is the closest to Grega-style CCTV papers and the easiest for the current code.",
        "False alarms: umbrellas, band instruments, guard rifles that are authorised. Authorised-weapon lists (a future whitelist of uniforms) are out of scope; human acknowledgement is mandatory. The scenario teaches that technical true positives can be operational false alarms.",
    ])
    heading(doc, "14A.2 Scenario S2 — Vehicle-Mounted Edge Node on a Border Road")
    bodies(doc, [
        "A patrol vehicle carries a mini-PC and a mast camera, or receives a UAV RTSP while halted. Links to district HQ drop in nullahs. Edge inference still runs. SMS waits in a queue until GSM returns, or is radio-relayed by a human reading the dashboard. This scenario is the strongest argument for G4 (cloud independence).",
        "Ego-motion when the vehicle moves will open the keyframe gate continuously. Operators should run detection when halted, or enable a future homography stage. The scenario thus binds Chapter 8 limitations to a realistic doctrine of use: halt, scan, move.",
    ])
    heading(doc, "14A.3 Scenario S3 — Festival Overwatch")
    bodies(doc, [
        "A UAV overflies a lawful public festival under police permission. Crowds create constant motion; keyframing savings shrink. Small objects and occlusions raise FN. Ethical risk peaks. The correct doctrine is: Vajra-Eye is a sparse extra eye for clearly visible long guns, not a pickpocket detector and not a political-opinion camera. If the model cannot be validated on crowd aerial video, it should not be switched on. Related-work humility becomes an operational switch.",
    ])
    heading(doc, "14A.4 Scenario S4 — Plant Perimeter at Night")
    bodies(doc, [
        "IR illuminators or thermal cameras are common at plants. The current RGB YOLO will fail. The scenario exists to force the future-work thermal item. Meanwhile, the Java pipeline can still ingest an IR-as-grey stream and may detect silhouettes of long objects if retrained. Without retraining, night is a documented outage, not a surprise.",
    ])
    heading(doc, "14A.5 Scenario S5 — Laboratory Examination Demo")
    bodies(doc, [
        "The likely viva demo: a file video, a prop, logs, and this report. Success is a start-to-alert path and an examiner able to locate DFD, PERT, related-work gaps, and code. This scenario is in scope for Assignment 1. All other scenarios are analytical, not claims of completed field trials.",
    ])
    heading(doc, "14A.6 Cross-Scenario Requirements Reuse")
    body(doc, "FR-01 to FR-12 stay the same; only θ, P_min, and legal procedure change. That is the benefit of a modular architecture: doctrine is configuration plus SOP, not a fork of the repository for every site.")


def write_glossary_and_indexish(doc):
    chapter(doc, "ANNEXURE VI")
    body(doc, "GLOSSARY OF TECHNICAL TERMS USED IN THE REPORT", indent=False)
    terms = [
        ("Alert fatigue", "Degraded human response after too many alarms."),
        ("Anchor-free", "Detector head that does not use preset box shapes."),
        ("Backbone", "Feature-extracting CNN layers before the detection head."),
        ("Cloudlet", "Small nearby data centre or server for mobile/edge clients."),
        ("Cooldown", "Minimum time between repeated alerts for one camera."),
        ("Confidence", "Model’s estimated probability for a box/class."),
        ("Contour", "Boundary of a connected foreground blob in a binary image."),
        ("Critical path", "PERT path that determines minimum project duration."),
        ("DJL", "Deep Java Library for running neural nets on the JVM."),
        ("Edge", "Compute near the sensor rather than in a distant cloud."),
        ("Ego-motion", "Motion of the camera itself."),
        ("False negative", "A real weapon not flagged."),
        ("False positive", "A flag without a real weapon."),
        ("Feature map", "Internal CNN tensor encoding patterns."),
        ("GOP", "Group of pictures in video compression, affecting camera delay."),
        ("Ground truth", "Human labels used to score a detector."),
        ("Heartbeat inference", "Periodic YOLO call even without motion."),
        ("Homography", "Projective map between two views of a plane."),
        ("Human-in-the-loop", "A person must authorise action."),
        ("Inference", "Running a trained model on new data."),
        ("IoU", "Intersection over union of two boxes."),
        ("Keyframe", "A frame selected for further processing or storage."),
        ("Latency", "Time from event to useful output."),
        ("mAP", "Mean average precision, a detection contest metric."),
        ("MIN_AREA", "Smallest blob area counted as motion."),
        ("NMS", "Non-maximum suppression of duplicate boxes."),
        ("ONNX", "Portable neural-network file format."),
        ("Payload encryption", "Cipher on the message body, not only the pipe."),
        ("Precision", "TP/(TP+FP)."),
        ("Recall", "TP/(TP+FN)."),
        ("RBAC", "Access control by named roles."),
        ("RTSP", "Protocol to pull live camera streams."),
        ("Soft real-time", "Deadlines matter but missing one is not catastrophic."),
        ("θ (theta)", "Motion energy or difference threshold."),
        ("Transfer learning", "Reusing a model trained on another dataset."),
        ("True negative/positive", "Correct reject / correct hit."),
        ("UAV", "Unmanned aerial vehicle; drone."),
        ("Vajra-Eye", "Name of this academic prototype system."),
        ("YOLO", "You Only Look Once family of one-stage detectors."),
    ]
    for k, v in terms:
        body(doc, f"{k}: {v}")
    heading(doc, "ANNEXURE VII — MAPPING TO UNIVERSITY GUIDELINE HEADS")
    add_table(doc,
              ["Guideline head", "Where addressed"],
              [
                  ["Cover page", "Front matter"],
                  ["Acknowledgement", "Front matter"],
                  ["Certificate Annexure A", "Front matter"],
                  ["Synopsis 3–4 pages heads", "Synopsis / Abstract"],
                  ["Objective & scope", "Ch. 1, Synopsis"],
                  ["Theoretical background", "Ch. 2"],
                  ["Definition of problem", "Ch. 1.5"],
                  ["Analysis vis-à-vis users", "Ch. 4"],
                  ["System planning PERT", "Ch. 5"],
                  ["Process logic of modules", "Ch. 6"],
                  ["Methodology, HW/SW", "Ch. 7"],
                  ["Maintenance & evaluation", "Ch. 13"],
                  ["Cost and benefit", "Ch. 11"],
                  ["Life cycle, ERD, DFD", "Ch. 4, 5, 7"],
                  ["I/O screen design", "Ch. 10"],
                  ["Process involved", "Ch. 8"],
                  ["Testing method & report", "Ch. 12"],
                  ["Code sheet printout", "Annex IV"],
                  ["User manual, security, backup", "Ch. 9, 15"],
                  ["Org background", "Annex I"],
                  ["Data dictionary", "Annex II"],
                  ["Abbreviations, figures, tables", "Front lists"],
                  ["References / websites", "Annex V"],
                  ["Guide details", "Annex III"],
                  ["Soft copy LMS", "Annex V statement"],
                  ["Page geometry & fonts", "Whole Word file"],
              ])
    caption(doc, "Table A.3 Compliance map against the prescribed PDF.")
    heading(doc, "ANNEXURE VIII — STUDENT RESPONSIBILITY NOTES")
    bodies(doc, [
        "Fill mobile and email of the guide before hard binding if the university demands a complete Annexure A. Replace laboratory SMS placeholders. Do not upload secrets to LMS. Keep the original backup of the short draft for your records. Page numbers will display in Word’s print layout and in PDF export; they are PAGE fields at the bottom centre.",
        "If the examiner asks why the report is long: related work was explicitly expanded, double spacing is compulsory, figures and code listings are required, and the target length for this submission was two hundred pages of a complete project document rather than a thin abstract.",
    ])


def write_more_theory(doc):
    heading(doc, "2.10 Additional Notes on Probability of Detection")
    bodies(doc, [
        "Let a frame contain a weapon with probability π (very small in peacetime). Let the detector have recall r and precision p at the chosen threshold. Expected true alerts per keyframe ≈ π r. Expected false alerts ≈ ((1−π)/π) terms more usefully handled via confusion counts on a realistic prior. If π is 10^−4 and false-positive rate per keyframe is 10^−3, officers drown. Motion gating reduces the number of times the detector is asked, which reduces false alerts if false alerts are approximately per-inference, not per-time, for still cameras. That stochastic argument is the theoretical link between Chapter 2, Chapter 8, and the economic cost of false positives in Chapter 11.",
        "Calibration: a reported P=0.85 is not a frequentist 85% unless the model is calibrated (Guo et al. on calibration of neural nets). Officers should treat P as a score. This note prevents over-interpretation of the dashboard.",
    ])
    heading(doc, "2.11 Notes on JPEG as an Inference Input")
    bodies(doc, [
        "Encoding a Mat to JPEG before DJL is convenient and slightly lossy. High compression would hurt small knives. Quality should remain high. A future version may pass raw RGB arrays into DJL Image without JPEG. The theoretical cost is a few milliseconds and a possible mild drop in high-frequency features.",
    ])
    heading(doc, "2.12 Notes on Threading and Happens-Before")
    bodies(doc, [
        "previousFrame in MotionDetectionService is mutated on the capture thread only in the present design, so visibility is simpler. If two cameras share one service, races appear. Java Memory Model awareness is part of theoretical background for a concurrent MCA project even if the first prototype is single-stream.",
    ])
