"""Figure 4 and Figures S1-S2 of manuscript v4, plotted directly from the projwfc.x sums
exported by the author (data/PDOS_*.csv: E - E_F in eV, states/eV, Gaussian broadening
degauss = 0.01 Ry, 2x2x2 NSCF with tetrahedron occupations).  Nothing is smoothed,
clipped or rescaled except where a label says so.

Figure 4  : spin-resolved PDOS of Pr_VO and Rb_VO (full window + zoom on E_F).
Figure S1 : Loewdin site spin polarisations of Rb_VO against distance from Rb (data/lowdin_Rb_VO.csv).
Figure S2 : spin-summed PDOS of both cells.
The Rb pseudopotential has no d projector (projwfc.x lists Rb 4S only), so no dopant-d curve is
drawn for Rb_VO; the corresponding CSV column is identically zero."""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

S1, S2, S3 = "#2a78d6", "#eb6834", "#1baf7a"
TI_C, O_C, PR_C, RB_C = S1, "#b2182b", S2, S3   # one key for every figure: Ti blue, O red, Pr orange, Rb green
INK, INK2, GRID, TOT = "#0b0b0b", "#52514e", "#d9d8d4", "#8a8985"
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9, "axes.edgecolor": INK2,
                     "axes.labelcolor": INK, "xtick.color": INK, "ytick.color": INK})
PR_SCALE = 5.0   # Pr-5d is drawn x5 so that it is visible on the same axis

load = lambda f: np.genfromtxt(f, delimiter=",", names=True)
spin = {"Pr_VO": load("data/PDOS_Pr_VO_spin.csv"), "Rb_VO": load("data/PDOS_Rb_VO_spin.csv")}
summ = {"Pr_VO": load("data/PDOS_Pr_VO.csv"), "Rb_VO": load("data/PDOS_Rb_VO.csv")}
assert np.all(summ["Rb_VO"]["Rb_d"] == 0), "Rb_d column expected to be zero (no Rb d projector)"
EF = {"Pr_VO": 10.306, "Rb_VO": 7.144}   # NSCF Fermi energies (eV) printed by pw.x


def integ(d, col, a, b):
    E = d["E_minus_EF_eV"]; m = (E > a) & (E <= b)
    return d[col][m].sum() * (E[1] - E[0])


def spin_panel(ax, d, name, xlim, zoom=False):
    E = d["E_minus_EF_eV"]
    ax.fill_between(E, 0, d["Ti3d_up"], color=TI_C, alpha=0.30, lw=0)
    ax.fill_between(E, 0, -d["Ti3d_dn"], color=TI_C, alpha=0.30, lw=0)
    ax.plot(E, d["Ti3d_up"], color=TI_C, lw=1.1, label="Ti-3d")
    ax.plot(E, -d["Ti3d_dn"], color=TI_C, lw=1.1)
    ax.plot(E, d["O2p_up"], color=O_C, lw=1.1, label="O-2p")
    ax.plot(E, -d["O2p_dn"], color=O_C, lw=1.1)
    if name == "Pr_VO":
        ax.plot(E, PR_SCALE * d["Prd_up"], color=PR_C, lw=1.0, ls=(0, (3, 1.5)), label=f"Pr-5d (×{PR_SCALE:.0f})")
        ax.plot(E, -PR_SCALE * d["Prd_dn"], color=PR_C, lw=1.0, ls=(0, (3, 1.5)))
    ax.plot(E, d["Total_up"], color=TOT, lw=0.7, label="total")
    ax.plot(E, -d["Total_dn"], color=TOT, lw=0.7)
    ax.axhline(0, color=INK2, lw=0.6)
    ax.axvline(0, color=INK, lw=0.8, ls=(0, (4, 3)))
    ax.set_xlim(*xlim)
    for s in ["top", "right"]:
        ax.spines[s].set_visible(False)


fig = plt.figure(figsize=(7.2, 6.4), dpi=300)
gs = fig.add_gridspec(2, 2, width_ratios=[3.1, 1.0], wspace=0.28, hspace=0.38)
panels = [("Pr_VO", "(a) Pr_VO", "(b)"), ("Rb_VO", "(c) Rb_VO", "(d)")]
for row, (name, lab, zlab) in enumerate(panels):
    d = spin[name]
    ax = fig.add_subplot(gs[row, 0]); spin_panel(ax, d, name, (-6.5, 4.3))
    ax.set_ylim(-37, 37); ax.set_ylabel("PDOS (states eV$^{-1}$)\n← spin down   spin up →", fontsize=8.5)
    ax.text(0.01, 0.97, lab, transform=ax.transAxes,
            ha="left", va="top", fontsize=9, fontweight="bold", color=INK)
    if row == 1:
        ax.set_xlabel("$E - E_\\mathrm{F}$ (eV)")
    ax.legend(loc="lower left", fontsize=7.5, frameon=False, ncol=2)
    az = fig.add_subplot(gs[row, 1]); spin_panel(az, d, name, (-1.0, 1.0), zoom=True)
    if name == "Pr_VO":
        az.set_ylim(-4.5, 4.5)
        up, dn = integ(d, "Total_up", -0.6, 0.0), integ(d, "Total_dn", -0.6, 0.0)
        ti = integ(d, "Ti3d_up", -0.6, 0.0) + integ(d, "Ti3d_dn", -0.6, 0.0)
        note = f"occupied,\n−0.6 to 0 eV:\n↑ {up:.2f}  ↓ {dn:.2f}\n{ti / (up + dn):.0%} Ti-3d"
        print("Pr_VO zoom:", note.replace("\n", " "))
    else:
        az.set_ylim(-4.5, 4.5)
        up, dn = integ(d, "Total_up", 0.0, 0.6), integ(d, "Total_dn", 0.0, 0.6)
        o = integ(d, "O2p_dn", 0.0, 0.6)
        note = f"empty,\n0 to 0.6 eV:\n↑ {up:.2f}  ↓ {dn:.2f}\n↓: {o / dn:.0%} O-2p"
        print("Rb_VO zoom:", note.replace("\n", " "))
    az.text(0.03, 0.97, zlab, transform=az.transAxes, fontsize=8.5,
            fontweight="bold", color=INK, va="top")
    if row == 1:
        az.set_xlabel("$E - E_\\mathrm{F}$ (eV)")
fig.savefig("Fig4_PDOS_v5.png", bbox_inches="tight", facecolor="white")
fig.savefig("Fig4_PDOS_v5.pdf", bbox_inches="tight", facecolor="white")
plt.close(fig)

# ---------- Figure S2: spin-summed PDOS ----------
fig, axes = plt.subplots(2, 1, figsize=(6.4, 5.6), dpi=300, sharex=True)
for ax, name, lab in zip(axes, ["Pr_VO", "Rb_VO"], ["(a) Pr_VO", "(b) Rb_VO"]):
    d = summ[name]; E = d["E_minus_EF_eV"]
    ax.fill_between(E, 0, d["Ti_3d"], color=TI_C, alpha=0.30, lw=0)
    ax.plot(E, d["Ti_3d"], color=TI_C, lw=1.1, label="Ti-3d")
    ax.plot(E, d["O_2p"], color=O_C, lw=1.1, label="O-2p")
    if name == "Pr_VO":
        ax.plot(E, PR_SCALE * d["Pr_d"], color=PR_C, lw=1.0, ls=(0, (3, 1.5)), label=f"Pr-5d (×{PR_SCALE:.0f})")
    ax.plot(E, d["Total"], color=TOT, lw=0.7, label="total")
    ax.axvline(0, color=INK, lw=0.8, ls=(0, (4, 3)))
    ax.set_xlim(-6.5, 4.3); ax.set_ylim(0, 72); ax.set_ylabel("PDOS (states eV$^{-1}$)")
    ax.text(0.01, 0.96, lab, transform=ax.transAxes,
            ha="left", va="top", fontsize=9, fontweight="bold")
    for s in ["top", "right"]:
        ax.spines[s].set_visible(False)
axes[1].set_xlabel("$E - E_\\mathrm{F}$ (eV)")
h, l = axes[0].get_legend_handles_labels()
fig.legend(h, [x.replace("(×5)", "(×5, Pr_VO only)") for x in l], loc="upper center", ncol=4, fontsize=7.5, frameon=False)
fig.tight_layout(rect=(0, 0, 1, 0.95)); fig.savefig("FigS2_PDOS_spin_summed_v5.png", facecolor="white"); plt.close(fig)

# ---------- Figure S1: Loewdin site moments of Rb_VO ----------
raw = np.genfromtxt("data/lowdin_Rb_VO.csv", delimiter=",", names=True, dtype=None, encoding=None, skip_header=1)
xyz = np.c_[raw["x_A"], raw["y_A"], raw["z_A"]]
cell = np.array([7.63632, 7.63632, 9.77900])
rb = xyz[raw["species"] == "Rb"][0]
dv = xyz - rb; dv -= cell * np.round(dv / cell); r = np.linalg.norm(dv, axis=1)
fig, ax = plt.subplots(figsize=(5.6, 3.4), dpi=300)
for sp, col, mk in [("O", O_C, "o"), ("Ti", TI_C, "s"), ("Rb", RB_C, "D")]:
    m = raw["species"] == sp
    ax.vlines(r[m], 0, raw["polarisation"][m], color=col, lw=1.0)
    ax.scatter(r[m], raw["polarisation"][m], color=col, marker=mk, s=16, zorder=3, label=sp)
ax.set_ylim(-0.08, 0.66)
ax.axhline(0, color=INK2, lw=0.6)
ax.set_xlabel("Distance from Rb (Å)"); ax.set_ylabel("Löwdin spin polarisation ($\\mu_\\mathrm{B}$)")
ax.legend(frameon=False, fontsize=8, loc="upper right")
for s in ["top", "right"]:
    ax.spines[s].set_visible(False)
fig.tight_layout(); fig.savefig("FigS1_Lowdin_RbVO_v5.png", facecolor="white"); plt.close(fig)
print("written Fig4_PDOS_v5.{png,pdf}, FigS2_PDOS_spin_summed_v5.png, FigS1_Lowdin_RbVO_v5.png")
