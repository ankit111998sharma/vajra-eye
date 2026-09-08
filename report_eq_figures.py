"""Render displayed equations used in the theoretical framework chapter."""
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUT = Path(r"d:\MCA PROJECT KUK SEM 3\figures")
OUT.mkdir(exist_ok=True)


def _eq(name, latex, h=1.35, fs=15):
    fig = plt.figure(figsize=(10.2, h), facecolor="white")
    ax = fig.add_axes([0.02, 0.05, 0.96, 0.9])
    ax.axis("off")
    ax.text(0.5, 0.5, f"${latex}$", ha="center", va="center", fontsize=fs, color="#1B365D")
    fig.savefig(OUT / name, dpi=180, facecolor="white", bbox_inches="tight", pad_inches=0.12)
    plt.close(fig)
    print("ok", name)


def make_all():
    specs = [
        ("eq_frames.png", r"F=\{F_0,F_1,\ldots,F_t,\ldots\},\quad F_t\in\mathbb{R}^{H\times W\times 3}", 1.2, 16),
        ("eq_gray.png", r"I_t(x,y)=0.299\,R_t+0.587\,G_t+0.114\,B_t", 1.15, 15),
        ("eq_gauss.png", r"I'_t=I_t*G_\sigma,\quad G_\sigma=\frac{1}{2\pi\sigma^2}\exp(-(i^2+j^2)/(2\sigma^2))", 1.35, 13),
        ("eq_diff.png", r"\Delta_t(x,y)=\left|I'_t(x,y)-I'_{t-1}(x,y)\right|", 1.15, 16),
        ("eq_bin.png", r"B_t=255\ \mathrm{if}\ \Delta_t\geq\theta_{pixel}\ \mathrm{else}\ 0", 1.2, 14),
        ("eq_dilate.png", r"B'_t=B_t\oplus S,\quad S=3\times 3", 1.2, 15),
        ("eq_area.png", r"A(c_i)=\frac{1}{2}\left|\sum_k(x_k y_{k+1}-x_{k+1} y_k)\right|", 1.25, 15),
        ("eq_key.png", r"IsKeyframe(F_t)=\exists c_i:\ A(c_i)\geq\theta_{area}", 1.25, 14),
        ("eq_loss.png", r"\mathcal{L}_{total}=\lambda_{box}\mathcal{L}_{CIoU}+\lambda_{cls}\mathcal{L}_{BCE}+\lambda_{dfl}\mathcal{L}_{DFL}", 1.25, 13),
        ("eq_ciou.png", r"\mathcal{L}_{CIoU}=1-IoU+\rho^2(b,b^{gt})/c^2+\alpha v", 1.2, 14),
        ("eq_prf.png", r"Prec=\frac{TP}{TP+FP},\ Rec=\frac{TP}{TP+FN},\ Spec=\frac{TN}{TN+FP}", 1.25, 14),
        ("eq_ap.png", r"AP=\int_0^1 P(R)\,dR", 1.1, 16),
        ("eq_map.png", r"mAP=\frac{1}{N}\sum_{i=1}^{N}AP_i", 1.15, 16),
        ("eq_lat.png", r"T_{total}=T_{cap}+T_{mot}+T_{prep}+T_{YOLO}+T_{NMS}+T_{AES}+T_{disp}", 1.35, 12),
        ("eq_budget.png", r"T_{total}<3.0\ s", 1.0, 16),
    ]
    for spec in specs:
        try:
            _eq(*spec)
        except Exception as e:
            print("FAIL", spec[0], e)
            plt.close("all")
    print("equation figures done")


if __name__ == "__main__":
    make_all()
