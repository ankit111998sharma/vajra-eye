"""Fault-tolerant edge implementation chapter (production hardening)."""
from report_styles import chapter, heading, subhead, body, bodies, bullets, add_table, caption, add_code_lines, add_figure


def write_resilience(doc):
    chapter(doc, "CHAPTER 8A")
    body(doc, "FAULT-TOLERANT EDGE IMPLEMENTATION AND GLITCH PREVENTION", indent=False)
    heading(doc, "8A.1 Purpose of this Chapter")
    bodies(doc, [
        "Chapter 8 states the motion-keyframing mathematics. This chapter states how that mathematics is hosted on a JVM that must run for hours on a companion computer without leaking native memory, stalling RTSP, or flooding SMS. The patterns are: RAII for Mats, DJL sub-managers, a bounded drop-oldest frame queue, gimbal-jitter suppression, exponential-backoff reconnect, ONNX execution-provider options, alert debounce, and G1GC flags.",
        "Without these controls the conceptual framework of Chapter 2 remains a laboratory screenshot. With them, Vajra-Eye becomes an enterprise-shaped prototype: still not a certified product, but no longer a single-thread demo that dies when the radio blips.",
    ])

    heading(doc, "8A.2 Eliminating Off-Heap Native Memory Leaks")
    bodies(doc, [
        "A primary cause of fatal OutOfMemoryError in long-running Java vision systems is off-heap native exhaustion. The JVM garbage collector tracks Java object references; the pixel matrices (cv::Mat) and ONNX tensors live in C++ heaps. finalize() is too late and too unreliable. Every intermediate Mat is opened inside NativeScope or a try/finally that calls release(). DJL work uses a nested NDManager that closes on exit.",
    ])
    add_code_lines(doc, """public final class NativeScope {
    private NativeScope() {}
    public static void usingMat(Consumer<Mat> block) {
        Mat mat = new Mat();
        try {
            block.accept(mat);
        } finally {
            mat.release();
        }
    }
}""")
    caption(doc, "Listing 8A.1: RAII wrapper for OpenCV Mat (excerpt).")
    add_code_lines(doc, """try (NDManager sub = model.getNDManager().newSubManager()) {
    // tensor transforms bound to sub; reclaimed on close
}""")
    caption(doc, "Listing 8A.2: DJL sub-manager scope for intermediate tensors.")
    body(doc, "The VideoProcessor never stores a Mat in a list ‘for later’ without a matching release. The bounded queue that does hold Mats is obliged to release the dropped frame when it evicts under backpressure. That obligation is the difference between a queue and a leak.")

    heading(doc, "8A.3 Multi-Thread Decoupling and Queue Backpressure")
    bodies(doc, [
        "Capture, motion, inference, and notify must not share one thread. If SMS dispatch waits on a cellular round-trip, a single-thread reader hangs, the OS socket buffer fills, and the RTSP session dies in a way that looks like an ‘OpenCV bug’. The production topology is:",
    ])
    add_code_lines(doc, """[RTSP Capture Thread]
        |
        v
(Bounded ArrayBlockingQueue, capacity 3-5, drop-oldest)
        |
        v
[Motion / AI worker]
        |
        v
[Alert worker / executor]""")
    caption(doc, "Figure 8A.1: Thread topology with drop-oldest backpressure.")
    add_code_lines(doc, """private final BlockingQueue<Mat> buffer = new ArrayBlockingQueue<>(5);

public boolean pushFrame(Mat frame) {
    if (!buffer.offer(frame)) {
        Mat dropped = buffer.poll();
        if (dropped != null) dropped.release();
        return buffer.offer(frame);
    }
    return true;
}""")
    caption(doc, "Listing 8A.3: Bounded frame buffer with leak-safe drop-oldest.")
    body(doc, "Capacity is kept tiny (3 to 5) so that the pipeline prefers a fresh frame to a long queue of stale history. OpenCV CAP_PROP_BUFFERSIZE is set to 1 for the same reason on the capture side.")

    heading(doc, "8A.4 Drone Motion Glitch Filtering")
    bodies(doc, [
        "Wind gusts and gimbal pans move almost every pixel. Temporal differencing then reports ‘massive motion’ and YOLO is invoked on every frame—the opposite of Chapter 2. An upper bound on total contour area distinguishes ego-motion from a weapon-sized blob. If more than 60% of the frame moves, the event is classified as panning, the baseline is allowed to reset, and inference is skipped.",
    ])
    add_code_lines(doc, """boolean exceedsMinimum = totalMotionArea >= minArea;
boolean isDronePanning = totalMotionArea > (frameArea * 0.60);
if (isDronePanning) {
    resetBaseline();
    return false;
}
return exceedsMinimum;""")
    caption(doc, "Listing 8A.4: Dual threshold — noise floor and pan ceiling.")
    add_figure(doc, "motion_keyframe.png", "Figure 8A.2: Keyframe peaks remain local; a full-frame pan would saturate the score and is rejected.")

    heading(doc, "8A.5 RTSP Reconnection and Network Self-Healing")
    bodies(doc, [
        "Drone RTSP links drop because of RF attenuation, interference, and power cycles. The capture loop must reconnect with exponential backoff, without tearing down the Spring context. After a successful reopen, the motion baseline is flushed so that the first new frame is not differenced against a previous landscape.",
    ])
    add_code_lines(doc, """if (!capture.isOpened()) {
    long backoff = Math.min(10000, 1000L * (1L << Math.min(failures, 4)));
    Thread.sleep(backoff);
    capture.open(rtspUrl);
    if (capture.isOpened()) {
        failures = 0;
        motionService.resetBaseline();
    }
    continue;
}""")
    caption(doc, "Listing 8A.5: Exponential backoff reconnect (excerpt).")
    body(doc, "Empty or failed reads release the Mat, close the capture, and re-enter the reconnect path. They do not throw through @PostConstruct into a dead application context.")

    heading(doc, "8A.6 ONNX Runtime and Hardware Acceleration")
    bodies(doc, [
        "Default CPU emulation is acceptable for a laboratory 720p keyframe path and insufficient for a Jetson that must also fly. DJL Criteria options bind ONNX Runtime to GPU when present and constrain intra-op threads on CPU boards so that the capture thread is not starved.",
    ])
    add_code_lines(doc, """# application.properties
ai.djl.onnxruntime.deviceType=cpu
vajra.model.path=src/main/resources/models/yolov8n.onnx
vajra.video.source=0
vajra.motion.min-area=1000
vajra.alert.cooldown-ms=15000""")
    caption(doc, "Listing 8A.6: Laboratory defaults. GPU deviceType=gpu is used on NVIDIA edge nodes.")
    add_code_lines(doc, """Criteria<Image, DetectedObjects> criteria = Criteria.builder()
    .setTypes(Image.class, DetectedObjects.class)
    .optModelPath(Paths.get(modelPath))
    .optEngine("OnnxRuntime")
    .optOption("intra_op_num_threads", "2")
    .optOption("inter_op_num_threads", "1")
    .optOption("execution_mode", "ORT_SEQUENTIAL")
    .build();""")
    caption(doc, "Listing 8A.7: ONNX thread affinity for small edge CPUs.")

    heading(doc, "8A.7 Alert De-duplication")
    bodies(doc, [
        "An armed person visible for five seconds at 30 frames per second must not generate 150 SMS messages. A ConcurrentHashMap of class name to last-dispatch time implements a 15-second cooldown. The map is the runtime form of the tracking-related-work refusal: identity-free, time-based, good enough for Assignment 1, and mandatory for not freezing Twilio.",
    ])
    add_code_lines(doc, """if (last == null || now - last > COOLDOWN_PERIOD_MS) {
    lastDispatchedTimes.put(weaponType, now);
    return true;
}
return false;""")
    caption(doc, "Listing 8A.8: Suppression window (15 s default).")

    heading(doc, "8A.8 JVM Ergonomics for Edge Hardware")
    bodies(doc, [
        "Heap and off-heap must be capped or the operating system will SIGKILL the process. G1GC with a 20 ms pause goal reduces the chance that an RTSP buffer overflows during a stop-the-world collection. JavaCPP / OpenCV native ceilings prevent silent native growth.",
    ])
    add_code_lines(doc, """java -server -Xms512m -Xmx2048m ^
  -XX:+UseG1GC -XX:MaxGCPauseMillis=20 ^
  -XX:InitiatingHeapOccupancyPercent=45 ^
  -XX:+ExplicitGCInvokesConcurrent ^
  -Dorg.bytedeco.javacpp.maxphysicalbytes=3G ^
  -Dorg.bytedeco.javacpp.maxbytes=2G ^
  -jar target/vajra-eye-1.0.0.jar""")
    caption(doc, "Listing 8A.9: Suggested launch line for a 16 GB laboratory / 8–16 GB edge node.")
    add_table(doc,
              ["Flag", "Role in glitch prevention"],
              [
                  ["UseG1GC", "Concurrent collector; avoids long parallel-GC stalls"],
                  ["MaxGCPauseMillis=20", "Keeps pauses short vs RTSP buffers"],
                  ["Xmx2048m", "Hard Java heap ceiling on small companions"],
                  ["maxphysicalbytes", "Ceiling on off-heap native (OpenCV/DJL)"],
                  ["ExplicitGCInvokesConcurrent", "Safer native reclaim without full stall"],
              ])
    caption(doc, "Table 8A.1: JVM flags mapped to failure modes.")

    heading(doc, "8A.9 Diagnostic Matrix")
    add_table(doc,
              ["Glitch", "Likely cause", "Control"],
              [
                  ["UnsatisfiedLinkError opencv", "Native lib not loaded", "OpenCV.loadShared() in static block"],
                  ["Memory creep over hours", "Mat without release()", "NativeScope / finally release"],
                  ["Latency 150 ms → 4 s", "Queue/socket backlog", "Queue cap 5; CAP_PROP_BUFFERSIZE=1"],
                  ["Tree-sway false motion", "Kernel / area too small", "Blur 21×21; minArea ≥ 1000"],
                  ["CPU > 80°C on drone", "YOLO every frame", "Motion gate + pan ceiling"],
                  ["SMS storm", "No cooldown", "AlertDebounceManager 15 s"],
                  ["Dead process after RF drop", "Exception kills thread", "Backoff reconnect loop"],
                  ["False alarm after reconnect", "Stale baseline", "resetBaseline() on open"],
              ])
    caption(doc, "Table 8A.2: End-to-end troubleshooting matrix used in the laboratory SOP.")
    bodies(doc, [
        "Chapter 15’s viva SOP tells the student to disable real SMS, play a known clip, and if the webcam fails, switch vajra.video.source to a file. Those operational sentences are instances of this matrix, not improvisation.",
        "The source tree that implements 8A.1–8A.8 is the Maven project vajra-eye/ submitted as the software soft-copy alongside this Word report.",
    ])
