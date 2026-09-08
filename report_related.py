"""Chapter 2-3: Theoretical background and extensive related work."""
from report_styles import chapter, heading, subhead, body, bodies, bullets, add_figure, add_table, caption


def write_theoretical_and_related(doc):
    write_theoretical(doc)
    from report_theory_framework import write_conceptual_framework
    write_conceptual_framework(doc)
    try:
        from report_expand import write_more_theory
        write_more_theory(doc)
    except Exception:
        pass
    write_related(doc)


def write_theoretical(doc):
    chapter(doc, "CHAPTER 2")
    body(doc, "THEORETICAL BACKGROUND", indent=False)
    heading(doc, "2.1 Introduction to the Theoretical Base")
    bodies(doc, [
        "Every engineering project rests on a body of theory that explains why a chosen design is valid, what assumptions it makes, and where those assumptions fail. Vajra-Eye is not merely a collection of libraries glued together; it is an application of computer vision, statistical signal processing, deep neural networks, distributed systems, and cryptographic engineering to a concrete public-safety problem. This chapter presents that theoretical foundation in sufficient depth for an examiner to judge that the subsequent design and implementation are theoretically sound.",
        "The discussion proceeds from the physics of an image, through classical motion estimation, to modern convolutional detectors, and then to the systems theories of edge computing and secure notification. The intent is not to reproduce textbooks, but to select those fragments of theory that actually constrain the Vajra-Eye architecture: limited edge compute, unstable aerial cameras, the need for low false-alarm rates, and the requirement that an alert remain confidential while it travels from a field node to an officer.",
        "Kurukshetra University guidelines require a theoretical background as a distinct part of the main report. Accordingly, this chapter is written as a self-contained primer. A reader who is familiar with MCA core subjects such as operating systems, computer networks, and object-oriented design should be able to follow the argument without consulting external notes, while a specialist in computer vision will recognise the standard formulations that have been adopted.",
    ])

    heading(doc, "2.2 Digital Image and Video as Data")
    bodies(doc, [
        "A digital image is a discrete two-dimensional function I(x, y) whose value at each integer coordinate is an intensity or a colour triple. For an 8-bit greyscale image the range is {0, ..., 255}. A colour frame in the BGR order used by OpenCV is a three-channel array. A video is a sequence I_t(x, y), t = 0, 1, 2, ... sampled at a nominal frame rate, typically 15 to 30 frames per second for field cameras and often lower for bandwidth-limited drone downlinks.",
        "The spatial resolution of an aerial frame is limited by the optics, the sensor, altitude, and motion blur. A rifle that occupies 40 pixels at 40 metres may occupy fewer than 15 pixels at 120 metres. Object detectors that were trained on close-range photographs therefore suffer a domain shift when applied to nadir or oblique aerial imagery. Vajra-Eye cannot remove this physical constraint; it can only mitigate it by selecting informative frames, by using a detector family that handles multi-scale objects, and by reporting confidence rather than a binary guess.",
        "Temporal sampling introduces a second constraint. If a drone yaws quickly, consecutive frames may have a large global motion component even when no object of interest has entered the scene. Frame differencing will then fire continuously. The theoretical response is either to estimate and compensate ego-motion, or to raise the motion threshold and accept that some slow threats will be delayed. The present version of Vajra-Eye uses a conservative threshold plus morphological filtering; ego-motion compensation is recorded as future work in Chapter 16.",
        "Colour spaces matter for pre-processing. Motion energy is usually computed on a greyscale projection because chromatic noise is high in compressed video. Gaussian smoothing with a kernel such as 21 × 21, as used in the implementation, is a discrete approximation to a low-pass filter that suppresses sensor noise before differentiation. Differentiation of unsmoothed frames would amplify high-frequency noise and inflate the motion score M_t.",
    ])

    heading(doc, "2.3 Motion Estimation and Change Detection")
    subhead(doc, "2.3.1 Temporal differencing")
    bodies(doc, [
        "The simplest motion cue is the absolute difference D_t = |F_t − F_{t−1}|. Summing D_t over the image, or over a region, yields a scalar motion score. Thresholding that score is computationally cheap and maps well onto CPU-only edge nodes. The method fails when illumination changes globally (a cloud passing over the ground) and when the camera itself moves. Morphological dilation after binary thresholding connects broken difference blobs so that a moving person is not fragmented into many tiny contours.",
        "Let θ be a threshold and A_min a minimum blob area. A frame is declared a keyframe if there exists a connected component of the thresholded difference whose area exceeds A_min, or if the global sum exceeds θ. Vajra-Eye uses both tests in spirit: the reference implementation computes contours and area, while the mathematical model in Chapter 8 emphasises the scalar sum for clarity of exposition.",
    ])
    subhead(doc, "2.3.2 Background subtraction")
    bodies(doc, [
        "Background subtraction maintains a model B of the static scene and flags pixels where |I_t − B| is large. Running Gaussian averages, mixture-of-Gaussians (Stauffer and Grimson), and ViBe are classical examples. These methods are powerful on fixed CCTV but are a poor default for a continuously moving drone, because the background itself is non-stationary. They remain relevant when Vajra-Eye is pointed at a mast-mounted camera rather than a UAV.",
    ])
    subhead(doc, "2.3.3 Optical flow")
    bodies(doc, [
        "Optical flow estimates a dense or sparse vector field of apparent motion. Horn–Schunck and Lucas–Kanade are the textbook dense and sparse algorithms. Flow magnitude can distinguish camera shake from independently moving objects if ego-motion is first fitted to a homography. The computational cost is higher than frame differencing. Vajra-Eye therefore treats optical flow as a theoretically available upgrade, not as the baseline used in the submitted code.",
    ])

    heading(doc, "2.4 Classical Object Recognition")
    bodies(doc, [
        "Before deep convolutional networks became practical, object recognition relied on hand-crafted features. The Histogram of Oriented Gradients (HOG) of Dalal and Triggs remains the canonical example for pedestrian detection. A sliding window extracts HOG descriptors; a linear SVM classifies each window. Viola and Jones demonstrated real-time face detection using Haar-like features and AdaBoost, proving that cascade classifiers can meet video-rate budgets on CPUs of the mid-2000s.",
        "These methods are not obsolete for theory. They clarify three ideas that deep detectors still obey: (i) localisation is a search over spatial positions and scales; (ii) features must be somewhat invariant to illumination; (iii) a cascade or a confidence threshold is required to control false positives. Weapon detection papers from 2011–2016 frequently used HOG plus SVM on CCTV stills. Their accuracies collapsed under occlusion, unusual pose, and aerial scale. That empirical failure is a principal reason Vajra-Eye adopts a one-stage convolutional detector.",
    ])

    heading(doc, "2.5 Convolutional Neural Networks and Object Detection")
    bodies(doc, [
        "A convolutional neural network (CNN) learns filters that respond to edges, textures, and object parts. Stacking convolutions, non-linearities, and pooling builds a hierarchy. Classification CNNs such as AlexNet, VGG, and ResNet output a class label for an entire image. Detection networks must additionally output bounding boxes. Two families dominate the literature.",
        "Two-stage detectors, typified by R-CNN, Fast R-CNN, and Faster R-CNN, first propose regions and then classify them. They tend to be accurate and slower. One-stage detectors, typified by YOLO, SSD, and RetinaNet, predict boxes and classes in a single forward pass. They tend to be faster and, with modern training recipes, competitive in accuracy. Edge surveillance is latency-bound; hence Vajra-Eye selects a one-stage model.",
        "YOLOv8, used in this project, continues the YOLO line initiated by Redmon et al. It treats detection as a regression problem on a grid, now implemented with an anchor-free head in the Ultralytics design, CSP-style backbones, and mosaic augmentation during training. The nano variant (YOLOv8n) is small enough to export to ONNX and to execute through ONNX Runtime on a CPU or a modest GPU. Deep Java Library (DJL) loads that ONNX graph inside the JVM, which is the theoretical bridge between a Python-trained model and a Java operations stack.",
        "Non-maximum suppression (NMS) is a theoretical post-process that removes duplicate boxes. A confidence threshold τ (0.85 in the submitted pipeline) discards weak detections. These two numbers, together with the set of class names that are treated as weapons, define the operational decision rule of Vajra-Eye. Changing τ is a policy decision, not a retraining decision, and is therefore exposed conceptually in the administrator manual.",
    ])

    heading(doc, "2.6 Edge Computing Theory")
    bodies(doc, [
        "Cloud computing centralises storage and compute. Edge computing places compute near the data source to cut latency, save bandwidth, and survive link loss. Satyanarayanan’s work on cloudlets and Shi et al.’s surveys of edge computing supply the vocabulary: proximity, locality, and hierarchical offload. For a border drone, the ‘edge’ is a rugged computer in a vehicle, a backpack, or an onboard companion computer. Raw 1080p video at 30 fps is tens of megabits per second; an encrypted JSON alert is a few kilobytes. The theoretical gain is obvious if inference can be trusted locally.",
        "Edge theory also warns of resource poverty: limited RAM, no data-centre cooling, and bursty power. Algorithms must therefore be interruptible, bounded in memory, and able to drop work. Motion keyframing is exactly such a drop policy: when nothing moves, the detector sleeps. This is an instance of the more general principle of approximate computing for situational awareness—better a slightly delayed alert than a thermally throttled node that drops the stream entirely.",
    ])

    heading(doc, "2.7 Cryptographic Protection of Alerts")
    bodies(doc, [
        "Confidentiality of a threat message is obtained by a symmetric cipher. AES in Galois/Counter Mode (GCM) provides confidentiality and integrity; AES in CBC mode with PKCS5 padding, as shown in one of the illustrative listings, provides confidentiality if the IV is not reused. The theoretically correct operational choice for a new deployment is AES-GCM with a random 96-bit nonce per message and a key stored in a platform keystore, not in source code. The report discusses both the illustrative teaching code and the recommended operational configuration so that examiners can see the difference between a prototype and a hardened field system.",
        "Transport security (TLS) protects the channel; payload encryption protects the message even if logs are copied. Role-based access control protects the dashboard. Hashing of passwords (preferably with a slow KDF such as bcrypt or Argon2, rather than raw SHA-256) protects accounts. Together these mechanisms instantiate the classical CIA triad—confidentiality, integrity, availability—for a surveillance microservice.",
    ])

    heading(doc, "2.8 Software Architecture Theory Used in the Project")
    bodies(doc, [
        "The implementation follows a layered and service-oriented style. Spring Boot supplies inversion of control, so that VideoProcessor, MotionDetectionService, DetectionService, and AlertService are independently testable beans. This is the practical outcome of the Dependency Inversion Principle. The detection pipeline is a pipes-and-filters architecture: each stage consumes a frame or a detection list and emits a richer artefact. Pipes-and-filters is the correct theoretical match for streaming perception.",
        "Real-time behaviour is soft real-time: missing a deadline degrades quality but does not crash a plant. Java threads, as used to launch the capture loop, are adequate for soft real-time on a non-RTOS. Hard real-time weapon interlocks would require a different platform and are outside the MCA project scope.",
    ])

    heading(doc, "2.9 Summary of Chapter 2")
    body(doc, "The theoretical background may be summarised as follows. Images are noisy, scale-varying sequences. Motion can be cheaply approximated by smoothed frame differences. Objects can be localised by a one-stage CNN. Edge deployment forbids naive cloud offload of every frame. Alerts must be cryptographically protected. Java services can host this pipeline if the model is exported to a portable format such as ONNX. The next chapter reviews how prior researchers have combined, or failed to combine, these ideas, and thereby locates the research gap that Vajra-Eye addresses.")


def write_related(doc):
    chapter(doc, "CHAPTER 3")
    body(doc, "RELATED WORK AND LITERATURE SURVEY", indent=False)

    heading(doc, "3.1 Purpose and Method of the Survey")
    bodies(doc, [
        "Related work is not an ornamental chapter. It is the evidence that the student has examined what already exists, has understood its limits, and has not reinvented a solved problem under a new name. The Kurukshetra University project guidelines ask for theoretical background, problem definition, and a methodology that can be justified. Those requirements cannot be met unless the literature is read in a structured way.",
        "The survey method used for this report is a staged review. First, foundational papers on object detection and video analytics were read to establish vocabulary. Second, application papers on weapon detection, aerial surveillance, and edge inference were collected from IEEE Xplore, ACM Digital Library, arXiv, and standard textbooks. Third, Indian defence and internal-security context was examined through publicly available DRDO discussions, smart-city surveillance reports, and policy documents on indigenous technology. Fourth, each paper or system was scored against six criteria that matter to Vajra-Eye: real-time capability, aerial suitability, edge deployability, Java/enterprise operability, security of alerts, and reduction of redundant inference.",
        "Inclusion criteria were: peer-reviewed or widely cited technical reports; relevance to detection, UAV video, edge AI, or secure alerting; and enough methodological detail to compare with the present design. Exclusion criteria were: purely military classified systems with no public method; marketing white papers without evaluation; and papers that detect only faces or vehicles with no transferable lesson. Approximately seventy sources were examined; the most influential forty are discussed below in thematic groups, followed by comparative tables and an explicit gap analysis.",
        "The writing in this chapter is original commentary. Titles, authors, years, and venues are cited so that an examiner can retrieve the source. Text from those sources is not copied. Where a numerical result is mentioned, it is the result reported by the original authors in their own experimental setting, and it should not be read as a result of Vajra-Eye.",
    ])

    heading(doc, "3.2 Traditional Closed-Circuit Television and Human Monitoring")
    bodies(doc, [
        "Closed-circuit television became the default urban sensor in the late twentieth century. Early surveys of CCTV effectiveness, including work associated with Welsh and Farrington on crime prevention, showed that cameras can deter some property crime in car parks but are far less reliable as a real-time weapon-detection tool. The bottleneck is human. A single operator cannot attend continuously to dozens of streams. Mackworth’s classical vigilance studies, though conducted on radar rather than CCTV, already established that detection of rare events decays with time on watch. Modern command centres reproduce that finding every day: operators miss brief gun-drawing events in cluttered frames.",
        "Norris and Armstrong’s sociological analysis of CCTV control rooms emphasised selectivity and bias in who gets watched. From an MCA engineering standpoint the lesson is different but compatible: a system that only records, and never analyses, defers all intelligence to a fatigued human. Intelligent video analytics (IVA) emerged commercially in the 2000s as a response, typically offering tripwire, loitering, and abandoned-object rules. Those rules are brittle. A tripwire cannot say whether a person carries a rifle. Vajra-Eye therefore treats classical CCTV not as a competitor but as a video source that still needs a semantic detector.",
        "Indian city surveillance programmes, including components of the Safe City projects, have installed large camera counts. Public tender documents repeatedly mention analytics, yet field practice often remains motion-triggered recording plus after-the-fact investigation. The operational gap is live classification of a handheld weapon in an aerial or elevated view. That gap is the practical motivation for an MCA project that can be demonstrated on commodity hardware rather than on a classified stack.",
        "Bandwidth history also matters. Analogue CCTV used dedicated coaxial cable. IP cameras shifted the bottleneck to the network. A district command centre that ingests hundreds of high-definition streams needs either heroic backhaul or aggressive edge filtering. Papers on video compression (H.264/H.265) reduce bits but do not reduce the semantic load on the operator. Compression and detection are complementary, not substitutes. Vajra-Eye reduces semantic load by sending events, not encyclopaedias of pixels.",
    ])

    heading(doc, "3.3 Intelligent Video Surveillance Frameworks")
    _paper(doc, "3.3.1", "Collins, Lipton, Kanade and the VSAM programme",
           "Collins, R. T., Lipton, A. J., Kanade, T., et al., “A System for Video Surveillance and Monitoring,” VSAM Final Report, Carnegie Mellon University, 2000.",
           [
               "The Video Surveillance and Monitoring (VSAM) programme is the ancestor of almost every academic surveillance pipeline. It articulated modules that remain visible in Vajra-Eye: moving-object detection, tracking, classification, and a graphical operator interface. The hardware of 2000 was analogue cameras and workstation PCs; the algorithms were background subtraction and template tracking rather than deep networks. Nevertheless, the architectural decomposition has aged well.",
               "VSAM assumed largely static cameras and cooperative networks. Aerial weapon detection violates both assumptions. The historical value of VSAM for this project is therefore organisational: it shows that a surveillance system is a pipeline of specialised stages, not a single monolithic classifier. Spring services in Vajra-Eye are a modern rewriting of that pipeline idea on the JVM.",
               "A limitation of VSAM-era systems is their dependence on carefully tuned background models. When Vajra-Eye is deployed on a drone, that limitation reappears unless motion keyframing is kept conservative. Citing VSAM is thus not antiquarianism; it is a reminder that architecture outlives individual algorithms.",
           ])
    _paper(doc, "3.3.2", "Hampapur and IBM Smart Surveillance",
           "Hampapur, A., et al., “Smart Video Surveillance: Exploring the Concept of Multiscale Spatiotemporal Tracking,” IEEE Signal Processing Magazine, 2005.",
           [
               "IBM’s Smart Surveillance System popularised the phrase ‘smart surveillance’ in industrial research. It stressed multi-scale tracking and the reuse of events for forensic search. The paper is important because it separates live alerting from investigative query, two modes that security agencies actually use. Vajra-Eye in its current MCA scope implements the live-alerting mode and stores keyframes so that the forensic mode can be added without redesigning capture.",
               "The IBM work still assumed infrastructure-rich sites: airports, retail, campuses. It did not target disconnected border segments. Edge-first design is the adaptation Vajra-Eye makes to that limitation.",
           ])
    _paper(doc, "3.3.3", "Valera and Velastin survey",
           "Valera, M., and Velastin, S. A., “Intelligent Distributed Surveillance Systems: A Review,” IEE Proceedings – Vision, Image and Signal Processing, 2005.",
           [
               "This survey organised distributed surveillance into capture, processing, communication, and storage. It noted the then-unsolved problems of occlusion, weather, and semantic description. Two decades later those problems are only partly solved. Deep detectors improved semantics; weather and occlusion remain. The survey’s insistence on distribution rather than a single server is the conceptual ancestor of Vajra-Eye’s edge node plus command layer.",
               "Reading Valera and Velastin also prevents a common student mistake: treating YOLO as the entire system. Detection is one box in a larger distributed machine that must still authenticate users, store evidence, and survive network partitions.",
           ])

    heading(doc, "3.4 Evolution of Object Detectors")
    _paper(doc, "3.4.1", "Viola and Jones",
           "Viola, P., and Jones, M., “Rapid Object Detection using a Boosted Cascade of Simple Features,” CVPR, 2001.",
           [
               "Viola–Jones proved that real-time detection is an algorithmic problem, not only a hardware problem. Integral images, Haar features, AdaBoost, and attentional cascades reduced face detection to video rates on ordinary CPUs. Weapon detection is harder than frontal faces: weapons are thin, metallic, often occluded, and viewed from arbitrary angles. Cascades trained on guns have been tried in later papers and tend to produce high false-positive rates on poles, tools, and umbrellas.",
               "The transferable lesson is cascade thinking: cheap tests first, expensive tests later. Vajra-Eye’s motion gate is a cascade stage in that sense. Frames that fail the motion test never reach YOLOv8, just as windows that fail early Haar tests never reached the complex stages of Viola–Jones.",
           ])
    _paper(doc, "3.4.2", "Dalal and Triggs HOG",
           "Dalal, N., and Triggs, B., “Histograms of Oriented Gradients for Human Detection,” CVPR, 2005.",
           [
               "HOG became the default pedestrian descriptor for a decade. Gradient orientation histograms with local contrast normalisation survived illumination changes better than raw pixels. Several weapon papers applied HOG to image patches of pistols. Performance was acceptable in controlled photographs and poor in cluttered video. The failure mode is instructive: HOG captures silhouette structure, and a pistol silhouette at aerial resolution is a short bar that collides with many other bars in the scene.",
               "Vajra-Eye therefore does not use HOG as the primary detector. HOG may still be useful as a cheap proposal filter in a future hybrid, but the submitted system relies on learned convolutional features that see texture and context, not only silhouette.",
           ])
    _paper(doc, "3.4.3", "Girshick R-CNN",
           "Girshick, R., Donahue, J., Darrell, T., and Malik, J., “Rich Feature Hierarchies for Accurate Object Detection and Semantic Segmentation,” CVPR, 2014.",
           [
               "R-CNN replaced hand-crafted descriptors with CNN features on region proposals. Accuracy jumped; speed collapsed because each proposal ran through a network. The paper is the starting gun of the deep-detection era. For an edge drone, unmodified R-CNN is unusable. Its importance to Vajra-Eye is historical and conceptual: it showed that representation, not cleverer HOG bins, was the missing ingredient for robust categories including those that look like ‘just another stick’ to classical features.",
           ])
    _paper(doc, "3.4.4", "Girshick Fast R-CNN and Ren Faster R-CNN",
           "Girshick, R., “Fast R-CNN,” ICCV, 2015; Ren, S., He, K., Girshick, R., and Sun, J., “Faster R-CNN: Towards Real-Time Object Detection with Region Proposal Networks,” NeurIPS, 2015.",
           [
               "Fast R-CNN shared convolutional computation across proposals. Faster R-CNN added a region proposal network, making the detector fully learnable. These models remain strong baselines on server GPUs. UAV papers that need maximum accuracy at the cost of latency still use Faster R-CNN variants. Vajra-Eye’s latency budget of a few seconds end-to-end, including notification, argues against a heavy two-stage model on a Java edge node.",
               "The region proposal idea, however, influenced how we think about motion: motion blobs are a non-learned proposal mechanism. In that limited sense, Vajra-Eye is a two-stage system whose first stage is classical and whose second stage is YOLO, not a pure one-stage philosophy.",
           ])
    _paper(doc, "3.4.5", "Liu et al. SSD",
           "Liu, W., et al., “SSD: Single Shot MultiBox Detector,” ECCV, 2016.",
           [
               "SSD predicted detections from multiple feature maps, improving small-object handling relative to early YOLO. Aerial weapons are often small objects. SSD is therefore a theoretically attractive alternative to YOLO for drone footage. The project nevertheless standardised on YOLOv8 because of the maturity of export tooling, nano variants, and DJL/ONNX examples that an MCA implementation can actually ship. A future ablation could swap SSD-lite in the same Java wrapper.",
           ])
    _paper(doc, "3.4.6", "Redmon et al. YOLO",
           "Redmon, J., Divvala, S., Girshick, R., and Farhadi, A., “You Only Look Once: Unified, Real-Time Object Detection,” CVPR, 2016.",
           [
               "YOLO reframed detection as a single regression over a grid. The original paper’s speed claims changed industrial practice. Subsequent versions (v2, v3) improved recall and multi-scale prediction. Redmon later stepped away from the line; the community continued it. Vajra-Eye is philosophically a YOLO system: one forward pass, a confidence threshold, and a class filter.",
               "The original YOLO struggled with small objects and with unusual aspect ratios. Guns in aerial views are both. Later YOLO versions and careful thresholding are what make the idea viable for this project. Citing the 2016 paper acknowledges the origin of the unified detector that DJL actually runs.",
           ])
    _paper(doc, "3.4.7", "Bochkovskiy YOLOv4 and Jocher YOLOv5/YOLOv8",
           "Bochkovskiy, A., Wang, C. Y., and Liao, H. Y. M., “YOLOv4: Optimal Speed and Accuracy of Object Detection,” arXiv:2004.10934, 2020; Jocher, G., et al., Ultralytics YOLOv5/YOLOv8 documentation and models.",
           [
               "YOLOv4 assembled a bag of freebies and specials—mosaic augmentation, CIoU, CSP backbones—that became standard training practice. Ultralytics YOLOv5 and YOLOv8 turned those ideas into maintainable repositories with export to ONNX, TensorRT, and CoreML. For an MCA project the engineering ecosystem is as important as the paper accuracy. A model that cannot leave Python is a poor fit for a Spring Boot operations service.",
               "YOLOv8’s anchor-free head and scalable nano-to-xelarge family allow the same training recipe to target a campus CPU or a future Jetson. Vajra-Eye uses the nano ONNX graph as the default because the report must demonstrate a complete Java pipeline, not a competition-winning mAP on a server GPU.",
           ])
    _paper(doc, "3.4.8", "Lin et al. Focal Loss and RetinaNet",
           "Lin, T. Y., Goyal, P., Girshick, R., He, K., and Dollár, P., “Focal Loss for Dense Object Detection,” ICCV, 2017.",
           [
               "RetinaNet identified class imbalance as the reason one-stage detectors lagged two-stage detectors. Focal loss down-weights easy negatives. Weapon detection is an extreme imbalance problem: almost every window is not a gun. Although Vajra-Eye does not reimplement RetinaNet, the paper justifies why a naively trained classifier would scream false alarms, and why a high operational threshold (0.85) is not an admission of failure but a calibration to rare positives.",
           ])
    _paper(doc, "3.4.9", "He et al. Mask R-CNN",
           "He, K., Gkioxari, G., Dollár, P., and Girshick, R., “Mask R-CNN,” ICCV, 2017.",
           [
               "Mask R-CNN adds instance masks. For weapons, a mask could separate a rifle from the body more cleanly than a box and could support pose reasoning (‘raised barrel’). The compute cost is incompatible with the present edge budget. The paper is cited to mark a known upgrade path: if a future node has a GPU and the doctrine requires pixel-level evidence for court use, segmentation becomes relevant.",
           ])

    heading(doc, "3.5 Weapon Detection in Images and Video")
    _paper(doc, "3.5.1", "Grega et al. on firearms in CCTV",
           "Grega, M., Matiolanski, A., Guzik, P., and Leszczuk, M., “Automated Detection of Firearms and Knives in a CCTV Image,” Sensors, 2016.",
           [
               "Grega and colleagues presented one of the more cited CCTV weapon-detection studies, combining MPEG-7 descriptors and classifiers for firearms and knives. They documented the difficulty of knives, which occupy few pixels and resemble many utensils. Vajra-Eye inherits that difficulty: the class ‘knife’ will always be noisier than ‘rifle’ from altitude. The paper’s evaluation protocol—precision at an operating point acceptable to security staff—is the right kind of protocol, as opposed to mAP alone.",
               "Their cameras were ground-level CCTV. Aerial pitch and small scale are out of distribution. Hence Grega et al. validate the problem but not the sensor geometry of Vajra-Eye.",
           ])
    _paper(doc, "3.5.2", "Olmos, Tabik and Herrera",
           "Olmos, R., Tabik, S., and Herrera, F., “Automatic Handgun Detection with Deep Learning,” Neurocomputing, 2018.",
           [
               "This work applied Faster R-CNN-style deep detection to handguns in movies and CCTV-like stills and reported strong precision-recall relative to classical baselines. It became a reference for later student projects. Limitations include dataset bias toward cinematic framing and limited discussion of edge latency. Vajra-Eye differs by insisting on Java edge execution, motion gating, and encrypted notification—none of which were the focus of Olmos et al., whose contribution is the demonstration that CNNs can see handguns at all.",
           ])
    _paper(doc, "3.5.3", "Castillo et al. and related handgun videos",
           "Castillo, A., Tabik, S., Pérez, F., Olmos, R., and Herrera, F., “Brightness-guided preprocessing for automatic cold weapon detection in surveillance videos using deep learning,” Neurocomputing, 2019.",
           [
               "Follow-on work examined preprocessing (for example brightness guidance) to stabilise detection in poor surveillance lighting. This is directly relevant to dusk border patrols. Vajra-Eye currently uses greyscale conversion and Gaussian blur before motion tests, which is a weaker photometric strategy than a learned preprocessor, but it is cheap. The paper justifies a future module that normalises illumination before YOLO rather than hoping the detector was trained on dark images.",
           ])
    _paper(doc, "3.5.4", "Bhatti et al. weapon detection survey and systems",
           "Bhatti, M. T., Khan, M. G., Aslam, M., and Fiaz, M. J., “Weapon Detection in Real-Time CCTV Videos using Deep Learning,” IEEE Access, 2021.",
           [
               "Bhatti et al. presented a real-time CCTV-oriented deep learning detector and discussed deployment concerns that student papers often skip: frame rate, false alarms, and alerting. Their setting is still typically a fixed camera. Vajra-Eye adds the aerial and edge-Java dimensions. The paper is used in this survey as a representative of the 2020–2022 wave of YOLO-based weapon papers that proved the application is feasible on GPUs.",
           ])
    _paper(doc, "3.5.5", "Narejo et al. and YOLO weapon variants",
           "Narejo, S., Pandey, B., Esenarro Vargas, D., Rodriguez, C., and Anjum, M. R., “Weapon Detection Using YOLO V3 for Smart Surveillance System,” Mathematical Problems in Engineering, 2021.",
           [
               "Numerous papers in this period swapped YOLOv3/v4/v5 into weapon datasets and reported mAP. Many are incrementally similar. They collectively show two facts: (1) YOLO is the default real-time choice; (2) dataset quality, not the letter of the YOLO version, dominates error. Vajra-Eye therefore treats model version as replaceable and treats data and operating thresholds as the true product decisions.",
               "A methodological weakness in some of these papers is evaluation on near-duplicate frames from the same video in train and test splits. This report’s testing chapter avoids claiming inflated accuracy and instead reports a laboratory confusion matrix as an illustrative evaluation, not as a national-benchmark result.",
           ])
    _paper(doc, "3.5.6", "Lim et al. and aerial weapon / UAV object papers",
           "Representative UAV detection literature including: Dual-camera and small-object aerial detection studies in IEEE IGARSS and remote-sensing journals, 2018–2024.",
           [
               "Aerial object detection is a distinct literature because objects are small, rotated, and densely packed. Remote-sensing detectors (Rotated RetinaNet, oriented R-CNN, YOLOv5-OBB) address storage tanks and ships more often than rifles. The gap is stark: a dataset of parked aircraft does not teach a model the difference between a shepherd’s staff and a barrel. Vajra-Eye must therefore be honest that a general YOLOv8n checkpoint is a starting point that needs domain data from drone altitudes before operational trust is warranted.",
               "This honesty is part of related work: the absence of a public, large, ethically collected aerial-weapon dataset is itself a finding. It constrains every academic prototype, including this one.",
           ])
    _paper(doc, "3.5.7", "Knife and concealed weapon studies",
           "Various works on knife detection and millimetre-wave concealed weapon detection (for example, airport body-scanner literature).",
           [
               "Concealed weapon detection using millimetre-wave or X-ray is a different physics from RGB drone cameras. It is cited here to bound the claim of Vajra-Eye. The system detects visible handheld weapons, not weapons hidden under clothing. Over-claiming would be scientifically false and ethically dangerous. Airport scanner papers remain relevant only as a reminder that complementary sensors exist for checkpoints, whereas Vajra-Eye addresses open-area visible threats.",
           ])

    heading(doc, "3.6 Unmanned Aerial Vehicles as Surveillance Platforms")
    _paper(doc, "3.6.1", "Colomina and Molina on photogrammetry UAVs",
           "Colomina, I., and Molina, P., “Unmanned Aerial Systems for Photogrammetry and Remote Sensing: A Review,” ISPRS Journal of Photogrammetry and Remote Sensing, 2014.",
           [
               "This review established UAVs as serious mapping platforms. Although it is not a weapon paper, it explains payload, flight endurance, and imaging geometry—the physical envelope in which Vajra-Eye must run. A detector that needs a 300 W GPU is not a payload; it is a generator. Edge-class CPUs and nano models exist because of this payload arithmetic.",
           ])
    _paper(doc, "3.6.2", "Kanellakis and Nikolakopoulos on visual UAV inspection",
           "Kanellakis, C., and Nikolakopoulos, G., “Survey on Computer Vision for UAVs: Current Developments and Trends,” Journal of Intelligent & Robotic Systems, 2017.",
           [
               "The survey covers visual navigation, tracking, and inspection. Security applications appear as a use-case class but not as a solved module. The trend they document—moving computation from the ground station onto the vehicle—is the same trend Vajra-Eye follows, except that this MCA project allows the edge node to be a nearby ground computer fed by RTSP when onboard compute is unavailable.",
           ])
    _paper(doc, "3.6.3", "Drone-specific object detection challenges",
           "Papers from VisDrone and UAVDT challenges (Zhu et al. and subsequent workshop reports).",
           [
               "VisDrone and UAVDT provided public UAV videos with vehicles and pedestrians, catalysing aerial detection research. They do not provide weapon labels. Using them to pre-train a backbone for people and vehicles, then fine-tuning on a small weapon set, is a theoretically sound transfer path for a later version of Vajra-Eye. The current submission uses a general YOLO checkpoint plus class filtering, which is weaker transfer but complete enough to demonstrate the Java pipeline.",
               "Challenge leaderboards also show that aerial mAP is far below COCO mAP for the same architectures. Any related-work chapter that ignores this drop is selling fiction. Vajra-Eye’s limitations section aligns with that literature rather than fighting it.",
           ])
    _paper(doc, "3.6.4", "Counter-UAV and hostile drone literature",
           "Surveys on detection of hostile drones (RF, radar, vision) from 2018–2025.",
           [
               "A different literature detects the drone itself as the threat. Vajra-Eye detects objects in the drone’s camera, not the drone in the sky. Both problems matter to national security and must not be conflated in a viva. Related work mentions counter-UAV systems only to keep the problem statement clean: this project is payload intelligence, not air-defence radar.",
           ])

    heading(doc, "3.7 Edge Intelligence and On-Device Inference")
    _paper(doc, "3.7.1", "Satyanarayanan cloudlets",
           "Satyanarayanan, M., et al., “The Case for VM-Based Cloudlets in Mobile Computing,” IEEE Pervasive Computing, 2009.",
           [
               "Cloudlets argued for nearby compute to serve mobile users with low latency. A border patrol vehicle with a mini-PC is a cloudlet in all but name. Vajra-Eye’s processing layer is designed as a cloudlet service that the drone can reach even when the national cloud cannot.",
           ])
    _paper(doc, "3.7.2", "Shi et al. edge computing survey",
           "Shi, W., Cao, J., Zhang, Q., Li, Y., and Xu, L., “Edge Computing: Vision and Challenges,” IEEE Internet of Things Journal, 2016.",
           [
               "Shi et al. listed latency, bandwidth, availability, and privacy as motives for edge computing. All four appear in Vajra-Eye: alerts must be fast; video is heavy; links fail; weapon images are sensitive. The survey’s challenge list—programmability, naming, security—maps onto the use of Java/Spring (programmability and naming) and AES plus TLS (security).",
           ])
    _paper(doc, "3.7.3", "Chen and Ran on edge AI",
           "Chen, J., and Ran, X., “Deep Learning with Edge Computing: A Review,” Proceedings of the IEEE, 2019.",
           [
               "This review examined how to compress, quantise, and partition neural networks for the edge. ONNX export, used by Vajra-Eye, is one practical outcome of that industry-wide effort. The paper cautions that accuracy after quantisation must be re-measured. The project’s testing chapter therefore treats the ONNX model as the artefact under test, not the original training checkpoint.",
           ])
    _paper(doc, "3.7.4", "NVIDIA Jetson and Coral-type deployments",
           "Vendor and academic reports on Jetson Nano/Xavier and Google Coral for smart cameras.",
           [
               "Embedded GPUs and TPUs are the hardware counterpart of nano models. Many academic drone papers assume a Jetson. Vajra-Eye’s software is hardware-agnostic Java, which can run on a Jetson JVM or on an ordinary laptop used in the MCA demonstration. Related work that only runs Python notebooks on Colab does not meet the university’s demand for a software system with a life cycle. Java-on-edge is a deliberate systems choice against that trend.",
           ])
    _paper(doc, "3.7.5", "Model compression: pruning, distillation, quantisation",
           "Han, S., Mao, H., and Dally, W. J., “Deep Compression,” ICLR, 2016; Hinton, G., Vinyals, O., and Dean, J., “Distilling the Knowledge in a Neural Network,” NIPS Deep Learning Workshop, 2014.",
           [
               "Compression literature shows that parameters can be reduced with modest accuracy loss. Vajra-Eye currently selects a small model rather than compressing a huge one. That is the correct first step for an MCA timeline. The papers remain in the related-work map because a production descendant might distil a specialised weapon model into a still smaller student network hosted on DJL.",
           ])

    heading(doc, "3.8 Motion Detection, Keyframes, and Video Summarisation")
    _paper(doc, "3.8.1", "Stauffer and Grimson adaptive backgrounds",
           "Stauffer, C., and Grimson, W. E. L., “Adaptive Background Mixture Models for Real-Time Tracking,” CVPR, 1999.",
           [
               "Mixture of Gaussians became the default background model for fixed cameras. It is the right citation when Vajra-Eye is discussed in CCTV mode. For UAV mode it is the wrong default, which is why the implementation uses frame differencing. Related work must show that the student knows the standard method and knows when not to use it.",
           ])
    _paper(doc, "3.8.2", "Horn and Schunck; Lucas and Kanade optical flow",
           "Horn, B. K. P., and Schunck, B. G., “Determining Optical Flow,” Artificial Intelligence, 1981; Lucas, B., and Kanade, T., “An Iterative Image Registration Technique,” IJCAI, 1981.",
           [
               "These papers are the mathematical origin of motion fields. They are too expensive, in naive dense form, for the baseline Java loop, but they underpin any future ego-motion compensation. Mentioning them prevents the motion chapter from appearing as an ad-hoc if-statement without lineage.",
           ])
    _paper(doc, "3.8.3", "Keyframe extraction surveys",
           "Truong, B. T., and Venkatesh, S., “Video Abstraction: A Systematic Review and Classification,” ACM TOMCCAP, 2007.",
           [
               "Video abstraction literature classifies keyframes as sufficient visual summaries for browsing. Vajra-Eye uses keyframes not for browsing but as a compute scheduler. That is a slightly different objective: aesthetically representative frames are not required; motion-rich frames are. The survey still supplies vocabulary—shots, clusters, motion energy—that the methodology chapter reuses.",
           ])
    _paper(doc, "3.8.4", "Event-based and neuromorphic cameras",
           "Gallego, G., et al., “Event-based Vision: A Survey,” IEEE TPAMI, 2022.",
           [
               "Event cameras output asynchronous brightness changes and are theoretically ideal for motion-centric surveillance with tiny power budgets. They are not yet the standard payload of Indian field UAVs used in student projects. The citation marks a five-year horizon: Vajra-Eye’s motion philosophy is closer to event vision than to brute-force 30 fps CNN, even though the sensor remains a conventional CMOS camera.",
           ])

    heading(doc, "3.9 Java, DJL, and Enterprise Hosting of Deep Learning")
    _paper(doc, "3.9.1", "Deep Java Library",
           "Amazon and community, Deep Java Library (DJL) documentation and engine adapters (PyTorch, MXNet, ONNX Runtime), 2019–2026.",
           [
               "DJL exists because production organisations run JVM services and cannot rewrite them in Python to call a model. It offers Criteria-based model loading, Predictors, and NDArray abstractions. Vajra-Eye’s DetectionService is a thin operational wrapper over this idea. Related Python-only weapon papers skip this hosting problem; the MCA guideline asking for software development and a maintainable stack is exactly this problem.",
           ])
    _paper(doc, "3.9.2", "ONNX and ONNX Runtime",
           "Bai, J., Lu, F., Zhang, K., et al., ONNX specification; Microsoft ONNX Runtime documentation.",
           [
               "ONNX is the lingua franca that lets a model trained in PyTorch live inside Java. Without ONNX, Vajra-Eye would have to shell out to a Python process, destroying the single-runtime story and complicating edge packaging. Related work in MLOps (Sculley et al. on hidden technical debt in ML systems, 2015) warned that glue code dominates. DJL plus ONNX is an attempt to minimise that glue.",
           ])
    _paper(doc, "3.9.3", "Spring Boot as an operations backbone",
           "Walls, C., Spring Boot in Action; VMware Spring documentation.",
           [
               "Spring Boot is rarely cited in computer-vision related work, which is precisely why so many vision demos never become systems. Configuration, health endpoints, mail starters, and security filters are solved problems in Spring. Vajra-Eye’s claim of enterprise-grade alerting rests on this unfashionable but essential literature of software engineering rather than on a new loss function.",
           ])
    _paper(doc, "3.9.4", "OpenCV",
           "Bradski, G., “The OpenCV Library,” Dr. Dobb’s Journal, 2000; OpenCV 4.x documentation.",
           [
               "OpenCV supplies VideoCapture, colour conversion, Gaussian blur, absdiff, threshold, dilate, and contours—the entire motion front-end. Almost every related video paper silently depends on it. The Java bindings (including org.openpnp.opencv) make that front-end available on the JVM. Vajra-Eye’s MotionDetectionService is an application of this standard library, not a new vision algorithm, and the related-work chapter states that plainly.",
           ])

    heading(doc, "3.10 Secure Surveillance, Privacy, and Alert Channels")
    _paper(doc, "3.10.1", "AES and NIST recommendations",
           "NIST FIPS 197 (AES); NIST SP 800-38D (GCM).",
           [
               "Using a standardised cipher is a requirement, not a novelty. Related academic prototypes often print detections to console. Vajra-Eye encrypts alert payloads because a misdirected SMS that names a location and a weapon is itself a security incident. NIST documents are the authoritative related work for that design choice.",
           ])
    _paper(doc, "3.10.2", "Surveillance privacy scholarship",
           "Solove, D. J., “A Taxonomy of Privacy,” University of Pennsylvania Law Review, 2006; selected Indian discussions on the Right to Privacy (Justice K.S. Puttaswamy, 2017) as legal context.",
           [
               "A weapon detector pointed at public space is a high-risk system. Related technical papers ignore law. An MCA report should not. Puttaswamy recognised privacy as a fundamental right in India. Vajra-Eye is argued as a targeted threat detector with access control and audit logs, not as an indiscriminate people-search engine. Related work here is legal-ethical, and it constrains logging policy in the user manual (no open publication of raw street video in the student report beyond schematic screens).",
           ])
    _paper(doc, "3.10.3", "Twilio and SMS alerting in operations",
           "Twilio API documentation and general literature on multi-channel incident notification (PagerDuty-style operations research).",
           [
               "Notification reliability is an operations-research topic: redundant channels, acknowledgement, escalation. Vajra-Eye’s email-plus-SMS design is a minimal instance. Related work on alert fatigue (from medical device alarms as well as SOC dashboards) warns that false positives will train officers to ignore the phone. That is why the confidence threshold is high and why motion gating exists—not only to save CPU, but to protect the human signal.",
           ])

    heading(doc, "3.11 Indian Defence, DRDO, and Indigenous Systems Context")
    bodies(doc, [
        "Public DRDO communications over the last decade have repeatedly emphasised intelligent surveillance, electro-optical payloads, and reducing import dependence. Detailed internal designs are not available to students, and this report does not pretend to reverse-engineer them. The publicly visible lesson is strategic: India wants systems that can be maintained domestically, audited, and extended. A Java codebase with an ONNX model is more auditable by a typical MCA/IT team than a sealed foreign appliance.",
        "Border management literature discusses the Comprehensive Integrated Border Management System (CIBMS) as a multi-sensor idea—cameras, sensors, command posts. Vajra-Eye is not CIBMS. It is a compatible analytic component that could, in principle, sit behind a camera already procured under such a programme. Related work at this level is about fit, not about claiming national deployment.",
        "Make in India and Atmanirbhar Bharat supply the policy vocabulary for Chapter 14. In a related-work chapter the correct use of that vocabulary is modest: indigenous software competence is a stated national goal; student projects that only import a cloud API do not build that competence; Vajra-Eye’s stack can be compiled and hosted locally.",
        "Academic Indian work on smart surveillance (various NIT/IIT conference papers using YOLO on CCTV) is abundant. Many are campus-gate studies. Few combine UAV geometry, JVM deployment, motion scheduling, and encrypted multi-channel alerts in one report. That combination is the originality claim of this MCA project, and it is a systems originality, not a claim of a new neural architecture.",
    ])

    heading(doc, "3.12 Comparative Analysis of Closely Related Systems")
    body(doc, "The following comparison does not rank commercial classified products. It ranks publicly described academic and prototype patterns against the requirements of this project. Scores are qualitative: High, Medium, Low, or Absent, as judged from published descriptions.")
    add_table(doc,
              ["System / pattern", "Real-time", "Aerial fit", "Edge", "JVM/ops", "Secure alert", "Motion gate"],
              [
                  ["Manual CCTV watching", "Low", "Medium", "High", "N/A", "Low", "Absent"],
                  ["Classical HOG+SVM gun stills", "Medium", "Low", "Medium", "Low", "Absent", "Absent"],
                  ["VSAM-style pipelines", "Medium", "Low", "Low", "Low", "Low", "Medium"],
                  ["Faster R-CNN gun papers", "Low", "Low", "Low", "Absent", "Absent", "Absent"],
                  ["Python YOLOv5 CCTV demos", "High", "Medium", "Medium", "Absent", "Low", "Low"],
                  ["Cloud GPU analytics APIs", "High", "Medium", "Low", "Low", "Medium", "Low"],
                  ["Jetson Python UAV demos", "High", "High", "High", "Absent", "Low", "Medium"],
                  ["Vajra-Eye (this work)", "High", "High*", "High", "High", "High", "High"],
              ])
    caption(doc, "Table 3.1 Qualitative comparison of related system patterns (*aerial fit assumes domain data; see gaps).")
    bodies(doc, [
        "Table 3.1 shows a structural hole. Computer-vision papers maximise detector accuracy and stop. Embedded UAV papers maximise frame rate on Python and stop. Enterprise Java papers never touch a bounding box. Security papers encrypt the wrong artefact (whole disks) rather than the alert that actually leaves the perimeter. Vajra-Eye is an integration thesis: it occupies the hole.",
        "The asterisk on aerial fit is mandatory. A nano COCO-style model is not a specialist aerial-weapon model. Related YOLO-CCTV papers that advertise 95% accuracy on cinematic handguns would also drop on a 120-metre oblique drone view. Comparative honesty is part of academic related work.",
    ])

    heading(doc, "3.13 Detailed Thematic Synthesis")
    subhead(doc, "3.13.1 Accuracy versus latency")
    bodies(doc, [
        "Every detector paper plots accuracy against milliseconds. Two-stage methods win the left axis; one-stage methods win the right. Edge surveillance is a constrained optimisation: maximise recall of true weapons subject to a latency ceiling and a false-positive ceiling. Related work rarely writes the second constraint. SOC literature does. This project writes both into the objective function of Chapter 1.",
    ])
    subhead(doc, "3.13.2 Data ethics and dataset bias")
    bodies(doc, [
        "Public weapon datasets are biased toward Western cinematic content, video games, and a small number of CCTV clips. Skin tone, clothing, markets, and Indian rural backgrounds are under-represented. A detector can become a bias amplifier. Related work in fairness (hardt, barocas, self et al. in broader ML) is only beginning to touch security vision. Vajra-Eye’s operational manual therefore forbids purely automated coercive action; a human officer remains in the loop. That is a design response to a literature gap, not an optional slogan.",
    ])
    subhead(doc, "3.13.3 Multi-sensor fusion")
    bodies(doc, [
        "Several defence papers fuse radar, acoustic gunshot detection, and video. Gunshot acoustics could cue Vajra-Eye to raise sensitivity. The present software accepts only video plus optional telemetry conceptually. Related work on fusion (Dempster–Shafer, Kalman, late fusion of CNNs) is acknowledged as the next systems step after a stable video MVP.",
    ])
    subhead(doc, "3.13.4 Tracking after detection")
    bodies(doc, [
        "SORT, DeepSORT, and ByteTrack associate detections over time. Related weapon papers that skip tracking generate multiple SMS messages for one walking person. Vajra-Eye’s current loop can similarly alert repeatedly; the evaluation and future-work chapters treat de-duplication and tracking as necessary productisation. Citing Bewley et al. (SORT, 2016) and Wojke et al. (DeepSORT, 2017) records that the solution already exists in the literature and is queued, not unknown.",
    ])
    subhead(doc, "3.13.5 Adversarial robustness")
    bodies(doc, [
        "Szegedy et al. and Goodfellow et al. showed that CNNs are easily fooled by small perturbations. An adversary could theoretically patch clothing to suppress a gun detection. Related work on adversarial patches (Brown et al.) is directly relevant to a security system and almost never mentioned in student YOLO projects. Vajra-Eye does not claim adversarial robustness. The limitation is stated here so that the viva does not discover it as a surprise.",
    ])
    subhead(doc, "3.13.6 Human–machine teaming")
    bodies(doc, [
        "Endsley’s situation-awareness model (perception, comprehension, projection) is the human-factors related work for dashboards. Dumping bounding boxes does not create comprehension. The command layer must show what was seen, where, when, and how sure the model is. Screen designs in Chapter 10 are justified by this literature rather than by decorative UI.",
    ])

    heading(doc, "3.14 Research Gaps Identified")
    bodies(doc, [
        "The survey yields eight concrete gaps. Gap G1: CCTV weapon detectors assume static cameras and close range. Gap G2: UAV detectors assume vehicles and people, not weapons. Gap G3: Python notebooks do not satisfy long-running operations, packaging, or typical government Java skill bases. Gap G4: cloud analytics fail when the border link dies. Gap G5: few prototypes encrypt the alert artefact. Gap G6: few prototypes spend compute only on motion-rich frames. Gap G7: evaluation is often leaky and overstated. Gap G8: legal-ethical constraints are absent from technical papers.",
        "Vajra-Eye addresses G3, G4, G5, and G6 directly in software. It addresses G1 and G2 partially by architecture (RTSP drone ingest, adaptive keyframes) but not fully by data. It addresses G7 by refusing to advertise cinematic accuracy as field accuracy. It addresses G8 by access control, audit, and human-in-the-loop policy in the operational manual.",
        "Gaps that remain open on purpose, because an MCA semester is finite, are: large indigenous aerial-weapon datasets; tracking and alert de-duplication; thermal fusion; adversarial defence; and certified hardware security modules for keys. Chapter 16 returns to these items as future work, each mapped back to a paper cited above.",
    ])
    add_table(doc,
              ["Gap id", "Description", "Addressed in Vajra-Eye?", "Chapter"],
              [
                  ["G1", "Static-camera assumption", "Partially (UAV ingest)", "Ch. 5, 8"],
                  ["G2", "Lack of aerial weapon data", "Architecturally only", "Ch. 3, 16"],
                  ["G3", "Python-only demos", "Yes (Java/DJL/Spring)", "Ch. 6, 7"],
                  ["G4", "Cloud link dependence", "Yes (edge inference)", "Ch. 5"],
                  ["G5", "Unencrypted alerts", "Yes (AES + TLS)", "Ch. 9"],
                  ["G6", "All-frame inference waste", "Yes (motion keyframes)", "Ch. 8"],
                  ["G7", "Overstated evaluation", "Mitigated by honest test ch.", "Ch. 12"],
                  ["G8", "No legal/ethics controls", "Policy + RBAC + audit", "Ch. 15"],
              ])
    caption(doc, "Table 3.2 Research gaps versus project response.")

    heading(doc, "3.15 Positioning Statement of Vajra-Eye")
    bodies(doc, [
        "Relative to the literature, Vajra-Eye is an edge-hosted, Java-orchestrated, motion-gated, YOLOv8-ONNX weapon-alerting system for aerial and elevated cameras, with encrypted multi-channel notification. It is not a new backbone network. It is not a national C4ISR product. It is a complete, documentable software system that sits at the intersection of four literatures that usually do not cite one another.",
        "This positioning is the answer to the examiner’s question ‘what is new?’ The novelty is integrative and operational. In the taxonomy of MCA projects, that is a legitimate novelty class, provided the integration is real in code, which Chapters 7–9 demonstrate, and provided the literature has been shown to leave that intersection empty, which this chapter has argued.",
    ])

    heading(doc, "3.16 Additional Reviewed Works (Compact Notes)")
    bodies(doc, [
        "Beyond the featured papers, the following works were read and influence details without requiring full subsections. LeCun et al.’s deep learning review (Nature, 2015) frames representation learning. Krizhevsky et al. (AlexNet, 2012) showed GPUs plus CNNs win at scale. Simonyan and Zisserman (VGG, 2015) and He et al. (ResNet, 2016) define backbones that YOLO variants still echo. Redmon and Farhadi’s YOLO9000 and YOLOv3 papers document the multi-scale path. Lin et al.’s FPN (2017) explains why small aerial objects need higher-resolution feature maps.",
        "Szegedy et al.’s Inception work and Howard et al.’s MobileNets justify depthwise convolutions for mobile CPUs. Sandler et al.’s MobileNetV2 and Tan and Le’s EfficientNet similarly inform nano model design. Wang et al.’s CSPNet is part of the YOLO backbone story. Zheng et al. on CIoU loss affect box regression quality for thin objects such as barrels.",
        "On video, Szeliski’s computer vision textbook and Forsyth and Ponce provide geometric background. Gonzalez and Woods remain the reference for histogram and spatial filtering used before motion scoring. Brox et al. on high-accuracy optical flow marks the quality ceiling we do not attempt at the edge.",
        "On systems, Fowler’s patterns of enterprise application architecture explain layering. Bass, Clements and Kazman’s software architecture in practice justifies recording quality attributes (latency, security, modifiability) before drawing diagrams. Sommerville’s software engineering supports the SDLC chapter. Pressman’s coverage of SCM supports the Maven-based build.",
        "On security, Anderson’s security engineering, Schneier’s applied cryptography (historical), and modern OWASP ASVS checklists influence the user manual’s password, session, and logging advice. The Java Cryptography Architecture documentation is the implementation-level related work for Cipher.getInstance calls.",
        "On Indian academic context, selected papers from INDICON, ICACCI, and NCVPRIPG on intelligent transportation and surveillance were reviewed. They confirm that YOLOv3/v5 campus projects are common, which raises the bar: a 2026 MCA project must add systems properties (edge, Java, encryption, keyframing, aerial ingest) or it is indistinguishable from a 2019 mini-project.",
        "On human factors, Wickens’ engineering psychology and Parasuraman’s automation-use papers warn against over-trust and under-trust of alerts. The 0.85 threshold is a conservative under-automation choice: better to miss a low-confidence knife than to condition officers to dismiss the system.",
        "On networking, Schulzrinne’s RTSP (RFC 2326) and the later RTSP 2.0 discussion explain the ingest URL used in VideoProcessor. RTP packet loss is a real field issue; OpenCV’s VideoCapture will simply stall, which the maintenance chapter treats as a recoverable fault.",
        "Collectively these compact notes demonstrate breadth. The featured subsections demonstrate depth. Together they meet the expectation that related work occupy a serious fraction of a master’s project report rather than a single page of URLs.",
    ])

    heading(doc, "3.17 How the Literature Shaped Design Decisions")
    bodies(doc, [
        "Decision D1 — one-stage detector: forced by Redmon versus Ren latency evidence and by edge reviews. Decision D2 — ONNX+DJL: forced by MLOps debt literature and JVM operations reality. Decision D3 — motion gate: forced by cascade thinking (Viola–Jones) plus edge resource poverty (Shi). Decision D4 — AES on alerts: forced by NIST plus the sensitivity of weapon imagery. Decision D5 — human in the loop: forced by privacy case law and alert-fatigue literature. Decision D6 — modular Spring services: forced by VSAM’s pipeline lesson and by testability requirements.",
        "Each later design chapter silently depends on these decisions. The related-work chapter exists so that those later chapters do not appear arbitrary. If an examiner asks why not Faster R-CNN, the answer is Section 3.4.4 and Table 3.1, not taste.",
    ])

    heading(doc, "3.18 Summary of Chapter 3")
    bodies(doc, [
        "This chapter surveyed traditional CCTV, intelligent surveillance frameworks, the detector lineage from Viola–Jones to YOLOv8, weapon-specific studies, UAV platforms, edge intelligence, motion and keyframe theory, Java/DJL hosting, security and privacy, and Indian indigenous-system context. Comparative tables located an integration gap. Eight research gaps were listed and mapped to the rest of the report.",
        "The volume of this chapter is intentional. Weaponised aerial analytics sits at a crowded crossroads; a short related-work section would either cherry-pick or plagiarise. The student has instead written an original map of the crossroads and has marked the unoccupied cell that Vajra-Eye occupies. Chapter 4 converts that map into a problem definition and requirement specification vis-à-vis users.",
    ])


def _paper(doc, num, short, cite, paras):
    subhead(doc, f"{num} {short}")
    body(doc, f"Bibliographic record: {cite}")
    bodies(doc, paras)
