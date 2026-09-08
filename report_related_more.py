"""Additional original related-work pages to reach the 200-page submission target."""
from report_styles import heading, subhead, body, bodies, bullets, bullet, add_table, caption


def write_related_more(doc):
    heading(doc, "3.51 Survey of YOLO Lineage After the Foundational Papers")
    bodies(doc, [
        "Redmon’s 2016 conference paper is necessary but not sufficient related work for a 2026 implementation that loads YOLOv8n. The lineage after YOLO and YOLOv2 includes YOLOv3’s multi-scale predictions, YOLOv4’s bag of freebies, the Ultralytics YOLOv5 engineering line, YOLOX’s decoupled head, YOLOv6 and YOLOv7 industrial variants, and YOLOv8’s anchor-free instance-segmentation-capable design. Each step changed the error profile on small objects, which is the profile that matters for aerial weapons.",
        "YOLOv3 (Redmon and Farhadi, 2018) introduced predictions at three scales and a deeper Darknet-53 backbone. Related-work consensus is that YOLOv3 was the first YOLO that a practitioner could trust on mixed-size COCO objects without heroic tricks. For Vajra-Eye, the lesson is architectural: a single coarse grid is not enough for a knife at altitude. The present nano model still uses a pyramid-like neck; the student did not re-implement Darknet-53 in Java, but the theoretical debt is acknowledged.",
        "Bochkovskiy, Wang and Liao (2020) presented YOLOv4 as a thoroughly ablated recipe: mosaic, CIoU, CSP connections, and PANet-style aggregation. The paper is as much a teaching document on training as it is a detector. MCA students often cite YOLOv4 for speed; the more honest citation is for the demonstration that data augmentation can substitute for some architectural novelty. Vajra-Eye does not retrain, so it inherits whatever augmentation Ultralytics used for the public nano weights, which is a related-work limitation, not a virtue.",
        "YOLOv5, though initially lacking a conventional peer-reviewed flagship paper, became the de facto engineering baseline in industry repositories. Related work here is socio-technical: open repositories can outrun conference cycles. A KUK examiner who insists on ‘only IEEE papers’ would miss how field systems are actually built. This report cites both the archival YOLO papers and the engineering line, and it labels which is which.",
        "Ge et al.’s YOLOX and later YOLOv6/v7 papers explored anchor-free heads and industrial deployment tricks (RepVGG-style re-parameterisation, more careful quantisation stories). YOLOv8 continues the anchor-free direction. Vajra-Eye’s DJL path does not depend on the training head, only on the exported ONNX graph. Related work therefore splits into ‘how the graph was born’ and ‘how the graph is executed’. Confusing those two is a common student error this chapter tries to prevent.",
        "Wang, Bochkovskiy and Liao’s YOLOv7 (2022) argued for trainable bag-of-freebies at real-time speeds. Jocher and collaborators’ YOLOv8 documentation (2023 onward) is the immediate ancestor of the file yolov8n.onnx. Later letters (v9, v10, v11 in community usage) appeared while this MCA was being written. The project freezes v8 nano on purpose: Chapter 3.24 already banned model-chasing. Related work records that newer letters exist so that the freeze is a decision, not ignorance.",
    ])

    heading(doc, "3.52 Two-Stage Detectors Revisited for Completeness")
    bodies(doc, [
        "Girshick et al.’s R-CNN (2014) showed that CNNs could classify region proposals. Fast R-CNN shared convolution. Faster R-CNN (Ren et al., 2015) added the Region Proposal Network. Mask R-CNN (He et al., 2017) added a mask head. Cascade R-CNN (Cai and Vasconcelos) refined boxes in stages. Libra R-CNN, DetectoRS, and Sparse R-CNN are later two-stage or query-based cousins. None of them is the runtime of Vajra-Eye; all of them are the accuracy ceiling against which YOLO is usually compared.",
        "The related-work question for an edge MCA is not ‘which paper has the highest COCO AP’ but ‘which family remains alive when the GPU is a laptop iGPU or a CPU’. Published Faster R-CNN speeds on server GPUs do not transfer. Several Indian conference papers still recommend Faster R-CNN for campus CCTV without measuring edge latency. Those papers are cited as cautionary related work: they optimise the wrong objective for this problem class.",
        "Feature Pyramid Networks (Lin et al., 2017) are theoretically shared by both families. Aerial small-object surveys keep returning to FPN, PANet, BiFPN (EfficientDet), and later query-based pyramids. If Vajra-Eye ever tiles 4K frames, it will be standing on this pyramid literature whether the head is YOLO or DETR.",
    ])

    heading(doc, "3.53 Transformer Detectors and Why They Are Deferred")
    bodies(doc, [
        "Carion et al.’s DETR (2020) reframed detection as set prediction with Hungarian matching. Deformable DETR, DINO, RT-DETR, and related papers closed much of the training-time gap. By 2024–2026, real-time DETR variants appear in industrial blogs as YOLO competitors. Related work must mention them because an examiner may ask ‘why not a transformer’.",
        "The answer is operational, not aesthetic. Transformer detectors still tend to need more memory and more careful ONNX export; DJL plus a nano YOLO is a known-good student path. Attention is also harder to justify in a viva unless the student can derive the matcher. Deferral is written here so that future work is not an empty ‘we will use transformers’ slogan. A later assignment could swap the ONNX file if an RT-DETR export is validated on the same SHALL-P1 budget.",
        "Vision-language models (CLIP, Grounding DINO, open-vocabulary YOLO variants) can detect ‘rifle’ from text prompts without a closed class list. They are exciting related work and dangerous operationally: open vocabulary increases both recall of rare weapons and false triggers on toys, tools, and media posters. Vajra-Eye keeps a closed weapon set for Assignment 1. Open-vocabulary detection is recorded as a research branch, not a drop-in replacement.",
    ])

    heading(doc, "3.54 Datasets that Shape What ‘Weapon Detection’ Means")
    bodies(doc, [
        "A detector is only as honest as its dataset. Related work on data is therefore first-class. COCO and Open Images contain some sports and household objects that are not weapons; they are pretraining sources, not evaluation for a border system. ImageNet is even further away. Students who quote ImageNet top-1 as if it were weapon mAP are mixing tasks.",
        "Olmos, Tabik and Herrera (2018) assembled pistol frames, many from films and the web. Subsequent GitHub datasets repeat that pattern: CCTV stills, video-game renders, and news photographs. Academic papers using these sets often report high accuracy that collapses on real streets. This report treats those numbers as in-domain scores, not as field scores.",
        "Military and police datasets are rarely public. That absence is itself related work: the literature has a structural hole. Synthetic data from game engines (Unreal, Unity, domain randomisation after Tobin et al.) is the ethical patch discussed earlier. Recent papers on synthetic firearms in thermal and RGB are appearing in remote-sensing workshops. They are promising and still face the sim-to-real gap that robotics has spent a decade documenting.",
        "Aerial datasets (VisDrone, UAVDT, Stanford Drone, some DOTA/xView categories) contain people and vehicles, rarely labelled firearms at useful resolution. Related work therefore cannot claim that ‘UAV detection is solved, we only swapped the class list’. Person AP on VisDrone is not rifle AP at 80 metres. Chapter 8’s small-object warning is a dataset warning.",
        "Indian-context data is thinner still: clothing, vegetation, light, and architecture differ from Western CCTV papers. Campus projects sometimes collect 200 images of a prop in a corridor and call it a dataset. Related work must distinguish a classroom collection from a benchmark. Vajra-Eye’s laboratory props are the former and are labelled as such in Chapter 12.",
    ])

    heading(doc, "3.55 Comparative Table of Dataset Families")
    add_table(doc,
              ["Family", "Typical content", "Use for Vajra-Eye", "Risk if misused"],
              [
                  ["COCO / OI", "Everyday objects", "Pretrain only", "False sense of AP"],
                  ["Film/web pistols", "Staged firearms", "Toy experiments", "Domain shift to field"],
                  ["VisDrone-like", "UAV people/vehicles", "Aerial people, not guns", "Wrong class transfer"],
                  ["Synthetic RGB", "Rendered rifles", "Possible G2 path", "Sim-to-real gap"],
                  ["Thermal public", "Coarse hot blobs", "Night future", "Poor blade signature"],
                  ["Own lab props", "Controlled indoor", "This MCA tests", "Not a border claim"],
              ])
    caption(doc, "Table 3.3 Dataset families reviewed for weapon-oriented aerial work.")

    heading(doc, "3.56 Literature on Occlusion, Pose and Carry Style")
    bodies(doc, [
        "A rifle on a sling, a pistol in a holster, a weapon inside a bag, and a weapon raised to aim are four different visual problems. Related papers that show only aimed pistols in movies overstate recall. Pose literature (OpenPose, HRNet) could in future gate ‘raised-arm plus object’, which is behaviour, not pure object detection. Vajra-Eye stays on the object side for Assignment 1 because behaviour models need even more data and more ethical caution.",
        "Occlusion papers in pedestrian detection (CrowdHuman, occlusion-aware R-CNN variants) teach that partial objects need part detectors or stronger pyramids. A half-hidden barrel is an occlusion problem. The current nano YOLO will miss many such cases; the limitations chapter agrees with this literature rather than promising part-based weapons.",
        "Carry-style variation is a cultural and climatic fact: winter coats in north India hide more than summer uniforms. Related work on clothing-invariant person ReID is only weakly transferable and is not used, because ReID of bystanders is out of ethical scope. The coat problem is left as a data problem (G2), not as a covert tracking problem.",
    ])

    heading(doc, "3.57 Compression, Encoding and the Hidden Pre-processor")
    bodies(doc, [
        "H.264/H.265 compression is a related-work actor that CV papers often ignore. Blocking artefacts and GOP keyframe pulsing change both motion scores and detector features. RTSP cameras in the field are compressed; laboratory webcams often are not. Several ‘motion detector too sensitive’ bugs are encoder bugs. Vajra-Eye’s Gaussian blur is a cheap related-work response to compression noise, not only to sensor noise.",
        "Bitrate drops on wireless drones introduce temporal holes. Optical-flow and differencing both suffer. Related streaming papers (DASH, adaptive bitrate) are designed for human viewing, not for Mt. An operational implication is to prefer I-frames for inference if a future parser can see NAL types. That is an advanced related-work item queued behind a working baseline loop.",
        "Colour subsampling (4:2:0) reduces chroma. Detectors trained on full chroma JPEGs may be slightly mismatched. This is a small effect next to scale and weather, and is mentioned for completeness so that ‘we converted BGR to RGB wrong’ is distinguished from ‘chroma is subsampled’. OpenCV and DJL colour-order bugs are a more common student failure; Chapter 12 tests should include a known-colour sanity image.",
    ])

    heading(doc, "3.58 Weather, Illumination and Atmospheric Related Work")
    bodies(doc, [
        "Dehazing (He’s dark-channel prior; later CNN dehazers), deraining, and low-light enhancement (Retinex, KinD, Zero-DCE) are entire subfields. They can be stacked in front of YOLO. Related work warns that enhancement can hallucinate edges that become false barrels. For a safety system, a missed detection in fog may be preferable to a hallucinated rifle if the operational policy is conservative—or the reverse if the policy is recall-first. Vajra-Eye currently does not dehaze; it documents weather as a limitation.",
        "Dawn and dusk produce long shadows that inflate photometric motion. Infrared cut filters switching on colour cameras cause global flashes that look like scene change. These are known CCTV-engineering facts, less often written in CVPR weapon papers. Including them is how a systems MCA differs from a methods paper.",
        "Monsoon rain on lenses is a blur kernel, not an ImageNet category. There is related work on adherent raindrop removal. It is future work. The honest related-work stance is that no student YOLO will be weather-proof without either thermal, radar, or a human who does not trust the box.",
    ])

    heading(doc, "3.59 Tracking Literature and Alert De-duplication")
    bodies(doc, [
        "SORT, DeepSORT, ByteTrack, and OC-SORT associate boxes across frames. Without tracking, one walking person with a visible rifle can generate an SMS storm. Related work on identity switches in crowded scenes explains why tracking is hard from a UAV. Vajra-Eye’s designed cooldown is a poor man’s tracker: time-based, not identity-based.",
        "Kalman filters in SORT are the same linear-Gaussian filters taught in MCA electives. The report mentions them so that tracking future work is not a mysterious ‘AI module’ but a named algorithm. ReID embeddings (OSNet and successors) would improve association and would increase privacy risk; they are not enabled.",
        "Track-to-alert policies in industrial VMS products (milestone, genetec—named as product class, not as copied manuals) usually require N consecutive frames or a dwell time. That policy literature is closer to SOC runbooks than to COCO. Chapter 15’s SOP is the academic cousin of those runbooks.",
    ])

    heading(doc, "3.60 Multi-Camera and Cross-View Related Work")
    bodies(doc, [
        "Multi-camera tracking (MCT) surveys describe overlapping and non-overlapping views, homographies, and appearance matching. A future Vajra-Eye farm of cameras would enter this literature. Assignment 1 is single-stream. The architecture’s camera_id field is the only present concession.",
        "Drone-plus-mast fusion is a related military pattern: UAV finds a cue; mast camera confirms. That pattern needs georegistration (Zhang calibration, GPS/IMU, terrain models). Related photogrammetry is non-trivial. The project records camera id, not lat-long, and does not pretend otherwise.",
        "Handover between a dying drone link and a ground camera is a systems related-work problem (make-before-break). Not implemented. Named because border narratives in Chapter 14 would otherwise sound like magic.",
    ])

    heading(doc, "3.61 Hardware Accelerators in the Related Landscape")
    bodies(doc, [
        "NVIDIA Jetson, Google Coral Edge TPU, Intel OpenVINO/NPU, Qualcomm Hexagon, and Apple Neural Engine are the 2026 edge-accelerator cast. Related work includes vendor model zoos and INT8 accuracy drops (Jacob et al. quantisation). Vajra-Eye’s Java/DJL/ONNX path is portable and not yet mapped to a Coral compiled graph. That is a performance left on the table, admitted in future work.",
        "CUDA versus CPU ONNX Runtime is the first practical split. A laboratory i7 CPU can still meet SHALL-P1 for nano YOLO on 720p keyframes. A busy 4K all-frame loop would not. Related work on throughput versus latency (little’s law in disguise) says that keyframing is what makes CPU viable.",
        "FPGA papers on YOLO exist in IEEE circuits journals. They are out of MCA software scope. They prove that the algorithm can be frozen into silicon if a later organisation needs watts, not jars.",
    ])

    heading(doc, "3.62 Programming-Language Related Work Beyond DJL")
    bodies(doc, [
        "Python dominates CV research (PyTorch, Ultralytics). C++ dominates OpenCV internals and TensorRT samples. C# appears in some Windows VMS. Go and Rust appear in new cloud video gateways. Java appears in enterprise backends and, more rarely, in DJL or DeepLearning4J inference. Related work on language choice is therefore a map of ecosystems, not a speed contest on one kernel.",
        "Deeplearning4j (Eclipse) is an older JVM DL stack. ONNX Runtime has Java bindings of its own, which DJL wraps. TensorFlow Java exists. Each path has version-skew pain. The project chose DJL because it is engine-agnostic and documented for ONNX. Related work records the alternatives so that ‘Java cannot do AI’ is refuted with names, not slogans.",
        "JNI fragility is discussed in reliability related work. Pure-Java image codecs would reduce native crashes and would slow the hot path. That trade-off is classical (safety versus speed) and is left as an experiment, not a rewrite.",
    ])

    heading(doc, "3.63 Software Product-Line and Modularity Papers")
    bodies(doc, [
        "Pohl’s software product-line engineering and Baldwin and Clark’s modularity literature explain why swapping DetectionService should not require rewriting AlertService. Spring’s @Autowired is a modest implementation of that modularity. Related work on microservices is declined in 6.10; product-line thinking still applies inside one JVM: optional thermal, optional SMS, optional dashboard.",
        "Feature toggles (Fowler; Humble and Farley on CD) would let a field node disable notify during a drill. The academic properties file is a crude toggle. Named so that maintenance Chapter 13 is not only ‘apply patches’.",
    ])

    heading(doc, "3.64 Human-in-the-Loop Machine Learning")
    bodies(doc, [
        "Interactive ML and HITL surveys (Amershi et al.; Holzinger) describe systems where humans correct models. Vajra-Eye’s officer ACK, if built, is HITL for operations more than for training. Active learning (Settles) would close the loop into G2. Related work cautions that officer time is the scarce resource; querying every uncertain frame recreates alert fatigue.",
        "Explanation (LIME, Grad-CAM, saliency) is often requested in vivas. Grad-CAM on a weapon box can be pedagogically useful and operationally misleading (heat on a trigger guard that a lay officer over-reads). This report does not ship explanations in the SMS. Related XAI work is cited as optional dashboard future, with a warning against theatrical heatmaps.",
    ])

    heading(doc, "3.65 Adversarial Machine Learning Related Work")
    bodies(doc, [
        "Szegedy’s intriguing properties, Goodfellow’s FGSM, and later patch attacks (Brown et al.; Thys, Van Ranst and Goedemé on adversarial patches for persons) show that detectors can be blinded by stickers. Weapon detectors in research have been attacked with patches on posters. A border adversary has stronger incentives than a conference attacker.",
        "Certified defences are incomplete for high-resolution video. Operational defences are diversity (second sensor), humans, and not publishing the exact ONNX on an unsecured path. Related work here is uncomfortable and necessary. Vajra-Eye does not claim robustness. Chapter 16 lists red-team tests as undone.",
        "Data poisoning of a future retraining pipeline is a supply-chain analogue. If officers’ ACK clicks become labels, an insider can skew the model. HITL related work and security related work meet at that sentence. Assignment 1 does not retrain in the field; the risk is queued with G2.",
    ])

    heading(doc, "3.66 Privacy, Law and Surveillance Studies")
    bodies(doc, [
        "Solove’s taxonomy of privacy harms, Nissenbaum’s contextual integrity, and Indian writings on informational privacy after Justice K.S. Puttaswamy v. Union of India (2017) form the legal-theoretical related work. A weapon-detection camera still captures people. Purpose limitation (only weapons, not general profiling) is the design response. Face galleries are out of scope.",
        "CCTV studies in criminology are mixed on deterrence. Related work that promises ‘AI will stop crime’ is not used. The project claims faster notice of visible weapons in a laboratory sense, not a crime-rate effect. That humility is a citation stance as much as an ethical stance.",
        "Workplace surveillance literature (employees under cameras) would apply if Vajra-Eye were pointed at a factory gate. Different consent and labour-law issues appear. The report’s application chapter lists sites as hypotheticals, not as installations.",
        "International humanitarian-law discussions of autonomy in weapons systems (GGE on LAWS) are cited only to draw a bright line: this MCA is a sensing-and-notify prototype. It is not a fire-control system. Related work that blurs sensing and shooting is rejected as a design parent.",
    ])

    heading(doc, "3.67 Public-Health Analogies Used Carefully")
    bodies(doc, [
        "Alarm fatigue in hospitals (Joint Commission alerts; Cvach’s reviews) is the best empirical literature on too many beeps. Security SOC fatigue is discussed more in industry white papers than in archival journals. This report uses the medical literature as the rigorous cousin, while admitting the domain gap.",
        "Screening-test theory (sensitivity, specificity, predictive values, Bayes at low prevalence) is undergraduate biostatistics and is the correct language for rare weapons. Low prevalence destroys positive predictive value even when specificity looks high. Related work that reports only accuracy on balanced test sets hides that Bayesian fact. Chapter 12’s TN-heavy matrix is closer to reality than a 50-50 classroom set.",
    ])

    heading(doc, "3.68 Command-and-Control and C4ISR Lite")
    bodies(doc, [
        "Military C4ISR primers (unclassified textbooks and staff-college notes) describe a loop from sense to command to act. Vajra-Eye occupies the sense-and-make-sense fragment. Related work on OODA (Boyd) is popular in slides and is used here only at the level of ‘observe–orient’ being automated, ‘decide–act’ remaining human.",
        "Digitised battlefield management systems in the Indian public discourse (various MoD statements, without copying classified material) mention sensors and fused pictures. A student project cannot claim interoperability with those systems. The related-work gesture is: alerts should be structured (JSON fields) so that a later adapter is possible. That is systems hygiene, not a partnership claim.",
    ])

    heading(doc, "3.69 GIS, Mapping and Location Related Work")
    bodies(doc, [
        "If a future version stamps GPS from a drone autopilot (MAVLink telemetry is the usual related protocol), alerts become map objects. Web GIS (Leaflet, OpenLayers) and QGIS are the display related work. Geodetic transforms (WGS84, UTM) must be correct or the box lands in the wrong village. The present system does not do this; Chapter 3.22 already said so. The paragraph exists so that Chapter 14’s border narrative is not misread as a GIS product.",
        "Geofencing literature (location-based services) could suppress alerts inside a known armoury polygon. That is a policy overlay, powerful and dual-use. It is future work with a legal review, not a weekend feature.",
    ])

    heading(doc, "3.70 Audio, Multimodal and Non-Visual Cues")
    bodies(doc, [
        "Gunshot detection (acoustic multilateration, ShotSpotter-class systems) is related multimodal work. Microphones plus cameras can raise confidence. They also raise cost and false alarms from fireworks. Vajra-Eye is vision-only. Acoustic fusion is a named non-goal for Assignment 1.",
        "Vibration and radar (mmWave people counters) are other modalities. Automotive radar-camera fusion papers show the template. Border units already use multiple sensors; this Java pipeline is one possible analytic on the camera branch.",
    ])

    heading(doc, "3.71 Evaluation Metrics Beyond a Single Accuracy Number")
    bodies(doc, [
        "mAP, AP50, AP75, AR, F1, PR curves, calibration (ECE), and latency percentiles are the professional metric set. Related papers that lead with ‘99% accuracy’ on imbalanced frames are treated as pedagogically weak. This report uses a confusion matrix, latency, CPU, and keyframe fraction because those match SHALL statements.",
        "Operational metrics: alerts per camera-hour on null video; median time-to-ACK if humans are in the study; duplicate-alert ratio. These come from SRE and SOC practice more than from CVPR. They are specified as future evaluation, not as faked tables.",
        "Fairness metrics (error by clothing, skin tone, gender presentation) are related work in face analytics and are only partly transferable to weapons. A detector that fires more on a community’s traditional tools would be a harm. No such audit was performed; that is a limitation, not a claim of neutrality.",
    ])

    heading(doc, "3.72 Reproducibility and Open Science Related Work")
    bodies(doc, [
        "Peng’s reproducibility papers, the ACM SIGMOD reproducibility effort, and Papers With Code’s culture of checkpoints are the related work for pinning Maven versions and naming the ONNX file. A report without a model hash is a story. Annex version pins are the student’s attempt to be in that culture.",
        "Stodden’s work on computational science and the general crisis-of-confidence literature in ML (Gundersen and Kjensmo) justify Chapter 12.13’s repeatability protocol. Small n and author-labelled clips remain a threat to validity even with pinned code.",
    ])

    heading(doc, "3.73 DevOps, MLOps and the Un-glamorous Related Work")
    bodies(doc, [
        "Sculley et al. (2015) on hidden technical debt in ML systems is the most important non-CV citation in this project. Glue code, data dependencies, and configuration debt all appear in Vajra-Eye: RTSP URLs, thresholds, class name lists, and Twilio keys. Related work says to treat configuration as code. application.properties is that attempt.",
        "Continuous integration for a JNI-heavy app is hard on public runners. Related work in reproducible containers (Docker) would help and is not required by KUK. A Dockerfile is listed as a maintenance enhancement.",
        "Observability (logs, metrics, traces—OpenTelemetry) is how a 3 a.m. failure is diagnosed. Spring Actuator is the small related-work nod. Full APM is out of scope.",
    ])

    heading(doc, "3.74 Comparative Systems — Academic Prototypes")
    bodies(doc, [
        "University intelligent-surveillance theses typically contain: a detector, screenshots, and a conclusion that ‘accuracy is high’. Few contain PERT, data dictionaries, encrypted SMS, and a STRIDE paragraph. Related work therefore includes those theses as a baseline this MCA is trying to beat on software-engineering completeness, not on COCO AP.",
        "Some theses integrate Raspberry Pi cameras and Telegram bots. They are close cousins: notify-on-detect. Vajra-Eye’s distinctions are the Java stack, AES discussion, motion gate, and the long survey. Telegram versus SMS is an adapter-level difference, not a scientific one.",
        "A smaller number of theses attempt drone offboard processing on Jetson. Those are the hardware cousins. If their Python loops omit keyframing, this project’s CPU story is the differentiator. If they include TensorRT and thermal, they are ahead on sensors; this project remains ahead on KUK documentation obligations.",
    ])

    heading(doc, "3.75 Comparative Systems — Industrial VMS Analytics")
    bodies(doc, [
        "Commercial video-management systems sell ‘weapon detection’ as an analytic pack. Public datasheets emphasise GPU servers, not disconnected hill-posts. Related work from vendor white papers is used cautiously (marketing). The architectural contrast remains cloud-or-campus-server versus edge-first Java. Cost-benefit Chapter 11 uses licence fees as a qualitative comparator, not a copied price list.",
        "Open-source VMS (ZoneMinder, Shinobi, Frigate, MotionEye) plus a coral detector is a hobbyist-related ecosystem. Frigate’s MQTT events are conceptually close to ThreatEvent. Vajra-Eye does not wrap Frigate; it re-implements a narrower pipeline for examination clarity. Citing Frigate prevents a false originality claim on the idea of event-driven NVR analytics.",
    ])

    heading(doc, "3.76 Indian Smart-City and Safe-City Programme Context")
    bodies(doc, [
        "Public tender language for Indian safe-city and smart-city camera networks often lists analytics as a bullet: intrusion, crowd, number plate, sometimes ‘object left’ and rarely ‘weapon’. Related work is the tender structure itself: agencies buy VMS plus analytics plus storage. An indigenous edge module could sit as a sub-system if it spoke ONVIF/RTSP and emitted structured events. This MCA does not bid tenders; it explains where a student system would plug in.",
        "Bandwidth economics of Indian last-mile links (shared in TRAI-type public reports at a high level) support edge processing. The citation is the public fact of constrained rural backhaul, not any non-public network map.",
        "Make in India and Atmanirbhar Bharat appear in Chapter 14 as policy context. Related work is policy documents as context, not as technical papers. They justify preferring open-source stacks a student can inspect, which DJL and OpenCV are.",
    ])

    heading(doc, "3.77 DRDO, BEL and Public Indigenous Sensing Narratives")
    bodies(doc, [
        "Public DRDO and BEL communications describe surveillance radars, electro-optics, and C2 software at a high level. This report does not invent access to those programmes. Related work is the existence of an indigenous sensing industry, which makes a student Java prototype a pedagogical step rather than a fantasy of replacing that industry.",
        "Academic collaborations (IITs, NITs, CAIR-adjacent public papers) on ATR and EO tracking appear in Indian journals. They are typically Python/C++ and sensor-rich. Vajra-Eye cites them as the professional ceiling and stays in the MCA software envelope.",
    ])

    heading(doc, "3.78 Ethics-by-Design Check Against the Survey")
    bodies(doc, [
        "Floridi’s information-ethics vocabulary and IEEE Ethically Aligned Design (high-level) suggest: transparency, accountability, and human agency. Vajra-Eye’s SMS is transparent as an alert, opaque as a model. Accountability is the audit log. Human agency is the refusal to actuate weapons or locks. Related work that skips human agency is not used as a parent.",
        "Datasheets and model cards, already cited, are the documentation ethics. The laboratory clips are not released with this zip, to avoid spreading weapon imagery. That is a related-work choice aligned with ‘do not include graphic stills’.",
    ])

    heading(doc, "3.79 What Was Read and Deliberately Not Followed")
    bodies(doc, [
        "End-to-end reinforcement learning for camera PTZ control looks attractive in papers and is unstable in student timeboxes. Not followed.",
        "GAN-based weapon image synthesis can help G2 and can also generate harmful media. Not followed in Assignment 1.",
        "Face-based watchlists. Not followed.",
        "Cloud-only GPU inference as the primary path. Not followed (contradicts edge theory).",
        "All-frame 4K YOLO on CPU. Not followed (contradicts resource poverty).",
        "These refusals are related work in the negative. A survey that only lists friends and no refusals is a brochure.",
    ])

    heading(doc, "3.80 Compact Annotated Bibliography Notes (Extended)")
    notes = [
        "Dalal and Triggs (HOG): baseline of hand-crafted detection; explains pre-2013 CCTV papers.",
        "Viola and Jones: cascade as a budget device; ancestor of motion-then-YOLO.",
        "Krizhevsky et al. (AlexNet): the deep-feature break; not used directly.",
        "Simonyan and Zisserman (VGG): depth and 3×3; historical backbone.",
        "He et al. (ResNet): residual learning; still inside many detectors.",
        "Lin et al. (FPN): small-object theory for aerial frames.",
        "Lin et al. (focal loss / RetinaNet): easy-negative problem of one-stage detectors.",
        "Liu et al. (SSD): contemporaneous one-stage alternative to YOLO.",
        "Redmon et al. (YOLO / YOLO9000 / YOLOv3): unified detection and real-time culture.",
        "Bochkovskiy et al. (YOLOv4): training recipe as contribution.",
        "Jocher / Ultralytics (YOLOv5–v8): engineering line behind the ONNX file.",
        "Ren et al. (Faster R-CNN): two-stage gold standard; rejected for edge latency.",
        "He et al. (Mask R-CNN): masks unused; future evidence outline.",
        "Carion et al. (DETR): transformer detection; deferred.",
        "Stauffer and Grimson: MOG background; contrast to UAV motion.",
        "Horn and Schunck; Lucas and Kanade: optical flow upgrades.",
        "Bradski (OpenCV): the practical vision substrate.",
        "Satyanarayanan (cloudlets); Shi et al. (edge surveys): the place of compute.",
        "Han et al. (deep compression); Jacob et al. (quantisation): future shrink path.",
        "NIST FIPS-197; Dworkin SP 800-38D (GCM): alert confidentiality/integrity.",
        "RFC 2326 (RTSP): camera interface in theory.",
        "Sculley et al.: ML systems debt; configuration as a first-class artefact.",
        "Amershi et al.: human-AI interaction guidelines for dashboards.",
        "Lee and See: trust calibration; copy in the manual.",
        "Parasuraman, Sheridan, Wickens: levels of automation; keep low.",
        "Cvach: alarm fatigue; threshold and cooldown.",
        "Gebru et al.; Mitchell et al.: datasheets and model cards for G2.",
        "Puttaswamy (privacy); Solove; Nissenbaum: legal-ethical filter.",
        "Olmos et al.; Grega et al.: application weapon papers; knives hard.",
        "VisDrone organisers: aerial people/vehicles, not firearms.",
        "Brown et al.; Thys et al.: adversarial patches; no robustness claim.",
        "Brooks (Mythical Man-Month): integration is work; Fowler: monolith is allowed.",
        "IEEE 830: SHALL language in Chapter 4A.",
        "KUK project guidelines PDF: the meta-related-work of this document’s shape.",
    ]
    for n in notes:
        bullet(doc, n)

    heading(doc, "3.81 Synthesis Paragraphs for Examiners Short on Time")
    bodies(doc, [
        "If Chapter 3 must be reduced to one page in a viva, the student should say: weapon detection literature is mature on movie-like pistols and immature on aerial Indian night data; YOLO-class one-stage models are the latency-rational choice; two-stage and transformer models are accuracy reserves; edge computing literature demands local inference and drop policies; motion keyframing is a cascade in the Viola–Jones sense; Java/DJL is a minority but documented path; encryption of alerts is standard crypto applied to a neglected application gap; humans remain in the loop because automation literature and law require it; the project occupies the empty cell of Table 3.1.",
        "If asked what is new, the student should not say ‘a new CNN’. The student should say ‘a documented, testable integration that the surveyed papers do not jointly occupy, with gaps named rather than hidden’.",
        "If asked what would change the related-work picture, the answer is a public ethical aerial weapon dataset, a measured Jetson+INT8 latency certificate, and a human-factors trial of alerts. Until those exist, both this MCA and most papers remain provisional.",
    ])

    heading(doc, "3.82 Chapter 3 Closing Note on Length")
    bodies(doc, [
        "The related-work chapter was expanded because the first Assignment-1 draft had no proper survey and because the university guideline asks for theoretical background plus a main report that can be examined. Double spacing further lengthens pages. The expansion is organised so that a reader can stop after the gap table or continue through datasets, weather, tracking, law, and annotated notes.",
        "Subsequent chapters consume this survey: requirements SHALL statements point back here; architecture chooses a modular monolith here; testing refuses inflated accuracy here; the manual calibrates trust here; future work is a list of literature debts rather than a wish list copied from the internet.",
        "With this closing note, the literature survey proper ends. System analysis in Chapter 4 begins from user-facing requirements that the survey has already constrained.",
    ])
