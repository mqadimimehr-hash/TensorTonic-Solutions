"""Graphical abstract, v5 (19 Oct 2026 manuscript). Drawn from the numbers below; no generated imagery.

Every value is taken from the 19 Oct manuscript: Table 2 (E_f), Section 3.3 / Table S11 (narrower
smearing), Section 3.7 (contrast tests), Table 1 (charge bookkeeping), Sections 3.1 and 3.6 (Rb hole).
Size: 13 x 5 cm (Elsevier graphical abstract), vector PDF/SVG plus 600 dpi PNG/TIFF.
"""
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Wedge, FancyBboxPatch, FancyArrowPatch

# --- data: total energies in Ry, E_f = E(V_O) - E(perfect) + 1/2 E(O2) -------------------------
RY = 13.605693122994
HALF_O2 = -41.51621
TOT = {"pristine": (-4275.01597, -4233.15036),        # Table 2 (perfect, V_O), Gamma, 0.01 Ry smearing
       "Pr": (-4576.71224, -4535.10106),
       "Rb": (-4330.38890, -4289.17135)}
TOT_NARROW = {"Pr": (-4576.70615, -4535.11739),       # Table S11, 0.002 Ry, Pr cells relaxed (magnetic)
              "Rb": (-4330.38382, -4289.17087)}       # Table S11, 0.002 Ry, production geometries
ef = lambda p, v: (v - p + HALF_O2) * RY
EF = {k: ef(*TOT[k]) for k in TOT}
EF_PR_NARROW = ef(*TOT_NARROW["Pr"])
CONTRAST = EF["Pr"] - EF["Rb"]
CONTRAST_NARROW = EF_PR_NARROW - ef(*TOT_NARROW["Rb"])
TEST_MAX = 0.04                                       # Section 3.7: k-mesh +0.04, cut-off <= 0.03, D3 0.005
HOLES = {"pristine": 0, "Pr": 1, "Rb": 3}             # formal holes per cell (Table 1)
# the rounded values printed in the manuscript
assert [f"{EF[k]:+.2f}" for k in TOT] == ["+4.75", "+1.29", "-4.06"]
assert (f"{CONTRAST:.2f}", f"{EF_PR_NARROW:+.2f}", f"{CONTRAST_NARROW:.2f}") == ("5.36", "+0.99", "5.11")

# --- style (validated categorical slots 1-3, as in Figure 2; status colours only with an icon) -
S1, S2, S3 = "#2a78d6", "#eb6834", "#1baf7a"
INK, INK2, GRID, PANEL = "#0b0b0b", "#52514e", "#b9b8b2", "#f3f2ee"
GOOD, WARN = "#0ca30c", "#fab219"
TI, OX = "#9b9a94", "#e34948"
plt.rcParams.update({"font.family": "DejaVu Sans", "mathtext.fontset": "dejavusans",
                     "pdf.fonttype": 42, "svg.fonttype": "path", "axes.linewidth": 0.5})
MINUS = lambda s: s.replace("-", "−")

W, H = 13.0, 5.0                                       # cm; one data unit of the overlay = 1 cm
fig = plt.figure(figsize=(W / 2.54, H / 2.54))
ov = fig.add_axes([0, 0, 1, 1]); ov.set_xlim(0, W); ov.set_ylim(0, H); ov.axis("off")

FH, FB, FN = 5.8, 5.0, 4.7                              # header, body, note sizes (pt)

def T(x, y, s, size=FB, color=INK, **kw):
    return ov.text(x, y, s, fontsize=size, color=color, **kw)

def hole(x, y, r=0.062):
    ov.add_patch(Circle((x, y), r, fc="white", ec=INK, lw=0.7, zorder=5))

def electron(x, y, r=0.062):
    ov.add_patch(Circle((x, y), r, fc=INK, ec=INK, lw=0.7, zorder=5))

def dopant(x, y, r=0.095):                             # half Pr colour, half Rb colour: "Pr or Rb"
    ov.add_patch(Wedge((x, y), r, 45, 225, fc=S2, ec="white", lw=0.4, zorder=4))
    ov.add_patch(Wedge((x, y), r, 225, 405, fc=S3, ec="white", lw=0.4, zorder=4))

def lattice(cx, cy, nx=4, ny=3, a=0.36, dop=(1, 1), vac=False):
    """Schematic Ti-O net (not the anatase geometry): Ti at nodes, O on the bonds."""
    xs = [cx + (i - (nx - 1) / 2) * a for i in range(nx)]
    ys = [cy + (j - (ny - 1) / 2) * a for j in range(ny)]
    for y in ys: ov.plot([xs[0], xs[-1]], [y, y], color=GRID, lw=0.5, zorder=1)
    for x in xs: ov.plot([x, x], [ys[0], ys[-1]], color=GRID, lw=0.5, zorder=1)
    vx, vy = xs[dop[0]] + a / 2, ys[dop[1]]           # first-shell O of the dopant
    for i, x in enumerate(xs):
        for j, y in enumerate(ys):
            if i < nx - 1 and not (vac and (i, j) == dop):
                ov.add_patch(Circle((x + a / 2, y), 0.045, fc=OX, ec="none", zorder=2))
            if j < ny - 1:
                ov.add_patch(Circle((x, y + a / 2), 0.045, fc=OX, ec="none", zorder=2))
            if (i, j) == dop: dopant(x, y)
            else: ov.add_patch(Circle((x, y), 0.068, fc=TI, ec="none", zorder=3))
    if vac:
        ov.add_patch(Circle((vx, vy), 0.068, fc=PANEL, ec=INK, lw=0.6, ls=(0, (2, 1.5)), zorder=4))
    return xs, ys, (vx, vy)

def panel(x0, x1, n, title):
    ov.add_patch(FancyBboxPatch((x0, 0.08), x1 - x0, 4.20, boxstyle="round,pad=0,rounding_size=0.12",
                                fc=PANEL, ec="none", zorder=0))
    ov.add_patch(Circle((x0 + 0.19, 4.05), 0.11, fc=INK, ec="none", zorder=2))
    T(x0 + 0.19, 4.045, str(n), 5.4, "white", ha="center", va="center", fontweight="bold", zorder=3)
    T(x0 + 0.36, 4.05, title, FH, ha="left", va="center", fontweight="bold")

def status(x, y, ok):
    ov.add_patch(Circle((x, y), 0.095, fc=GOOD if ok else WARN, ec="none", zorder=3))
    T(x, y - 0.005, "✓" if ok else "!", 5.4, "white" if ok else INK, ha="center", va="center",
      fontweight="bold", zorder=4)

# --- title: the one central finding ---------------------------------------------------------------
T(W / 2, 4.71, "Pr and Rb both lower the O-vacancy cost in anatase TiO$_2$; only Rb makes it spontaneous",
  6.6, ha="center", va="center", fontweight="bold")
T(W / 2, 4.45, "Spin-polarised PBE+U, U(Ti-3d) = 3.5 eV  ·  oxygen-rich reference "
  "$\\mu_\\mathrm{O} = \\frac{1}{2}E(\\mathrm{O_2})$  ·  one dopant per 48-atom cell", 5.0, INK2,
  ha="center", va="center")

# panel x-ranges (cm)
P = [(0.08, 1.78), (1.87, 3.57), (3.66, 6.41), (6.50, 9.60), (9.69, 12.92)]

# 1 Build cell -------------------------------------------------------------------------------------
x0, x1 = P[0]; panel(x0, x1, 1, "Build cell")
lattice((x0 + x1) / 2, 3.08)
T((x0 + x1) / 2, 2.58, "schematic", FN, INK2, ha="center", va="center")
ly = 2.27
ov.add_patch(Circle((x0 + 0.20, ly), 0.06, fc=TI, ec="none")); T(x0 + 0.31, ly, "Ti", FB, va="center")
ov.add_patch(Circle((x0 + 0.62, ly), 0.045, fc=OX, ec="none")); T(x0 + 0.71, ly, "O", FB, va="center")
dopant(x0 + 1.00, ly, 0.075); T(x0 + 1.10, ly, "Pr/Rb", FB, va="center")
T(x0 + 0.13, 1.95, "2×2×1 anatase,\n48 atoms\n\nOne Ti → Pr$^{3+}$\nor Rb$^{+}$\n(separate cells)",
  FB, va="top", linespacing=1.3)

# 2 Remove one O -----------------------------------------------------------------------------------
x0, x1 = P[1]; panel(x0, x1, 2, "Remove O")
xs, ys, (vx, vy) = lattice((x0 + x1) / 2, 3.08, vac=True)
T(vx, vy - 0.15, "V$_\\mathrm{O}$", FB, ha="center", va="top", fontweight="bold",
  bbox=dict(fc=PANEL, ec="none", pad=0.2))
T(x0 + 0.13, 2.30, "First-shell O of\nthe dopant", FB, va="top", linespacing=1.3)
T(x0 + 0.13, 1.55, "V$_\\mathrm{O}$ releases", FB, va="center")
electron(x0 + 0.22, 1.22); electron(x0 + 0.40, 1.22)
T(x0 + 0.52, 1.22, "2 e$^-$", FB, va="center")

# 3 Protocol and tests -----------------------------------------------------------------------------
x0, x1 = P[2]; panel(x0, x1, 3, "Protocol")
for k, s in enumerate(["Γ-only relaxations, 40 Ry",
                       "$E_\\mathrm{f} = E(V_\\mathrm{O}) - E(\\mathrm{perfect})$",
                       "$\\quad\\quad + \\frac{1}{2}E(\\mathrm{O_2})$"]):
    T(x0 + 0.13, 3.72 - 0.24 * k, s, FB, va="center")
ov.plot([x0 + 0.13, x1 - 0.13], [3.02, 3.02], color=GRID, lw=0.5)
T(x0 + 0.13, 2.80, f"Pr–Rb contrast, {CONTRAST:.2f} eV", FB, va="center", fontweight="bold")
status(x0 + 0.23, 2.40, True)
T(x0 + 0.40, 2.40, f"2×2×2 k-mesh, 55/70 Ry,\nD3: shifts ≤ {TEST_MAX:.2f} eV", FB, va="center", linespacing=1.25)
status(x0 + 0.23, 1.70, False)
T(x0 + 0.40, 1.70, "smearing, U(O-2p):\nPr spin state changes", FB, va="center", linespacing=1.25)
T(x0 + 0.40, 1.10, MINUS(f"narrower smearing:\nPr {EF_PR_NARROW:+.2f} eV,\ncontrast {CONTRAST_NARROW:.2f} eV"),
  FN, INK2, va="center", linespacing=1.25)

# 4 Charge bookkeeping -----------------------------------------------------------------------------
x0, x1 = P[3]; panel(x0, x1, 4, "Charge bookkeeping")
hole(x0 + 0.22, 3.72); T(x0 + 0.33, 3.72, "hole h$^+$", FB, va="center")
electron(x0 + 1.32, 3.72); T(x0 + 1.43, 3.72, "electron e$^-$", FB, va="center")
DX = 0.17
CD, CP, CE, CA, CR = 0.55, 0.92, 1.10, 1.50, 1.72      # columns (cm from panel edge): dopant, +, V_O, ->, net

def row(y, label, colour, n_h, result_is_hole, result, note, heads=False):
    ov.add_patch(Circle((x0 + 0.22, y + 0.42), 0.08, fc=colour, ec="none"))
    T(x0 + 0.36, y + 0.42, label, 5.4, va="center", fontweight="bold")
    for k in range(n_h): hole(x0 + CD + (k - (n_h - 1) / 2) * DX, y)
    T(x0 + CP, y, "+", 5.6, ha="center", va="center")
    electron(x0 + CE, y); electron(x0 + CE + DX, y)
    T(x0 + CA, y, "\u2192", 6, ha="center", va="center")
    (hole if result_is_hole else electron)(x0 + CR, y)
    T(x0 + CR + 0.13, y, result, FB, va="center", fontweight="bold")
    if heads:
        for xx, s in [(CD, "dopant"), (CE + DX / 2, "V$_\\mathrm{O}$"), (CR, "net")]:
            T(x0 + xx, y + 0.19, s, FN, INK2, ha="center", va="center")
    T(x0 + 0.13, y - 0.17, note, FN, INK2, va="top", linespacing=1.25)

row(2.78, "Pr$^{3+}$", S2, HOLES["Pr"], False, "1 e$^-$ left",
    "extra e$^-$ in Ti-3d conduction band", heads=True)
row(1.55, "Rb$^{+}$", S3, HOLES["Rb"], True, "1 h$^+$ left",
    "residual h$^+$ on O-2p: 0.59 $\\mu_\\mathrm{B}$ on\none O bonded to Rb")
T(x0 + 0.13, 0.42, "Rb shifts 1.27 Å towards V$_\\mathrm{O}$", FN, INK2, va="center")

# 5 Result -----------------------------------------------------------------------------------------
x0, x1 = P[4]; panel(x0, x1, 5, "Result: $E_\\mathrm{f}(V_\\mathrm{O})$ (eV)")
ax = fig.add_axes([(x0 + 0.42) / W, 0.92 / H, 2.72 / W, 2.82 / H])
keys = ["pristine", "Pr", "Rb"]; vals = [EF[k] for k in keys]; X = [0, 1.25, 2.35]; BW = 0.5
ax.bar(X, vals, width=BW, color=[S1, S2, S3], zorder=3)
ax.set_facecolor("none")
ax.axhline(0, color=INK2, lw=0.6, zorder=4)
ax.set_xlim(-0.45, 3.22); ax.set_ylim(-5.4, 6.0)
ax.set_yticks([-4, -2, 0, 2, 4]); ax.set_yticklabels([MINUS(f"{t:d}") for t in [-4, -2, 0, 2, 4]])
ax.tick_params(axis="y", labelsize=FN, length=2, width=0.5, colors=INK2, pad=1.5)
ax.yaxis.grid(True, color="#d9d8d4", lw=0.4, zorder=0)
ax.set_xticks(X)
ax.set_xticklabels([f"{n}\n{HOLES[k]} h$^+$" for n, k in zip(["pristine", "Pr$^{3+}$", "Rb$^{+}$"], keys)],
                   fontsize=FB, color=INK, linespacing=1.15)
ax.tick_params(axis="x", length=0, pad=2)
for s in ["top", "right", "bottom"]: ax.spines[s].set_visible(False)
ax.spines["left"].set_color(INK2)
for x, v in zip(X, vals):
    ax.text(x, v + (0.25 if v > 0 else -0.25), MINUS(f"{v:+.2f}"), ha="center",
            va="bottom" if v > 0 else "top", fontsize=5.4, fontweight="bold", color=INK, zorder=5)
ax.plot([X[1] - BW / 2, X[1] + BW / 2], [EF_PR_NARROW] * 2, color=INK, lw=0.8, ls=(0, (2.2, 1.4)), zorder=5)
ax.text(X[1] - BW / 2 - 0.04, EF_PR_NARROW, MINUS(f"{EF_PR_NARROW:+.2f}"), fontsize=FN, color=INK2,
        va="center", ha="right")
XA = 2.80
ax.annotate("", xy=(XA, EF["Rb"]), xytext=(XA, EF["Pr"]),
            arrowprops=dict(arrowstyle="<->", color=INK, lw=0.6, shrinkA=0, shrinkB=0))
for y0, xa in [(EF["Pr"], X[1] + BW / 2), (EF["Rb"], X[2] + BW / 2)]:
    ax.plot([xa, XA + 0.05], [y0, y0], color=INK2, lw=0.4, ls=(0, (1, 1)), zorder=2)
ax.text(XA + 0.09, (EF["Pr"] + EF["Rb"]) / 2, f"Δ {CONTRAST:.2f} eV", rotation=90, fontsize=FB,
        color=INK, ha="left", va="center")
ax.text(0.62, -0.45, "below 0:\nspontaneous", fontsize=FN, color=INK2, ha="center", va="top", linespacing=1.15)
T(x0 + 0.13, 0.22, "Dashed: Pr, narrower smearing", FN, INK2, va="center")

for ext, kw in [("pdf", {}), ("svg", {}), ("png", {"dpi": 600}), ("tiff", {"dpi": 600, "pil_kwargs": {"compression": "tiff_lzw"}})]:
    fig.savefig(f"Graphical_Abstract_v5.{ext}", **kw)
print("Graphical_Abstract_v5.{pdf,svg,png,tiff} written")
