"""Graphical abstract, v5 detailed variant (19 Oct 2026 manuscript): every qualifier, for slides or
enlarged viewing; the upload version (legible at 13 x 5 cm) is make_graphical_abstract_v5.py. Drawn from the numbers below; no generated imagery.

Every value is taken from the 19 Oct manuscript: Table 2 (E_f), Section 3.3 / Table S11 (narrower
smearing), Section 3.7 (contrast tests), Table 1 (charge bookkeeping), Sections 3.1, 3.6 and 4.3
(Rb hole and displacement, ionic radii), Table 4 (U(O-2p)).
Size: 13 x 5 cm (Elsevier graphical abstract); vector PDF/SVG plus 600 dpi RGB PNG/TIFF.
The script stops if a printed number differs from the manuscript or if any text leaves its panel.
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
CONTRAST_NARROW = EF_NARROW["Pr"] - EF_NARROW["Rb"]
TEST_MAX = 0.04          # Section 3.7, change in the Pr-Rb contrast: k-mesh +0.038, cut-off 0.006, D3 +0.005 eV
HOLES = {"pristine": 0, "Pr": 1, "Rb": 3}             # formal holes of the vacancy-free cells (Table 1)
RADIUS = {"pristine": "0.605", "Pr": "0.99", "Rb": "1.52"}  # six-fold ionic radii (A) of Ti4+, Pr3+, Rb+ (Sec. 4.3)
# the rounded values printed in the manuscript
assert [f"{EF[k]:+.2f}" for k in TOT] == ["+4.75", "+1.29", "-4.06"]
assert [f"{EF_NARROW[k]:+.2f}" for k in TOT_NARROW] == ["+0.99", "-4.13"]
assert (f"{CONTRAST:.2f}", f"{CONTRAST_NARROW:.2f}") == ("5.36", "5.11")

# --- style (validated categorical slots 1-3, as in Figure 2; status colours only with an icon) -
S1, S2, S3 = "#2a78d6", "#eb6834", "#1baf7a"
INK, INK2, GRID, PANEL = "#0b0b0b", "#52514e", "#b9b8b2", "#f3f2ee"
GOOD, WARN = "#0ca30c", "#fab219"
TI, OX = "#6da7ec", "#b2182b"                     # Ti blue, O red (same key as Figure 1)
plt.rcParams.update({"font.family": "DejaVu Sans", "mathtext.fontset": "dejavusans",
                     "pdf.fonttype": 42, "svg.fonttype": "path", "svg.hashsalt": "ga_v5", "axes.linewidth": 0.5})
MINUS = lambda s: s.replace("-", "−")
VO = "V$_\\mathrm{O}$"

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

# --- title: the one central finding, with its condition ------------------------------------------
T(W / 2, 4.71, "Pr and Rb both lower the O-vacancy cost in TiO₂; at the O-rich limit only Rb makes it spontaneous",
  6.2, ha="center", va="center", fontweight="bold")
T(W / 2, 4.45, "Anatase, spin-polarised PBE+U, U(Ti-3d) = 3.5 eV  ·  oxygen-rich reference "
  "$\\mu_\\mathrm{O} = E(\\mathrm{O_2})/2$  ·  neutral " + VO + ", one dopant per 48-atom cell",
  5.0, INK2, ha="center", va="center")

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
T(x0 + 0.13, 1.95, "2×2×1 anatase,\n48 atoms\n\nOne Ti → Pr³⁺\nor Rb⁺\n(separate cells)",
  FB, va="top", linespacing=1.3)

# 2 Remove one O -----------------------------------------------------------------------------------
x0, x1 = P[1]; panel(x0, x1, 2, "Remove O")
xs, ys, (vx, vy) = lattice((x0 + x1) / 2, 3.08, vac=True)
ov.add_patch(Circle((x0 + 0.20, 2.27), 0.068, fc=PANEL, ec=INK, lw=0.6, ls=(0, (2, 1.5))))
T(x0 + 0.33, 2.27, VO + ": removed O", FN, va="center")
T(x0 + 0.13, 1.95, "First-shell O of\nthe dopant", FB, va="top", linespacing=1.3)
T(x0 + 0.13, 1.20, "Neutral " + VO + "\nreleases", FB, va="center", linespacing=1.3)
electron(x0 + 0.22, 0.77); electron(x0 + 0.40, 0.77)
T(x0 + 0.52, 0.77, "2 e⁻", FB, va="center")

# 3 Protocol and tests -----------------------------------------------------------------------------
x0, x1 = P[2]; panel(x0, x1, 3, "Protocol")
for k, s in enumerate(["Γ-only relaxations, 40 Ry",
                       "$E_\\mathrm{f} = E(\\mathrm{V}_\\mathrm{O}) - E(\\mathrm{perfect})$",
                       "$\\quad\\quad + E(\\mathrm{O_2})/2$"]):
    T(x0 + 0.13, 3.72 - 0.24 * k, s, FB, va="center")
ov.plot([x0 + 0.13, x1 - 0.13], [3.02, 3.02], color=GRID, lw=0.5)
T(x0 + 0.13, 2.80, f"Δ(Pr–Rb) = {CONTRAST:.2f} eV", FB, va="center", fontweight="bold")
status(x0 + 0.23, 2.45, True)
T(x0 + 0.40, 2.45, f"2×2×2 k-mesh, 55, 70 Ry,\nD3: Δ changes ≤ {TEST_MAX:.2f} eV", FB,
  va="center", linespacing=1.25)
status(x0 + 0.23, 1.92, False)
T(x0 + 0.40, 1.92, "narrower smearing:\nPr cells spin-polarise", FB, va="center", linespacing=1.25)
T(x0 + 0.40, 1.66, MINUS(f"Pr {EF_NARROW['Pr']:+.2f}, Rb {EF_NARROW['Rb']:+.2f} eV,\nΔ = {CONTRAST_NARROW:.2f} eV"),
  FN, INK2, va="top", linespacing=1.25)
status(x0 + 0.23, 0.98, False)
T(x0 + 0.40, 0.98, "U(O-2p): spin states of\nPr, Rb parent cells change", FB, va="center", linespacing=1.25)
T(x0 + 0.40, 0.70, "$E_\\mathrm{f}$ not recomputed", FN, INK2, va="top")

# 4 Charge bookkeeping -----------------------------------------------------------------------------
x0, x1 = P[3]; panel(x0, x1, 4, "Charge bookkeeping")
hole(x0 + 0.22, 3.72); T(x0 + 0.33, 3.72, "hole h⁺", FB, va="center")
electron(x0 + 1.32, 3.72); T(x0 + 1.43, 3.72, "electron e⁻", FB, va="center")
T(x0 + 0.13, 3.49, "formal (Kröger–Vink) counts", FN, INK2, va="center")
DX = 0.17
CD, CP, CE, CA, CR = 0.55, 0.92, 1.10, 1.50, 1.72      # columns (cm from panel edge): dopant, +, V_O, ->, net

def row(y, label, colour, n_h, result_is_hole, result, note, heads=False):
    yl = y + (0.42 if heads else 0.30)                # row label (higher where column heads sit)
    ov.add_patch(Circle((x0 + 0.22, yl), 0.08, fc=colour, ec="none"))
    T(x0 + 0.36, yl, label, 5.4, va="center", fontweight="bold")
    for k in range(n_h): hole(x0 + CD + (k - (n_h - 1) / 2) * DX, y)
    T(x0 + CP, y, "+", 5.6, ha="center", va="center")
    electron(x0 + CE, y); electron(x0 + CE + DX, y)
    T(x0 + CA, y, "→", 6, ha="center", va="center")
    (hole if result_is_hole else electron)(x0 + CR, y)
    T(x0 + CR + 0.13, y, result, FB, va="center", fontweight="bold")
    if heads:
        for xx, s in [(CD, "dopant"), (CE + DX / 2, VO), (CR, "net")]:
            T(x0 + xx, y + 0.19, s, FN, INK2, ha="center", va="center")
    T(x0 + 0.13, y - 0.17, note, FN, INK2, va="top", linespacing=1.25)

row(2.78, "Pr³⁺", S2, HOLES["Pr"], False, "1 e⁻ left",
    "extra e⁻ in Ti-3d conduction band;\nnarrower smearing: partly on 4 Ti", heads=True)
row(1.45, "Rb⁺", S3, HOLES["Rb"], True, "1 h⁺ left",
    "residual h⁺ on O-2p: Löwdin\n0.59 $\\mu_\\mathrm{B}$ on one O bonded to Rb")
T(x0 + 0.13, 0.58, "Rb lies 1.27 Å off its ideal site,\ntowards " + VO, FN, INK2, va="top", linespacing=1.25)

# 5 Result -----------------------------------------------------------------------------------------
x0, x1 = P[4]; panel(x0, x1, 5, "Result: $E_\\mathrm{f}(\\mathrm{V}_\\mathrm{O}^{0})$ (eV)")
ax = fig.add_axes([(x0 + 0.42) / W, 1.30 / H, 2.72 / W, 2.44 / H])
keys = ["pristine", "Pr", "Rb"]; vals = [EF[k] for k in keys]; X = [0, 1.25, 2.35]; BW = 0.42
ax.bar(X, vals, width=BW, color=[S1, S2, S3], zorder=3)
ax.set_facecolor("none")
ax.plot([-0.45, 2.70], [0, 0], color=INK2, lw=0.6, zorder=4)
ax.set_xlim(-0.45, 3.22); ax.set_ylim(-5.4, 6.0)
ax.set_yticks([-4, -2, 0, 2, 4]); ax.set_yticklabels([MINUS(f"{t:d}") for t in [-4, -2, 0, 2, 4]])
ax.tick_params(axis="y", labelsize=FN, length=2, width=0.5, colors=INK2, pad=1.5)
ax.yaxis.grid(True, color="#d9d8d4", lw=0.4, zorder=0)
ax.set_xticks(X)
ax.set_xticklabels([f"{n}\n{HOLES[k]} h⁺\n{RADIUS[k]} Å" for n, k in zip(["pristine", "Pr³⁺", "Rb⁺"], keys)],
                   fontsize=FB, color=INK, linespacing=1.15)
ax.tick_params(axis="x", length=0, pad=2)
for s in ["top", "right", "bottom"]: ax.spines[s].set_visible(False)
ax.spines["left"].set_color(INK2)
for x, k in zip(X[:2], keys[:2]):
    ax.text(x, EF[k] + 0.25, MINUS(f"{EF[k]:+.2f}"), ha="center", va="bottom", fontsize=5.4,
            fontweight="bold", color=INK, zorder=5, bbox=dict(fc=PANEL, ec="none", pad=0.3))
ax.text(X[2] - BW / 2 - 0.06, EF["Rb"], MINUS(f"{EF['Rb']:+.2f}"), ha="right", va="center", fontsize=5.4,
        fontweight="bold", color=INK, zorder=5, bbox=dict(fc=PANEL, ec="none", pad=0.3))
for x, k in [(X[1], "Pr"), (X[2], "Rb")]:                # open diamonds: narrower-smearing values
    ax.plot(x, EF_NARROW[k], marker="D", ms=3.2, mfc="white", mec=INK, mew=0.7, zorder=6)
ax.text(X[1] - BW / 2 - 0.05, EF_NARROW["Pr"], MINUS(f"{EF_NARROW['Pr']:+.2f}"), fontsize=FN, color=INK2,
        va="center", ha="right")
XA = 2.80
ax.annotate("", xy=(XA, EF["Rb"]), xytext=(XA, EF["Pr"]),
            arrowprops=dict(arrowstyle="<->", color=INK, lw=0.6, shrinkA=0, shrinkB=0))
for y0, xa in [(EF["Pr"], X[1] + BW / 2), (EF["Rb"], X[2] + BW / 2)]:
    ax.plot([xa, XA + 0.05], [y0, y0], color=INK2, lw=0.4, ls=(0, (1, 1)), zorder=2)
ax.text(XA + 0.09, (EF["Pr"] + EF["Rb"]) / 2, f"Δ {CONTRAST:.2f} eV", rotation=90, fontsize=FB,
        color=INK, ha="left", va="center", zorder=6, bbox=dict(fc=PANEL, ec="none", pad=0.4))
ax.text(0.62, -0.45, "below 0:\nspontaneous", fontsize=FN, color=INK2, ha="center", va="top", linespacing=1.15, bbox=dict(fc=PANEL, ec="none", pad=0.3))
ax.text(2.3, 5.6, "◇ narrower\nsmearing", fontsize=FN, color=INK2, ha="center", va="top", linespacing=1.15, bbox=dict(fc=PANEL, ec="none", pad=0.3))
T(x0 + 0.13, 0.42, "h⁺: formal holes before V$_\\mathrm{O}$ removal", FN, INK2, va="center")
T(x0 + 0.13, 0.20, "Å: cation radius; both rise together", FN, INK2, va="center")

# --- layout check: every text inside its panel (or the title band), no two texts overlapping --------
fig.canvas.draw(); rend = fig.canvas.get_renderer()
cm = lambda bb: (bb.x0 / fig.dpi * 2.54, bb.y0 / fig.dpi * 2.54, bb.x1 / fig.dpi * 2.54, bb.y1 / fig.dpi * 2.54)
boxes = [(t, cm(t.get_window_extent(rend))) for t in ov.texts + ax.texts + ax.get_xticklabels() + ax.get_yticklabels()
         if t.get_text().strip()]
bad = []
for t, (a0, b0, a1, b1) in boxes:
    if b0 > 4.30:                                     # title band
        lim = (0.10, 4.30, W - 0.10, H - 0.02)
    else:
        xc = (a0 + a1) / 2
        p0, p1 = next(p for p in P if p[0] - 0.05 <= xc <= p[1] + 0.05)
        lim = (p0 + 0.03, 0.10, p1 - 0.03, 4.28)
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

fig.savefig(os.path.join(OUT, "Graphical_Abstract_v5_detailed.pdf"), metadata={"CreationDate": None})   # reproducible file
fig.savefig(os.path.join(OUT, "Graphical_Abstract_v5_detailed.svg"), metadata={"Date": None})   # reproducible file
buf = io.BytesIO(); fig.savefig(buf, format="png", dpi=600, facecolor="white"); buf.seek(0)
im = Image.open(buf).convert("RGB")                   # no alpha channel in the raster files
im.save(os.path.join(OUT, "Graphical_Abstract_v5_detailed.png"), dpi=(600, 600))
im.save(os.path.join(OUT, "Graphical_Abstract_v5_detailed.tiff"), dpi=(600, 600), compression="tiff_lzw")
print(f"Graphical_Abstract_v5_detailed.{{pdf,svg,png,tiff}} written ({im.size[0]} x {im.size[1]} px)")
