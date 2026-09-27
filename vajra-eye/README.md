# VAJRA-EYE

Edge-based intelligent aerial surveillance prototype (Java 17, Spring Boot, OpenCV, DJL/ONNX).

Copyright © Ankit Sharma.

## About this project

VAJRA-EYE is the Maven application inside the Vajar Eye workspace. It streams a camera, overlays detections, and stores alerts in MySQL. The command UI is a Spring Boot site on port 8088.

## Purpose

Detect and label people and objects on a live feed, and raise threat alerts only for weapons that can harm a living human. Person, face, and hand are labeled but do not alert.

## How it works

The overlay and **Camera sees** line print the **exact class name** of each object:

| Label | How it is found | Threat alert |
| --- | --- | --- |
| **person** | COCO YOLO | No |
| **face** | YuNet / Haar | No |
| **hand** | Skin region on the person | No |
| **knife** | COCO YOLO | **Yes** |
| **scissors** | COCO YOLO | **Yes** |
| **fork** | COCO YOLO | **Yes** |
| **baseball bat** | COCO YOLO | **Yes** |
| **gun / pistol / rifle** | Weapon ONNX only | **Yes** if detected |
| cell phone, bottle, chair, … | COCO YOLO | No |

Stock COCO cannot see a firearm. Place a weapon-trained graph at `src/main/resources/models/yolov8n.onnx` to label **gun**.

The Threat alerts tab shows the label listing, live **Camera sees** names, and dispatched alerts (`/api/alerts`). APIs: `GET /api/weapons` and `GET /api/alerts`.

## Advantages

- Local command UI and JAR deploy.
- Weapon alerts are separated from person/face/hand labels.
- MySQL-backed alert history for a lab or demo command post.

## Technologies

Java 17, Spring Boot 3.3, Spring Data JPA, MySQL, OpenCV, DJL (ONNX Runtime and PyTorch engines), optional Twilio.

## How to run this project

```bash
cd vajra-eye
mvn -q -DskipTests package
java -jar target/vajra-eye-1.0.0.jar
```

- Command UI: http://localhost:8088/
- Login: `localhost` / `root` (also `admin` / `vajra`)
- MySQL Workbench: host `localhost`, user `root`, password `root`, schema **vajra_eye**

Do not commit real Twilio keys or AES production keys.

Copyright © Ankit Sharma.
