"""Extract per-atom Loewdin charges and spin polarisations from projwfc.x output, and
atomic coordinates from the matching pw.x NSCF output, into CSV files under data/.

Usage: python3 extract_lowdin.py proj_Rb_VO.out [nscf_Rb_VO.out]
Writes data/lowdin_<prefix>.csv with columns
atom, species, charge, s, p, d, polarisation[, x_A, y_A, z_A]."""
import re, sys, os
import numpy as np

CELL = np.diag([7.63632, 7.63632, 9.77900])  # Angstrom, as in CELL_PARAMETERS


def read_lowdin(fn):
    txt = open(fn).read()
    species = {int(a): s for a, s in re.findall(r"state #\s*\d+: atom\s+(\d+) \((\w+)\s*\)", txt)}
    sec = txt[txt.index("Lowdin Charges"):]
    rows = []
    for a, q, s, p, d, pol in re.findall(
            r"Atom #\s*(\d+): total charge =\s*([-\d.]+), s =\s*([-\d.]+), p =\s*([-\d.]+), d =\s*([-\d.]+),"
            r"(?:.|\n)*?polarization =\s*([-\d.]+),", sec):
        rows.append([int(a), species[int(a)], float(q), float(s), float(p), float(d), float(pol)])
    spill = float(re.search(r"Spilling Parameter:\s*([\d.]+)", txt).group(1))
    prefix = re.search(r"Reading xml data from directory:\s*\n\s*\./(\w+)\.save", txt).group(1)
    return prefix, rows, spill


def read_crystal_coords(fn, nat):
    txt = open(fn).read()
    blk = txt[txt.index("positions (cryst. coord.)"):]
    at = re.findall(r"\d+\s+(\w+)\s+tau\(\s*\d+\) = \(\s*([-\d.]+)\s+([-\d.]+)\s+([-\d.]+)", blk)[:nat]
    return [a[0] for a in at], np.array([[float(x) for x in a[1:]] for a in at])


if __name__ == "__main__":
    prefix, rows, spill = read_lowdin(sys.argv[1])
    header = "atom,species,charge,s,p,d,polarisation"
    if len(sys.argv) > 2:
        sp, frac = read_crystal_coords(sys.argv[2], len(rows))
        assert [r[1] for r in rows] == sp, "species order differs between projwfc and pw.x outputs"
        cart = (frac % 1.0) @ CELL
        rows = [r + list(c) for r, c in zip(rows, cart)]
        header += ",x_A,y_A,z_A"
    os.makedirs("data", exist_ok=True)
    out = f"data/lowdin_{prefix}.csv"
    with open(out, "w") as f:
        f.write(f"# projwfc.x Loewdin analysis of {prefix}; spilling parameter {spill}\n" + header + "\n")
        for r in rows:
            f.write(",".join(f"{v:.4f}" if isinstance(v, float) else str(v) for v in r) + "\n")
    pol = np.array([r[6] for r in rows])
    print(f"{out}: {len(rows)} atoms, sum of polarisations {pol.sum():+.4f}, sum of |polarisations| {np.abs(pol).sum():.4f}")
