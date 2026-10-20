"""Figure 2 of the manuscript (v5, 19 Oct 2026): neutral V_O formation energies at mu_O = 1/2 E(O2).

Bars: Gamma-only relaxed cells (Table 2, relaxed pristine perfect cell). Dashed ticks: 2x2x2 single points
on the Gamma geometries (Table 2). Open diamonds: lowest-energy spin solutions at narrower smearing,
sigma -> 0 estimates (Table S11). All values are computed here from the Ry totals; nothing is fitted.
Written at 5.4 x 3.9 in, 300 dpi (1620 x 1170 px), the size of the figure in the manuscript.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

RY = 13.605693122994
S1, S2, S3 = "#2a78d6", "#eb6834", "#1baf7a"      # validated categorical slots 1-3
INK, INK2, GRID = "#0b0b0b", "#52514e", "#d9d8d4"
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10, "axes.edgecolor": INK2,
                     "axes.labelcolor": INK, "xtick.color": INK, "ytick.color": INK,
                     "svg.hashsalt": "fig2_v5"})

E = {"halfO2": -41.51621,
     # Table 2: Gamma-only, 0.01 Ry smearing (pristine perfect cell relaxed, Section 2.6)
     "Pristine_perfect": -4275.01597, "Pristine_VO": -4233.15036,
     "Pr_perfect": -4576.71224, "Pr_VO": -4535.10106,
     "Rb_perfect": -4330.38890, "Rb_VO": -4289.17135,
     # Table 2 last column: 2x2x2 single points on the Gamma geometries
     "Pr_perfect_222": -4576.62183, "Pr_VO_222": -4535.01814,
     "Rb_perfect_222": -4330.28761, "Rb_VO_222": -4289.08034,
     # Table S11: 0.002 Ry, sigma -> 0 estimates (Pr cells relaxed in their magnetic states)
     "Pr_perfect_n": -4576.70615, "Pr_VO_n": -4535.11739,
     "Rb_perfect_n": -4330.38382, "Rb_VO_n": -4289.17087}
ef = lambda v, p: (E[v] - E[p] + E["halfO2"]) * RY
vals = [ef("Pristine_VO", "Pristine_perfect"), ef("Pr_VO", "Pr_perfect"), ef("Rb_VO", "Rb_perfect")]
vals222 = [None, ef("Pr_VO_222", "Pr_perfect_222"), ef("Rb_VO_222", "Rb_perfect_222")]
valsn = [None, ef("Pr_VO_n", "Pr_perfect_n"), ef("Rb_VO_n", "Rb_perfect_n")]
fmt = lambda v, unit="": (f"{v:+.2f}" + unit).replace("-", "−")
# the values printed in Table 2, Table S11 and the text
assert [fmt(v) for v in vals] == ["+4.75", "+1.29", "−4.06"]
assert [fmt(v) for v in vals222[1:]] == ["+1.19", "−4.20"]
assert [fmt(v) for v in valsn[1:]] == ["+0.99", "−4.13"]
assert f"{vals[1] - vals[2]:.2f}" == "5.36" and f"{valsn[1] - valsn[2]:.2f}" == "5.11"

labels = ["Pristine TiO$_2$", "Pr$_{\\mathrm{Ti}}$", "Rb$_{\\mathrm{Ti}}$"]
fig, ax = plt.subplots(figsize=(5.4, 3.9), dpi=300)
x = np.arange(3); BW = 0.5
bars = ax.bar(x, vals, width=BW, color=[S1, S2, S3], edgecolor="none", zorder=3)
for i in (1, 2):
    ax.plot([x[i] - BW / 2, x[i] + BW / 2], [vals222[i]] * 2, color=INK, lw=1.2, ls=(0, (3, 2)), zorder=4)
    ax.plot(x[i] + BW / 2 + 0.16, valsn[i], marker="D", ms=5.5, mfc="white", mec=INK, mew=1.0, zorder=5)
    ax.text(x[i] + BW / 2 + 0.27, valsn[i], fmt(valsn[i]), fontsize=7.5, color=INK2, va="center", ha="left")
ax.axhline(0, color=INK2, lw=0.8, zorder=2)
ax.set_ylabel("$E_{\\mathrm{f}}(\\mathrm{V}_{\\mathrm{O}}^{0})$ (eV)")
ax.set_xticks(x); ax.set_xticklabels(labels)
ax.set_ylim(-5.2, 5.6); ax.yaxis.grid(True, color=GRID, lw=0.6, zorder=0); ax.set_axisbelow(True)
for s in ["top", "right"]: ax.spines[s].set_visible(False)
for b, v in zip(bars, vals):
    if v > 0:
        ax.text(b.get_x() + b.get_width() / 2, v + 0.18, fmt(v, " eV"), ha="center", va="bottom", color=INK,
                fontsize=9.5, fontweight="bold")
    else:
        ax.text(b.get_x() - 0.05, v / 2, fmt(v, " eV"), ha="right", va="center", color=INK,   # beside the bar
                fontsize=9.5, fontweight="bold", bbox=dict(fc="white", ec="none", pad=1.5))
ax.text(x[1] - BW / 2 - 0.05, vals222[1], fmt(vals222[1]), fontsize=7.5, color=INK2, va="center",
        ha="right")
ax.text(x[2] - BW / 2 - 0.05, vals222[2] - 0.2, fmt(vals222[2]), fontsize=7.5, color=INK2, va="top",
        ha="right")
ax.set_xlim(-0.55, 2.95); fig.tight_layout()

# layout check: no text overlaps another text, a bar, a tick or a marker
fig.canvas.draw(); r = fig.canvas.get_renderer()
texts = [t for t in ax.texts + fig.texts + ax.get_xticklabels() if t.get_text().strip()]
obst = [(b.get_window_extent(r), "bar") for b in ax.patches] + [(l.get_window_extent(r), "line") for l in ax.lines[:-1]]
hit = lambda A, B: A.x0 < B.x1 - 1 and B.x0 < A.x1 - 1 and A.y0 < B.y1 - 1 and B.y0 < A.y1 - 1
bad = []
for i, t in enumerate(texts):
    A = t.get_window_extent(r)
    bad += [f"{t.get_text()!r} / {u.get_text()!r}" for u in texts[i + 1:] if hit(A, u.get_window_extent(r))]
    bad += [f"{t.get_text()!r} on {k}" for B, k in obst if hit(A, B)]
assert not bad, "\n".join(bad)

fig.savefig("Fig2_formation_energies_v5.png", facecolor="white")
fig.savefig("Fig2_formation_energies_v5.pdf", metadata={"CreationDate": None})
print("written Fig2_formation_energies_v5.{png,pdf}:", ", ".join(fmt(v) for v in vals),
      "| 2x2x2", ", ".join(fmt(v) for v in vals222[1:]), "| narrow", ", ".join(fmt(v) for v in valsn[1:]))
