"""Figure 1 of manuscript v4: the (010) atomic plane that contains the dopant site and the
oxygen vacancy, (a) at ideal anatase positions with the lattice parameters of this work and
(b) in the relaxed Rb_VO cell, read from the pw.x output header (data/nscf_Rb_VO.out; the
NSCF run re-used the final coordinates of the production relaxation).  Arrows show the
displacement of each in-plane atom (where larger than 0.2 Å) from its ideal site (after removing the mean displacement
of all atoms); the spin-carrying oxygen is coloured by its Loewdin moment (data/lowdin_Rb_VO.csv).

If data/nscf_Pr_VO.out (or any pw.x output of the relaxed Pr_VO cell) is added, a panel (c)
for Pr_VO is drawn automatically.  Nothing in this figure is drawn by hand."""
import os, re, itertools
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyArrowPatch

S1, S2, S3 = "#2a78d6", "#eb6834", "#1baf7a"
INK, INK2, GRID = "#0b0b0b", "#52514e", "#d9d8d4"
TI_C, O_C = "#b9b8b4", "#d9534f"
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9})
A, C = 7.63632, 9.77900
CELL = np.array([A, A, C])
U_O = 0.2080   # anatase oxygen parameter used only for the ideal reference positions

ti_conv = [[0, 0, 0], [0, .5, .25], [.5, 0, .75], [.5, .5, .5]]
o_conv = [[0, 0, U_O], [0, 0, -U_O], [0, .5, .25 + U_O], [0, .5, .25 - U_O],
          [.5, 0, .75 + U_O], [.5, 0, .75 - U_O], [.5, .5, .5 + U_O], [.5, .5, .5 - U_O]]
IDEAL_TI = np.array([[(t[0] + i) / 2, (t[1] + j) / 2, t[2] % 1] for i, j in itertools.product(range(2), repeat=2) for t in ti_conv])
IDEAL_O = np.array([[(o[0] + i) / 2, (o[1] + j) / 2, o[2] % 1] for i, j in itertools.product(range(2), repeat=2) for o in o_conv])


def mic(df):
    return df - np.round(df)


def read_pw(fn, nat=47):
    txt = open(fn).read()
    blk = txt[txt.index("positions (cryst. coord.)"):]
    at = re.findall(r"\d+\s+(\w+)\s+tau\(\s*\d+\) = \(\s*([-\d.]+)\s+([-\d.]+)\s+([-\d.]+)", blk)[:nat]
    return np.array([a[0] for a in at]), np.array([[float(x) for x in a[1:]] for a in at]) % 1.0


def assign_ideal(sp, f):
    """Map every atom to its nearest ideal site of the same sublattice; return ideal coords,
    the vacant O site and the substituted cation site."""
    ideal = np.zeros_like(f)
    used_ti, used_o = set(), set()
    for i, (s, x) in enumerate(zip(sp, f)):
        lat, used = (IDEAL_O, used_o) if s == "O" else (IDEAL_TI, used_ti)
        d = np.linalg.norm(mic(lat - x) * CELL, axis=1)
        k = int(np.argmin(d)); used.add(k); ideal[i] = lat[k]
    vac = [k for k in range(len(IDEAL_O)) if k not in used_o]
    return ideal, IDEAL_O[vac[0]]


def stats(sp, f, ideal, vac):
    dop = int(np.where((sp != "Ti") & (sp != "O"))[0][0])
    disp = mic(f - ideal); disp -= disp.mean(axis=0)
    out = {"dopant": sp[dop], "index": dop + 1,
           "dop_disp": np.linalg.norm(disp[dop] * CELL),
           "dop_to_vac": np.linalg.norm(mic(f[dop] - vac) * CELL),
           "site_to_vac": np.linalg.norm(mic(ideal[dop] - vac) * CELL)}
    dO = sorted((np.linalg.norm(mic(f[i] - f[dop]) * CELL), i + 1) for i in range(len(sp)) if sp[i] == "O")
    out["dop_O"] = dO[:6]
    return out, disp


def draw_plane(ax, sp, f, ideal, vac, disp, moments=None, title="", show_ideal=False):
    dop = int(np.where((sp != "Ti") & (sp != "O"))[0][0])
    y0 = ideal[dop][1]
    inplane = [i for i in range(len(sp)) if abs(mic(ideal[i][1] - y0)) < 0.05]
    # Unwrap about the midpoint of the dopant site and the vacant site, choosing each atom's periodic
    # image from its IDEAL position, so that both panels show the same images and both Ti bonded to
    # the vacant site appear next to it (an atom exactly half a cell from the dopant column is otherwise
    # placed arbitrarily by the minimum-image rounding).
    centre = (np.array([ideal[dop][0], y0, ideal[dop][2]]) + vac) / 2
    centre[1] = y0
    xy = {}
    for i in inplane:
        shift = np.floor(ideal[i] - centre + 0.5)          # image chosen on ideal coordinates
        p = (ideal[i] if show_ideal else ideal[i] + mic(f[i] - ideal[i])) - shift
        xy[i] = (p[0] * A, p[2] * C)
    vshift = np.floor(vac - centre + 0.5); vxy = ((vac - vshift)[0] * A, (vac - vshift)[2] * C)
    # bonds
    for i, j in itertools.combinations(inplane, 2):
        a, b = np.array(xy[i]), np.array(xy[j])
        dist = np.linalg.norm(a - b)
        pair = {sp[i], sp[j]}
        cut = 2.25 if pair == {"Ti", "O"} else (2.75 if "O" in pair and pair != {"O"} else 0)
        if cut and dist < cut:
            ax.plot([a[0], b[0]], [a[1], b[1]], color=GRID, lw=1.6, zorder=1)
    # vacancy
    ax.add_patch(Circle(vxy, 0.42, fill=False, ls=(0, (3, 2)), lw=1.3, ec=INK, zorder=2))
    ax.text(vxy[0] - 0.55, vxy[1] - 0.05, "V$_\\mathrm{O}$", ha="right", va="center", fontsize=8.5, color=INK)
    for i in inplane:
        x, z = xy[i]
        if sp[i] == "Ti":
            ax.add_patch(Circle((x, z), 0.36, fc=TI_C, ec=INK2, lw=0.6, zorder=3))
        elif sp[i] == "O":
            fc = O_C
            if moments is not None and moments[i] > 0.1:
                fc = S1
            ax.add_patch(Circle((x, z), 0.27, fc=fc, ec=INK2, lw=0.6, zorder=3))
            if moments is not None and moments[i] > 0.1:
                ax.text(x + 0.38, z + 0.25, f"O{i + 1}\n{moments[i]:+.2f} $\\mu_\\mathrm{{B}}$", fontsize=7.5, color=S1, va="bottom")
        else:
            ax.add_patch(Circle((x, z), 0.52, fc=S3 if sp[i] == "Pr" else S2, ec=INK, lw=0.8, zorder=4))
            ax.text(x, z, sp[i], ha="center", va="center", fontsize=7.5, color="white", fontweight="bold", zorder=5)
        if not show_ideal:
            dv = disp[i] * CELL
            if np.linalg.norm(dv[[0, 2]]) > 0.2:
                x0, z0 = x - dv[0], z - dv[2]
                ax.add_patch(FancyArrowPatch((x0, z0), (x, z), arrowstyle="-|>", mutation_scale=8,
                                             color=INK, lw=0.9, zorder=6, shrinkA=0, shrinkB=6))
                if sp[i] not in ("Ti", "O"):
                    ax.add_patch(Circle((x0, z0), 0.52, fill=False, ls=":", ec=INK2, lw=0.9, zorder=2))
    cx, cz = centre[0] * A, centre[2] * C
    ax.set_xlim(cx - 4.1, cx + 4.1); ax.set_ylim(cz - 4.75, cz + 3.75)
    ax.set_aspect("equal"); ax.set_xlabel("$a$ (Å)"); ax.set_ylabel("$c$ (Å)")
    ax.set_title(title, fontsize=9, color=INK, loc="left")
    for s in ["top", "right"]:
        ax.spines[s].set_visible(False)


cells = [("Rb_VO", "data/nscf_Rb_VO.out", "data/lowdin_Rb_VO.csv")]
if os.path.exists("data/nscf_Pr_VO.out"):
    cells.append(("Pr_VO", "data/nscf_Pr_VO.out", None))

sp, f = read_pw(cells[0][1])
ideal, vac = assign_ideal(sp, f)
st, disp = stats(sp, f, ideal, vac)
mom = np.genfromtxt(cells[0][2], delimiter=",", names=True, dtype=None, encoding=None, skip_header=1)["polarisation"]
print(f"{cells[0][0]}: dopant {st['dopant']} (atom {st['index']}) displaced {st['dop_disp']:.2f} Å; "
      f"ideal site to vacancy {st['site_to_vac']:.2f} Å; relaxed dopant to vacant site {st['dop_to_vac']:.2f} Å")
print("  nearest O:", ", ".join(f"O{i} {d:.3f}" for d, i in st["dop_O"]))

n = 1 + len(cells)
fig, axes = plt.subplots(1, n, figsize=(3.5 * n, 3.9), dpi=300)
draw_plane(axes[0], sp, f, ideal, vac, disp, title="(a) ideal anatase sites, (010) plane\n     through the dopant site", show_ideal=True)
draw_plane(axes[1], sp, f, ideal, vac, disp, moments=mom,
           title=f"(b) relaxed Rb_VO\n     Rb displaced {st['dop_disp']:.2f} Å towards V$_\\mathrm{{O}}$")
if len(cells) > 1:
    sp2, f2 = read_pw(cells[1][1]); ideal2, vac2 = assign_ideal(sp2, f2); st2, disp2 = stats(sp2, f2, ideal2, vac2)
    draw_plane(axes[2], sp2, f2, ideal2, vac2, disp2, title=f"(c) relaxed Pr_VO\n     Pr displaced {st2['dop_disp']:.2f} Å")
    print(f"Pr_VO: dopant displaced {st2['dop_disp']:.2f} Å; to vacant site {st2['dop_to_vac']:.2f} Å; nearest O:",
          ", ".join(f"O{i} {d:.3f}" for d, i in st2["dop_O"]))
fig.tight_layout()
fig.savefig("Fig1_structures_v4.png", facecolor="white"); fig.savefig("Fig1_structures_v4.pdf", facecolor="white")
print("written Fig1_structures_v4.{png,pdf}")
