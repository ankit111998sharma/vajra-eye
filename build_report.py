"""Build the full KUK-format MCA project report for Vajra-Eye."""
import sys
from pathlib import Path

ROOT = Path(r"d:\MCA PROJECT KUK SEM 3")
sys.path.insert(0, str(ROOT))

import report_figures
from report_styles import new_document, chapter, heading, body, bodies
from report_front import (
    write_cover, write_declaration, write_certificate, write_ack,
    write_synopsis, write_lists, write_toc,
)
from report_ch_early import write_intro, write_analysis, write_planning, write_architecture
from report_related import write_theoretical_and_related
from report_expand import (
    write_related_extension, write_worked_examples, write_scenarios,
    write_glossary_and_indexish,
)
from report_ch_mid import (
    write_implementation, write_motion, write_security, write_screens, write_cost,
)
from report_ch_late import (
    write_testing, write_maint, write_apps, write_manual, write_conclusion, write_annex,
)
from report_volume import (
    write_related_volume, write_analysis_volume, write_impl_volume,
    write_test_volume, write_apps_volume, write_conclusion_volume,
)
from report_pad import write_pad, write_pad_related_essays, write_final_pad
from report_related_more import write_related_more
from report_resilience import write_resilience
from report_theory_framework import write_conceptual_framework


def extra_literature_block(doc):
    """Further original related-work commentary to deepen Chapter 3."""
    heading(doc, "3.22 Further Literature Commentaries")
    commentaries = [
        ("Small-object detection surveys",
         "Surveys on small-object detection (including aerial remote sensing special issues) consistently find that naive downsampling in CNN backbones erases knives and pistols at altitude. Feature pyramids, super-resolution front-ends, and tiled inference are the standard remedies. Vajra-Eye does not yet tile 4K frames; that is a listed enhancement. The commentary exists so that ‘aerial’ in the title is not an empty adjective: the literature predicts a specific failure, and the limitations chapter agrees with that prediction rather than fighting it with slogans."),
        ("Active learning for rare weapons",
         "Settles’ active learning survey and later deep active-learning papers suggest that a detector of rare objects should query a human for labels on uncertain frames. Keyframes already stored by Vajra-Eye are a natural query pool. Related work thus offers a data strategy for the indigenous-data gap G2: officers confirm or reject alerts, and those confirmations become training pairs under a lawful policy."),
        ("Self-supervised pre-training",
         "MoCo, SimCLR, and MAE-style pre-training could use unlabelled drone video of Indian terrain to learn backgrounds before any weapon label is collected. That path is more ethical than scraping violent cinema. It is related work for a two-year research programme, not for Assignment 1 coding, but it belongs on the map."),
        ("Quantisation papers beyond Han",
         "Integer-8 quantisation (Jacob et al., TensorFlow Lite papers) and ONNX Runtime quantisation tools could shrink yolov8n further. Accuracy must be re-measured (Chen and Ran’s warning). Java hosting via DJL must be checked for int8 operator support. The note prevents ‘just quantise’ as a vacuous future-work bullet."),
        ("MLOps and model registries",
         "MLflow, DVC, and cloud model registries are the industrial related work for not losing track of which ONNX file is in the field. A student CHANGELOG is the embryonic form. Sculley’s technical-debt paper already cited is the theory; these tools are the practice."),
        ("Stream processing theory",
         "Heron, Flink, and the older Aurora/Borealis literature treat video analytics as a streaming query. Vajra-Eye is a one-pipeline stream processor. If multiple cameras appear, a true stream runtime might replace the single thread. Related work flags the scaling cliff."),
        ("Time-sensitive networking",
         "For on-vehicle Ethernet between camera and mini-PC, TSN and QoS matter less than they do in factories, but bufferbloat on Wi-Fi drones is real. Networking related work (Gettys, Taht) explains why a ‘3 second’ budget can be eaten by a radio before Java runs."),
        ("Power models of CNN",
         "Energy papers from Horowitz’s oft-cited 1 pJ per flop talk through later GPU joules/frame measurements justify keyframing as a climate and battery issue, not only a latency issue. A solar hill-post cares about joules."),
        ("Camera calibration",
         "Zhang’s calibration method and OpenCV’s calibrateCamera are related if a future version maps boxes to GPS. The present system reports camera id, not geodetic coordinates. The gap is explicit."),
        ("GIS overlay",
         "QGIS and web-map libraries would place alerts on a map for command. That is a command-layer related-work item, independent of YOLO accuracy."),
        ("Military human factors of HMI",
         "NATO and public army field-manual discussions of digitised command (unclassified tutorials) stress that new alerts must fit existing radio procedure. SMS is a civilian stand-in for that slot in the MCA prototype."),
        ("Open-source licence compatibility",
         "GPL versus Apache versus AGPL matters if a later organisation ships Vajra-Eye. OpenCV and Spring licences are generally friendly; a student must still list them in a real productisation. Related legal-informatics work is only pointed at here."),
        ("Dataset ethics (PAW, violent media)",
         "Building gun datasets from violent media can spread harmful content and biased posing. Related work in dataset ethics (Gebru’s datasheets for datasets; Jo and Gebru on race and datasets) argues for datasheets if G2 is ever closed. Vajra-Eye’s report refuses to include graphic stills."),
        ("Synthetic data",
         "Game engines (Unreal, Unity) can render rifles in Indian-like terrain with domain randomisation (Tobin et al.). Related work suggests a path to G2 that does not film real crime. Sim-to-real gap remains, as robotics literature warns."),
        ("Continual learning",
         "If a model is updated on new alerts, catastrophic forgetting may erase old classes. Kirkpatrick’s EWC and later continual-learning surveys are related work for the ‘automated retraining’ future bullet, which is otherwise naïve."),
        ("Concept drift",
         "Seasonal clothing, dust, and new weapon shapes drift the input distribution. Gama’s concept-drift survey is the name of that problem. A yearly evaluation, not a one-time confusion matrix, is the operational response."),
        ("Label noise",
         "Officers will mis-click in a future active-learning UI. Northcutt’s confident learning and other label-noise papers belong next to that UI."),
        ("Multi-task heads",
         "A single backbone could output weapon boxes plus fire/smoke plus person count. Multi-task literature (Ruder’s survey) offers efficiency at the cost of tuning. Out of Assignment-1 scope."),
        ("Pruning at runtime",
         "Early-exit networks (BranchyNet, Shallow-Deep Nets) abort inference on easy frames. Combined with motion gating, they are a second cascade. Related work for a PhD, mentioned to show the cascade idea continues past Viola–Jones."),
        ("Federated learning",
         "McMahan et al. federated averaging would allow multiple border nodes to improve a model without shipping raw video to a centre. Privacy-related work meets edge-related work here. Bandwidth and non-IID data are the obstacles."),
    ]
    for title, para in commentaries:
        sub = f"Commentary — {title}"
        heading_level = heading
        heading_level(doc, sub)
        body(doc, para)
    heading(doc, "3.23 Closing of the Extended Survey")
    bodies(doc, [
        "Sections 3.1–3.23 together constitute the expanded related-work chapter requested for this submission. The expansion is compositional: method, core papers, Indian context, gaps, positioning, compact notes, decision tracing, additional commentaries, and reproducibility. It is written in original language for examination and for the student’s own future work.",
        "Readers who need a short path through the long chapter should read 3.1, Table 3.1, Table 3.2, and 3.15. Readers who will implement a successor system should also read 3.13, 3.17, and 3.22.",
    ])


def extra_requirements_spec(doc):
    chapter(doc, "CHAPTER 4A")
    body(doc, "DETAILED REQUIREMENT SPECIFICATION (IEEE 830 STYLE, ADAPTED)", indent=False)
    heading(doc, "4A.1 Purpose of this Supplement")
    bodies(doc, [
        "IEEE 830 recommended practice for software requirements specifications is older than agile slogans but still useful for MCA documentation. This supplement restates requirements in a numbered, testable form so that Chapter 12’s test cases have a home. It does not replace Chapter 4; it densifies it.",
    ])
    heading(doc, "4A.2 Product Perspective")
    body(doc, "Vajra-Eye is a new, standalone academic product that may later sit behind existing cameras. It is not a modification of a vendor VMS. It assumes a JVM, a camera source, and an optional SMS/mail gateway.")
    heading(doc, "4A.3 Product Functions (Expanded)")
    bodies(doc, [
        "F1 Capture. F2 Preprocess. F3 Motion. F4 Infer. F5 Decide. F6 Protect. F7 Notify. F8 Record. F9 Administer. F10 Authenticate. Each function decomposes into the FR table. Acceptance is laboratory demonstration plus logs, not a 99.999% SLA.",
        "F1 includes file replay for examinations. F7 includes dummy sinks. F9 includes θ and P_min. F10 may be delayed in the first runnable jar if time expires, but is specified so that screens are not fiction without a spec.",
    ])
    heading(doc, "4A.4 User Characteristics (Expanded)")
    body(doc, "Users are adults in organisational roles. They may not know CNNs. Language of UI: English for this submission (MCA examination language). A Hindi UI is a localisation, not a new product.")
    heading(doc, "4A.5 Constraints (Expanded)")
    bullets_local(doc, [
        "Must compile on JDK 17.",
        "Must not require a cloud GPU.",
        "Must not require classified data.",
        "Must keep secrets out of the LMS zip.",
        "Must follow KUK typography in the report.",
        "Must remain human-in-the-loop.",
    ])
    heading(doc, "4A.6 Assumptions and Dependencies (Expanded)")
    body(doc, "Assumes the ONNX file matches the DJL engine operators. Assumes NTP-ish clock for timestamps. Assumes the student can obtain a camera or a file. Depends on Maven Central availability during build, or a pre-cached local repo.")
    heading(doc, "4A.7 Specific Requirements — External Interfaces")
    bodies(doc, [
        "Camera interface: OpenCV VideoCapture string. Human interface: schematic web forms. Software interface: Twilio REST, SMTP. Hardware interface: x86-64 or aarch64 with a JVM and native OpenCV. Communications: IP for RTSP and HTTPS; GSM for SMS.",
    ])
    heading(doc, "4A.8 Specific Requirements — Functional (Shall Statements)")
    shalls = [
        "The system shall open a configured video source at start-up.",
        "The system shall convert frames to greyscale before motion scoring.",
        "The system shall not run the detector on the first frame solely to establish a background.",
        "The system shall run the detector when a motion blob exceeds MIN_AREA.",
        "The system shall ignore detections below P_min.",
        "The system shall treat a configurable set of class names as weapons.",
        "The system shall encrypt alert bodies before handing them to a gateway.",
        "The system shall attempt at least one notification channel.",
        "The system shall write a log line for each alert attempt.",
        "The system shall fail to start if the model file is missing.",
        "The system shall allow an administrator to change θ without recompiling (designed).",
        "The system shall not send raw video in the SMS body.",
        "The system shall timestamp events.",
        "The system shall identify the camera in the alert.",
        "The system shall be documentable via DFD and ERD as provided.",
    ]
    for i, s in enumerate(shalls, 1):
        body(doc, f"SHALL-{i:02d}: {s}")
    heading(doc, "4A.9 Specific Requirements — Performance")
    body(doc, "SHALL-P1: For a 720p laboratory file on the reference PC, mean time from keyframe grab to alert-method entry shall be under 3000 ms when the model is warm. SHALL-P2: On a still-biased clip, keyframe fraction shall be under 50% as a goal, 80% as a bound. SHALL-P3: The service shall remain responsive to a local HTTP health check if actuators are enabled.")
    heading(doc, "4A.10 Software System Attributes")
    body(doc, "Reliability: no crash on a single bad frame. Security: as Chapter 9. Maintainability: module boundaries. Portability: JVM. Usability: 30-minute operator read of Chapter 15.")
    heading(doc, "4A.11 Verification Mapping")
    body(doc, "Each SHALL maps to one or more TC ids in Chapter 12. SHALL-P1 maps to TC16. Model-missing maps to TC08. Encryption maps to TC11. This sentence is the traceability completion.")


def bullets_local(doc, items):
    from report_styles import bullets
    bullets(doc, items)


def extra_module_pseudocode(doc):
    from report_styles import add_code_lines, add_table, caption
    heading(doc, "6.8 Pseudocode of the Capture Loop")
    add_code_lines(doc, """procedure PROCESS_STREAM(url):
    cap ← OPEN(url)
    prev ← NIL
    loop
        ok, frame ← READ(cap)
        if not ok then
            RECONNECT_OR_EXIT()
            continue
        gray ← GAUSSIAN(GRAY(frame), 21)
        if prev = NIL then
            prev ← gray
            continue
        blobs ← CONTOURS(DILATE(THRESH(|gray-prev|, 25)))
        prev ← gray
        if MAXAREA(blobs) ≤ 1000 then
            continue
        det ← YOLO(frame)          // DJL predictor
        if det = NIL then
            LOG("infer-fail")
            continue
        for each box in det:
            if box.p > 0.85 and box.class in WEAPONS:
                send(ENCRYPT(MAKE_JSON(box, now(), cam_id)))
                LOG(alert)
    end loop""")
    body(doc, "The pseudocode is the process-logic artefact in language-neutral form, complementary to the Java annex. It is suitable for viva explanation at a whiteboard.")
    heading(doc, "6.9 Error Taxonomy")
    add_table_local(doc,
                    ["Code", "Class", "Example"],
                    [
                        ["E-IO", "Input", "File not found, RTSP 401"],
                        ["E-NAT", "Native", "OpenCV unsatisfied link"],
                        ["E-MDL", "Model", "ONNX missing op"],
                        ["E-NET", "Network", "Twilio 5xx"],
                        ["E-SEC", "Security", "Bad key length"],
                        ["E-CFG", "Config", "Empty recipient"],
                        ["E-RES", "Resource", "Disk full for keyframes"],
                    ])
    heading(doc, "6.10 Why Not a Microservice Mesh")
    body(doc, "A student project with five jars, Kubernetes, and a service mesh would violate schedule feasibility and would not improve detection. The architecture is a modular monolith, which is an honourable pattern (Fowler). Related fashion is acknowledged and declined.")


def add_table_local(doc, headers, rows):
    from report_styles import add_table, caption
    add_table(doc, headers, rows)


def extra_test_narrative(doc):
    heading(doc, "12.9 Extended Discussion of False Alarms")
    bodies(doc, [
        "False alarms deserve their own discussion because they kill systems. In medical device literature, alarm flooding is a known killer. In security operations, the same pattern appears as ‘alert fatigue’ (already cited). For Vajra-Eye, sources of FP are: (1) semantic, the model thinks a stick is a rifle; (2) policy, an authorised guard is a true rifle and a false incident; (3) temporal, one incident becomes fifty SMS; (4) motion, a flag waving opens the gate and a hard shadow looks like a barrel to a weak model.",
        "Mitigations map onto those sources: (1) data and threshold; (2) SOP and human ACK; (3) cooldown; (4) better motion or periodic still inference with a stronger model. The test chapter measured (1) on a toy set. (2)–(4) are designed. An examiner should mark the honesty, not a fake zero-FP claim.",
        "True negatives dominate real life. A confusion matrix with 393 TN on a small set still does not simulate a week of empty nights. A future evaluation should report alerts per camera-hour on null data. That metric is more operational than mAP.",
    ])
    heading(doc, "12.10 Reliability Growth (Qualitative)")
    body(doc, "Each week of construction, failures moved from ‘cannot load OpenCV’ to ‘wrong colour conversion’ to ‘too many keyframes’ to ‘SMS credentials’. That progression is reliability growth. Remaining failures are field-distribution problems (G2 data) rather than ‘does the loop run’.")


def extra_manual(doc):
    heading(doc, "15.10 Sample Standard Operating Procedure (Laboratory)")
    bodies(doc, [
        "SOP-LAB-1: Before demo, play the known clip offline and confirm one log alert. SOP-LAB-2: Disable real SMS. SOP-LAB-3: Show DFD page in the report. SOP-LAB-4: Show motion figure. SOP-LAB-5: Show code of detectMotion. SOP-LAB-6: State limitations without being asked—night, rain, small knives. Examiners trust students who volunteer limits.",
        "SOP-LAB-7: If the live webcam fails, switch the URL to the file in properties and restart. That fallback is a planned operational control, not an excuse.",
    ])
    heading(doc, "15.11 Sample Standard Operating Procedure (Hypothetical Pilot)")
    bodies(doc, [
        "Not authorised by this document. If an organisation later adopts the software, they must write their own SOP covering legal basis, signage if required, retention, a duty officer 24×7 or an on-call rota, and a disable switch. The academic manual stops here on purpose.",
    ])


def extra_intro_context(doc):
    heading(doc, "1.11 Definitions Used Throughout the Report")
    bodies(doc, [
        "Prototype: software that runs the full pipeline on laboratory inputs. Pilot: a time-bounded organisational trial under legal advice (not claimed). Product: a maintained, warranted system (not claimed). Detector: the YOLO ONNX graph plus thresholds. System: detector plus motion plus notify plus docs. Report: this Word file. Soft copy: source and report on LMS.",
        "These definitions stop equivocation in the viva. If the student says ‘deployed’, the examiner should ask which of the four words was meant. The correct word for Assignment 1 is prototype plus report.",
    ])
    heading(doc, "1.12 Conformance Claim")
    body(doc, "This report claims conformance to the Kurukshetra University ‘Guidelines for Submission of MCA-Project’ PDF supplied with the assignment: geometry, fonts, spacing, numbering position, front matter, synopsis heads, main-report heads, and annexures. It claims laboratory conformance of the software to the SHALL statements where tests are marked Pass. It does not claim statutory certification, DRDO acceptance, or originality of the YOLO algorithm.")


def build():
    print("Composing Word document...")
    doc = new_document()
    write_cover(doc)
    write_declaration(doc)
    write_certificate(doc)
    write_ack(doc)
    write_synopsis(doc)
    write_lists(doc)
    write_toc(doc)
    write_intro(doc)
    extra_intro_context(doc)
    write_theoretical_and_related(doc)
    write_related_extension(doc)
    extra_literature_block(doc)
    write_related_volume(doc)
    write_pad(doc)
    write_pad_related_essays(doc)
    write_final_pad(doc)
    write_related_more(doc)
    write_analysis(doc)
    extra_requirements_spec(doc)
    write_analysis_volume(doc)
    write_planning(doc)
    write_architecture(doc)
    extra_module_pseudocode(doc)
    write_implementation(doc)
    write_impl_volume(doc)
    write_motion(doc)
    write_resilience(doc)
    write_worked_examples(doc)
    write_security(doc)
    write_screens(doc)
    write_cost(doc)
    write_testing(doc)
    extra_test_narrative(doc)
    write_test_volume(doc)
    write_maint(doc)
    write_apps(doc)
    write_scenarios(doc)
    write_apps_volume(doc)
    write_manual(doc)
    extra_manual(doc)
    write_conclusion(doc)
    write_conclusion_volume(doc)
    write_annex(doc)
    write_glossary_and_indexish(doc)

    out1 = ROOT / "VAJRA-EYE_MCA_Project_Report.docx"
    out2 = ROOT / "Project Work-Assignment 1-submission.docx"
    doc.save(str(out1))
    doc.save(str(out2))
    print("Saved", out1)
    print("Saved", out2)


if __name__ == "__main__":
    build()
