package com.vajra.service;

import ai.djl.inference.Predictor;
import ai.djl.modality.cv.Image;
import ai.djl.modality.cv.ImageFactory;
import ai.djl.modality.cv.output.DetectedObjects;
import ai.djl.modality.cv.output.Rectangle;
import ai.djl.modality.cv.translator.YoloV5TranslatorFactory;
import ai.djl.repository.zoo.Criteria;
import ai.djl.repository.zoo.ZooModel;
import com.vajra.model.SceneObject;
import jakarta.annotation.PostConstruct;
import jakarta.annotation.PreDestroy;
import org.opencv.core.CvType;
import org.opencv.core.Mat;
import org.opencv.core.Rect;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;

import java.awt.image.BufferedImage;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.Collections;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

@Service
public class DetectionService {

    private static final Logger log = LoggerFactory.getLogger(DetectionService.class);

    @Value("${vajra.model.path:src/main/resources/models/yolov8n.onnx}")
    private String modelPath;

    private final BodyPartDetector bodyParts;

    private ZooModel<Image, DetectedObjects> model;
    private Predictor<Image, DetectedObjects> predictor;
    private volatile boolean modelReady;
    private volatile String engineLabel = "loading";
    private volatile String lastError = "";
    private volatile List<Map<String, Object>> lastSeen = List.of();

    public DetectionService(BodyPartDetector bodyParts) {
        this.bodyParts = bodyParts;
    }

    @PostConstruct
    public void startLoad() {
        Thread loader = new Thread(this::loadModel, "vajra-model-load");
        loader.setDaemon(true);
        loader.start();
    }

    private void loadModel() {
        Path path = Paths.get(modelPath);
        if (Files.exists(path)) {
            if (tryLoad(Criteria.builder()
                    .setTypes(Image.class, DetectedObjects.class)
                    .optModelPath(path)
                    .optEngine("OnnxRuntime")
                    .optTranslatorFactory(new YoloV5TranslatorFactory())
                    .optArgument("threshold", 0.18f)
                    .optArgument("width", 640)
                    .optArgument("height", 640)
                    .optArgument("resize", true)
                    .optArgument("rescale", true)
                    .optArgument("toTensor", true)
                    .optArgument("optApplyRatio", true)
                    .build(), "local-onnx")) {
                return;
            }
        }
        if (tryLoad(yoloV5Criteria("djl://ai.djl.pytorch/yolov5s"), "zoo-yolov5s")) {
            return;
        }
        engineLabel = "none";
        lastError = "No detector loaded";
        log.warn("No COCO detector loaded.");
    }

    private Criteria<Image, DetectedObjects> yoloV5Criteria(String url) {
        return Criteria.builder()
                .setTypes(Image.class, DetectedObjects.class)
                .optModelUrls(url)
                .optEngine("PyTorch")
                .optTranslatorFactory(new YoloV5TranslatorFactory())
                .optArgument("threshold", 0.18f)
                .optArgument("width", 640)
                .optArgument("height", 640)
                .optArgument("resize", true)
                .optArgument("rescale", true)
                .optArgument("toTensor", true)
                .optArgument("optApplyRatio", true)
                .build();
    }

    private boolean tryLoad(Criteria<Image, DetectedObjects> criteria, String label) {
        try {
            log.info("Trying detection model {} …", label);
            ZooModel<Image, DetectedObjects> loaded = criteria.loadModel();
            Predictor<Image, DetectedObjects> p = loaded.newPredictor();
            model = loaded;
            predictor = p;
            modelReady = true;
            engineLabel = label + "+face+hand";
            lastError = "";
            warmup();
            log.info("Detection model ready ({}) — labels: person, face, hand, knife, and other COCO classes", engineLabel);
            return true;
        } catch (Exception e) {
            lastError = e.getMessage() == null ? e.getClass().getSimpleName() : e.getMessage();
            log.warn("Could not load {} ({})", label, lastError);
            return false;
        }
    }

    private void warmup() {
        Mat dummy = Mat.zeros(480, 640, CvType.CV_8UC3);
        try {
            detectAll(dummy);
        } finally {
            dummy.release();
        }
    }

    public boolean isModelReady() {
        return modelReady || bodyParts.isReady();
    }

    public String getEngineLabel() {
        return engineLabel;
    }

    public String getLastError() {
        return lastError;
    }

    public List<Map<String, Object>> getLastSeen() {
        return lastSeen;
    }

    public synchronized List<SceneObject> detectAll(Mat frame) {
        List<SceneObject> out = new ArrayList<>();
        if (frame == null || frame.empty()) {
            lastSeen = List.of();
            return out;
        }
        int fw = frame.cols();
        int fh = frame.rows();
        List<Rect> personBoxes = new ArrayList<>();
        if (modelReady && predictor != null) {
            try {
                Image img = toDjlImage(frame);
                DetectedObjects found = predictor.predict(img);
                if (found != null) {
                    found.items().forEach(obj -> {
                        String name = obj.getClassName() == null ? "object" : obj.getClassName().trim();
                        double p = obj.getProbability();
                        double x = 0;
                        double y = 0;
                        double bw = 0;
                        double bh = 0;
                        if (obj instanceof DetectedObjects.DetectedObject det && det.getBoundingBox() != null) {
                            Rectangle r = det.getBoundingBox().getBounds();
                            x = r.getX();
                            y = r.getY();
                            bw = r.getWidth();
                            bh = r.getHeight();
                            if (bw <= 1.05 && bh <= 1.05) {
                                x *= fw;
                                y *= fh;
                                bw *= fw;
                                bh *= fh;
                            }
                        }
                        boolean threat = WeaponCatalog.isHumanHarmingWeapon(name);
                        out.add(new SceneObject(name, p, x, y, bw, bh, threat));
                        if ("person".equalsIgnoreCase(name)) {
                            personBoxes.add(new Rect((int) x, (int) y, Math.max(1, (int) bw), Math.max(1, (int) bh)));
                        }
                    });
                }
            } catch (Exception e) {
                lastError = e.getMessage() == null ? e.getClass().getSimpleName() : e.getMessage();
                log.warn("YOLO inference failed: {}", lastError);
            }
        }
        try {
            out.addAll(bodyParts.detect(frame, personBoxes));
        } catch (Exception e) {
            log.debug("Body-part detect: {}", e.getMessage());
        }
        remember(out);
        return out;
    }

    private void remember(List<SceneObject> found) {
        List<Map<String, Object>> rows = new ArrayList<>();
        for (SceneObject obj : found) {
            Map<String, Object> row = new LinkedHashMap<>();
            row.put("className", obj.getClassName());
            row.put("probability", obj.getProbability());
            row.put("threat", obj.isThreat());
            rows.add(row);
        }
        lastSeen = rows;
    }

    private Image toDjlImage(Mat bgr) {
        Mat src = bgr;
        Mat copy = null;
        if (!bgr.isContinuous()) {
            copy = bgr.clone();
            src = copy;
        }
        try {
            int w = src.cols();
            int h = src.rows();
            byte[] data = new byte[w * h * 3];
            src.get(0, 0, data);
            BufferedImage image = new BufferedImage(w, h, BufferedImage.TYPE_3BYTE_BGR);
            image.getRaster().setDataElements(0, 0, w, h, data);
            return ImageFactory.getInstance().fromImage(image);
        } finally {
            if (copy != null) {
                copy.release();
            }
        }
    }

    @PreDestroy
    public void close() {
        try {
            if (predictor != null) {
                predictor.close();
            }
        } catch (Exception ignored) {
        }
        if (model != null) {
            model.close();
        }
    }
}
