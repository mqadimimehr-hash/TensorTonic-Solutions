#!/usr/bin/env python3
"""Summarise the reviewer-requested Quantum ESPRESSO runs of revision_calculations.

usage:
    python3 analyze_revision_runs.py [RUN_DIR] [--prod-dir DIR] [--pristine-vo-out FILE]
                                     [--dualu-rb-perfect FILE_OR_RY] [--csv FILE]

RUN_DIR             folder with the jobN_*.out files (default: ./runs next to this script)
--prod-dir          folder with the production outputs (default: the parent of this script's
                    folder, i.e. ~/tio2_vo). Used only to cross-check the production energies
                    hard-coded below; missing files are ignored.
--pristine-vo-out   pristine V_O relaxation output (its name is not fixed)
--dualu-rb-perfect  dual-U Rb_perfect relaxation output, or its total energy in Ry, to form the
                    dual-U E_f(V_O; Rb) with job 7b
--csv               where to write the summary table (default: RUN_DIR/revision_summary.csv)

Prints one table with every run (E_tot, -TS, internal energy, total and absolute
magnetisation, Fermi energy, convergence status) followed by the job-specific analyses:
cut-off series and E_f(V_O) contrast (job 1), pristine 2x2x2 (job 2), smearing (job 3),
D3 cycle (job 4), nosym hole search versus production (jobs 5 and 6), dual-U (job 7, 7b),
tight relaxations (job 8) and hp.x U values (job 9).
"""

import argparse
import csv
import glob
import os
import re
import sys

RY_EV = 13.605693                 # eV per Ry
HALF_O2_PROD = -41.51621          # Ry, half of the production PBE O2 box energy (-83.03242804 Ry)

# Production single-U totals, Gamma, 40/320 Ry (Ry). Rb_VO and Rb_perfect: reviewer brief;
# the others: energy_ledger.csv of manuscript v4 (SI Table S9, runs 1-6).
PROD = {
    'Pristine_perfect': -4275.01530,
    'Pristine_VO': -4233.15036,
    'Pr_perfect': -4576.71224,
    'Pr_VO': -4535.10106,
    'Rb_perfect': -4330.38890,
    'Rb_VO': -4289.17135,
}
PROD_FILES = {'Pristine_perfect': 'Pristine_perfect.out', 'Pr_perfect': 'Pr_perfect.out',
              'Pr_VO': 'Pr_VO.out', 'Rb_perfect': 'Rb_perfect.out', 'Rb_VO': 'Rb_VO.out'}
# Other ledger values used below (SI Table S9 run numbers in brackets)
LEDGER = {
    'Pristine_perfect_k222': -4274.93072431,   # (28) k-mesh series
    'Pr_perfect_k222': -4576.62183,            # (8)
    'Pr_VO_k222': -4535.01814146,              # (32)
    'Rb_perfect_k222': -4330.28761,            # (10)
    'Rb_VO_k222': -4289.08033502,              # (36)
    'Pr_VO_scratch': -4535.09824686,           # (30) Gamma SCF from scratch, production geometry
    'Rb_VO_scratch': -4289.17088018,           # (34)
    'Pr_VO_D3': -4535.85463552,                # (22) D3 term -0.75639 Ry
    'Rb_VO_D3': -4289.91254013,                # (23) D3 term -0.74166 Ry
    'Pr_VO_D3_term': -0.75639,
    'Rb_VO_D3_term': -0.74166,
    'Pr_perfect_dualU': -4571.33095,           # (19) dual-U relaxation
}
CELLS = ('Pr_perfect', 'Pr_VO', 'Rb_perfect', 'Rb_VO')
NAT = {'Pr_perfect': 48, 'Pr_VO': 47, 'Rb_perfect': 48, 'Rb_VO': 47}

RE_FLOAT = re.compile(r'-?\d+\.\d+(?:[EeDd][-+]?\d+)?')
RE_FORCE = re.compile(r'^\s*atom\s+(\d+)\s+type\s+\d+\s+force\s+=\s+(-?\d+\.\d+)\s+(-?\d+\.\d+)\s+(-?\d+\.\d+)')
RE_MOM = re.compile(r'atom[:\s]+(\d+)\s*(?:\(R=\s*[\d.]+\))?\s+charge[:=]\s*(-?\d+\.\d+)\s+magn[:=]\s*(-?\d+\.\d+)')
RE_WALL = re.compile(r'^\s*(PWSCF|HP)\s*:.*CPU\s+(.+?)\s+WALL')


def floats(line):
    return [float(x.replace('D', 'E').replace('d', 'e')) for x in RE_FLOAT.findall(line)]


def last_float(line):
    v = floats(line)
    return v[-1] if v else None


def parse_out(path):
    """Line-by-line parser (relaxation outputs can be large)."""
    r = {'path': path, 'tag': os.path.basename(path)[:-4], 'program': 'PW', 'done': False,
         'E': None, 'n_bang': 0, 'TS': None, 'Eint': None, 'mtot': None, 'mabs': None,
         'EF': None, 'd3': None, 'conv_iter': None, 'scf_fail': False, 'relax': False,
         'bfgs_steps': None, 'maxstep': False, 'fmax': None, 'nsym': None, 'smear': None,
         'width': None, 'ecut': None, 'wall': None, 'ram': None, 'moments': {}, 'hp': []}
    fstate = mstate = hstate = 0
    forces, moms = [], {}
    with open(path, errors='replace') as fh:
        for line in fh:
            s = line.strip()
            if fstate:
                m = RE_FORCE.match(line)
                if m:
                    forces.append(max(abs(float(m.group(k))) for k in (2, 3, 4)))
                    fstate = 2
                    continue
                if not s and fstate == 1:
                    continue
                fstate = 0
                if forces:
                    r['fmax'] = max(forces)
            if mstate:
                m = RE_MOM.search(line)
                if m:
                    moms[int(m.group(1))] = float(m.group(3))
                    mstate = 2
                    continue
                if not s and mstate == 1:
                    continue
                mstate = 0
                if moms:
                    r['moments'] = dict(moms)
            if hstate:
                if s.startswith('=-') or (not s and hstate > 3):
                    hstate = 0
                else:
                    if s:
                        r['hp'].append(s)
                    hstate += 1
                    continue
            if line.startswith('!'):
                r['E'] = last_float(line)
                r['n_bang'] += 1
            elif 'smearing contrib. (-TS)' in line:
                r['TS'] = last_float(line)
            elif 'internal energy E=F+TS' in line:
                r['Eint'] = last_float(line)
            elif 'total magnetization' in line and '=' in line:
                r['mtot'] = last_float(line.split('=', 1)[1].replace('Bohr mag/cell', ''))
            elif 'absolute magnetization' in line and '=' in line:
                r['mabs'] = last_float(line.split('=', 1)[1].replace('Bohr mag/cell', ''))
            elif 'the Fermi energy is' in line:
                r['EF'] = '%.4f' % last_float(line)
            elif 'Fermi energies are' in line:
                v = floats(line)
                if len(v) >= 2:
                    r['EF'] = '%.3f/%.3f' % (v[-2], v[-1])
            elif 'DFT-D3 Dispersion' in line:
                r['d3'] = last_float(line)
            elif 'convergence has been achieved in' in line:
                r['conv_iter'] = int(re.findall(r'in\s+(\d+)\s+iterations', line)[0]) \
                    if re.search(r'in\s+\d+\s+iterations', line) else 0
            elif 'convergence NOT achieved' in line:
                r['scf_fail'] = True
            elif 'BFGS Geometry Optimization' in line:
                r['relax'] = True
            elif 'bfgs converged in' in line:
                m = re.search(r'and\s+(\d+)\s+bfgs steps', line)
                r['bfgs_steps'] = int(m.group(1)) if m else -1
            elif 'The maximum number of steps has been reached' in line:
                r['maxstep'] = True
            elif 'Forces acting on atoms' in line:
                fstate, forces = 1, []
            elif 'Magnetic moment per site' in line:
                mstate, moms = 1, {}
            elif 'smearing, width (Ry)' in line:
                m = re.search(r'(\S+)\s+smearing, width \(Ry\)=\s*(\S+)', line)
                if m:
                    r['smear'] = m.group(1)
                    try:
                        r['width'] = float(m.group(2))
                    except ValueError:
                        pass
            elif 'kinetic-energy cutoff' in line:
                r['ecut'] = last_float(line)
            elif 'Sym. Ops.' in line:
                m = re.search(r'(\d+)\s+Sym\. Ops\.', line)
                if m:
                    r['nsym'] = int(m.group(1))
            elif 'No symmetry found' in line:
                r['nsym'] = 1
            elif 'Estimated total dynamical RAM' in line:
                r['ram'] = line.split('>')[-1].strip() if '>' in line else s.split()[-2] + ' ' + s.split()[-1]
            elif 'Program HP' in line:
                r['program'] = 'HP'
            elif r['program'] == 'HP' and 'Hubbard U parameters' in line:
                hstate, r['hp'] = 1, []
            elif 'JOB DONE' in line:
                r['done'] = True
            m = RE_WALL.match(line)
            if m:
                r['wall'] = m.group(2).replace(' ', '')
    if fstate and forces:
        r['fmax'] = max(forces)
    if mstate and moms:
        r['moments'] = dict(moms)
    return r


def status(r):
    if r['program'] == 'HP':
        return 'DONE' if r['done'] else 'INCOMPLETE'
    if not r['done']:
        return 'RUNNING/CRASHED'
    if r['scf_fail']:
        return 'SCF NOT CONVERGED'
    if r['relax']:
        if r['bfgs_steps'] is not None:
            return 'relax conv (%d steps)' % r['bfgs_steps']
        return 'relax MAX STEPS' if r['maxstep'] else 'relax unclear'
    if r['conv_iter'] is not None:
        return 'scf conv (%d it)' % r['conv_iter']
    return 'done, unclear'


def usable(r):
    return r is not None and r['done'] and not r['scf_fail'] and r['E'] is not None and \
        (not r['relax'] or r['bfgs_steps'] is not None)


def energy(R, tag):
    r = R.get(tag)
    return r['E'] if usable(r) else None


def ef(e_vo, e_perf, half_o2):
    if e_vo is None or e_perf is None or half_o2 is None:
        return None
    return (e_vo - e_perf + half_o2) * RY_EV


def f(x, fmt='%.3f', width=9):
    return ('%' + str(width) + 's') % (fmt % x if x is not None else '-')


def header(title):
    print()
    print('=' * 100)
    print(title)
    print('=' * 100)


# ---------------------------------------------------------------- sections
def table(R, csv_path):
    header('ALL RUNS')
    cols = ('job', 'E_tot (Ry)', '-TS (Ry)', 'E=F+TS (Ry)', 'm_tot', 'm_abs', 'E_F (eV)', 'nsym',
            'status', 'wall')
    print('%-34s %16s %11s %16s %7s %6s %13s %4s  %-22s %s' % cols)
    rows = []
    for tag in sorted(R, key=sort_key):
        r = R[tag]
        print('%-34s %16s %11s %16s %7s %6s %13s %4s  %-22s %s' % (
            tag, f(r['E'], '%.8f', 16), f(r['TS'], '%.6f', 11), f(r['Eint'], '%.8f', 16),
            f(r['mtot'], '%.2f', 7), f(r['mabs'], '%.2f', 6), r['EF'] or '-',
            r['nsym'] if r['nsym'] is not None else '-', status(r), r['wall'] or '-'))
        rows.append([tag, r['E'], r['TS'], r['Eint'], r['mtot'], r['mabs'], r['EF'], r['nsym'],
                     status(r), r['fmax'], r['d3'], r['smear'], r['width'], r['ecut'], r['wall'],
                     r['ram']])
    try:
        with open(csv_path, 'w', newline='') as fh:
            w = csv.writer(fh)
            w.writerow(['job', 'E_tot_Ry', 'minus_TS_Ry', 'E_internal_Ry', 'm_tot', 'm_abs',
                        'E_F_eV', 'nsym', 'status', 'Fmax_Ry_Bohr', 'D3_Ry', 'smearing',
                        'width_Ry', 'ecutwfc_Ry', 'wall', 'RAM'])
            w.writerows(rows)
        print('\n(table also written to %s)' % csv_path)
    except OSError as exc:
        print('\n(could not write %s: %s)' % (csv_path, exc))


def sort_key(tag):
    m = re.match(r'job(\d+)(b?)_(.*)', tag)
    if not m:
        return (99, '', tag)
    return (int(m.group(1)), m.group(2), m.group(3))


def section_cutoff(R):
    header('JOB 1 -- cut-off convergence (reviewer Q1). E_f(V_O) = E(VO) - E(perfect) + 1/2 E(O2)')
    have = [t for t in R if t.startswith('job1_')]
    if not have:
        print('no job-1 outputs yet')
        return
    cuts = sorted({int(m.group(1)) for t in have for m in [re.search(r'_ec(\d+)$', t)] if m} | {40})
    print('40 Ry values: job-1 reference single point if present, otherwise production '
          '(relaxation endpoint; marked *).')
    print('O2 "fixed": production 1/2 E(O2) = %.5f Ry at every cut-off; O2 "same ec": O2 box '
          'at the same cut-off (job 1).' % HALF_O2_PROD)
    print('The Pr-Rb contrast does not depend on the O2 reference.\n')
    print('%5s | %10s %10s | %10s %10s | %9s | %s' % ('ecut', 'Ef(Pr)fix', 'Ef(Rb)fix', 'Ef(Pr)ec',
                                                     'Ef(Rb)ec', 'contrast', 'sources'))
    base = {}
    E40 = {}
    for ec in cuts:
        E, src = {}, []
        for c in CELLS:
            e = energy(R, 'job1_%s_ec%d' % (c, ec))
            if e is None and ec == 40:
                e = PROD[c]
                src.append(c + '*')
            E[c] = e
        if ec == 40:
            E40 = dict(E)
        o2 = energy(R, 'job1_O2_ec%d' % ec)
        half = o2 / 2 if o2 is not None else None
        pr_f, rb_f = ef(E['Pr_VO'], E['Pr_perfect'], HALF_O2_PROD), ef(E['Rb_VO'], E['Rb_perfect'], HALF_O2_PROD)
        pr_c, rb_c = ef(E['Pr_VO'], E['Pr_perfect'], half), ef(E['Rb_VO'], E['Rb_perfect'], half)
        con = pr_f - rb_f if pr_f is not None and rb_f is not None else None
        if ec == 40:
            base = {'pr_f': pr_f, 'rb_f': rb_f, 'pr_c': pr_c, 'rb_c': rb_c, 'con': con}
        print('%5d | %s %s | %s %s | %s | %s' % (ec, f(pr_f, '%.4f', 10), f(rb_f, '%.4f', 10),
                                                f(pr_c, '%.4f', 10), f(rb_c, '%.4f', 10),
                                                f(con, '%.4f', 9), ' '.join(src) or 'runs'))
        if ec != 40 and base:
            def d(a, b):
                return a - b if a is not None and b is not None else None
            print('%5s | %s %s | %s %s | %s |   (change from 40 Ry, eV)' % (
                '', f(d(pr_f, base['pr_f']), '%+.4f', 10), f(d(rb_f, base['rb_f']), '%+.4f', 10),
                f(d(pr_c, base['pr_c']), '%+.4f', 10), f(d(rb_c, base['rb_c']), '%+.4f', 10),
                f(d(con, base['con']), '%+.4f', 9)))
    print('\nTotal-energy change per atom from 40 Ry (meV/atom) and magnetisation m / m_abs:')
    print('%5s | ' % 'ecut' + ' | '.join('%-24s' % c for c in CELLS))
    for ec in cuts:
        cells = []
        for c in CELLS:
            r = R.get('job1_%s_ec%d' % (c, ec))
            e = energy(R, 'job1_%s_ec%d' % (c, ec))
            de = (e - E40[c]) / NAT[c] * RY_EV * 1000 if e is not None and E40.get(c) is not None else None
            mm = '%s/%s' % (f(r['mtot'], '%.2f', 0), f(r['mabs'], '%.2f', 0)) if r else '-'
            cells.append('%9s  %-13s' % (f(de, '%+.2f', 9).strip() if de is not None else '-', mm))
        print('%5d | ' % ec + ' | '.join('%-24s' % x for x in cells))
    print('A change of m_abs between cut-offs means a different spin solution: compare with care.')
    for ec in cuts:
        r = R.get('job1_O2_ec%d' % ec)
        if usable(r):
            print('O2 box %d Ry: E = %.8f Ry (production 40 Ry O2: %.8f Ry)' % (ec, r['E'], 2 * HALF_O2_PROD))


def section_pristine(R, prod_pvo):
    header('JOB 2 -- pristine V_O at 2x2x2 (reviewer Q3, audit R10)')
    ePVO = energy(R, 'job2_Pristine_VO_k222')
    efG = ef(prod_pvo, PROD['Pristine_perfect'], HALF_O2_PROD)
    print('E_f(V_O; pristine), Gamma, production          : %s eV' % f(efG, '%.4f', 8))
    for t in sorted(t for t in R if t.startswith('job2_Pristine_VO_G')):
        e = energy(R, t)
        print('E_f(V_O; pristine), Gamma, %-20s: %s eV' % (t[5:], f(ef(e, PROD['Pristine_perfect'], HALF_O2_PROD), '%.4f', 8)))
    ef2 = ef(ePVO, LEDGER['Pristine_perfect_k222'], HALF_O2_PROD)
    print('E_f(V_O; pristine), 2x2x2 (job 2 + ledger run 28): %s eV' % f(ef2, '%.4f', 8))
    r = R.get('job2_Pristine_VO_k222')
    if r:
        print('  job 2: m = %s, m_abs = %s, -TS = %s Ry, width %s Ry' % (
            f(r['mtot'], '%.2f', 0), f(r['mabs'], '%.2f', 0), f(r['TS'], '%.6f', 0), r['width']))
    pr2 = ef(LEDGER['Pr_VO_k222'], LEDGER['Pr_perfect_k222'], HALF_O2_PROD)
    rb2 = ef(LEDGER['Rb_VO_k222'], LEDGER['Rb_perfect_k222'], HALF_O2_PROD)
    print('2x2x2 set: pristine %s | Pr %s | Rb %s eV (Pr, Rb from ledger runs 8/32, 10/36)' % (
        f(ef2, '%.3f', 0), f(pr2, '%.3f', 0), f(rb2, '%.3f', 0)))
    print('NOTE: the production pristine V_O relaxation used degauss 0.01 Ry (SI S1); the width of job 2'
          ' is printed above.')


def section_smearing(R):
    header('JOB 3 -- smearing test on the odd-electron Pr cells (reviewer Q7)')
    print('F = "!" total energy (free energy), E = F + TS (internal energy). For Gaussian smearing'
          ' (F+E)/2 estimates the sigma -> 0 energy; for cold (m-v) smearing F itself does.\n')
    print('%-12s %-22s %16s %11s %16s %16s %10s %6s %6s %9s' % (
        'cell', 'setting', 'F (Ry)', '-TS (Ry)', 'E (Ry)', '(F+E)/2 (Ry)', 'dF (meV)', 'm', 'm_abs', 'E_F'))
    efs = {}
    for c in ('Pr_perfect', 'Pr_VO'):
        ref = R.get('job1_%s_ec40' % c)
        variants = [('gaussian 0.005 (ref)', ref), ('gaussian 0.002', R.get('job3_%s_gauss0p002' % c)),
                    ('m-v 0.005', R.get('job3_%s_mv0p005' % c))]
        Fref = ref['E'] if usable(ref) else PROD[c]
        for name, r in variants:
            if r is None:
                print('%-12s %-22s %s' % (c, name, 'not run'))
                continue
            F, TS, E = r['E'], r['TS'], r['Eint']
            half = (F + E) / 2 if F is not None and E is not None and 'gauss' in name else None
            dF = (F - Fref) * RY_EV * 1000 if F is not None else None
            print('%-12s %-22s %s %s %s %s %s %s %s %9s' % (
                c, name, f(F, '%.8f', 16), f(TS, '%.6f', 11), f(E, '%.8f', 16), f(half, '%.8f', 16),
                f(dF, '%+.2f', 10), f(r['mtot'], '%.2f', 6), f(r['mabs'], '%.2f', 6), r['EF'] or '-'))
            efs.setdefault(name, {})[c] = F if usable(r) else None
    print('\nE_f(V_O; Pr) per smearing setting (F energies, production 1/2 E(O2)):')
    for name, d in efs.items():
        print('  %-22s %s eV' % (name, f(ef(d.get('Pr_VO'), d.get('Pr_perfect'), HALF_O2_PROD), '%.4f', 8)))


def section_d3(R):
    header('JOB 4 -- D3(BJ) formation-energy cycle (completes the dispersion correction)')
    print('Existing D3 single points (ledger): Pr_VO %.8f Ry (D3 term %.5f), Rb_VO %.8f Ry (D3 term %.5f)' % (
        LEDGER['Pr_VO_D3'], LEDGER['Pr_VO_D3_term'], LEDGER['Rb_VO_D3'], LEDGER['Rb_VO_D3_term']))
    d3 = {}
    for t in ('job4_Pr_perfect_D3', 'job4_Rb_perfect_D3', 'job4_O2_D3'):
        r = R.get(t)
        if r is None:
            print('%-20s not run' % t)
            continue
        d3[t] = r['d3']
        print('%-20s E = %s Ry  D3 term = %s Ry  m = %s  status: %s' % (
            t, f(r['E'], '%.8f', 16), f(r['d3'], '%.6f', 10), f(r['mtot'], '%.2f', 0), status(r)))
    o2t = d3.get('job4_O2_D3')
    for dop in ('Pr', 'Rb'):
        pt = d3.get('job4_%s_perfect_D3' % dop)
        vt = LEDGER['%s_VO_D3_term' % dop]
        if pt is None or o2t is None:
            print('Delta E_f(D3; %s): needs job4_%s_perfect_D3 and job4_O2_D3' % (dop, dop))
            continue
        dEf = (vt - pt + 0.5 * o2t) * RY_EV
        e_vo = energy(R, 'job1_%s_VO_ec40' % dop) or LEDGER['%s_VO_scratch' % dop]
        e_pf = energy(R, 'job1_%s_perfect_ec40' % dop) or PROD['%s_perfect' % dop]
        base = ef(e_vo, e_pf, HALF_O2_PROD)
        tot = ef(LEDGER['%s_VO_D3' % dop], energy(R, 'job4_%s_perfect_D3' % dop),
                 energy(R, 'job4_O2_D3') / 2 if energy(R, 'job4_O2_D3') is not None else None)
        print('%s: Delta E_f(D3) = D3(VO) - D3(perfect) + 1/2 D3(O2) = %+.4f eV;  E_f(PBE+U, from-scratch '
              'refs) = %s eV  ->  E_f(PBE+U+D3) = %s eV;  total-energy route: %s eV' % (
                  dop, dEf, f(base, '%.4f', 0), f(base + dEf if base is not None else None, '%.4f', 0),
                  f(tot, '%.4f', 0)))
    print('(The D3 term changes the energy only, so the D3-term route is free of the from-scratch'
          ' versus relaxation-endpoint offsets.)')


def section_nosym(R):
    header('JOBS 5 and 6 -- symmetry-broken hole search without symmetry (reviewer Q2)')
    tags = sorted(t for t in R if t.startswith('job5_') or t.startswith('job6_'))
    if not tags:
        print('no job-5 or job-6 outputs yet')
        return
    print('dE_prod: versus the production total energy (Rb_VO %.5f, Rb_perfect %.5f Ry);' % (
        PROD['Rb_VO'], PROD['Rb_perfect']))
    print('dE_ref : versus the 40 Ry from-scratch single point with symmetry (job 1, or ledger run 34'
          ' for Rb_VO).\n')
    print('%-32s %16s %10s %10s %6s %6s %4s %8s  %-30s %s' % (
        'job', 'E (Ry)', 'dE_prod', 'dE_ref', 'm', 'm_abs', 'nsym', 'm(Oh)', 'largest site moments', 'note'))
    for t in tags:
        r = R[t]
        cell = 'Rb_VO' if '_Rb_VO_' in t else 'Rb_perfect'
        m = re.search(r'Oh(\d+)', t)
        oh = int(m.group(1)) if m else None
        e = r['E'] if usable(r) else None
        dprod = (e - PROD[cell]) * RY_EV * 1000 if e is not None else None
        ref = energy(R, 'job1_%s_ec40' % cell) or (LEDGER['Rb_VO_scratch'] if cell == 'Rb_VO' else None)
        dref = (e - ref) * RY_EV * 1000 if e is not None and ref is not None else None
        moms = r['moments']
        top = sorted(moms.items(), key=lambda kv: -abs(kv[1]))[:3]
        tops = ' '.join('%d:%+.2f' % kv for kv in top) if top else '-'
        note = ''
        if t.startswith('job5_') and e is not None:
            note = 'LOWER than production -> job 6' if e < PROD[cell] - 1e-4 else 'not lower'
        print('%-32s %s %s %s %s %s %4s %s  %-30s %s' % (
            t, f(e, '%.8f', 16), f(dprod, '%+.1f', 10), f(dref, '%+.1f', 10), f(r['mtot'], '%.2f', 6),
            f(r['mabs'], '%.2f', 6), r['nsym'] if r['nsym'] is not None else '-',
            f(moms.get(oh), '%+.3f', 8), tops, note or status(r)))
    print('\n(dE in meV; site moments are the pw.x sphere-integrated values "atom:moment", not Loewdin;'
          ' run projwfc.x on the kept .save folders for Loewdin moments.)')


def section_relax(R, dualu_rbp):
    header('JOBS 7, 7b and 8 -- dual-U (reviewer Q4, audit R06) and tight relaxations (audit R09)')
    tags = sorted((t for t in R if re.match(r'job(7|7b|8)_', t)), key=sort_key)
    if not tags:
        print('no job-7 or job-8 outputs yet')
        return
    print('%-28s %16s %-24s %10s %6s %6s %13s' % ('job', 'E (Ry)', 'status', 'Fmax', 'm', 'm_abs', 'E_F'))
    for t in tags:
        r = R[t]
        print('%-28s %s %-24s %s %s %s %13s' % (t, f(r['E'], '%.8f', 16), status(r), f(r['fmax'], '%.5f', 10),
                                                 f(r['mtot'], '%.2f', 6), f(r['mabs'], '%.2f', 6), r['EF'] or '-'))
    # job 8: re-evaluated formation energies
    print('\nTight relaxations (job 8): E_f(V_O) with production 1/2 E(O2); a perfect cell not yet '
          'tightened falls back to its production energy (*).')
    for dop in ('Pr', 'Rb'):
        vo = energy(R, 'job8_%s_VO_tight' % dop)
        pf = energy(R, 'job8_%s_perfect_tight' % dop)
        star = '' if pf is not None else '*'
        if pf is None:
            pf = PROD['%s_perfect' % dop]
        new = ef(vo, pf, HALF_O2_PROD)
        old = ef(PROD['%s_VO' % dop], PROD['%s_perfect' % dop], HALF_O2_PROD)
        print('  %s: production %.4f eV -> tight %s eV%s  (change %s eV)' % (
            dop, old, f(new, '%.4f', 0), star, f(new - old if new is not None else None, '%+.4f', 0)))
    # job 7 and 7b: dual-U
    o2u = energy(R, 'job7_O2_dualU')
    print('\nDual-U formation energies. O2 reference: (i) production PBE 1/2 E(O2) = %.5f Ry; '
          '(ii) dual-U O2 box (job 7) = %s Ry.' % (HALF_O2_PROD, f(o2u / 2 if o2u else None, '%.5f', 0)))
    e7 = energy(R, 'job7_Pr_VO_dualU_relax')
    print('  Pr (dual-U Pr_perfect = ledger run 19, %.5f Ry): (i) %s eV  (ii) %s eV' % (
        LEDGER['Pr_perfect_dualU'], f(ef(e7, LEDGER['Pr_perfect_dualU'], HALF_O2_PROD), '%.4f', 0),
        f(ef(e7, LEDGER['Pr_perfect_dualU'], o2u / 2 if o2u else None), '%.4f', 0)))
    e7b = energy(R, 'job7b_Rb_VO_dualU_relax')
    if dualu_rbp is None:
        print('  Rb: needs the dual-U Rb_perfect energy (--dualu-rb-perfect FILE_OR_RY)')
    else:
        print('  Rb (dual-U Rb_perfect = %.5f Ry): (i) %s eV  (ii) %s eV' % (
            dualu_rbp, f(ef(e7b, dualu_rbp, HALF_O2_PROD), '%.4f', 0),
            f(ef(e7b, dualu_rbp, o2u / 2 if o2u else None), '%.4f', 0)))
    print('  Report both O2 choices: U on the O-2p states of an isolated O2 molecule is not standard.')


def section_pristine_perfect(R):
    header('JOB 0 -- relaxation of the pristine perfect cell (production value: unrelaxed single point, F_max 0.0225 Ry/Bohr)')
    r = R.get('job0_Pristine_perfect_relax')
    if not r:
        print('no job-0 output yet')
        return
    e = r['E'] if usable(r) else None
    if e is None:
        print('job 0: ' + status(r))
        return
    print('E(Pristine_perfect) relaxed   : %.8f Ry   (production single point %.5f Ry)' % (e, PROD['Pristine_perfect']))
    print('relaxation energy             : %+.4f eV  (expected negative)' % ((e - PROD['Pristine_perfect']) * RY_EV))
    ef_old = ef(PROD['Pristine_VO'], PROD['Pristine_perfect'], HALF_O2_PROD)
    ef_new = ef(PROD['Pristine_VO'], e, HALF_O2_PROD)
    print('E_f(V_O; pristine): production %.3f eV (lower bound) -> with the relaxed perfect cell %.3f eV' % (ef_old, ef_new))
    for lab, vo, perf in (('Pr', 'Pr_VO', 'Pr_perfect'), ('Rb', 'Rb_VO', 'Rb_perfect')):
        efd = ef(PROD[vo], PROD[perf], HALF_O2_PROD)
        print('reduction relative to pristine, %s: %.3f eV (manuscript lower bound %.3f eV)' % (lab, ef_new - efd, ef_old - efd))
    print('status: %s. Update Table 2, Sections 2.6, 3.2, 4.1, 5(iv) and the Conclusions with these values.' % status(r))


def section_hp(R):
    r = R.get('job9_anatase_hp')
    if r is None:
        return
    header('JOB 9 -- hp.x linear-response U (12-atom anatase); check the q-mesh convergence')
    if r['hp']:
        for line in r['hp']:
            print('  ' + line)
    else:
        print('  no "Hubbard U parameters" block found (status: %s); read the end of %s' % (status(r), r['path']))


def check_production(prod_dir, pristine_vo):
    header('PRODUCTION ENERGIES used above (cross-check against the production outputs if found)')
    files = dict(PROD_FILES)
    if pristine_vo:
        files['Pristine_VO'] = pristine_vo
    for c, e in PROD.items():
        fn = files.get(c)
        path = fn if fn and os.path.isabs(fn) else (os.path.join(prod_dir, fn) if fn and prod_dir else None)
        msg = 'output not found'
        if path and os.path.isfile(path):
            r = parse_out(path)
            if r['E'] is None:
                msg = 'no "!" energy in %s' % path
            elif abs(r['E'] - e) < 2e-5:
                msg = 'matches %s (%.8f)' % (os.path.basename(path), r['E'])
            else:
                msg = 'WARNING: %s ends at %.8f Ry (differs by %.1f meV)' % (
                    os.path.basename(path), r['E'], (r['E'] - e) * RY_EV * 1000)
            if r['width'] is not None:
                msg += '; smearing %s %.4f Ry' % (r['smear'], r['width'])
        print('  %-17s %.5f Ry   %s' % (c, e, msg))
    return files


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('run_dir', nargs='?', default=os.path.join(here, 'runs'))
    ap.add_argument('--prod-dir', default=os.path.dirname(here))
    ap.add_argument('--pristine-vo-out', default=os.environ.get('PRISTINE_VO_OUT', ''))
    ap.add_argument('--dualu-rb-perfect', default='')
    ap.add_argument('--csv', default=None)
    a = ap.parse_args()

    outs = sorted(p for p in glob.glob(os.path.join(a.run_dir, 'job*.out')))
    if not outs:
        print('no job*.out files in %s' % a.run_dir)
        return 1
    R = {}
    for p in outs:
        try:
            r = parse_out(p)
        except OSError as exc:
            print('cannot read %s: %s' % (p, exc))
            continue
        R[r['tag']] = r

    print('Revision runs in %s (%d outputs); 1 Ry = %.6f eV' % (os.path.abspath(a.run_dir), len(R), RY_EV))
    table(R, a.csv or os.path.join(a.run_dir, 'revision_summary.csv'))

    pvo = a.pristine_vo_out
    if pvo and not os.path.isabs(pvo):
        pvo = os.path.join(a.prod_dir, pvo)
    check_production(a.prod_dir, pvo)

    dualu_rbp = None
    if a.dualu_rb_perfect:
        try:
            dualu_rbp = float(a.dualu_rb_perfect)
        except ValueError:
            if os.path.isfile(a.dualu_rb_perfect):
                dualu_rbp = parse_out(a.dualu_rb_perfect)['E']

    section_cutoff(R)
    section_pristine(R, PROD['Pristine_VO'])
    section_pristine_perfect(R)
    section_smearing(R)
    section_d3(R)
    section_nosym(R)
    section_relax(R, dualu_rbp)
    section_hp(R)
    return 0


if __name__ == '__main__':
    sys.exit(main())
