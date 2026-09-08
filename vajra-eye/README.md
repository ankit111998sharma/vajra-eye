# VAJRA-EYE

Edge-based intelligent aerial surveillance prototype (Java 17, Spring Boot, OpenCV, DJL/ONNX).

## Run

```bash
cd vajra-eye
mvn -q -DskipTests package
java -jar target/vajra-eye-1.0.0.jar
```

- Command UI: http://localhost:8088/
- Login: `localhost` / `root` (also `admin` / `vajra`)
- MySQL Workbench: host `localhost`, user `root`, password `root`, schema **vajra_eye**

## What the camera labels (same names on the live feed)

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

A **threat alert** is sent only for weapons that can harm a living human. Person, face, and hand are labeled but do not alert.

Stock COCO cannot see a firearm. Place a weapon-trained graph at `src/main/resources/models/yolov8n.onnx` to label **gun**.

## Threat alerts tab

Shows the label listing, live **Camera sees** names, and dispatched alerts (`/api/alerts`).

API: `GET /api/weapons` and `GET /api/alerts`.

Do not commit real Twilio keys or AES production keys.
