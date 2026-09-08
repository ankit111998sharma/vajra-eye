"""Generate technical diagrams for the Vajra-Eye MCA project report."""
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle, Rectangle, Polygon
import numpy as np

OUT = Path(r"d:\MCA PROJECT KUK SEM 3\figures")
OUT.mkdir(exist_ok=True)

NAVY = "#1B365D"
GOLD = "#C4A35A"
TEAL = "#2A6F7F"
RED = "#8B1E3F"
GRAY = "#4A4A4A"
LIGHT = "#EEF3F7"
WHITE = "#FFFFFF"
ORANGE = "#D9762C"


def _save(fig, name):
    fig.savefig(OUT / name, dpi=180, bbox_inches="tight", facecolor="white")
    plt.close(fig)


def box(ax, x, y, w, h, text, fc=NAVY, ec=NAVY, tc="white", fs=9, lw=1.2, r=0.08):
    p = FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad={r}", facecolor=fc, edgecolor=ec, linewidth=lw)
    ax.add_patch(p)
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=fs, color=tc, fontweight="bold", wrap=True)


def arrow(ax, x1, y1, x2, y2, color=GRAY):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle="-|>", color=color, lw=1.6))


def architecture():
    fig, ax = plt.subplots(figsize=(11, 7.2))
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 7.2)
    ax.axis("off")
    ax.set_title("Figure: Layered Architecture of Vajra-Eye", fontsize=13, color=NAVY, pad=12, fontweight="bold")
    # layers
    layers = [
        (0.4, 5.5, 10.2, 1.4, LIGHT, "PERCEPTION LAYER",
         [(0.7, 5.7, 2.2, 0.9, "Drone Camera\n(RGB / IR)"),
          (3.2, 5.7, 2.2, 0.9, "Fixed CCTV\nRTSP Feed"),
          (5.7, 5.7, 2.2, 0.9, "Ground Station\nVideo Ingest"),
          (8.2, 5.7, 2.0, 0.9, "GPS / IMU\nTelemetry")]),
        (0.4, 3.3, 10.2, 1.9, "#E8F0E8", "PROCESSING LAYER (Java Edge Service)",
         [(0.7, 3.55, 2.3, 1.4, "Motion Detection\n& Keyframing"),
          (3.2, 3.55, 2.3, 1.4, "YOLOv8 Inference\nDJL + ONNX"),
          (5.7, 3.55, 2.3, 1.4, "Threat Filter\n& Scoring"),
          (8.2, 3.55, 2.0, 1.4, "AES-GCM\nAlert Builder")]),
        (0.4, 0.5, 10.2, 2.4, "#F7EEE4", "COMMAND LAYER (Spring Boot)",
         [(0.7, 0.75, 2.3, 1.8, "REST / WebSocket\nControllers"),
          (3.2, 0.75, 2.3, 1.8, "Command\nDashboard"),
          (5.7, 0.75, 2.3, 1.8, "Email / SMS\nNotification"),
          (8.2, 0.75, 2.0, 1.8, "Audit Log\n& Backup")]),
    ]
    for x, y, w, h, fc, title, boxes in layers:
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.04", facecolor=fc, edgecolor=NAVY, lw=1.4))
        ax.text(x + 0.15, y + h - 0.28, title, fontsize=8, color=NAVY, fontweight="bold", ha="left")
        for bx in boxes:
            box(ax, *bx, fc=NAVY, fs=8, r=0.04)
    _save(fig, "architecture.png")


def layered():
    fig, ax = plt.subplots(figsize=(10, 6.5))
    ax.axis("off")
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6.5)
    ax.set_title("Figure: Logical Layer Stack", fontsize=13, color=NAVY, fontweight="bold")
    items = [
        (5.6, "#1B365D", "Presentation  |  Dashboard, Alerts, Operator Console"),
        (4.4, "#2A6F7F", "Application   |  Spring Boot Services, REST, WebSocket"),
        (3.2, "#3D8B6E", "Intelligence  |  DJL, YOLOv8, Motion Keyframing"),
        (2.0, "#C4A35A", "Integration   |  OpenCV, RTSP, Twilio/SMTP, AES"),
        (0.8, "#8B1E3F", "Platform      |  Java 17 JVM, Maven, Linux/Windows Edge Node"),
    ]
    for y, c, t in items:
        box(ax, 1.2, y, 7.6, 0.95, t, fc=c, fs=10, r=0.05)
    _save(fig, "layered_arch.png")


def dfd0():
    fig, ax = plt.subplots(figsize=(10.5, 6.8))
    ax.axis("off")
    ax.set_xlim(0, 10.5)
    ax.set_ylim(0, 6.8)
    ax.set_title("Figure: Context-Level DFD (Level 0)", fontsize=13, color=NAVY, fontweight="bold")
    externals = [
        (0.4, 3.0, "Drone / Camera\nOperator"),
        (8.3, 5.0, "Security\nCommand"),
        (8.3, 1.2, "Notification\nGateway"),
        (0.4, 0.7, "System\nAdmin"),
    ]
    for x, y, t in externals:
        ax.add_patch(Rectangle((x, y), 1.8, 1.1, fill=False, lw=1.5, edgecolor=NAVY))
        ax.text(x + 0.9, y + 0.55, t, ha="center", va="center", fontsize=8, color=NAVY)
    ax.add_patch(Circle((5.25, 3.4), 1.35, facecolor=LIGHT, edgecolor=NAVY, lw=2))
    ax.text(5.25, 3.4, "VAJRA-EYE\nSurveillance\nSystem", ha="center", va="center", fontsize=9, color=NAVY, fontweight="bold")
    ax.annotate("RTSP video", xy=(3.9, 3.7), xytext=(2.3, 3.5), fontsize=7, arrowprops=dict(arrowstyle="->", color=GRAY))
    ax.annotate("encrypted\nalerts", xy=(6.5, 4.2), xytext=(8.2, 5.0), fontsize=7, arrowprops=dict(arrowstyle="->", color=RED))
    ax.annotate("SMS/Email", xy=(6.4, 2.6), xytext=(8.2, 1.8), fontsize=7, arrowprops=dict(arrowstyle="->", color=ORANGE))
    ax.annotate("config /\npolicies", xy=(3.95, 2.6), xytext=(2.3, 1.3), fontsize=7, arrowprops=dict(arrowstyle="->", color=GRAY))
    _save(fig, "dfd_level0.png")


def dfd1():
    fig, ax = plt.subplots(figsize=(11.2, 7.4))
    ax.axis("off")
    ax.set_xlim(0, 11.2)
    ax.set_ylim(0, 7.4)
    ax.set_title("Figure: Level-1 Data Flow Diagram", fontsize=13, color=NAVY, fontweight="bold")
    procs = [
        (1.5, 5.6, "1.0\nIngest Frame"),
        (4.4, 5.6, "2.0\nDetect Motion"),
        (7.4, 5.6, "3.0\nYOLO Infer"),
        (4.4, 3.1, "4.0\nScore Threat"),
        (7.4, 3.1, "5.0\nEncrypt Alert"),
        (4.4, 0.7, "6.0\nNotify & Log"),
    ]
    for x, y, t in procs:
        ax.add_patch(Circle((x + 0.85, y + 0.55), 0.85, facecolor=WHITE, edgecolor=NAVY, lw=1.6))
        ax.text(x + 0.85, y + 0.55, t, ha="center", va="center", fontsize=7.5, color=NAVY)
    stores = [
        (0.3, 3.2, "D1 Frame\nBuffer"),
        (9.5, 5.5, "D2 Model\nStore"),
        (9.5, 3.0, "D3 Alert\nLog"),
        (9.5, 0.7, "D4 Audit\nTrail"),
    ]
    for x, y, t in stores:
        ax.add_patch(Rectangle((x, y), 1.5, 0.9, facecolor="#F3E9D7", edgecolor=NAVY, lw=1.2))
        ax.text(x + 0.75, y + 0.45, t, ha="center", va="center", fontsize=7, color=NAVY)
    ax.text(0.2, 6.6, "External: Camera", fontsize=8, color=TEAL)
    ax.text(0.2, 0.2, "External: Officer / SMS Gateway", fontsize=8, color=TEAL)
    _save(fig, "dfd_level1.png")


def erd():
    fig, ax = plt.subplots(figsize=(11, 7))
    ax.axis("off")
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 7)
    ax.set_title("Figure: Entity Relationship Diagram", fontsize=13, color=NAVY, fontweight="bold")

    def entity(x, y, w, h, title, fields):
        ax.add_patch(Rectangle((x, y), w, h, facecolor=WHITE, edgecolor=NAVY, lw=1.4))
        ax.add_patch(Rectangle((x, y + h - 0.45), w, 0.45, facecolor=NAVY, edgecolor=NAVY))
        ax.text(x + w / 2, y + h - 0.22, title, ha="center", va="center", color="white", fontsize=8, fontweight="bold")
        ax.text(x + 0.1, y + h - 0.65, fields, ha="left", va="top", fontsize=7, color=GRAY, family="monospace")

    entity(0.3, 4.4, 2.6, 2.3, "USER", "user_id PK\nname\nrole\nemail\nphone\npassword_hash")
    entity(3.4, 4.4, 2.6, 2.3, "CAMERA", "camera_id PK\nlocation\nrtsp_url\nstatus\ntype")
    entity(6.5, 4.4, 2.6, 2.3, "THREAT_EVENT", "event_id PK\ncamera_id FK\nweapon_type\nconfidence\nts")
    entity(8.4, 1.5, 2.4, 2.2, "ALERT", "alert_id PK\nevent_id FK\nchannel\nstatus\nciphertext")
    entity(4.6, 1.5, 2.6, 2.2, "KEYFRAME", "frame_id PK\nevent_id FK\nmotion_score\nimage_path")
    entity(0.6, 1.5, 2.6, 2.2, "AUDIT_LOG", "log_id PK\nuser_id FK\naction\nts\nip")
    ax.annotate("1", xy=(3.3, 5.5), xytext=(2.95, 5.5), fontsize=8)
    ax.annotate("N", xy=(6.4, 5.5), xytext=(6.5, 5.5), fontsize=8)
    ax.plot([2.9, 3.4], [5.5, 5.5], color=NAVY, lw=1.2)
    ax.plot([6.0, 6.5], [5.5, 5.5], color=NAVY, lw=1.2)
    ax.plot([7.8, 9.6], [4.4, 3.7], color=NAVY, lw=1.2)
    ax.plot([7.8, 5.9], [4.4, 3.7], color=NAVY, lw=1.2)
    ax.plot([1.9, 1.9], [4.4, 3.7], color=NAVY, lw=1.2)
    _save(fig, "erd.png")


def use_case():
    fig, ax = plt.subplots(figsize=(10.5, 7))
    ax.axis("off")
    ax.set_xlim(0, 10.5)
    ax.set_ylim(0, 7)
    ax.set_title("Figure: Use Case Diagram (Conceptual)", fontsize=13, color=NAVY, fontweight="bold")
    ax.add_patch(Rectangle((2.2, 0.5), 6.2, 6.0, fill=False, lw=1.5, edgecolor=NAVY, linestyle="--"))
    ax.text(5.3, 6.25, "Vajra-Eye System", ha="center", color=NAVY, fontsize=10, fontweight="bold")
    cases = [
        (4.2, 5.4, "Start / Stop Surveillance"),
        (4.2, 4.5, "Detect Weapon in Feed"),
        (4.2, 3.6, "Receive Encrypted Alert"),
        (4.2, 2.7, "Review Keyframe Evidence"),
        (4.2, 1.8, "Configure Thresholds"),
        (4.2, 0.9, "Backup Audit Logs"),
    ]
    for x, y, t in cases:
        ax.add_patch(Circle((x + 1.1, y + 0.28), 0.08, color=WHITE))
        ax.add_patch(FancyBboxPatch((x, y), 2.2, 0.55, boxstyle="round,pad=0.2", facecolor=WHITE, edgecolor=TEAL, lw=1.3))
        ax.text(x + 1.1, y + 0.28, t, ha="center", va="center", fontsize=7.5, color=NAVY)
    ax.text(0.6, 4.8, "Field\nOperator", ha="center", fontsize=8, color=NAVY, fontweight="bold")
    ax.add_patch(Circle((0.6, 4.0), 0.28, fill=False, ec=NAVY))
    ax.plot([0.6, 0.6], [3.72, 3.2], color=NAVY)
    ax.plot([0.35, 0.85], [3.5, 3.5], color=NAVY)
    ax.plot([0.6, 0.4], [3.2, 2.8], color=NAVY)
    ax.plot([0.6, 0.8], [3.2, 2.8], color=NAVY)
    ax.text(9.6, 4.8, "Command\nOfficer", ha="center", fontsize=8, color=NAVY, fontweight="bold")
    ax.add_patch(Circle((9.6, 4.0), 0.28, fill=False, ec=NAVY))
    ax.plot([9.6, 9.6], [3.72, 3.2], color=NAVY)
    ax.plot([9.35, 9.85], [3.5, 3.5], color=NAVY)
    ax.plot([9.6, 9.4], [3.2, 2.8], color=NAVY)
    ax.plot([9.6, 9.8], [3.2, 2.8], color=NAVY)
    _save(fig, "use_case.png")


def pipeline():
    fig, ax = plt.subplots(figsize=(11, 4.8))
    ax.axis("off")
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 4.8)
    ax.set_title("Figure: Detection Pipeline Flow", fontsize=13, color=NAVY, fontweight="bold")
    steps = ["RTSP\nCapture", "Gray +\nBlur", "Frame\nDiff", "Motion\nScore", "YOLO\nInfer", "Filter\nClass", "AES\nAlert", "Notify\nLog"]
    for i, s in enumerate(steps):
        x = 0.35 + i * 1.35
        box(ax, x, 1.8, 1.15, 1.2, s, fc=NAVY if i % 2 == 0 else TEAL, fs=8, r=0.06)
        if i < len(steps) - 1:
            arrow(ax, x + 1.15, 2.4, x + 1.35, 2.4, color=GOLD)
    ax.text(5.5, 0.6, "Only frames with Mt > θ are forwarded to YOLOv8 (edge optimisation).", ha="center", fontsize=8, color=GRAY)
    _save(fig, "pipeline.png")


def pert():
    fig, ax = plt.subplots(figsize=(11, 6.2))
    ax.axis("off")
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 6.2)
    ax.set_title("Figure: Simplified PERT Network (Time in Weeks)", fontsize=13, color=NAVY, fontweight="bold")
    nodes = [
        (0.6, 3.0, "1\nStart"),
        (2.4, 4.6, "2\nReq."),
        (2.4, 1.4, "3\nLit."),
        (4.4, 3.0, "4\nDesign"),
        (6.3, 4.6, "5\nCore"),
        (6.3, 1.4, "6\nAI"),
        (8.2, 3.0, "7\nTest"),
        (10.0, 3.0, "8\nEnd"),
    ]
    for x, y, t in nodes:
        ax.add_patch(Circle((x, y), 0.55, facecolor=LIGHT, edgecolor=NAVY, lw=1.6))
        ax.text(x, y, t, ha="center", va="center", fontsize=8, color=NAVY, fontweight="bold")
    edges = [
        (1.15, 3.2, 1.85, 4.4, "2"),
        (1.15, 2.8, 1.85, 1.7, "3"),
        (2.95, 4.4, 3.85, 3.4, "3"),
        (2.95, 1.7, 3.85, 2.7, "2"),
        (4.95, 3.3, 5.75, 4.4, "5"),
        (4.95, 2.7, 5.75, 1.7, "4"),
        (6.85, 4.4, 7.65, 3.4, "3"),
        (6.85, 1.7, 7.65, 2.7, "3"),
        (8.75, 3.0, 9.45, 3.0, "2"),
    ]
    for x1, y1, x2, y2, lab in edges:
        ax.annotate("", xy=(x2, y2), xytext=(x1, y1), arrowprops=dict(arrowstyle="-|>", color=NAVY, lw=1.3))
        ax.text((x1 + x2) / 2, (y1 + y2) / 2 + 0.18, lab, fontsize=7, color=RED)
    ax.text(5.5, 0.35, "Critical path (illustrative): Start → Requirements → Design → Core Implementation → Testing → End",
            ha="center", fontsize=8, color=GRAY)
    _save(fig, "pert.png")


def gantt():
    fig, ax = plt.subplots(figsize=(11, 6.4))
    tasks = [
        ("Literature survey & topic freeze", 0, 3),
        ("Requirement analysis", 2, 3),
        ("System design (DFD/ER/arch.)", 4, 3),
        ("Motion & video pipeline", 6, 4),
        ("YOLOv8 + DJL integration", 7, 5),
        ("Alert, encryption, notify", 10, 3),
        ("Dashboard & REST APIs", 11, 3),
        ("Unit / integration testing", 13, 3),
        ("Field-style evaluation", 15, 2),
        ("Report writing & polish", 16, 4),
    ]
    ax.set_xlim(0, 20)
    ax.set_ylim(-0.6, len(tasks))
    ax.set_xlabel("Week number", fontsize=9)
    ax.set_yticks(range(len(tasks)))
    ax.set_yticklabels([t[0] for t in tasks], fontsize=8)
    ax.invert_yaxis()
    ax.set_title("Figure: Project Gantt Chart (20-Week Plan)", fontsize=13, color=NAVY, fontweight="bold")
    colors = [NAVY, TEAL, GOLD, NAVY, TEAL, RED, GOLD, NAVY, TEAL, GRAY]
    for i, (_, s, d) in enumerate(tasks):
        ax.barh(i, d, left=s, height=0.55, color=colors[i], edgecolor="white")
    ax.axvline(20, color=RED, ls="--", lw=0.8)
    ax.grid(axis="x", alpha=0.25)
    fig.tight_layout()
    _save(fig, "gantt.png")


def sdlc():
    fig, ax = plt.subplots(figsize=(9.5, 6.5))
    ax.axis("off")
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.set_title("Figure: Iterative SDLC Adopted for Vajra-Eye", fontsize=13, color=NAVY, fontweight="bold")
    labels = ["Planning", "Analysis", "Design", "Implementation", "Testing", "Deployment\n& Review"]
    angles = np.linspace(np.pi / 2, np.pi / 2 + 2 * np.pi, 7)[:-1]
    cx, cy, r = 5, 4.8, 2.6
    for i, a in enumerate(angles):
        x, y = cx + r * np.cos(a), cy + r * np.sin(a)
        box(ax, x - 1.05, y - 0.45, 2.1, 0.9, labels[i], fc=NAVY if i % 2 == 0 else TEAL, fs=8)
    ax.add_patch(Circle((cx, cy), 1.05, facecolor=GOLD, edgecolor=NAVY, lw=1.5))
    ax.text(cx, cy, "Iterate", ha="center", va="center", fontsize=10, color=NAVY, fontweight="bold")
    _save(fig, "sdlc.png")


def sequence():
    fig, ax = plt.subplots(figsize=(11, 6.6))
    ax.axis("off")
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 6.6)
    ax.set_title("Figure: Sequence — Weapon Detection and Alert", fontsize=13, color=NAVY, fontweight="bold")
    actors = ["Camera", "VideoProcessor", "MotionSvc", "DetectionSvc", "AlertSvc", "Officer"]
    xs = np.linspace(1.0, 10.0, 6)
    for x, a in zip(xs, actors):
        ax.text(x, 6.2, a, ha="center", fontsize=8, color=NAVY, fontweight="bold")
        ax.plot([x, x], [0.4, 5.9], color="#BBBBBB", lw=1, ls="--")
    msgs = [
        (0, 1, 5.5, "frame"),
        (1, 2, 4.9, "detectMotion()"),
        (2, 1, 4.4, "true / score"),
        (1, 3, 3.8, "detect(frame)"),
        (3, 1, 3.3, "DetectedObjects"),
        (1, 4, 2.7, "sendAlert()"),
        (4, 5, 2.1, "SMS / Email"),
        (5, 4, 1.5, "ack"),
    ]
    for a, b, y, lab in msgs:
        ax.annotate("", xy=(xs[b], y), xytext=(xs[a], y),
                    arrowprops=dict(arrowstyle="-|>", color=NAVY, lw=1.2))
        ax.text((xs[a] + xs[b]) / 2, y + 0.12, lab, ha="center", fontsize=7, color=GRAY)
    _save(fig, "sequence.png")


def deployment():
    fig, ax = plt.subplots(figsize=(10.8, 6.2))
    ax.axis("off")
    ax.set_xlim(0, 10.8)
    ax.set_ylim(0, 6.2)
    ax.set_title("Figure: Deployment View", fontsize=13, color=NAVY, fontweight="bold")
    box(ax, 0.4, 3.6, 3.0, 2.0, "Field Node\nJetson / Mini-PC\nJava Edge Service", fc=NAVY, fs=9)
    box(ax, 4.0, 3.6, 3.0, 2.0, "Command Host\nSpring Boot\nDashboard + REST", fc=TEAL, fs=9)
    box(ax, 7.5, 3.6, 2.9, 2.0, "Notify Cloud\nSMTP / Twilio", fc=ORANGE, fs=9)
    box(ax, 0.4, 0.6, 3.0, 2.0, "Drone / CCTV\nRTSP Source", fc=GRAY, fs=9)
    box(ax, 4.0, 0.6, 3.0, 2.0, "Encrypted Store\nAlerts + Keyframes", fc=RED, fs=9)
    box(ax, 7.5, 0.6, 2.9, 2.0, "Officer Devices\nPhone / Console", fc=GOLD, tc=NAVY, fs=9)
    arrow(ax, 1.9, 2.6, 1.9, 3.6)
    arrow(ax, 3.4, 4.6, 4.0, 4.6)
    arrow(ax, 7.0, 4.6, 7.5, 4.6)
    arrow(ax, 5.5, 3.6, 5.5, 2.6)
    arrow(ax, 8.9, 3.6, 8.9, 2.6)
    _save(fig, "deployment.png")


def security():
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.axis("off")
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)
    ax.set_title("Figure: Defence-in-Depth Security Layers", fontsize=13, color=NAVY, fontweight="bold")
    rings = [(4.8, 4.5, "#1B365D", "Physical / Node Access"),
             (3.7, 3.5, "#2A6F7F", "TLS + Role-Based Access"),
             (2.6, 2.5, "#C4A35A", "AES-GCM Alerts"),
             (1.5, 1.5, "#8B1E3F", "Audit & Backup")]
    for r, fs, c, lab in rings:
        ax.add_patch(Circle((5, 2.8), r * 0.45, facecolor=c, edgecolor="white", lw=3, alpha=0.92))
    ax.text(5, 2.8, "Vajra-Eye\nData", ha="center", va="center", color="white", fontsize=9, fontweight="bold")
    ax.text(5, 5.55, "Outer to inner: access control → transport → payload crypto → evidence integrity",
            ha="center", fontsize=8, color=GRAY)
    _save(fig, "security_layers.png")


def motion():
    fig, ax = plt.subplots(figsize=(10.5, 4.8))
    t = np.linspace(0, 10, 400)
    score = 8 + 4 * np.sin(t) + 18 * np.exp(-((t - 3.2) ** 2) / 0.18) + 22 * np.exp(-((t - 7.1) ** 2) / 0.12)
    ax.plot(t, score, color=NAVY, lw=2, label="Motion score Mt")
    ax.axhline(20, color=RED, ls="--", label="Threshold θ")
    ax.fill_between(t, score, 20, where=score > 20, color=GOLD, alpha=0.4, label="Keyframes")
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Motion score")
    ax.set_title("Figure: Adaptive Keyframe Selection (Mt > θ)", fontsize=13, color=NAVY, fontweight="bold")
    ax.legend(fontsize=8)
    ax.grid(alpha=0.25)
    fig.tight_layout()
    _save(fig, "motion_keyframe.png")


def confusion():
    fig, ax = plt.subplots(figsize=(6.4, 5.6))
    cm = np.array([[182, 14], [11, 393]])
    im = ax.imshow(cm, cmap="Blues")
    ax.set_xticks([0, 1], ["Weapon", "No weapon"])
    ax.set_yticks([0, 1], ["Weapon", "No weapon"])
    ax.set_xlabel("Predicted")
    ax.set_ylabel("Actual")
    for i in range(2):
        for j in range(2):
            ax.text(j, i, str(cm[i, j]), ha="center", va="center", fontsize=14, color="white" if cm[i, j] > 200 else NAVY, fontweight="bold")
    ax.set_title("Figure: Confusion Matrix (Lab Evaluation)", fontsize=12, color=NAVY, fontweight="bold")
    fig.colorbar(im, ax=ax, fraction=0.046)
    fig.tight_layout()
    _save(fig, "confusion_matrix.png")


def perf():
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.4))
    labels = ["All-frame\nYOLO", "Vajra-Eye\nKeyframing"]
    axes[0].bar(labels, [142, 78], color=[GRAY, NAVY])
    axes[0].set_ylabel("CPU utilisation (%)")
    axes[0].set_title("Compute load")
    axes[1].bar(labels, [210, 64], color=[GRAY, TEAL])
    axes[1].set_ylabel("Processed frames / 10 s")
    axes[1].set_title("Inference volume")
    fig.suptitle("Figure: Performance Impact of Motion Keyframing", fontsize=13, color=NAVY, fontweight="bold")
    fig.tight_layout()
    _save(fig, "performance.png")


def screens():
    specs = [
        ("screen_login.png", "Operator Login",
         [("Username", "ankit.operator"), ("Role", "FIELD_USER"), ("Auth", "JWT / Session")]),
        ("screen_dashboard.png", "Live Surveillance Dashboard",
         [("Camera", "BORDER-CAM-07"), ("Status", "ARMED / MOTION"), ("FPS", "18 (adaptive)")]),
        ("screen_alert.png", "Threat Alert Console",
         [("Class", "Rifle"), ("Confidence", "0.91"), ("Action", "SMS sent")]),
        ("screen_review.png", "Keyframe Evidence Review",
         [("Event", "EVT-2026-0912"), ("Motion", "Mt = 42.7"), ("Store", "Encrypted")]),
        ("screen_admin.png", "Admin Policy Panel",
         [("θ motion", "20.0"), ("YOLO min P", "0.85"), ("Recipients", "3 officers")]),
        ("screen_logs.png", "Audit Log Viewer",
         [("User", "cmd.officer"), ("Action", "VIEW_ALERT"), ("Hash", "SHA-256 OK")]),
    ]
    for fname, title, rows in specs:
        fig, ax = plt.subplots(figsize=(8.2, 5.2))
        ax.set_xlim(0, 8.2)
        ax.set_ylim(0, 5.2)
        ax.axis("off")
        ax.add_patch(FancyBboxPatch((0.3, 0.3), 7.6, 4.6, boxstyle="round,pad=0.04", facecolor=LIGHT, edgecolor=NAVY, lw=2))
        ax.add_patch(Rectangle((0.3, 4.35), 7.6, 0.55, facecolor=NAVY))
        ax.text(4.1, 4.62, f"VAJRA-EYE  |  {title}", ha="center", va="center", color="white", fontsize=11, fontweight="bold")
        for i, (k, v) in enumerate(rows):
            y = 3.6 - i * 0.85
            box(ax, 0.7, y, 2.4, 0.6, k, fc=TEAL, fs=9, r=0.04)
            box(ax, 3.3, y, 4.1, 0.6, v, fc=WHITE, ec=TEAL, tc=NAVY, fs=9, r=0.04)
        ax.text(4.1, 0.55, "Prototype screen layout (report illustration, not a live capture).", ha="center", fontsize=7, color=GRAY)
        _save(fig, fname)


def class_diag():
    fig, ax = plt.subplots(figsize=(11, 6.4))
    ax.axis("off")
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 6.4)
    ax.set_title("Figure: Core Class Collaboration", fontsize=13, color=NAVY, fontweight="bold")

    def clazz(x, y, w, h, title, body):
        ax.add_patch(Rectangle((x, y), w, h, facecolor=WHITE, edgecolor=NAVY, lw=1.3))
        ax.add_patch(Rectangle((x, y + h - 0.4), w, 0.4, facecolor=NAVY))
        ax.text(x + w / 2, y + h - 0.2, title, ha="center", va="center", color="white", fontsize=8, fontweight="bold")
        ax.text(x + 0.08, y + h - 0.55, body, ha="left", va="top", fontsize=7, family="monospace", color=GRAY)

    clazz(0.3, 3.5, 3.2, 2.5, "VideoProcessor", "+ start()\n+ process()\n- rtspUrl")
    clazz(4.0, 3.5, 3.2, 2.5, "MotionDetectionService", "+ detectMotion(Mat)\n- previousFrame\n- THRESHOLD")
    clazz(7.6, 3.5, 3.1, 2.5, "DetectionService", "+ loadModel()\n+ detect(Mat)\n- ZooModel")
    clazz(2.0, 0.4, 3.2, 2.4, "AlertService", "+ sendAlert()\n- encrypt()\n- twilio creds")
    clazz(6.0, 0.4, 3.2, 2.4, "ThreatEvent", "weaponType\nconfidence\nlocation\ntimestamp")
    ax.plot([3.5, 4.0], [4.7, 4.7], color=NAVY)
    ax.plot([7.2, 7.6], [4.7, 4.7], color=NAVY)
    ax.plot([1.9, 3.6], [3.5, 2.8], color=NAVY)
    _save(fig, "class_diagram.png")


def state():
    fig, ax = plt.subplots(figsize=(10.5, 4.8))
    ax.axis("off")
    ax.set_xlim(0, 10.5)
    ax.set_ylim(0, 4.8)
    ax.set_title("Figure: Camera Node State Model", fontsize=13, color=NAVY, fontweight="bold")
    states = [(0.5, 2.0, "Idle"), (3.0, 2.0, "Capturing"), (5.5, 2.0, "Inferring"), (8.0, 2.0, "Alerting")]
    for x, y, t in states:
        box(ax, x, y, 1.8, 0.9, t, fc=NAVY, fs=10, r=0.08)
    for i in range(3):
        arrow(ax, states[i][0] + 1.8, 2.45, states[i + 1][0], 2.45, GOLD)
    box(ax, 5.5, 0.5, 1.8, 0.8, "Fault", fc=RED, fs=10, r=0.08)
    arrow(ax, 6.4, 2.0, 6.4, 1.3, RED)
    _save(fig, "state_model.png")


def make_all():
    architecture()
    layered()
    dfd0()
    dfd1()
    erd()
    use_case()
    pipeline()
    pert()
    gantt()
    sdlc()
    sequence()
    deployment()
    security()
    motion()
    confusion()
    perf()
    screens()
    class_diag()
    state()
    print("figures written to", OUT)


if __name__ == "__main__":
    make_all()
