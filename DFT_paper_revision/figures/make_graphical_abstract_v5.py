"""Graphical abstract, v5 (19 Oct 2026 manuscript). Drawn from the numbers below; no generated imagery.

Five steps as in the author's design, with text kept to 7 pt or larger so that it stays readable at the
Elsevier display size (13 x 5 cm at 96 dpi). The variant with every qualifier (smaller type, for slides
or enlarged viewing) is make_graphical_abstract_v5_detailed.py.
Values: Table 2 (E_f), Table S11 (narrower smearing), Section 3.7 (contrast tests), Table 1 (formal
carriers), Sections 3.3 and 3.6 (where the carriers sit).
Size 13 x 5 cm; vector PDF/SVG plus 600 dpi RGB PNG/TIFF. The script stops if a printed number differs
from the manuscript, if any text is set below 7 pt, leaves its panel, or overlaps another text, a line, a
marker or a bar. Charges and subscripts are mathtext scripts (0.7x the base size; Unicode superscript
glyphs are about 0.56x), and mu_O = E(O2)/2 is written with full-size digits.
"""
import io, os
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Wedge, FancyBboxPatch
from PIL import Image

OUT = os.path.dirname(os.path.abspath(__file__))

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
EF_NARROW = {k: ef(*TOT_NARROW[k]) for k in TOT_NARROW}
CONTRAST = EF["Pr"] - EF["Rb"]
TEST_MAX = 0.04          # Section 3.7, change in the Pr-Rb contrast: k-mesh +0.038, cut-off 0.006, D3 +0.005 eV
assert [f"{EF[k]:+.2f}" for k in TOT] == ["+4.75", "+1.29", "-4.06"]
assert [f"{EF_NARROW[k]:+.2f}" for k in TOT_NARROW] == ["+0.99", "-4.13"]
assert f"{CONTRAST:.2f}" == "5.36"

# --- style (validated categorical slots 1-3, as in Figure 2; status colours only with an icon) -
S1, S2, S3 = "#2a78d6", "#eb6834", "#1baf7a"
INK, INK2, GRID, PANEL = "#0b0b0b", "#52514e", "#b9b8b2", "#f3f2ee"
GOOD, WARN = "#0ca30c", "#fab219"
TI, OX = "#9b9a94", "#e34948"
plt.rcParams.update({"font.family": "DejaVu Sans", "mathtext.fontset": "dejavusans",
                     "pdf.fonttype": 42, "svg.fonttype": "path", "svg.hashsalt": "ga_v5", "axes.linewidth": 0.6})
MINUS = lambda s: s.replace("-", "−")
VO = "V$_\\mathrm{O}$"
FT, FH, FB, FN = 8.5, 7.5, 7.5, 7.0                    # title, header, body, note sizes (pt)

W, H = 13.0, 5.0                                       # cm; one data unit of the overlay = 1 cm
fig = plt.figure(figsize=(W / 2.54, H / 2.54))
ov = fig.add_axes([0, 0, 1, 1]); ov.set_xlim(0, W); ov.set_ylim(0, H); ov.axis("off")

def T(x, y, s, size=FB, color=INK, **kw):
    return ov.text(x, y, s, fontsize=size, color=color, **kw)

def hole(x, y, r=0.075):
    ov.add_patch(Circle((x, y), r, fc="white", ec=INK, lw=0.9, zorder=5))

def electron(x, y, r=0.075):
    ov.add_patch(Circle((x, y), r, fc=INK, ec=INK, lw=0.9, zorder=5))

def dopant(x, y, r=0.115):                             # half Pr colour, half Rb colour: "Pr or Rb"
    ov.add_patch(Wedge((x, y), r, 45, 225, fc=S2, ec="white", lw=0.5, zorder=4))
    ov.add_patch(Wedge((x, y), r, 225, 405, fc=S3, ec="white", lw=0.5, zorder=4))

def lattice(cx, cy, nx=4, ny=3, a=0.40, dop=(1, 1), vac=False):
    """Schematic Ti-O net (not the anatase geometry): Ti at nodes, O on the bonds."""
    xs = [cx + (i - (nx - 1) / 2) * a for i in range(nx)]
    ys = [cy + (j - (ny - 1) / 2) * a for j in range(ny)]
    for y in ys: ov.plot([xs[0], xs[-1]], [y, y], color=GRID, lw=0.6, zorder=1)
    for x in xs: ov.plot([x, x], [ys[0], ys[-1]], color=GRID, lw=0.6, zorder=1)
    vx, vy = xs[dop[0]] + a / 2, ys[dop[1]]           # first-shell O of the dopant
    for i, x in enumerate(xs):
        for j, y in enumerate(ys):
            if i < nx - 1 and not (vac and (i, j) == dop):
                ov.add_patch(Circle((x + a / 2, y), 0.052, fc=OX, ec="none", zorder=2))
            if j < ny - 1:
                ov.add_patch(Circle((x, y + a / 2), 0.052, fc=OX, ec="none", zorder=2))
            if (i, j) == dop: dopant(x, y)
            else: ov.add_patch(Circle((x, y), 0.078, fc=TI, ec="none", zorder=3))
    if vac:
        ov.add_patch(Circle((vx, vy), 0.078, fc=PANEL, ec=INK, lw=0.8, ls=(0, (2, 1.5)), zorder=4))

def panel(x0, x1, n, title):
    ov.add_patch(FancyBboxPatch((x0, 0.08), x1 - x0, 4.02, boxstyle="round,pad=0,rounding_size=0.12",
                                fc=PANEL, ec="none", zorder=0))
    ov.add_patch(Circle((x0 + 0.21, 3.84), 0.14, fc=INK, ec="none", zorder=2))
    T(x0 + 0.21, 3.835, str(n), 7, "white", ha="center", va="center", fontweight="bold", zorder=3)
    T(x0 + 0.42, 3.84, title, FH, ha="left", va="center", fontweight="bold")

def status(x, y, ok):
    ov.add_patch(Circle((x, y), 0.12, fc=GOOD if ok else WARN, ec="none", zorder=3))
    T(x, y - 0.005, "✓" if ok else "!", 7, "white" if ok else INK, ha="center", va="center",
      fontweight="bold", zorder=4)

# --- title: the one central finding, with its condition ------------------------------------------
T(W / 2, 4.72, "Pr and Rb lower the O-vacancy cost; only Rb makes it spontaneous", FT,
  ha="center", va="center", fontweight="bold")
T(W / 2, 4.37, "Anatase TiO$_2$, PBE+U, neutral " + VO + ", O-rich limit "
  "$\\mu_\\mathrm{O} = E(\\mathrm{O_2})/2$", FN, INK2, ha="center", va="center")

P = [(0.08, 1.84), (1.92, 3.88), (3.96, 6.46), (6.54, 9.18), (9.26, 12.92)]   # panel x-ranges (cm)

# 1 Build cell -------------------------------------------------------------------------------------
x0, x1 = P[0]; panel(x0, x1, 1, "Dope")
lattice((x0 + x1) / 2, 2.82)
T(x0 + 0.14, 2.05, "Ti → Pr$^{3{+}}$\nor Rb$^{+}$;\n1 per cell,\n48 atoms", FB, va="top", linespacing=1.25)

# 2 Remove one O -----------------------------------------------------------------------------------
x0, x1 = P[1]; panel(x0, x1, 2, "Remove O")
lattice((x0 + x1) / 2, 2.82, vac=True)
T(x0 + 0.14, 2.05, "Neutral " + VO + "\nreleases", FB, va="top", linespacing=1.25)
electron(x0 + 0.24, 1.18); electron(x0 + 0.44, 1.18)
T(x0 + 0.58, 1.18, "2 e$^{-}$", FB, va="center")

# 3 Protocol and tests -----------------------------------------------------------------------------
x0, x1 = P[2]; panel(x0, x1, 3, "Protocol")
T(x0 + 0.14, 3.55, "U(Ti-3d) 3.5 eV\nΓ-only, 40 Ry", FB, va="top", linespacing=1.25)
status(x0 + 0.24, 2.24, True)
T(x0 + 0.42, 2.24, f"k-mesh, cut-off,\nD3: Pr–Rb Δ\nshifts ≤ {TEST_MAX:.2f} eV", FN, va="center", linespacing=1.25)
status(x0 + 0.24, 1.04, False)
T(x0 + 0.42, 1.04, MINUS(f"smearing: Pr\ncells polarise,\nPr {EF_NARROW['Pr']:+.2f} eV"), FN, va="center",
  linespacing=1.25)

# 4 Charge bookkeeping -----------------------------------------------------------------------------
x0, x1 = P[3]; panel(x0, x1, 4, "Bookkeeping")
hole(x0 + 0.24, 3.42); T(x0 + 0.37, 3.42, "h$^{+}$", FB, va="center")
electron(x0 + 0.95, 3.42); T(x0 + 1.08, 3.42, "e$^{-}$ (formal)", FB, va="center")
DX = 0.20
CD, CP, CE, CA, CR = 0.48, 0.90, 1.16, 1.66, 1.92      # columns (cm from panel edge): dopant, +, V_O, ->, net

def row(y, label, colour, n_h, result_is_hole, note):
    ov.add_patch(Circle((x0 + 0.24, y + 0.36), 0.09, fc=colour, ec="none"))
    T(x0 + 0.40, y + 0.36, label, 8.5, va="center")
    for k in range(n_h): hole(x0 + CD + (k - (n_h - 1) / 2) * DX, y)
    T(x0 + CP, y, "+", 8, ha="center", va="center")
    electron(x0 + CE, y); electron(x0 + CE + DX, y)
    T(x0 + CA, y, "→", 8, ha="center", va="center")
    (hole if result_is_hole else electron)(x0 + CR, y)
    T(x0 + 0.14, y - 0.22, note, FN, INK2, va="top")

row(2.55, "Pr$^{3{+}}$", S2, 1, False, "1 e$^{-}$ left: on Ti-3d")
row(1.30, "Rb$^{+}$", S3, 3, True, "1 h$^{+}$ left: on O-2p")

# 5 Result -----------------------------------------------------------------------------------------
x0, x1 = P[4]; panel(x0, x1, 5, "Result: $E_\\mathrm{f}$ (eV)")
ax = fig.add_axes([(x0 + 0.55) / W, 0.52 / H, 3.00 / W, 3.02 / H])
keys = ["pristine", "Pr", "Rb"]; X = [0, 1.35, 2.55]; BW = 0.52
ax.bar(X, [EF[k] for k in keys], width=BW, color=[S1, S2, S3], zorder=3)
ax.set_facecolor("none")
ax.set_xlim(-0.62, 3.55); ax.set_ylim(-5.7, 6.3)
ax.plot([-0.62, 2.98], [0, 0], color=INK2, lw=0.7, zorder=4)
ax.set_yticks([-4, 0, 4]); ax.set_yticklabels([MINUS(f"{t:d}") for t in [-4, 0, 4]])
ax.tick_params(axis="y", labelsize=FN, length=2.5, width=0.6, colors=INK2, pad=1.5)
ax.yaxis.grid(True, color="#d9d8d4", lw=0.5, zorder=0)
ax.set_xticks(X); ax.set_xticklabels(["TiO$_2$", "Pr$^{3{+}}$", "Rb$^{+}$"], fontsize=8, color=INK, va="baseline")
ax.tick_params(axis="x", length=0, pad=9)
for s in ["top", "right", "bottom"]: ax.spines[s].set_visible(False)
ax.spines["left"].set_color(INK2)
for x, k in zip([X[0] + 0.12, X[1]], keys[:2]):
    ax.text(x, EF[k] + 0.3, MINUS(f"{EF[k]:+.2f}"), ha="center", va="bottom", fontsize=8,
            fontweight="bold", color=INK, zorder=5, bbox=dict(fc=PANEL, ec="none", pad=0.3))
ax.text(X[2] - BW / 2 - 0.07, EF["Rb"], MINUS(f"{EF['Rb']:+.2f}"), ha="right", va="center", fontsize=8,
        fontweight="bold", color=INK, zorder=5, bbox=dict(fc=PANEL, ec="none", pad=0.3))
for x, k in [(X[1], "Pr"), (X[2], "Rb")]:                # open diamonds, as in Figure 2
    ax.plot(x, EF_NARROW[k], marker="D", ms=4, mfc="white", mec=INK, mew=0.8, zorder=6)
ax.text(X[1] + BW / 2 + 0.06, 0.66, MINUS(f"{EF_NARROW['Pr']:+.2f}"), fontsize=FN,
        color=INK2, va="center", ha="left")
XA = 3.05
ax.annotate("", xy=(XA, EF["Rb"]), xytext=(XA, EF["Pr"]),
            arrowprops=dict(arrowstyle="<->", color=INK, lw=0.7, shrinkA=0, shrinkB=0))
ax.plot([X[2] + BW / 2, XA + 0.05], [EF["Rb"]] * 2, color=INK2, lw=0.5, ls=(0, (1, 1)), zorder=2)
ax.plot([X[1] + BW / 2, XA + 0.05], [EF["Pr"]] * 2, color=INK2, lw=0.5, ls=(0, (1, 1)), zorder=2)
ax.text(XA + 0.1, (EF["Pr"] + EF["Rb"]) / 2, f"Δ {CONTRAST:.2f}", rotation=90, fontsize=FB,
        color=INK, ha="left", va="center", zorder=6, bbox=dict(fc=PANEL, ec="none", pad=0.4))
ax.text(0.62, -0.5, "< 0:\nspontaneous", fontsize=FN, color=INK2, ha="center", va="top", linespacing=1.15,
        bbox=dict(fc=PANEL, ec="none", pad=0.3))
ax.text(2.6, 6.2, "◇ narrower\nsmearing", fontsize=FN, color=INK2, ha="center", va="top", linespacing=1.15,
        bbox=dict(fc=PANEL, ec="none", pad=0.3))

# --- checks: minimum size, every text inside its panel (or the title band), no two texts overlapping
fig.canvas.draw(); rend = fig.canvas.get_renderer()
cm = lambda bb: (bb.x0 / fig.dpi * 2.54, bb.y0 / fig.dpi * 2.54, bb.x1 / fig.dpi * 2.54, bb.y1 / fig.dpi * 2.54)
texts = [t for t in ov.texts + ax.texts + ax.get_xticklabels() + ax.get_yticklabels() if t.get_text().strip()]
small = [t.get_text() for t in texts if t.get_fontsize() < 7]
assert not small, f"below 7 pt: {small}"
boxes = [(t, cm(t.get_window_extent(rend))) for t in texts]
bad = []
for t, (a0, b0, a1, b1) in boxes:
    if b0 > 4.12:                                     # title band
        lim = (0.10, 4.12, W - 0.10, H - 0.02)
    else:
        xc = (a0 + a1) / 2
        p0, p1 = next(p for p in P if p[0] - 0.05 <= xc <= p[1] + 0.05)
        lim = (p0 + 0.03, 0.10, p1 - 0.03, 4.08)
    if a0 < lim[0] or b0 < lim[1] or a1 > lim[2] or b1 > lim[3]:
        bad.append(f"outside panel: {t.get_text()!r} box {a0:.2f}-{a1:.2f} x {b0:.2f}-{b1:.2f}, limits {lim}")
for i, (t, A) in enumerate(boxes):
    for u, B in boxes[i + 1:]:
        if A[0] < B[2] - 0.01 and B[0] < A[2] - 0.01 and A[1] < B[3] - 0.01 and B[1] < A[3] - 0.01:
            bad.append(f"overlap: {t.get_text()!r} / {u.get_text()!r}")
ann = [t for t in ax.texts if not t.get_text().strip()]
obstacles = [("line/marker", cm(l.get_window_extent(rend))) for l in ax.lines]
obstacles += [("bar", cm(b.get_window_extent(rend))) for b in ax.patches]
obstacles += [("arrow", cm(a.arrow_patch.get_window_extent(rend))) for a in ann]
axl = cm(ax.get_window_extent(rend))[0]
obstacles.append(("y-axis line", (axl - 0.02, cm(ax.get_window_extent(rend))[1], axl + 0.02, cm(ax.get_window_extent(rend))[3])))
for t in ax.texts:
    if not t.get_text().strip(): continue
    A = cm(t.get_window_extent(rend))
    for name, O in obstacles:
        if A[0] < O[2] - 0.005 and O[0] < A[2] - 0.005 and A[1] < O[3] - 0.005 and O[1] < A[3] - 0.005:
            bad.append(f"text on {name}: {t.get_text()!r}")
assert not bad, "\n".join(bad)

fig.savefig(os.path.join(OUT, "Graphical_Abstract_v5.pdf"), metadata={"CreationDate": None})   # reproducible file
fig.savefig(os.path.join(OUT, "Graphical_Abstract_v5.svg"), metadata={"Date": None})   # reproducible file
buf = io.BytesIO(); fig.savefig(buf, format="png", dpi=600, facecolor="white"); buf.seek(0)
im = Image.open(buf).convert("RGB")                   # no alpha channel in the raster files
im.save(os.path.join(OUT, "Graphical_Abstract_v5.png"), dpi=(600, 600))
im.save(os.path.join(OUT, "Graphical_Abstract_v5.tiff"), dpi=(600, 600), compression="tiff_lzw")
print(f"Graphical_Abstract_v5.{{pdf,svg,png,tiff}} written ({im.size[0]} x {im.size[1]} px)")
