"""Rebuild Figures 2 and 3 of manuscript v4 from the reported Quantum ESPRESSO totals.
All numbers are taken from the Supporting Information Ry ledger; nothing is fitted."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

RY = 13.605693123
S1, S2, S3 = "#2a78d6", "#eb6834", "#1baf7a"      # validated categorical slots 1-3
INK, INK2, GRID = "#0b0b0b", "#52514e", "#d9d8d4"
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10, "axes.edgecolor": INK2,
                     "axes.labelcolor": INK, "xtick.color": INK, "ytick.color": INK})

# ---------- Figure 2: neutral V_O formation energies ----------
E = {"Pristine_perfect": -4275.01530, "Pristine_VO": -4233.15036,
     "Pr_perfect": -4576.71224, "Pr_VO": -4535.10106,
     "Rb_perfect": -4330.38890, "Rb_VO": -4289.17135, "halfO2": -41.51621,
     "Pr_perfect_222": -4576.62183, "Pr_VO_222": -4535.01814,
     "Rb_perfect_222": -4330.28761, "Rb_VO_222": -4289.08034}
ef = lambda a, b: (E[a] - E[b] + E["halfO2"]) * RY
vals = [ef("Pristine_VO", "Pristine_perfect"), ef("Pr_VO", "Pr_perfect"), ef("Rb_VO", "Rb_perfect")]
vals222 = [None, ef("Pr_VO_222", "Pr_perfect_222"), ef("Rb_VO_222", "Rb_perfect_222")]
labels = ["Pristine TiO$_2$", "Pr$_{\\mathrm{Ti}}$", "Rb$_{\\mathrm{Ti}}$"]
cols = [S1, S2, S3]

fig, ax = plt.subplots(figsize=(5.4, 3.9), dpi=300)
x = np.arange(3)
bars = ax.bar(x, vals, width=0.58, color=cols, edgecolor="none", zorder=3)
for i, v in enumerate(vals222):
    if v is not None:
        ax.plot([x[i] - 0.29, x[i] + 0.29], [v, v], color=INK, lw=1.2, ls=(0, (3, 2)), zorder=4)
ax.axhline(0, color=INK2, lw=0.8, zorder=2)
ax.set_ylabel("$E_{\\mathrm{f}}(V_{\\mathrm{O}}^{0})$ at $\\mu_{\\mathrm{O}} = \\frac{1}{2}E(\\mathrm{O}_2)$  (eV)")
ax.set_xticks(x); ax.set_xticklabels(labels)
ax.set_ylim(-5.2, 5.6); ax.yaxis.grid(True, color=GRID, lw=0.6, zorder=0); ax.set_axisbelow(True)
for s in ["top", "right"]: ax.spines[s].set_visible(False)
for b, v in zip(bars, vals):
    if v > 0:
        ax.text(b.get_x() + b.get_width() / 2, v + 0.18, f"{v:+.2f} eV".replace("-", "\u2212"), ha="center", va="bottom", color=INK, fontsize=9.5, fontweight="bold")
    else:
        ax.text(b.get_x() + b.get_width() / 2, v / 2, f"{v:+.2f} eV".replace("-", "\u2212"), ha="center", va="center", color="white", fontsize=9.5, fontweight="bold")
ax.text(x[1] + 0.31, vals222[1], f"{vals222[1]:+.2f}".replace("-", "\u2212") + "\n(2×2×2)", fontsize=7, color=INK2, va="center", ha="left", linespacing=1.1)
ax.text(x[2] - 0.31, vals222[2] - 0.35, f"{vals222[2]:+.2f} (2×2×2)".replace("-", "\u2212"), fontsize=7, color=INK2, va="top", ha="right")
ax.set_title("Neutral oxygen-vacancy formation energy, PBE+U, U(Ti-3d) = 3.5 eV", fontsize=9.5, color=INK)
fig.text(0.5, 0.005, "Bars: Γ-only relaxed cells. Dashed ticks: 2×2×2 single points on the Γ geometries.", ha="center", va="bottom", fontsize=7, color=INK2)
ax.set_xlim(-0.55, 2.75); fig.tight_layout(rect=(0, 0.04, 1, 1)); fig.savefig("Fig2_formation_energies_v4.png"); fig.savefig("Fig2_formation_energies_v4.pdf")

# ---------- Figure 3: total and absolute magnetisation ----------
systems = ["Pristine\nperfect", "Pr_perfect", "Pr_VO", "Rb_perfect", "Rb_VO", "O$_2$ (box)"]
m_tot = [0.00, 0.00, 0.00, 1.00, 0.97, 2.00]     # |m|, signed total magnetisation magnitude
m_abs = [0.00, 0.00, 0.00, 1.00, 1.21, 2.00]     # m_abs, absolute magnetisation
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
fig.tight_layout(); fig.savefig("Fig3_magnetisation_v4.png"); fig.savefig("Fig3_magnetisation_v4.pdf")
print("figures written")
