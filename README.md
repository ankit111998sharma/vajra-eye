# VAJRA-EYE (Vajar Eye)

An edge-oriented aerial / webcam surveillance prototype. A Java Spring Boot service runs object detection on a camera feed, labels people and objects on screen, and raises **threat alerts** only for weapons that can harm a person. This folder also holds MCA report-building Python scripts that generate Word/PDF documentation around the same system.

Copyright © Ankit Sharma.

## About this project

The runnable product lives in the `vajra-eye/` Maven module. It uses Java 17, Spring Boot, OpenCV, and DJL with ONNX/PyTorch engines. A command UI on port **8088** shows the live overlay, what the camera currently names, and dispatched alerts. Detections and alerts can be stored in MySQL schema `vajra_eye`. Optional Twilio can notify by SMS when configured; do not commit real Twilio or AES production keys.

Stock COCO YOLO can label everyday objects and some melee items (knife, scissors, fork, baseball bat). Firearms need a separate weapon-trained ONNX graph at `vajra-eye/src/main/resources/models/yolov8n.onnx`.

## Purpose

- Prototype intelligent camera monitoring for a command post (MCA / lab context).
- Label **person**, **face**, and **hand** for awareness without treating them as threats.
- Alert on detected weapons (COCO melee classes and optional gun/pistol/rifle from a weapon model).
- Document the system in KUK-style report files generated from the Python scripts in this folder.

## How it works

1. Spring Boot starts a web app and camera pipeline (OpenCV).
2. YOLO (ONNX via DJL) scores COCO classes on each frame. YuNet or Haar can mark faces. A skin-region heuristic can mark a hand on a person.
3. The overlay and **Camera sees** line print the **exact class name** of each object.
4. A threat alert is sent only for weapon-like classes, not for person/face/hand.
5. The Threat alerts tab lists labels, live names, and alerts from `/api/alerts`. Related APIs: `GET /api/weapons`, `GET /api/alerts`.
6. Report scripts (`build_report.py` and `report_*.py`) assemble academic chapters into `.docx` files; they are not required to run the camera app.

## Advantages

- Runs as a local JAR with a browser command UI — no separate front-end repo.
- Clear split: identity labels vs weapon alerts.
- MySQL persistence for alerts and related records (Workbench-friendly).
- ONNX/DJL so models can be swapped without rewriting the whole pipeline.
- Face/hand helpers add context on the same feed as object detection.

## Technologies

| Area | Choice |
| --- | --- |
| Language | Java 17 |
| Framework | Spring Boot 3.3 (Web, Data JPA) |
| Vision | OpenCV, DJL, ONNX Runtime, PyTorch engine |
| Database | MySQL (`mysql-connector-j`) |
| Optional notify | Twilio SDK |
| Build | Maven |
| Reports (this folder) | Python (`python-docx` style report builders) |

## How to run this project

MySQL Workbench: host `localhost`, user `root`, password `root`, schema **vajra_eye**.

```bash
cd vajra-eye
mvn -q -DskipTests package
java -jar target/vajra-eye-1.0.0.jar
```

- Command UI: [http://localhost:8088/](http://localhost:8088/)
- Login: `localhost` / `root` (also `admin` / `vajra`)

Place a weapon-trained graph at `vajra-eye/src/main/resources/models/yolov8n.onnx` if you need **gun / pistol / rifle** labels. Stock COCO cannot see a firearm.

Copyright © Ankit Sharma.
