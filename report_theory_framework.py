"""Chapter 2 continuation: theoretical foundations supplied for Vajra-Eye."""
from report_styles import heading, subhead, body, bodies, bullets, add_figure, add_table, caption, formula, add_code_lines


def write_conceptual_framework(doc):
    heading(doc, "2.10 Theoretical Foundations and Conceptual Framework of Project VAJRA-EYE")
    bodies(doc, [
        "This section records the formal system philosophy, the layered architecture, the mathematical model of adaptive keyframe filtering, the YOLOv8 detection theory, the rationale for the Deep Java Library on a Java 17 runtime, the AES-GCM alert model, and the evaluation metrics that together constitute the conceptual framework of Vajra-Eye. It is the theoretical spine against which later chapters of design, implementation, testing, and maintenance are judged.",
        "The framework is edge-first: analysis is moved to the companion computer or field gateway so that the system can still detect a visible weapon when a wide-area link is congested, jammed, or absent. Only a small encrypted packet is emitted after a verified detection. That sentence is the paradigmatic shift from classical CCTV backhaul.",
    ])

    heading(doc, "2.11 System Philosophy and Paradigmatic Shift")
    bodies(doc, [
        "Traditional visual surveillance relies on centralised stream ingestion. Raw or lightly compressed video packets travel over a wide-area network to a remote command facility, where human operators watch banks of monitors. That model introduces three structural vulnerabilities that become acute in tactical and aerial deployments.",
    ])
    subhead(doc, "2.11.1 Cognitive bottlenecks and vigilance decrement")
    body(doc, "Continuous observation of multiple surveillance monitors produces human fatigue. Subtle or brief security events—such as a person drawing a weapon—are missed not because the photons never reached a sensor, but because the observer’s vigilance decrement is a documented human-factors fact. Vajra-Eye does not abolish the officer; it stops asking the officer to stare at empty terrain.")
    subhead(doc, "2.11.2 Network and bandwidth depletion")
    body(doc, "Continual uplink of high-definition video over wireless radio-frequency links exhausts available bandwidth. The operational symptoms are frame loss, jitter, and high telemetry latency. A drone that spends its radio budget on empty sky cannot spend it on a verified alert. Edge inference converts a continuous video problem into a sparse event problem.")
    subhead(doc, "2.11.3 Vulnerability to electronic warfare and link loss")
    body(doc, "Centralised processing collapses if hostile actors sever or jam the wireless channel, or if ordinary rural backhaul simply dies. A sentry that can see only while the WAN lives is not a sentry. Moving the analytical pipeline onto an on-drone companion computer or a forward field gateway enables autonomous on-device threat detection. The system functions without continuous network dependency and transmits only lightweight, encrypted alert packets when an active threat is verified.")
    subhead(doc, "2.11.4 Statement of the paradigm")
    bodies(doc, [
        "The paradigm is therefore: sense locally, think locally, speak rarely, speak encrypted, and keep a human in the act loop. Cloud analytics remain optional for later forensic review of stored keyframes; they are not on the critical path of the three-second laboratory budget.",
        "This philosophy constrains every later SHALL statement: no raw video in SMS, fail-visible if the model file is missing, motion gating before YOLO, and AES-GCM on the payload even when TLS is also present.",
    ])

    heading(doc, "2.12 Multi-Layer System Architecture (Conceptual)")
    bodies(doc, [
        "The architecture separates hardware abstraction, computer vision, neural inference, and secure communication into three decoupled tiers. Decoupling is not decoration: it is what allows a camera to be swapped without rewriting encryption, and encryption to be swapped without rewriting YOLO.",
    ])
    add_figure(doc, "architecture.png", "Figure 2.10: Three-tier conceptual architecture of Vajra-Eye.")
    subhead(doc, "2.12.1 Perception layer — capture and ingestion")
    bodies(doc, [
        "The perception layer captures optical frames from airborne or fixed electro-optical sensors. The preferred live transport is the Real-Time Streaming Protocol (RTSP). In the field, RTP media commonly rides UDP in order to avoid the transmission-buffer latency associated with TCP handshakes over lossy wireless channels. The laboratory implementation also accepts a local file and a webcam index so that Assignment-1 demonstration does not depend on a flying airframe.",
        "Frames are decoded into native memory buffers (OpenCV Mat). That buffer is the contract object of the rest of the pipeline. Colour order is BGR unless an explicit conversion is applied before a model that expects RGB. Getting that conversion wrong is a theoretical error, not a cosmetic one.",
    ])
    subhead(doc, "2.12.2 Processing layer — edge intelligence engine")
    body(doc, "The processing layer executes a two-stage sequential pipeline: adaptive temporal motion gating followed by deep neural inference. Stage one is cheap and runs on every frame. Stage two is expensive and runs only on candidate keyframes. This cascade is the engineering form of the Viola–Jones insight that a cheap rejector should sit in front of an expensive classifier. The mathematical model of stage one is given in Section 2.13. The detector of stage two is YOLOv8, Section 2.14.")
    subhead(doc, "2.12.3 Command layer — orchestration and tactical dispatch")
    bodies(doc, [
        "The command layer manages service lifecycles (Spring Boot), aggregates event metadata, enforces symmetric payload encryption, and broadcasts alerts across cellular SMS channels, SMTP endpoints, and real-time WebSocket or REST command dashboards. It is also the home of audit logs, cooldowns, and role-based access.",
        "If the command layer blocks the capture thread while waiting for an SMS acknowledgement, the perception layer will stall and the RTSP socket will overflow. That coupling is forbidden. Chapter 8A therefore places capture, inference, and notify on isolated threads with a bounded queue and a drop-oldest policy.",
    ])
    add_figure(doc, "layered_arch.png", "Figure 2.11: Logical layer stack from presentation down to the JVM platform.")

    heading(doc, "2.13 Mathematical Model of Adaptive Keyframe Filtering")
    bodies(doc, [
        "Running continuous deep neural inference on a high-frame-rate video feed depletes drone battery reserves and drives edge compute modules into thermal throttling. Because the vast majority of surveillance frames contain static terrain or empty perimeters, Vajra-Eye employs an upstream temporal motion-gating filter. The model below is the formal statement of the MotionDetectionService implemented in Java.",
        "Let an incoming video stream be a discrete sequence of trichromatic frames",
    ])
    add_figure(doc, "eq_frames.png", "Equation (2.1): Discrete trichromatic frame sequence.", width_cm=14.0)
    body(doc, "where H and W are the frame height and width in pixels and the third dimension is the colour channel count.")

    subhead(doc, "2.13.1 Step 1 — perceptual greyscale reduction")
    bodies(doc, [
        "Incoming frames are converted from three-channel colour matrices to a single-channel luminance matrix I_t in R^{H×W} using ITU-R BT.601 perceptual weights. The reduction is not an aesthetic preference: motion energy on compressed video is more stable on luma than on chroma, and the subsequent Gaussian and difference operators become three times cheaper.",
    ])
    add_figure(doc, "eq_gray.png", "Equation (2.2): ITU-R BT.601 luma transform.", width_cm=14.0)
    body(doc, "In OpenCV this is Imgproc.cvtColor(..., COLOR_BGR2GRAY), whose weights match the same family of luma coefficients. The report states BT.601 explicitly so that an examiner can audit the conversion.")

    subhead(doc, "2.13.2 Step 2 — spatial Gaussian smoothing")
    bodies(doc, [
        "High-frequency sensor noise, atmospheric scintillation, compression blocking, and motor vibration from drone rotors are suppressed by convolving the greyscale image with a two-dimensional Gaussian kernel G_σ. Differentiation of unsmoothed frames would amplify those high-frequency terms and inflate the motion score.",
    ])
    add_figure(doc, "eq_gauss.png", "Equation (2.3): Discrete Gaussian pre-filter (kernel width K = 21).", width_cm=14.5)
    body(doc, "The submitted implementation uses a 21 × 21 kernel (Size(21, 21) in OpenCV). The standard deviation is left at OpenCV’s default derivation from the aperture when the last argument of GaussianBlur is 0. That choice is a documented heuristic, not a claim of an optimal Wiener filter.")

    subhead(doc, "2.13.3 Step 3 — absolute temporal frame differencing")
    bodies(doc, [
        "The spatial intensity variation between the current smoothed frame I′_t and the stored previous frame I′_{t−1} is evaluated by absolute matrix subtraction. The first frame of a session has no predecessor; it is stored as baseline and is never a keyframe. After an RTSP reconnect the baseline is flushed so that a new scene is not compared with a dead one.",
    ])
    add_figure(doc, "eq_diff.png", "Equation (2.4): Absolute temporal difference.", width_cm=13.5)

    subhead(doc, "2.13.4 Step 4 — binary thresholding and morphological dilation")
    bodies(doc, [
        "Continuous pixel differences are binarised against an intensity threshold θ_pixel, empirically set to 25 on 8-bit luma. The value 25 is a starting calibration, not a universal constant; Chapter 8 records the two-clip tune (null clip versus walk-in clip) that an operator should repeat per camera.",
    ])
    add_figure(doc, "eq_bin.png", "Equation (2.5): Binary motion mask.", width_cm=14.0)
    bodies(doc, [
        "To connect fragmented pixels caused by camouflage patterning, broken shadows, or subtle limb movement, the binary mask is dilated with a rectangular structuring element S of size 3 × 3. Dilation is Minkowski addition on the binary grid: a pixel survives if the reflected structuring element centred on it intersects the mask.",
    ])
    add_figure(doc, "eq_dilate.png", "Equation (2.6): Morphological dilation of the motion mask.", width_cm=13.0)

    subhead(doc, "2.13.5 Step 5 — contour analysis and the decision boundary")
    bodies(doc, [
        "Topological outer contours C = {c_1, …, c_m} are extracted from the dilated mask using Suzuki’s border-following algorithm (OpenCV RETR_EXTERNAL, CHAIN_APPROX_SIMPLE). The pixel area A(c_i) of each closed contour is computed by the discrete Green’s theorem (shoelace formula), which OpenCV exposes as Imgproc.contourArea.",
    ])
    add_figure(doc, "eq_area.png", "Equation (2.7): Shoelace area of a contour polygon.", width_cm=13.5)
    bodies(doc, [
        "A video frame is classified as a candidate keyframe for deep-learning inference if and only if at least one moving region exceeds the area threshold θ_area, calibrated to 1000 pixels in the laboratory build. Frames that fail the test are discarded from the inference path; they are not deleted from the capture clock.",
    ])
    add_figure(doc, "eq_key.png", "Equation (2.8): Keyframe decision rule.", width_cm=14.5)
    bodies(doc, [
        "This filtering process is designed to eliminate on the order of 70% to 77% of redundant background frames before they reach the neural network, reducing CPU and GPU utilisation and extending flight-battery duration. Chapter 12 reports a laboratory still-scene reduction near 70%. A shaking airframe will reduce that saving; an upper-bound panning suppressor (Section 8A.3) is therefore part of the production loop: if more than about 60% of the frame area moves, the event is treated as ego-motion, not as a weapon-sized blob, and the baseline is allowed to catch up.",
        "The pair (θ_pixel, θ_area) is the entire classical parameter surface of stage one. Raising them starves YOLO; lowering them converges to all-frame inference and destroys the project’s algorithmic story. They are administrator-visible quantities in the operational manual.",
    ])
    add_figure(doc, "motion_keyframe.png", "Figure 2.12: Motion score versus time with threshold θ; shaded peaks are keyframes.")
    add_figure(doc, "pipeline.png", "Figure 2.13: End-to-end detection pipeline from RTSP capture to encrypted notify.")

    heading(doc, "2.14 Deep Learning Object Detection Theory — YOLOv8")
    bodies(doc, [
        "Frames that pass the motion threshold are forwarded to a YOLOv8 single-stage object detector. Unlike two-stage detectors such as Faster R-CNN, which first generate region proposals and then classify them, YOLO treats detection as a unified regression problem: bounding-box offsets and class probabilities are predicted in one forward pass. That unification is why a nano graph can meet a three-second end-to-end budget on a laboratory CPU when it is not invoked on every frame.",
        "The conceptual tensor path is: a raw frame is resized and letterboxed to the network input, typically 640 × 640 × 3, then passed through a CSP-style backbone (CSPDarknet lineage), a path-aggregation neck, and two decoupled heads.",
    ])
    add_code_lines(doc, """Raw Frame (640 x 640 x 3)
        | 
        v
 [ CSPDarknet-style Backbone ]
        |
        v
 [ Path Aggregation Neck (FPN/PAN family) ]
        |
        +--------------------+
        |                    |
        v                    v
 Classification Head     Regression Head (DFL)
 (class probabilities)   (continuous box distances)""")
    caption(doc, "Figure 2.14: Conceptual YOLOv8 forward path used in Vajra-Eye (ONNX graph).")

    subhead(doc, "2.14.1 Anchor-free detection")
    body(doc, "Traditional detectors rely on fixed anchor boxes that must be tuned to a training set of aspect ratios. Aerial weapons seen from a steep gimbal angle violate those ratios. YOLOv8 uses an anchor-free design that predicts the distance from an assigned point to the four sides of the box. Hyperparameter load falls, and generalisation to unusual perspectives improves in principle. Vajra-Eye inherits this property from the exported ONNX graph; it does not re-derive anchors in Java.")

    subhead(doc, "2.14.2 Decoupled head")
    bodies(doc, [
        "Earlier YOLO versions often unified classification and localisation in one output tensor. YOLOv8 decouples them into separate convolutional branches. The classification branch produces class-specific probability distributions. The regression branch produces spatial localisation, including a distribution focal-loss representation of box edges. Decoupling reduces the well-known optimisation conflict in which a shared head cannot simultaneously be a good classifier and a good box fitter.",
        "At inference time DJL (or ONNX Runtime beneath it) executes both branches inside one session. The Java service sees only DetectedObjects: class name, probability, and bounding geometry.",
    ])

    subhead(doc, "2.14.3 Multi-task training loss (background of the frozen graph)")
    bodies(doc, [
        "The submitted project does not train YOLOv8; it executes a frozen graph. The loss that produced that graph is nevertheless part of the theoretical framework, because it explains which errors the network was punished for. The total loss is a weighted sum of box, classification, and distribution-focal terms.",
    ])
    add_figure(doc, "eq_loss.png", "Equation (2.9): YOLOv8 multi-task training loss.", width_cm=14.5)
    bodies(doc, [
        "Complete IoU loss penalises overlap error, centroid distance, and aspect-ratio inconsistency together. Let b and b^gt be predicted and ground-truth centroids, ρ the Euclidean distance, c the diagonal of the smallest enclosing box, and v the aspect-ratio consistency term.",
    ])
    add_figure(doc, "eq_ciou.png", "Equation (2.10): CIoU localisation loss.", width_cm=14.0)
    bodies(doc, [
        "Distribution Focal Loss treats a box edge as a discrete distribution over nearby integer locations rather than as a single deterministic offset. That representation is useful when weapon contours are blurred by motion or partial occlusion. Binary cross-entropy (or a closely related classification objective in the training recipe) evaluates class confidence on assigned samples.",
        "Inference in Vajra-Eye applies two additional decision parameters that are not inside the graph: a probability floor P_min (0.85 in the laboratory build) and a closed set of class names treated as weapons. Those parameters are policy, not learning. They are how related-work warnings about alert fatigue enter the runtime.",
        "Non-maximum suppression (NMS) removes duplicate boxes on the same object. It is executed inside the translator or post-process attached to the ONNX graph. The student must not count two overlapping rifle boxes as two incidents.",
    ])

    heading(doc, "2.15 Deep Java Library and Java Runtime Advantages")
    bodies(doc, [
        "Machine-learning research predominantly occurs in Python. Deploying long-running, mission-critical aerial-surveillance middleware in CPython nevertheless introduces operational hazards that an MCA systems project is entitled to refuse.",
    ])
    subhead(doc, "2.15.1 Global Interpreter Lock")
    body(doc, "The CPython Global Interpreter Lock limits pure multi-threaded concurrency. Concurrent RTSP decoding, motion differencing, and socket communication contend for the same interpreter lock unless the heavy work is in native extensions that release it. Java threads are real operating-system threads. java.util.concurrent is the native vocabulary of the capture-queue-worker design in Chapter 8A.")
    subhead(doc, "2.15.2 Memory management of multi-megabyte frames")
    bodies(doc, [
        "Continuous allocation of multi-megabyte NumPy arrays can fragment native heaps during multi-hour runs. The JVM’s garbage collector tracks Java references, but OpenCV Mat and ONNX tensors live off-heap. The theoretical rule is therefore RAII: every Mat is released in a finally block or a NativeScope; every DJL NDManager is a try-with-resources sub-manager. Relying on finalize() is forbidden.",
        "DJL provides engine-agnostic Java abstractions over native C++ execution providers, specifically ONNX Runtime and, optionally, LibTorch. Off-heap direct buffers can be reclaimed without a full Stop-the-World pause if the application does not pin them incorrectly. Near-native C++ speed is thereby combined with Java type safety, Spring lifecycle management, and a deployment story that MCA examiners already understand.",
        "The implementation language is therefore a theoretical choice, not a fashion choice: Spring operations plus DJL inference plus OpenCV pixels, on Java 17, with a documented native-memory protocol.",
    ])

    heading(doc, "2.16 Cryptographic Theory and Tactical Alert Security")
    bodies(doc, [
        "Surveillance alerts transmitted over public cellular networks or tactical RF bands can be intercepted, replayed, or replaced. Vajra-Eye encrypts alert metadata—weapon class, confidence, camera identifier, optional geography, and timestamp—with the Advanced Encryption Standard in Galois/Counter Mode (AES-GCM).",
        "Unlike CBC, AES-GCM is authenticated encryption with associated data (AEAD). Confidentiality is counter-mode encryption with a 12-byte nonce (IV) from a cryptographic random generator (SecureRandom). Identical plaintexts then yield distinct ciphertexts. Integrity and authenticity are obtained from a GHASH-style universal hash over GF(2^128), producing a 128-bit tag. If any byte of ciphertext or bound associated data is altered, decryption fails closed; a spoofed ‘all clear’ cannot be injected by bit-flipping a captured SMS blob.",
        "AES-GCM is accelerated on modern processors (Intel AES-NI, ARMv8 cryptographic extensions). Encryption latency is expected well under one millisecond and is negligible beside YOLO. Hardware acceleration is a reason to prefer GCM over a slow purely software cipher in a 3-second budget.",
        "The laboratory listing must not ship a hard-coded key or a fixed IV. A fixed IV with CBC was shown in an early teaching snippet and is explicitly rejected by this theoretical section. Production keys belong in a platform store or an HSM. Associated data may bind camera_id and a timestamp so that a ciphertext cannot be replayed against a different camera.",
    ])
    add_figure(doc, "security_layers.png", "Figure 2.15: Defence-in-depth around the alert payload.")

    heading(doc, "2.17 Theoretical Evaluation Metrics")
    bodies(doc, [
        "System performance is evaluated with information-retrieval and detection metrics, plus an additive latency budget. Accuracy on a TN-dominated stream is not the lead number.",
    ])
    add_figure(doc, "eq_prf.png", "Equation (2.11): Precision, recall, and specificity.", width_cm=14.5)
    bodies(doc, [
        "True positives (TP) are correctly detected and localised weapons. False positives (FP) are benign objects called weapons. False negatives (FN) are missed weapons. True negatives (TN) are non-threat frames correctly ignored. In a still night, TN dominate; a 99% accuracy can hide a useless precision. Chapter 12 therefore leads with counts, not with a single percentage.",
        "Average precision is the area under the precision–recall curve. Mean average precision averages AP across N weapon classes. The laboratory Assignment-1 set is too small to publish a competitive mAP; the formulae are recorded so that a later dataset can be scored correctly.",
    ])
    add_figure(doc, "eq_ap.png", "Equation (2.12): Average precision as area under the PR curve.", width_cm=10.5)
    add_figure(doc, "eq_map.png", "Equation (2.13): Mean average precision over N classes.", width_cm=10.5)
    body(doc, "End-to-end latency is modelled as the sum of sequential pipeline stages on the keyframe path:")
    add_figure(doc, "eq_lat.png", "Equation (2.14): Additive end-to-end latency budget.", width_cm=15.0)
    add_figure(doc, "eq_budget.png", "Equation (2.15): Real-time operational constraint used in SHALL-P1.", width_cm=8.0)
    bodies(doc, [
        "On a warm laboratory PC the YOLO term dominates when a keyframe is admitted; the SMS/network term dominates when a real gateway is used; motion differencing is cheap. Keyframing attacks the YOLO term. Thread isolation attacks queueing delay. G1GC pause targets attack capture overruns. Those three sentences are how Chapter 2’s mathematics become Chapter 8A’s engineering.",
        "By maintaining T_total < 3.0 seconds on the reference edge-class host for a 720p laboratory file, the system claims real-time operational response in the soft-real-time sense: a missed deadline degrades quality; it does not violate a hard interlock, because Vajra-Eye does not fire a weapon.",
    ])
    add_figure(doc, "performance.png", "Figure 2.16: Illustrative compute and inference-volume effect of keyframing.")
    add_figure(doc, "confusion_matrix.png", "Figure 2.17: Laboratory confusion matrix used with Equations (2.11)–(2.13).")

    heading(doc, "2.18 Conceptual Framework — Compact Restatement")
    bodies(doc, [
        "Philosophy: edge-first, speak rarely, speak encrypted, human-in-the-loop. Architecture: perception (RTSP/Mat), processing (motion gate then YOLOv8), command (Spring, AES-GCM, notify). Mathematics: BT.601 luma, Gaussian K=21, |Δ|, θ_pixel=25, dilate 3×3, Suzuki contours, θ_area=1000, optional 60% pan reject. Learning: frozen YOLOv8 nano, anchor-free, decoupled heads, CIoU+BCE+DFL heritage, P_min=0.85. Runtime: Java 17, DJL/ONNX, RAII for Mats. Security: AES-GCM AEAD, random 12-byte nonce. Metrics: precision, recall, specificity, AP, mAP, T_total < 3 s.",
        "Everything that follows in analysis, PERT, implementation, testing, and the user manual is an expansion of this restatement. If a later feature cannot be traced to a sentence here, it is either a KUK documentation obligation (DFD, data dictionary) or it does not belong in Assignment 1.",
    ])
    add_table(doc,
              ["Framework element", "Symbol / artefact", "Runtime counterpart"],
              [
                  ["Luma", "Eq. 2.2", "cvtColor BGR2GRAY"],
                  ["Gaussian", "K=21", "GaussianBlur"],
                  ["Difference", "Δ_t", "Core.absdiff"],
                  ["Pixel gate", "θ_pixel=25", "THRESH_BINARY"],
                  ["Area gate", "θ_area=1000", "contourArea"],
                  ["Pan reject", "60% area", "isSalientMotion"],
                  ["Detector", "YOLOv8n ONNX", "DetectionService"],
                  ["Policy", "P_min=0.85", "Threat filter"],
                  ["AEAD", "AES-GCM", "AlertService"],
                  ["Budget", "T_total<3s", "TC16 / SHALL-P1"],
              ])
    caption(doc, "Table 2.1: Traceability from conceptual framework to code symbols.")
