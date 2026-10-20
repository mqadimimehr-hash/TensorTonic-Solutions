"""Figure 3 of the manuscript (v5, 20 Oct 2026): |m| and m_abs of the production cells, values from Table 3.
v5 corrects m_abs of Rb_perfect (1.13, not 1.00 as plotted in v4)."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

RY = 13.605693123
S1, S2, S3 = "#2a78d6", "#eb6834", "#1baf7a"      # validated categorical slots 1-3
INK, INK2, GRID = "#0b0b0b", "#52514e", "#d9d8d4"
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10, "axes.edgecolor": INK2,
                     "axes.labelcolor": INK, "xtick.color": INK, "ytick.color": INK})

# ---------- Figure 3: total and absolute magnetisation ----------
systems = ["Pristine\nperfect", "Pr_perfect", "Pr_VO", "Rb_perfect", "Rb_VO", "O$_2$ (box)"]
m_tot = [0.00, 0.00, 0.00, 1.00, 0.97, 2.00]     # |m|, signed total magnetisation magnitude
m_abs = [0.00, 0.00, 0.00, 1.13, 1.21, 2.00]     # m_abs (Table 3: Rb_perfect 1.13, Rb_VO 1.21)
fig, ax = plt.subplots(figsize=(6.2, 3.6), dpi=300)
x = np.arange(len(systems)); w = 0.36
b1 = ax.bar(x - w / 2 - 0.01, m_tot, w, color=S1, label="|m|  (magnitude of total magnetisation)", zorder=3)
b2 = ax.bar(x + w / 2 + 0.01, m_abs, w, color=S2, hatch="///", edgecolor="white", lw=0,
            label="$m_{\\mathrm{abs}}$  (absolute magnetisation)", zorder=3)
ax.set_ylabel("Magnetisation per cell ($\\mu_{\\mathrm{B}}$)"); ax.set_ylim(0, 2.45)
ax.set_xticks(x); ax.set_xticklabels(systems, fontsize=9)
ax.yaxis.grid(True, color=GRID, lw=0.6, zorder=0); ax.set_axisbelow(True)
for s in ["top", "right"]: ax.spines[s].set_visible(False)
for bars, vals_ in ((b1, m_tot), (b2, m_abs)):
    for b, v in zip(bars, vals_):
        ax.text(b.get_x() + b.get_width() / 2, v + 0.04, f"{v:.2f}", ha="center", fontsize=8 if v > 0 else 7, color=INK if v > 0 else INK2)
ax.legend(frameon=False, fontsize=8.5, loc="upper left")
ax.set_title("Converged magnetisation, PBE+U relaxations with U on Ti-3d only", fontsize=9.5, color=INK)
fig.tight_layout(); fig.savefig("Fig3_magnetisation_v5.png"); fig.savefig("Fig3_magnetisation_v5.pdf", metadata={"CreationDate": None})
print("written Fig3_magnetisation_v5.{png,pdf}")
