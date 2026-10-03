"""Recompute every derived energy quoted in manuscript v4 and its SI from energy_ledger.csv.
Run: python3 check_ledger.py   (prints each quantity; exits non-zero if a quoted value is not reproduced)."""
import csv, sys

RY = 13.605693123
rows = {}
for r in csv.DictReader(l for l in open("energy_ledger.csv") if not l.startswith("#")):
    try:
        rows[r["run"]] = float(r["E_Ry"])
    except ValueError:
        pass
E = lambda k: rows[str(k)]
half = E(7) / 2
ef = lambda vo, perf: (E(vo) - E(perf) + half) * RY

checks = [  # (label, computed, quoted value, tolerance)
    ("half E(O2) (Ry)", half, -41.51621, 5e-6),
    ("Ef pristine", ef(2, 1), 4.74, 0.005),
    ("Ef Pr", ef(4, 3), 1.29, 0.005),
    ("Ef Rb", ef(6, 5), -4.06, 0.005),
    ("dEf Pr-Rb (G)", ef(4, 3) - ef(6, 5), 5.36, 0.005),
    ("Ef Pr 2x2x2", ef(9, 8), 1.19, 0.005),
    ("Ef Rb 2x2x2", ef(11, 10), -4.20, 0.005),
    ("dEf Pr-Rb (2x2x2)", ef(9, 8) - ef(11, 10), 5.39, 0.005),
    ("ddE contrast", (ef(9, 8) - ef(11, 10)) - (ef(4, 3) - ef(6, 5)), 0.04, 0.005),
    ("Ef reduction Pr vs pristine", ef(4, 3) - ef(2, 1), -3.45, 0.005),
    ("Ef reduction Rb vs pristine", ef(6, 5) - ef(2, 1), -8.81, 0.005),
    ("Ef site O1", ef(12, 3), 2.07, 0.005),
    ("Ef site O7", ef(13, 3), 2.72, 0.005),
    ("Ef site O17", ef(14, 3), 2.07, 0.005),
    ("Pr magnetic trial vs logged non-magnetic", (E(24) - E(25)) * RY, 0.281, 0.0005),
    ("Pr magnetic trial vs production", (E(24) - E(4)) * RY, 0.394, 0.0005),
    ("Rb_VO from-scratch G minus production (meV)", (E(34) - E(6)) * RY * 1000, 6.4, 0.05),
    ("Pr_VO from-scratch G minus production", (E(30) - E(4)) * RY, 0.038, 0.0005),
    ("Pr_VO D3 electronic part minus run 30 (Ry)", (E(22) + 0.75638867) - E(30), 0.0, 1e-6),
    ("Rb_VO D3 electronic part minus run 34 (Ry)", (E(23) + 0.74165995) - E(34), 0.0, 1e-6),
    ("Pristine E(G) - E(3x3x2) per atom (meV)", (E(26) - E(29)) * RY / 48 * 1000, -21.8, 0.05),
    ("Pr_VO E(G) - E(3x3x2) per atom (meV)", (E(30) - E(33)) * RY / 47 * 1000, -23.0, 0.05),
    ("Rb_VO E(G) - E(3x3x2) per atom (meV)", (E(34) - E(37)) * RY / 47 * 1000, -24.7, 0.05),
    ("Pristine |E(2x2x1) - E(3x3x2)| per atom (meV)", abs(E(27) - E(29)) * RY / 48 * 1000, 1.15, 0.005),
    ("Pr_VO |E(2x2x1) - E(3x3x2)| per atom (meV)", abs(E(31) - E(33)) * RY / 47 * 1000, 1.05, 0.005),
    ("Rb_VO |E(2x2x1) - E(3x3x2)| per atom (meV)", abs(E(35) - E(37)) * RY / 47 * 1000, 0.42, 0.005),
]
for lo, hi, lab in [(38, 1, "Pristine"), (41, 4, "Pr_VO"), (44, 6, "Rb_VO")]:
    seq = [E(lo), E(hi), E(lo + 1), E(lo + 2)]
    steps = [(b - a) * RY for a, b in zip(seq, seq[1:])]
    print(f"U-sweep energy steps {lab}: " + ", ".join(f"{s:.2f}" for s in steps) + " eV per 0.5 eV of U")
bad = 0
for lab, val, quoted, tol in checks:
    ok = abs(val - quoted) <= tol
    bad += not ok
    print(f"{'OK ' if ok else 'BAD'} {lab}: {val:.4f} (quoted {quoted})")
sys.exit(1 if bad else 0)
