"""Figure 2 of the manuscript (19 Oct 2026 version): neutral V_O formation energies at mu_O = 1/2 E(O2).

Bars: Gamma-only relaxed cells (Table 2, relaxed pristine perfect cell), with their values and the Pr-Rb contrast.
Everything else (2x2x2 single points, narrower-smearing values, conditions) is stated in the caption.
All values are computed here from the Ry totals; nothing is fitted.
Written at 5.4 x 3.9 in, 300 dpi (1620 x 1170 px), the size of the figure in the manuscript.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

RY = 13.605693122994
TI_C, PR_C, RB_C = "#2a78d6", "#eb6834", "#1baf7a"   # same key as every figure: TiO2 blue, Pr orange, Rb green
INK, INK2 = "#0b0b0b", "#52514e"
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10, "axes.edgecolor": INK2,
                     "axes.labelcolor": INK, "xtick.color": INK, "ytick.color": INK})

E = {"halfO2": -41.51621,
     # Table 2: Gamma-only, 0.01 Ry smearing (pristine perfect cell relaxed, Section 2.6)
     "Pristine_perfect": -4275.01597, "Pristine_VO": -4233.15036,
     "Pr_perfect": -4576.71224, "Pr_VO": -4535.10106,
     "Rb_perfect": -4330.38890, "Rb_VO": -4289.17135,
     # quoted in the caption: Table 2 last column (2x2x2) and Table S11 (0.002 Ry, sigma -> 0)
     "Pr_perfect_222": -4576.62183, "Pr_VO_222": -4535.01814,
     "Rb_perfect_222": -4330.28761, "Rb_VO_222": -4289.08034,
     "Pr_perfect_n": -4576.70615, "Pr_VO_n": -4535.11739,
     "Rb_perfect_n": -4330.38382, "Rb_VO_n": -4289.17087}
ef = lambda v, p: (E[v] - E[p] + E["halfO2"]) * RY
vals = [ef("Pristine_VO", "Pristine_perfect"), ef("Pr_VO", "Pr_perfect"), ef("Rb_VO", "Rb_perfect")]
fmt = lambda v: f"{v:+.2f}".replace("-", "−")
assert [fmt(v) for v in vals] == ["+4.75", "+1.29", "−4.06"]
assert f"{vals[1] - vals[2]:.2f}" == "5.36"
# the caption values
assert [fmt(ef("Pr_VO_222", "Pr_perfect_222")), fmt(ef("Rb_VO_222", "Rb_perfect_222"))] == ["+1.19", "−4.20"]
assert [fmt(ef("Pr_VO_n", "Pr_perfect_n")), fmt(ef("Rb_VO_n", "Rb_perfect_n"))] == ["+0.99", "−4.13"]

fig, ax = plt.subplots(figsize=(5.4, 3.9), dpi=300)
x = np.arange(3); BW = 0.5
ax.bar(x, vals, width=BW, color=[TI_C, PR_C, RB_C], edgecolor="none", zorder=3)
ax.axhline(0, color=INK2, lw=0.8, zorder=2)
for xi, v in zip(x, vals):
    ax.text(xi, v + (0.15 if v > 0 else -0.15), fmt(v), ha="center", va="bottom" if v > 0 else "top",
            fontsize=10, fontweight="bold", color=INK, zorder=4)
XA = 2.55                                              # Pr-Rb contrast
ax.plot([x[1] + BW / 2, XA + 0.06], [vals[1]] * 2, color=INK2, lw=0.8, ls=(0, (3, 2)), zorder=2)
ax.plot([x[2] + BW / 2, XA + 0.06], [vals[2]] * 2, color=INK2, lw=0.8, ls=(0, (3, 2)), zorder=2)
ax.annotate("", xy=(XA, vals[2]), xytext=(XA, vals[1]),
            arrowprops=dict(arrowstyle="<->", color=INK, lw=1.0, shrinkA=0, shrinkB=0))
ax.text(XA + 0.08, (vals[1] + vals[2]) / 2, f"Δ = {vals[1] - vals[2]:.2f} eV", fontsize=10, color=INK,
        ha="left", va="center")
ax.set_ylabel("$E_{\\mathrm{f}}$ (eV)")
ax.set_xticks(x)
ax.set_xticklabels(["TiO$_2$", "TiO$_2$:Pr$^{3{+}}$", "TiO$_2$:Rb$^{+}$"])
ax.tick_params(axis="x", length=0, pad=6)
ax.set_ylim(-6, 6); ax.set_yticks(range(-6, 7, 2))
ax.set_yticklabels([str(t).replace("-", "−") for t in range(-6, 7, 2)])
ax.set_xlim(-0.5, 3.35)
for s in ["top", "right"]: ax.spines[s].set_visible(False)
fig.tight_layout()

# layout check: no text overlaps another text, a bar or a line
fig.canvas.draw(); r = fig.canvas.get_renderer()
texts = [t for t in ax.texts + ax.get_xticklabels() if t.get_text().strip()]
obst = [(b.get_window_extent(r), "bar") for b in ax.patches] + [(l.get_window_extent(r), "line") for l in ax.lines]
hit = lambda A, B: A.x0 < B.x1 - 1 and B.x0 < A.x1 - 1 and A.y0 < B.y1 - 1 and B.y0 < A.y1 - 1
bad = []
for i, t in enumerate(texts):
    A = t.get_window_extent(r)
    bad += [f"{t.get_text()!r} / {u.get_text()!r}" for u in texts[i + 1:] if hit(A, u.get_window_extent(r))]
    bad += [f"{t.get_text()!r} on {k}" for B, k in obst if hit(A, B)]
assert not bad, "\n".join(bad)

fig.savefig("Fig2_formation_energies_v5.png", facecolor="white")
fig.savefig("Fig2_formation_energies_v5.pdf", metadata={"CreationDate": None})
print("written Fig2_formation_energies_v5.{png,pdf}:", ", ".join(fmt(v) for v in vals))
