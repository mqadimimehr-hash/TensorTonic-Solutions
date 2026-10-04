# Revision calculations: Pr- and Rb-substituted anatase TiO2 (DFT+U)

## Queue summary

Wall times are for the i5-3570 with `mpirun -np 4`. They are scaled from the measured times in SI Table S6:
- D3 Γ single points of Pr_VO and Rb_VO: ≈ 6 h each.
- 2×2×2 single points of Pr_perfect and Rb_perfect: ≈ 3 h each.
- Production relaxations: ≈ 3 days each.
- Pristine V_O relaxation: ≈ 14 h.
- Dual-U Pristine single point plus Pr_perfect relaxation: ≈ 24 h together.
- Three alternative-site relaxations: ≈ 33 h together.

Basis used here: a from-scratch Γ SCF of a 47/48-atom cell at 40 Ry takes **≈ 3–6 h**. For 55 and 70 Ry, multiply by (ecut/40)^1.5, i.e. ≈ 1.6× and ≈ 2.3×.

| Job | Purpose (reviewer question / audit item) | Runs | Est. wall time |
|---|---|---|---|
| **P1** | *default queue* | **27** | **≈ 5–11 days** |
| 1 | Cut-off convergence of E_f(V_O) and the Pr–Rb contrast (Q1, R09): 55/440 and 70/560 Ry for Pr_perfect, Pr_VO, Rb_perfect, Rb_VO. Also 40 Ry reference single points on the same geometries, and O2 boxes at 40/55/70 Ry | 8 + 4 refs + 3 O2 | ≈ 2.5–5 days (the 8 requested runs alone: ≈ 2–4 days) |
| 2 | Pristine V_O at 2×2×2 k-points (Q3, R10) | 1 (+1 optional Γ ref) | ≈ 3–8 h |
| 0 | Relaxation of the pristine perfect cell: its production energy is an unrelaxed single point (F_max 0.0225 Ry/Bohr), so the pristine E_f and the two reductions measured from it are lower bounds (main text Section 2.6) | 1 relax | ≈ 1–3 days |
| 3 | Smearing test on the odd-electron Pr cells: Gaussian 0.002 Ry and cold (m-v) 0.005 Ry (Q7) | 4 | ≈ 12–24 h |
| 4 | D3(BJ) on Pr_perfect, Rb_perfect and O2; with the existing D3 runs on Pr_VO and Rb_VO this completes the D3 cycle (R13) | 3 | ≈ 7–14 h |
| 5 | Symmetry-broken hole search: nosym SCF with one seeded oxygen, species label "O1" (Q2) | 3 | ≈ 12–24 h |
| **P2** | *`RUN_P2=1`* | **6–9** | **≈ 4–11 days (+ job 6 if triggered)** |
| 6 | nosym re-relaxation, **only** if a job-5 SCF lies below the production energy (Q2) | 0–2 | ≈ 1–3 days each |
| 7 | Dual-U Pr_VO relaxation, plus the optional dual-U O2 single point (Q4, R06) | 1 + 1 | ≈ 1–3 days |
| 7b | Optional: finish the dual-U Rb_VO relaxation from its last geometry (Q4). Runs only if `DUALU_RBVO_OUT` is set | 0–1 | ≈ 0.5–2 days |
| 8 | Tight relaxations, forc_conv_thr 0.001 Ry/Bohr, of Pr_VO, Rb_VO, Pr_perfect, Rb_perfect (R09) | 4 | ≈ 0.5–1.5 days each, 2–6 days total |
| **P3** | *HPC; `RUN_P3=1` only* | | |
| 9 | Linear-response U (hp.x) for 12-atom anatase, Ti-3d and O-2p (supports the choice of U) | 1 pw.x + 1 hp.x | i5: ≈ 1 h + 0.5–1.5 days; one HPC node: ≈ 1–3 h |
| 10 | 2×2×2 supercell (96 atoms) of Rb_VO and Pr_VO: cost note only (below) | – | single point ≈ 0.6–2 days on the i5; relaxations need HPC |

The order above is the run order (jobs 1, 2, 0, 3, 4, 5). Job 0 reads the positions from `Pristine_perfect.out` (variable `SRC_Pristine_perfect`) and relaxes them with the production thresholds; the analysis prints the relaxation energy, the corrected pristine E_f and the corrected reductions. A run whose `.out` already contains `JOB DONE` is skipped, so the launcher can be restarted at any time.

## Files

| File | What it is |
|---|---|
| `launch_revision_queue.sh` | Builds every input from `templates/` and runs the queue. Positions come from the production relaxation outputs, using the `extract_positions()` logic of `launch_U_sensitivity_queue.sh`: the `Begin final coordinates` block, else the last *complete* `ATOMIC_POSITIONS` block |
| `analyze_revision_runs.py` | Parses every `runs/job*.out` and prints the summary table and the job-specific analyses (also writes `runs/revision_summary.csv`) |
| `templates/job1_cutoff_scf.in`, `job1_O2_box_cutoff.in` | Job 1: cut-off single point; triplet O2 box (12 Å, short relax from 1.23 Å) at the same cut-off |
| `templates/job2_pristine_VO_k222.in` | Job 2 |
| `templates/job3_smearing_scf.in` | Job 3 |
| `templates/job4_d3_scf.in`, `job4_O2_box_d3.in` | Job 4 (`vdw_corr='dft-d3'`, `dftd3_version=4`, `dftd3_threebody=.false.`) |
| `templates/job5_nosym_hole_scf.in`, `job6_nosym_hole_relax.in` | Jobs 5 and 6: `nosym`, `noinv`; species Ti, O, O1 (same O PAW file), Rb; `starting_magnetization(3)=0.5` on Oh only; U on Ti-3d only |
| `templates/job7_dualU_PrVO_relax.in`, `job7_O2_box_dualU.in`, `job7b_dualU_RbVO_relax.in` | Jobs 7 and 7b (U Ti-3d 3.5 + U O-2p 5.5) |
| `templates/job8_tight_relax.in` | Job 8 |
| `templates/job9_anatase_lr_scf.in`, `job9_anatase_hp.in` | Job 9 (pw.x ground state with U = 1.0d-8 on Ti-3d and O-2p, then hp.x) |

Placeholders in the templates have the form `__NAME__`; the launcher refuses to write an input that still contains one.

## What each job answers

- **Job 1, Q1 (cut-off).** The paper's E_f(V_O) use 40/320 Ry. Job 1 repeats the four doped cells at 55/440 and 70/560 Ry on identical geometries. The analysis prints E_f(V_O; Pr), E_f(V_O; Rb) and the Pr–Rb contrast at each cut-off, in two versions:
  - with the production ½E(O2) = −41.51621 Ry fixed;
  - with the O2 box recomputed at the same cut-off.

  The contrast does not depend on the O2 reference at all. Why the extra 40 Ry references:
  - The production energies are relaxation endpoints. From-scratch single points on the extracted geometries differ from them by 0.5 mRy (Rb_VO, a different spin solution) and 2.8 mRy (Pr_VO, whose relaxation was stopped by hand; SI S7).
  - A cut-off difference is therefore only clean against a 40 Ry single point run the same way.
  - The 40 Ry references also serve as the job-3 and job-4 baselines.
- **Job 2, Q3 (pristine 2×2×2).** The 2×2×2 energies exist for the doped cells and for Pristine_perfect (ledger run 28) but not for the pristine V_O cell. Job 2 completes the three formation energies at 2×2×2.
- **Job 3, Q7 (smearing).** Pr_perfect (383 valence electrons) and Pr_VO (377) have odd electron counts and m = 0, so the smearing decides the fractional occupations.
  - The analysis extracts `smearing contrib. (-TS)` and `internal energy E=F+TS` and prints (F+E)/2, the σ→0 estimate for Gaussian smearing.
  - It compares Gaussian 0.005 (job-1 reference), Gaussian 0.002 and Marzari–Vanderbilt 0.005, and gives E_f(V_O; Pr) for each.
- **Job 4, dispersion (R13).** The existing D3 single points on Pr_VO and Rb_VO (SI Table S5) **complete the set** together with job 4's Pr_perfect, Rb_perfect and O2. The analysis then gives the D3-corrected E_f(V_O) for both dopants.
  - It uses the D3 terms directly: D3 changes only the energy, so ΔE_f(D3) = D3(VO) − D3(perfect) + ½D3(O2).
  - This route is free of endpoint offsets. The total-energy route is printed as a check.
- **Job 5, Q2 (symmetry).** The relaxed Rb_VO cell keeps a mirror plane (2 operations). Rb (atom 3) and the hole-carrying O8 (+0.59 μB) lie on that plane; O6 and O17 (+0.11 each) are its mirror pair.
  - Job 5 switches symmetry off and seeds one oxygen (species label O1, `starting_magnetization` 0.5, all other species 0; output files are tagged `Oh<atom number>`).
  - Rb_VO seeds: O8 (on the mirror) and O6 (off the mirror).
  - Rb_perfect seed: the oxygen with the shortest Rb–O bond. **The launcher computes it** with a small python snippet: minimum image in the production geometry, the six nearest O printed to the log. Override it with `RB_PERFECT_OH_INDEX=<atom>`.
  - The analysis compares each energy with the production energy (Rb_VO −4289.17135 Ry, Rb_perfect −4330.38890 Ry) and with the 40 Ry symmetric reference. It also lists the pw.x site moments, including the moment on Oh.
- **Job 6, Q2 follow-up.** Runs only with `RUN_P2=1`. For Rb_VO, the lowest job-5 seed is re-relaxed (same O1 seed, nosym, production thresholds) if it lies more than `P2_ETOL_RY` (default 1×10⁻⁴ Ry ≈ 1.4 meV) below the production energy. Rb_perfect follows the same rule.
- **Job 7, Q4 (dual-U, R06).** Dual-U relaxation of Pr_VO from the production single-U geometry, with spin seeds Ti 0.3 and Pr 0.5 so that a localised O-2p hole can form. With ledger run 19 (dual-U Pr_perfect, −4571.33095 Ry) this gives the dual-U E_f(V_O; Pr).
  - The optional dual-U O2 single point (U O-2p 5.5 on O, triplet) provides a consistent O2 reference. The launcher uses the relaxed geometry of `job1_O2_ec40` when that run has finished.
  - The analysis prints E_f with both O2 references. U on an isolated O2 molecule is not standard, so report both.
- **Job 7b, Q4 (optional).** The dual-U Rb_VO relaxation was "not completed when logged". Set `DUALU_RBVO_OUT` (line 54 of the launcher) to its output: the launcher restarts it from the last complete geometry and reads the starting magnetisation that run used.
  - For the dual-U E_f(V_O; Rb), also set `DUALU_RBP_OUT` (line 57) to the dual-U Rb_perfect output. Its Ry energy was logged only in eV.
- **Job 8, force convergence (R09).** Re-relaxes from the production geometries to 0.001 Ry/Bohr; the analysis re-evaluates E_f(V_O). If a perfect cell is not finished yet, its production energy is used and the result is marked.
- **Job 9, U (P3).** Linear-response U for Ti-3d and O-2p in the 12-atom anatase cell (a = 3.81816 Å, c = 9.77900 Å, u = 0.208), followed by hp.x with nq = 3×3×1.
  - **The q mesh must be converged:** repeat with 3×3×2, and with 4×4×2 using k 8×8×2.
  - The ground-state `conv_thr` is deliberately 1.0d-12, because linear response needs a tightly converged SCF.
  - hp.x prints the U values at the end of its output and writes `anatase_lr.Hubbard_parameters.dat` (the file name can vary between versions).
  - All hp.x keywords used (`prefix`, `outdir`, `nq1–3`, `conv_thr_chi`, `iverbosity`) are standard `&inputhp` entries. Inside a namelist, comments must start with `!`.

## Commands

```bash
# 1. Copy this folder into the QE working directory (adjust the source path)
mkdir -p ~/tio2_vo/revision_calculations
cp -r /mnt/c/Users/<you>/Desktop/revision_calculations/. ~/tio2_vo/revision_calculations/
cd ~/tio2_vo/revision_calculations
sed -i 's/\r$//' launch_revision_queue.sh analyze_revision_runs.py   # only if the files passed through a Windows editor
chmod +x launch_revision_queue.sh

# 2. Set the name of the pristine V_O relaxation output: edit line 50 of the launcher
#    (PRISTINE_VO_OUT=...). For job 7b also set line 54 (DUALU_RBVO_OUT) and line 57 (DUALU_RBP_OUT).
ls -lt ~/tio2_vo/*.out

# 3. Dry run: builds all inputs into runs/, runs nothing. Read the log.
bash launch_revision_queue.sh --dry-run 2>&1 | tee dryrun.log
grep -E "ERROR|WARNING|FALLBACK|Oh = atom|production output" dryrun.log

# 4. Launch P1 (nothing else may be running on the 4 cores)
pgrep -a -x 'pw\.x|hp\.x|projwfc\.x' || echo "nothing running"
nohup bash launch_revision_queue.sh > revision.log 2>&1 & disown

# 5. Later: P2. Finished P1 runs are skipped.
RUN_P2=1 nohup bash launch_revision_queue.sh > revision_p2.log 2>&1 & disown
```

Monitoring and control:

```bash
tail -f revision.log                                      # START/END lines with time stamps
column -t -s $'\t' runs/queue_times.tsv                   # start, end, seconds, status of every run
grep -c '^!' runs/job8_Pr_VO_tight.out                    # SCF cycles completed in a relaxation
grep 'Total force' runs/job8_Pr_VO_tight.out | tail -3
python3 analyze_revision_runs.py runs | tee revision_analysis.txt   # any time; also written automatically at the end
```

Options:
- **Selected jobs only:** `JOBS="2 3"` or `JOBS="7 7b 8"` overrides RUN_P1/2/3.
- **The quickest cut-off answer first:** `JOB1_CUTS="55"` runs only the 55 Ry set. A later launch without it adds 70 Ry.
- **Optional pristine Γ reference** at the job-2 smearing width: `JOB2_GAMMA_REF=1`.
- **Stopping and resuming:** `pkill -f launch_revision_queue.sh; pkill -x pw.x`. Relaunch later:
  - an interrupted relaxation restarts from the last complete geometry in its `.out`, and the old file is kept as `*.out.interrupted_<date>`;
  - an interrupted SCF starts again from scratch.
- **A relaxation that stopped at nstep:** relaunch with `RESTART_MAXSTEP=1` to continue it.
- **Spin pools:** `PW_FLAGS="-nk 2"` puts the two spin channels on separate pools. This is often 1.3–1.7× faster but needs about twice the memory. Try it on one 40 Ry job before using it at 70 Ry.
- **P3 on an HPC system:** `RUN_P3=1 bash launch_revision_queue.sh --dry-run` writes `runs/job9_anatase_lr_scf.in` and `runs/job9_anatase_hp.in`. Copy both, fix `pseudo_dir`, then run `pw.x -in job9_anatase_lr_scf.in`, followed by `hp.x -in job9_anatase_hp.in` in the same directory.

## Checks the launcher makes before it runs anything

- `pw.x` and `mpirun` are on PATH, no pw.x/hp.x/projwfc.x is running, the four UPF files exist in `~/tio2_vo/pseudo`, and there is at least 15 GB free disk.
- For every production output it reads the composition (Ti/O/dopant counts), the printed cut-offs and the smearing width.
  - **It stops if a width differs from `DEGAUSS` (default 0.005 Ry).** Re-run with `DEGAUSS=0.01` if production used 0.01, or force it with `ALLOW_DEGAUSS_MISMATCH=1`.
  - The pristine V_O cell is exempt: its relaxation used 0.01 Ry (SI S1); job 2 uses `JOB2_DEGAUSS`, which defaults to `DEGAUSS`.
- The starting magnetisation of the replicate runs is read from the `Starting magnetic structure` block of each production output. The run log says 0 on all species, and that is the fallback; the log flags any fallback.
- In Rb_VO, atom 3 must be Rb and every seeded atom must be an oxygen.

## Disk and memory

- **Disk.** Everything goes to `runs/`, with pw.x scratch in `runs/scratch/`. Each Γ single point keeps about 130 MB of wavefunctions and density at 40 Ry, about 200 MB at 55 Ry and about 300 MB at 70 Ry; the 2×2×2 run keeps about 1 GB. Relaxation outputs (verbosity high) can reach 50–200 MB each. Plan for **≈ 10 GB**; the launcher warns below 15 GB free.
  - The `.save` folders of jobs 5 and 6 are worth keeping: `projwfc.x` on them gives Löwdin moments of the nosym states. Use the existing projwfc template with prefix = tag and outdir = `./scratch`.
  - Everything else in `runs/scratch` can be deleted once the analysis is done.
- **Memory.** Estimates for 4 MPI ranks:
  - 40 Ry, 48-atom Γ LSDA run: ≈ 1.5–2.5 GB;
  - 70 Ry: ≈ 3–4 GB;
  - 2×2×2: ≈ 2–3 GB;
  - O2 box at 70 Ry: ≈ 1–2 GB.

  pw.x prints `Estimated total dynamical RAM` near the top of every output; check it in the first minutes of the first 70 Ry run. With 7.7 GB visible in WSL, close large Windows programs during the 70 Ry runs. If WSL is capped lower, raise `memory=` under `[wsl2]` in `%UserProfile%\.wslconfig`.
- **Multi-day runs.** Disable Windows sleep and pause Windows Update for the P2 period. A reboot kills the queue; relaunching resumes it as described above.
- **Location.** Keep the runs on the Linux filesystem (`~/tio2_vo`), not under `/mnt/c`.

## Job 10: 2×2×2 supercell (96 atoms), cost note

The 96-atom cell is 2×2×2 of the conventional 12-atom cell, i.e. the 48-atom cell doubled along c (7.636 × 7.636 × 19.558 Å).

**Single point.** Twice the atoms means twice the plane waves and twice the bands, so one SCF costs about 5–8× a 47-atom SCF: **≈ 15–48 h (0.6–2 days) per Γ single point on the i5**. It needs ≈ 4–6 GB, which is tight on 7.7 GB.

**Why a single point is not enough.**
- Replicating the relaxed 47-atom cell gives the same defect concentration and exactly the same energy per cell.
- A dilute single point needs a 95-atom cell with one dopant and one vacancy. Without relaxation its energy is only an upper bound.

**Relaxations.** A meaningful dilute-limit E_f needs relaxed V_O and perfect 96-atom cells for each dopant (4 relaxations, 5 with the pristine reference). At ≈ 6–8× the 3-day production relaxations, each takes **≈ 3 weeks on the i5**. That is impractical locally (for scale, the HSE06 single point took 8 days).
- On an HPC allocation (64–128 cores per run): ≈ 1–3 days per relaxation, roughly **6,000–10,000 core-hours** in total including single points (order of magnitude).
- Doubling c increases the defect separation along c only. A 3×3×1 conventional supercell (108 atoms) increases it in-plane instead.

## What to send back

```bash
cd ~/tio2_vo/revision_calculations
tar czf revision_results_$(date +%Y%m%d).tgz --exclude='runs/scratch' --exclude='runs/_positions' \
    revision*.log dryrun.log revision_analysis.txt runs
cp revision_results_*.tgz /mnt/c/Users/<you>/Desktop/
```

The archive contains:
- all `runs/*.in` and `runs/*.out`, including `*.out.interrupted_*`;
- `runs/queue_times.tsv` and `runs/revision_summary.csv`;
- the logs;
- the output of `analyze_revision_runs.py` (`revision_analysis.txt`).

## Assumptions to check before launching

1. **`PRISTINE_VO_OUT`** (line 50) is a placeholder name. Job 2 is skipped until it points to the real pristine V_O relaxation output.
2. **Smearing width.** The templates use `DEGAUSS` = 0.005 Ry, which is the production value as far as known. SI Table S10 leaves 0.005 versus 0.01 open; the launcher reads the printed width and stops on a mismatch.
3. **Starting magnetisation.** Read from the production outputs. Check the `starting magnetisation (...)` lines of the dry-run log.
4. **Rb_VO has two near-degenerate spin solutions.** The production relaxation has m_abs 1.21 μB at −4289.17135 Ry; from-scratch runs give m_abs 1.00 μB at −4289.17088 Ry.
   - Job 5 is compared with the production energy as requested, and also with the 40 Ry from-scratch reference.
   - Job 6 uses the production energy plus `P2_ETOL_RY`.
5. **Species label `O1`.** The seeded oxygen is a separate species "O1" (element symbol plus a digit, the form the pw.x input documentation allows for extra labels of one element). It uses the O PAW file, and the species table of the output should show it with 6 valence electrons. Output files keep the tag `Oh<atom number>`.
6. **Relaxation thresholds.** Relaxations use `nstep = 300`; the QE default of 50 would stop the multi-day runs early. `etot_conv_thr` is left at the QE default (1×10⁻⁴ Ry) because the production value is not recorded; BFGS needs both the energy and the force criteria.
7. **O2 reference geometry.** The production O2 box geometry is unknown. Compare `job1_O2_ec40` with the production −83.03242804 Ry in the analysis output before using the cut-off-consistent O2 values.
8. **Hard-coded production energies.** The analysis takes them from the reviewer brief (Rb_VO, Rb_perfect) and from `energy_ledger.csv` (SI Table S9). It cross-checks them against `~/tio2_vo/*.out` when those files are present.
9. **Wall times.** The estimates above are extrapolations from SI Table S6; `runs/queue_times.tsv` records the real times.
