# HANDOFF — DFT+U manuscript on oxygen vacancies in Pr- and Rb-substituted anatase TiO₂

**Written:** 13 October 2026, at the end of the first Claude Code session on this project.
**Purpose:** paste or attach this file in a new Claude session so it can continue without re-deriving anything. Every number and path below was checked against the repository at commit `457e6e3` (branch head; it adds this file, the cover-letter fix and the `tools_package.sh` change described in §8; parent `2a43130`).

---

## 1. How to use this document

- **Start with §16 (quick start) and §9 (next steps).** The first job of the next session is almost certainly to fold in simulation outputs the user says already exist (§9.1).
- The repository is the single source of truth. This file tells you where things are and why they are the way they are; open the files before editing them.
- Rules that must not be broken are in §13. The user's communication style is in §14.

---

## 2. The project in one paragraph

Mohammad Ghadimimehr (PhD researcher, Universiti Malaya) has a Quantum ESPRESSO DFT+U study comparing Pr³⁺ and Rb⁺ substitution on the Ti site of anatase TiO₂ and how each changes the formation energy of a neutral oxygen vacancy (V_O). The original manuscript ("FINAL", June 2026) overclaimed heavily (design rules, "trap-free" Pr, 4f mechanism with a 4f-in-core pseudopotential, "closed-shell singlet", Ti³⁺ traps). Two external audits (Error Audit E1–E13, Full Reviewer/Editor Audit R01–R18) said "do not submit". This session rebuilt it as **manuscript v4**: same computed energies, bounded claims, full energy ledger, regenerated figures, verified citations, and a complete Elsevier submission package for **Applied Surface Science**. The package is finished (0 author-action markers in the cover letter, manuscript, highlights and SI). The user says the extra calculations requested by reviewers have already been run on his PC; their outputs have not yet been provided.

---

## 3. People, funding, journal, repository

| Item | Value |
|---|---|
| Authors | Mohammad Ghadimimehr (¹ Institute for Advanced Studies, UM; ² UMPEDAC, UM), **Azimah Binti Omar** (², ³ Dept. of Electrical Engineering, UM; **corresponding author**, azimahomar@um.edu.my), Siti Rohani Binti Sheikh Raihan (²) |
| Funding line (inserted 5 Oct 2026, supplied by the user) | "This work was supported by the Universiti Malaya Research Grant [grant number RU004-2025H]." |
| Acknowledgement | UMPEDAC, Universiti Malaya, for computational resources |
| Target journal | **Applied Surface Science** (Elsevier). Fallback: Journal of Alloys and Compounds (same submission system). Shortlist with 9 journals: `submission/Journal_Shortlist.md` |
| Claude's acceptance estimate (given to the user) | 20–30 % as submitted; 35–45 % if the reviewer-requested calculations are folded in. Largest risk: desk return on scope (bulk defect study, no surface calculation) |
| Submission status | **Unknown.** Package was ready on 5 Oct 2026 (cover letter fixed and package rebuilt on 13 Oct, see §8); whether the user uploaded it to Editorial Manager is not known. Ask. |
| Repository | `github.com/mqadimimehr-hash/TensorTonic-Solutions`, everything under `DFT_paper_revision/` |
| Branch | `claude/exciting-shannon-z4bl69` — develop and push only here: `git push -u origin claude/exciting-shannon-z4bl69` |
| Pull request | #5 — https://github.com/mqadimimehr-hash/TensorTonic-Solutions/pull/5 (open, mergeable, no CI, no reviews). Do **not** open a new PR unless asked. The PR description is stale (written in round 1) but has not been edited. When pushing the next round, update the PR #5 description (`gh pr edit 5 --body ...`) to summarise rounds 1–6 and end it with the PR attribution line from the system reminder; do not open a new PR. |
| Git identity for commits | `git -c user.email="23057283@siswa.um.edu.my" -c user.name="Mohammad Ghadimimehr" commit ...` |
| Commit message footer | Use the attribution lines the session's system reminder prescribes (a `Co-Authored-By:` line and a `Claude-Session:` URL line). No model names anywhere else in repo files. |
| Last commits | `457e6e3` HANDOFF.md, cover-letter fix, package script checks 01/03 · `2a43130` funding statement, package complete · `daa1c1a` round 5 · `8ec643f` revision_calculations · `d9e4af4` round 4 · `21ba26f` submission package folder |

---

## 4. Scientific content

### 4.1 Title, abstract, structure

- **Title:** *Oxygen-Vacancy Energetics and Dopant-Induced Holes in Pr- and Rb-Substituted Anatase TiO₂: A DFT+U Comparison* (original FINAL title was "Aliovalency over Ionic Radius: First-Principles Design Rules for Trap-Free Pr- and Rb-Doped Anatase TiO₂ Electron-Transport Layers in Indoor Photovoltaics").
- **Abstract:** 250 words counted as Word and Editorial Manager count (whitespace split; the stand-alone "Å" counts). Fixed on 13 Oct by deleting "wide-gap" from the first sentence; `tools_rebuild.sh` now prints this Word-style count. Limit 250: do not add words. It states the pristine value as "+4.74 eV (lower bound)".
- **Keywords:** DFT+U; anatase TiO₂; oxygen vacancy; aliovalent substitution; hole localisation; electron-transport layer.
- **Sections:** 1 Introduction · 2 Computational Methods (2.1 code/pseudopotentials with Table 1 electron counts, 2.2 Hubbard, 2.3 supercells, 2.4 k-sampling/electronic, 2.5 magnetisation conventions, 2.6 geometry, 2.7 formation energies, 2.8 additional calculations (i)–(vii)) · 3 Results (3.1 structure + Fig 1; 3.2 formation energies + Table 2 + Fig 2; 3.3 spin states + Table 3 + Fig 3; 3.4 oxygen-site Hubbard test + Table 4; 3.5 charged-cell spin series; 3.6 electronic structure + Fig 4; 3.7 sensitivity tests incl. "Uncertainty of the main results") · 4 Discussion (4.1–4.5) · 5 Limitations (i)–(xiv) · 6 Conclusions · Acknowledgements · Funding · Generative-AI declaration · CRediT · Data availability · Competing interest · References (50 cited).
- **Highlights** (`submission/Highlights.md`, each ≤ 85 characters):
  1. Pr³⁺ and Rb⁺ compared in one anatase TiO₂ supercell with one PBE+U protocol
  2. Oxygen-vacancy formation energy: ≥ +4.74 eV pristine, +1.29 eV Pr, −4.06 eV Rb (78 chars)
  3. The energetic order matches the formal hole count of 0, 1 and 3 per cell
  4. Löwdin spin of the Rb-cell hole sits mainly on one O bonded to Rb
  5. The spin state of the Pr-induced hole depends on an O-2p Hubbard term

### 4.2 Computational settings

| Setting | Value | Status |
|---|---|---|
| Code | Quantum ESPRESSO 7.5, run by the user on an Intel i5-3570 (4 cores, 7.7 GB under WSL), `mpirun -np 4` | |
| Functional | PBE | |
| PAW datasets (PSlibrary 1.0.0) | Ti.pbe-spn-kjpaw_psl.1.0.0 (Z_val 12), O.pbe-n-kjpaw_psl.1.0.0 (6), Pr.pbe-spdn-kjpaw_psl.1.0.0 (11, **4f frozen in core**), Rb.pbe-spn-kjpaw_psl.1.0.0 (9) | MD5 recorded for Ti, O, Rb; **Pr MD5 not recorded** |
| Hubbard | Dudarev, ortho-atomic projectors, U(Ti-3d) = 3.5 eV. Dual-U tests add U(O-2p) = 5.5 eV (transferred from Carey & Nolan Cr₂O₃ work; first-principles anatase value 7.66 eV per Orhan & O'Regan 2020) | linear-response U not done |
| Cut-offs | 40 Ry / 320 Ry | **no convergence test** in the paper |
| Supercell | 2×2×1 anatase, a = b = 7.63632 Å, c = 9.77900 Å, 570.25 Å³; 48 atoms perfect, 47 with V_O; 6.25 % cation substitution, 1 V_O = 3.1 % of O = 1.75×10²¹ cm⁻³ | lattice from vc-relax of 12-atom cell (its k-mesh, cut-off, stress not recorded) |
| k-points | Γ-only for relaxations; 2×2×2 single points for the doped cells; PDOS from 2×2×2 NSCF | pristine V_O never at 2×2×2 |
| Smearing | Gaussian; degauss 0.005 Ry in single-point templates, 0.01 Ry in pristine-V_O relaxation and PDOS SCFs | **production degauss not established**; −TS not extracted (estimate in §2.4 of the paper: ≈0.02 eV per level at 0.005 Ry) |
| Spin | nspin = 2; production starts from starting_magnetization = 0 on all species; one magnetic trial on Pr_VO (Ti 0.3, Pr 0.5) | symmetry left to default; Rb_VO kept a mirror plane (2 symmetry ops) |
| Relaxation | BFGS, forc_conv_thr 0.005 Ry/Bohr (0.129 eV/Å), mixing_beta 0.1, bfgs_ndim 3. Final F_max: Pr_perfect 0.0026, Pr_VO 0.0042 (stopped manually), Rb_perfect 0.0037, Rb_VO 0.0040 Ry/Bohr; pristine V_O 0.00563 | etot_conv_thr not recorded |
| **Pristine perfect cell** | **Single point on unrelaxed positions, F_max 0.0225 Ry/Bohr** (found in round 5 from the run spreadsheet) | → pristine E_f and the two reductions are **lower bounds** |
| O₂ reference | Triplet O₂ in 12 Å box, E = −83.03242804 Ry, ½E(O₂) = −41.51621 Ry = −564.857 eV; μ_O = ½E(O₂) (oxygen-rich), no overbinding or finite-T correction | |
| Extra | charged cells q = +1, +2 (uniform background, used only as spin diagnostic); U sweep 3.0/4.0/4.5 eV; HSE06 single point on pristine (input_dft 'hse', exx_fraction 0.25, screening 0.106 Bohr⁻¹; total not comparable with PBE+U); D3(BJ) single points on Pr_VO, Rb_VO; three alternative Pr V_O sites; Bader (valence pseudo-density, grid convergence not tested); projwfc.x Löwdin/PDOS | |

Electron counts (Table 1): Pristine_perfect 384, Pristine_VO 378, Pr_perfect 383 (1 hole), Pr_VO 377 (1 net excess electron), Rb_perfect 381 (3 holes), Rb_VO 375 (1 residual hole). Every doped cell is odd-electron, so m = 0 solutions are smeared, not closed-shell.

### 4.3 Key results (energy-derived values reproduced by `supporting_information_v4/check_ledger.py`, 29 checks, all OK; magnetisations, Löwdin, PDOS, Bader and structural values come from the ledger, SI Tables S3/S8 and `figures/data/` and are not script-checked)

| Quantity | Value | Where |
|---|---|---|
| E_f(V_O) pristine | **+4.74 eV (lower bound)**; unrounded 4.7447 | Table 2, run 2 − run 1 |
| E_f(V_O) Pr | **+1.29 eV** (1.2921); 2×2×2: +1.19 | Table 2, runs 4/3; 9/8 |
| E_f(V_O) Rb | **−4.06 eV** (−4.0635); 2×2×2: −4.20 | Table 2, runs 6/5; 11/10 |
| Pr − Rb contrast | **5.36 eV** (5.356) Γ; 5.394 at 2×2×2; ΔΔE = +0.038 eV | Table 2, S2b |
| Reductions vs pristine | at least 3.45 eV (Pr), 8.81 eV (Rb) | §3.2 |
| Alternative Pr sites | site 1 / 17 (3.99 Å): +2.07 eV each; site 7 (4.94 Å): +2.72 eV; production lowest by 0.78 eV; in-cell association energy 1.43 eV (0.78 from 2nd shell), not dilute-limit | §3.7, Table S4 |
| Magnetisation (Ti-3d-only U) | Pr_perfect 0/0, Pr_VO 0/0 (trial m 1.00, m_abs 1.13, +0.281 eV vs logged, +0.394 eV vs production), Rb_perfect 1.00/1.00, **Rb_VO m −0.97, m_abs 1.21** (from-scratch solution m 1.00 lies 6.4 meV higher) | Table 3 |
| Dual-U (U(O-2p) 5.5 eV) | Pristine 0.00; **Pr_perfect 1.00**; Pr_VO not computed; Rb_perfect 3.00; Rb_VO 1.00 (relaxation incomplete). Energies −4269.72111, −4571.33095, −4324.98591, −4284.02974 Ry (last two converted from logged eV). m_abs not recorded | Table 4, S5 |
| Charged series | Pr_VO m = 0 at q = 0, +1, +2; Rb_VO \|m\| 0.97 → 1.99 → 2.99 (m_abs 3.82 at +2) | §3.5 |
| Rb_VO hole | empty minority-spin band 0.04–0.13 eV above E_F, 93 % O-2p; Löwdin +0.59 μB on O8, +0.11 on O6 and O17, O total +1.12, Ti −0.12; KS gap 2.87 eV (majority) | §3.6, Fig 4, S2 |
| Rb_VO structure | Rb displaced 1.27 Å towards the vacancy (0.87 Å from the vacant site); Rb–O 2.54 (×2), 2.56, 2.71 Å; Ti2/Ti26 at 2.362/2.378 Å from vacancy | §3.1, Table S8 |
| Bader | totals 376.998 / 374.998 e; dopant populations implied by totals and means: Pr 8.96 e (+2.04 ± 0.03), Rb 8.13 e (+0.87 ± 0.03) — the run notes' +2.14/+0.82 are not reproduced; O8 −0.257 e, O30 −0.14 e | §3.7, Table S3 |
| k-mesh | Γ lies 22–25 meV/atom below 3×3×2 (−21.8 / −23.0 / −24.7); 2×2×1 within 1.15 / 1.05 / 0.42 meV/atom | Tables S2a/S2b |
| U sweep | Pr_VO non-magnetic, Rb_VO m = 1.00 at U = 3.0, 4.0, 4.5; E_F varies ≤ 0.26 eV | Table S1 |
| D3(BJ) | −0.75639 Ry (Pr_VO), −0.74166 Ry (Rb_VO); not done on Pr_perfect, Rb_perfect, O₂, so no D3-corrected E_f | Table S5 |

### 4.4 What the paper claims and does not claim

Claims: the ordering pristine > Pr > Rb follows the formal hole count (0, 1, 3); Rb makes V_O spontaneous at the O-rich reference *if Rb sits on a Ti site*; the Rb_VO residual hole is an O-2p state mostly on one O bonded to Rb; the Pr hole's spin state depends on the O-2p Hubbard term.
Does not claim: Pr "suppresses" vacancies (withdrawn); any 4f mechanism; closed-shell singlets; Ti³⁺ traps; band alignment from raw Fermi energies; device or indoor-PV performance; that size and valence are separated (radius ordering is the same as hole-count ordering — stated as a confound).

### 4.5 Known weaknesses and how the text handles them now

| Weakness | Current text |
|---|---|
| Pristine perfect cell unrelaxed | Stated in §2.6; "lower bound" in abstract, Table 2 footnote b, §3.2, §4.1, §4.2, Limitation (iv), Conclusions, highlights, graphical abstract |
| No cut-off test (40 Ry) | Limitation (iii); §2.1 |
| Γ-only relaxations, 48-atom cell | Limitations (i), (ii); k-mesh single points reported |
| Loose forces | Limitation (iv) |
| Symmetry not broken | §2.4, §3.6, Limitation (xiii) |
| U(O-2p) transferred | §2.2 (Orhan 7.66 eV, Falletta PWL route), Limitation (vii) |
| No −TS / degauss unknown | §2.4 with order-of-magnitude estimate |
| No chemical-potential window, competing phases, Rb interstitials | §4.2, Limitations (ix), (x) |
| D3 incomplete | Limitation (xii) |
| HSE06 only on pristine | §2.8(iii), §3.6, Limitation (xi) |

---

## 5. Repository map (`/home/user/TensorTonic-Solutions/DFT_paper_revision/`)

**Hand-edited sources of truth (edit only these):**
- `manuscript_v4/part1_front_intro_methods.md`, `part2_results.md`, `part3_discussion_end.md` — manuscript text with `{{Key}}` citations. Line 13 of part1 is an internal "Revision note" blockquote (kept in the working copy, stripped at packaging).
- `manuscript_v4/refs.py` — `REFS = {key: "reference string"}` (54 entries, 50 cited; unused: Yang2020, Ahmad2020, Deak2014, Wang2020) and a `VERIFY` dict of notes.
- `manuscript_v4/build_refs.py` — numbers citations by first appearance, compresses ranges, appends References.
- `supporting_information_v4/SI_v4.md` — SI (S1–S10; S11 and Figure S3 were removed in round 5). The last main-text citation of Figure S3 (§3.1) was removed on 13 Oct. Line 7 has its own revision note.
- `supporting_information_v4/energy_ledger.csv` — Table S9, 48 rows (runs 1–46 plus 20a/20b).
- `supporting_information_v4/check_ledger.py` — 29 checks; exits non-zero on any BAD.
- `figures/make_figures.py` (Fig 2, 3), `make_pdos_figures.py` (Fig 4, S1, S2), `make_fig1_structures.py` (Fig 1; adds panel c automatically if `figures/data/nscf_Pr_VO.out` appears), `make_graphical_abstract.py`, `extract_lowdin.py`; data in `figures/data/` (PDOS CSVs, Löwdin CSVs, `nscf_Rb_VO.out`). Run them from inside `figures/` (relative `data/` paths).
- `submission/Highlights.md`, `submission/Cover_Letter_Applied_Surface_Science.md` (its .docx is regenerated by `tools_package.sh` since `457e6e3`), `submission/Journal_Shortlist.md/.docx`.
- `SUBMISSION_PACKAGE/00_READ_ME_FIRST.md/.docx` — the user-facing checklist.
- `revision_calculations/` — QE inputs, launcher and analysis for the extra runs (§10).
- `response_to_audit/Editorial_Pass_Log.md` (rounds 1–5, all finding IDs), `Response_to_Audit_v4.md` (answers to R01–R18, E1–E13), `Response_to_AI_PreSubmission_Review.md` (answers to the paperreview.ai review).
- `REVISION_REPORT.md` — the round-1 report with later appendices (§7a–§7c).
- `device_paper_review/` — audit of the user's separate device paper (§15).
- `source_text/` — pandoc text of the original FINAL manuscript, BACKUP, FINAL SI, and both audits.

**Generated (never hand-edit):** `manuscript_v4/manuscript_v4_src.md`, `manuscript_v4/Ghadimimehr_DFT_TiO2_PrRb_v4_MANUSCRIPT.{md,docx}`, `*_PREVIEW.pdf`, `supporting_information_v4/Ghadimimehr_DFT_TiO2_PrRb_v4_Supporting_Information.docx`, figure PNG/PDFs, everything in `SUBMISSION_PACKAGE/` except `00_READ_ME_FIRST.*`, and `SUBMISSION_PACKAGE.zip` (gitignored).

**Local only (gitignored, may be absent in a fresh clone):** `*.bak`, `*.round3.bak`, `*.round4.bak` backups, `__pycache__/`.

---

## 6. Build and check procedure

```bash
cd /home/user/TensorTonic-Solutions/DFT_paper_revision
# 1. if figure data or scripts changed:
(cd figures && python3 make_figures.py && python3 make_pdos_figures.py && python3 make_fig1_structures.py && python3 make_graphical_abstract.py)
# 2. rebuild manuscript + SI Word files and previews
bash tools_rebuild.sh
#    must print: "50 references cited; missing keys: []" ; "0" (unreplaced {{ ) ; "abstract words (Word-style count, limit 250): 250" (or fewer)
# 3. energy checks
(cd supporting_information_v4 && python3 check_ledger.py)      # 3 U-sweep info lines, then 29 lines starting "OK", no "BAD", exit 0
# 4. journal package
bash tools_package.sh
#    must print: revision notes left = 0 (02, 06); markers left = 0 for 01, 02, 03, 06; check_ledger OK; "Zenodo scripts parse"; zip size
```

- `tools_rebuild.sh` and `tools_package.sh` hard-code the scratch path `/tmp/claude-0/-home-user-TensorTonic-Solutions/0159629d-9bba-513e-9e05-92ed56279e63/scratchpad/...`, the Chromium path `/opt/pw-browsers/chromium-1194/chrome-linux/chrome` and a docx validator under `/root/.claude/skills/synced/...`. **In a new session, change `S=` at the top of both scripts to the new scratchpad (and, if needed, `CH=` in both and `V=` in `tools_rebuild.sh`; `tools_package.sh` has no `V=`)** or they will fail.
- `tools_check_numbers.py` compares numbers against the old round-2 `.bak` files; for a new edit round, make fresh backups (`cp part2_results.md part2.round6.bak` etc.) and diff the decimal numbers yourself (a 10-line Python Counter over `re.findall(r'[−-]?\d+\.\d+', text)` was used in rounds 4–5).

---

## 7. Revision history (details and every ID in `response_to_audit/Editorial_Pass_Log.md`)

- **Pre-history.** Error Audit E1–E13 (10 Jun 2026) and Full Reviewer/Editor Audit R01–R18 (15 Sep 2026, verdict "do not submit"). Both answered in `Response_to_Audit_v4.md`.
- **Round 1 (2 Oct).** v4 written from FINAL (≈11,500 → ≈7,400 words); editorial and computational-methods panels: 87 findings, 80 applied; graphical abstract and highlights created; journal shortlist and cover letter.
- **Round 2 (3 Oct).** Defect-chemistry, copy-editing, citation and SI-consistency panels: 192 findings accepted, 16 rejected; k-mesh sign error from round 1 corrected; title changed from "Hole Localisation" to "Dopant-Induced Holes"; radius confound stated.
- **Round 3 (3 Oct).** The user's archive (run spreadsheet, PDOS data, projwfc outputs, NSCF output, templates) integrated: energy ledger to 46 runs with `check_ledger.py`; Rb_VO hole located on O8 by Löwdin analysis; Rb off-centring 1.27 Å found; Figure 1 redrawn from relaxed coordinates; starting_magnetization claim corrected against QE 7.5 source; citations checked against the user's PDFs in Google Drive (Arrigoni comparison withdrawn, Vural sentence deleted, Deák replaced by Orhan & O'Regan); independent adversarial review R3-34…R3-46.
- **Round 4 (4 Oct).** Automated pre-submission review (paperreview.ai, 10 weaknesses, 12 questions) answered; four arXiv papers added after reading them (Falletta 2022, Chen 2020, McBride 2024, Ahart 2026); HSE06 energy comparison removed; association energy and "Uncertainty of the main results" paragraph added; `revision_calculations/` built; `tools_package.sh` written (strips revision notes; Zenodo `data/` folder fixed).
- **Round 5 (4–5 Oct).** All remaining author notes resolved from the files at hand or stated as "not recorded"; **pristine perfect cell found to be unrelaxed → lower bounds**; illuminance sentence reworded so the unreadable Pecunia paper is not needed for it; Bader dopant charges replaced by values derivable from recorded totals; Figure S3 (raster-patched) removed; AI declaration and data statement reworded; funding inserted; job 0 added to the calculation queue.

---

## 8. Current status (13 Oct 2026)

- Package `DFT_paper_revision/SUBMISSION_PACKAGE/` (+ `SUBMISSION_PACKAGE.zip`, rebuilt 13 Oct with the fixed cover letter; the copy sent to the user on 5 Oct still has the old cover letter with the AUTHOR ACTION placeholder, so send the 13 Oct zip again): 01 cover letter, 02 manuscript (+ preview PDF), 03 highlights, 04 graphical abstract, 05 Figures 1–4 (PDF + PNG), 06 SI (+ preview PDF), 07 Zenodo data and scripts (not for the journal).
- Manuscript, highlights, SI: **0** AUTHOR ACTION / NEEDS CITATION markers. Abstract 250 words (Word count). 29 ledger checks pass.
- Cover letter: fixed on 13 Oct (suggested-reviewer placeholder replaced by "Suggested reviewers are listed in the submission system."; data sentence aligned with the manuscript). 0 markers. Enter 3–5 suggested reviewers in Editorial Manager.
- The zip the user received on 5 Oct contains the OLD cover letter (reviewer placeholder; claim that the data are already deposited). The corrected zip (fixed cover letter, abstract trimmed to 250 Word-counted words, Figure S3 citation removed) was rebuilt and sent to the user on 13 Oct. If he submitted the 5 Oct version, he should replace the cover letter and manuscript in Editorial Manager.
- `tools_package.sh` rebuilds the cover letter from its .md and checks markers in 01, 02, 03 and 06.
- `00_READ_ME_FIRST.md/.docx` updated on 13 Oct (date, abstract count, "cover letter, manuscript, highlights and SI", suggested reviewers to be entered in Editorial Manager).
- Whether the paper has been submitted: **unknown**.

---

## 9. Next steps, in priority order

### 9.1 Fold in the outputs the user says already exist (FIRST TASK)

On 5 Oct the user wrote "i have all these simulations already". None of these outputs has ever been uploaded. Ask for them (two archives, in WSL: (1) the revision queue, exactly as in `revision_calculations/README.md` "What to send back": `cd ~/tio2_vo/revision_calculations && tar czf revision_results_$(date +%Y%m%d).tgz --exclude='runs/scratch' --exclude='runs/_positions' revision*.log dryrun.log revision_analysis.txt runs`; (2) the production files: `cd ~/tio2_vo && tar czf tio2_outputs.tar.gz *.in *.out */*.out $(find . -name ACF.dat -not -path './revision_calculations/*')`. The READ_ME calls the production bundle `tio2_needed.tar.gz`; accept either name.), put each archive in its own new empty directory, read with `python3 -I`, and update the paper:

| Output to request | What it changes |
|---|---|
| **Relaxed Pristine_perfect** (job 0) | Replace −4275.01530 Ry in Table 2, ledger run 1 (add a new run row), `check_ledger.py` (Ef pristine, reductions), `figures/make_figures.py` and `make_graphical_abstract.py` constants; remove "lower bound" / "at least" from abstract, Table 2 footnote b, §2.6, §3.2, §3.7 (Uncertainty paragraph), §4.1, §4.2, Limitation (iv), Conclusions, Highlights (bullet 2), graphical abstract ("≥" prefix in `make_graphical_abstract.py`), and update SI Table S6 (run-1 row), Table S9 (run 1 note) and Table S10 (Pristine_perfect row and footnote d). The doped results and contrast do not change. |
| **Cut-off 55/70 Ry** (job 1, plus O₂ at each cut-off) | §2.1 "No cut-off convergence test was performed" and Limitation (iii); add a table to SI S4; add to "Uncertainty of the main results" (§3.7) |
| **Pristine V_O at 2×2×2** (job 2) | Table 2 footnote a and empty cell; Table S2b; Limitation (ii) "the pristine E_f was not checked"; `check_ledger.py` |
| **Smearing tests / −TS lines** (job 3, or the "smearing contrib. (-TS)" lines of the production outputs) | §2.4 (replace the estimate), §3.3, S1 last sentence, Table S10 degauss column, uncertainty paragraph |
| **D3 on Pr_perfect, Rb_perfect, O₂** (job 4) | §3.7 *Dispersion* paragraph and Limitation (xii): compute D3-corrected E_f and contrast; Table S5; ledger rows; checks |
| **nosym / O-seeded Rb runs** (job 5/6) | §2.4 symmetry sentence, §3.6 caveat, Limitations (v) and (xiii) |
| **Dual-U Pr_VO; finished dual-U Rb_VO; dual-U O₂** (job 7/7b) | Table 4 ("not computed", "preliminary"), §3.4, §4.4, Limitation (vii); dual-U E_f possible only with a dual-U O₂ reference |
| **Tight relaxations** (job 8) | Limitation (iv) last sentence "The effect of tighter relaxation on the energetics and on the localisation results has not been tested"; §2.6 force statement; Table 2/ledger rows (new runs) and E_f re-evaluation in the uncertainty paragraph (§3.7) |
| **Linear-response U** (job 9) | §2.2 "linear-response determination of U ... was not performed for any cell in this work" and the U(O-2p) "transferred ... no such calibration was attempted" sentence; Limitation (vii) |
| **Production .in files** | degauss, etot_conv_thr, starting_magnetization statements in §2.4–2.6 and Table S10 ("not recorded", "not re-inspected") |
| **Pristine_VO relaxation output** | E_F and m_abs in Table 3 |
| **dual-U and q = +1 outputs** | m_abs in Table 4, §3.5, Table S5 |
| **Any output with wall time** | Table S6 |
| **PDOS SCF output** | E_tot, m, m_abs (§3.6, R3-38) |
| **NSCF with diago_full_acc / spin-density cube** (optional) | §3.6 unconverged-eigenvalue caveat; Limitation (xiii) "not cross-checked with a spin-density isosurface" |
| **Pr-cell output header** | Pr MD5 in Table S7 |
| **Relaxed Pr_VO output** (e.g. `nscf_Pr_VO.out` or `Pr_VO.out`; any pw.x output of the relaxed cell) | Copy it to `figures/data/nscf_Pr_VO.out` (that exact name; `make_fig1_structures.py` tests only this path) → Figure 1 panel (c) appears; Pr–O distances in §3.1 and Table S8; confirm the removed oxygen (§2.3) |
| **Bader ACF.dat** (Pr_VO, Rb_VO) | Table S3 per-atom tables, dopant charges in §3.7 |
| **HSE06 input/output** | §2.8(iii) q-grid/ecutfock; optionally band gap |
| **vc-relax output** | §2.3 k-mesh, cut-off, residual stress |

Procedure each time: back up the sources → extract numbers from the outputs (first read the production smearing widths and any `DEGAUSS`/`ALLOW_DEGAUSS_MISMATCH` override from `dryrun.log`/`revision.log`; use them to fill the degauss statements in §2.4 and Table S10 and to confirm the job runs used the production width; compare job 5/6 Rb_VO energies with both −4289.17135 Ry (production, m_abs 1.21) and −4289.17088 Ry (from-scratch, m_abs 1.00), README assumption 4) → edit `part*.md`, `SI_v4.md`, `energy_ledger.csv`, `check_ledger.py`, figure scripts as needed → `tools_rebuild.sh` → `check_ledger.py` → `tools_package.sh` → diff decimal numbers against the backup → add a round-6 section to `Editorial_Pass_Log.md` → commit → push → send the new zip.

**Check first when `Pristine_perfect.out` arrives:** the "unrelaxed" status of the pristine reference rests on the run spreadsheet §2 row and the progress report (calculation type scf, F_max 0.022530 Ry/Bohr, E_F 7.887 eV, eV total −58164.5462 = −4275.0153 Ry). The spreadsheet §16 header and the U-sweep README describe the same cell loosely as "previously-relaxed", and the Γ k-mesh single point with the same energy prints E_F 8.2442 eV. Open the output and check `calculation =` and the last "Total force". If it was in fact a relaxation that converged below 0.005 Ry/Bohr, remove every "lower bound" / "at least" statement (list in the job-0 row above, plus the cover letter's "+4.74 (a lower bound)") and correct ledger run 1 (calc, E_F, Fmax) — no energy changes.

### 9.2 Other items

1. Ask whether the paper was submitted. If reviews arrive, answer them point by point (the repo has the format in `Response_to_Audit_v4.md`).
2. Check the four arXiv preprints for published versions before submission or at revision: McBride 2024 (arXiv:2410.21452), Ahart 2026 (2606.01763), Chen 2020 (2011.03269), Falletta 2022 (2209.11341).
3. Zenodo deposit: if the user deposits `07_Data_and_scripts_for_Zenodo/` plus QE inputs/outputs, replace the Data availability sentence with the DOI.
4. If the user asks for the remaining calculations instead of having them: `revision_calculations/` (§10).

---

## 10. `revision_calculations/` summary

Inputs, launcher and analysis for the extra runs; validated by a round-4 dry run against stand-in production outputs (37 inputs consistent; job 0, added in round 5, was not part of that dry run and has not been dry-run since), never executed here (no pw.x in this environment).

| Job | Purpose | Runs | Time on the i5 |
|---|---|---|---|
| 0 | Relax pristine perfect cell | 1 relax | 1–3 days |
| 1 | Cut-off 55/70 Ry on Pr_perfect, Pr_VO, Rb_perfect, Rb_VO; 40 Ry references; O₂ at 40/55/70 | 8 + 4 + 3 | 2.5–5 days |
| 2 | Pristine V_O at 2×2×2 | 1 | 3–8 h |
| 3 | Smearing tests on Pr cells (Gaussian 0.002, cold 0.005) with −TS | 4 | 12–24 h |
| 4 | D3(BJ) on Pr_perfect, Rb_perfect, O₂ | 3 | 7–14 h |
| 5 | nosym SCF of Rb_VO (seed on O8 and O6) and Rb_perfect (nearest O), seeded oxygen labelled `O1` | 3 | 12–24 h |
| 6 | nosym re-relaxation, only if job 5 is lower by > 1e-4 Ry | 0–2 | 1–3 days each |
| 7 / 7b | Dual-U Pr_VO relaxation + dual-U O₂ / finish dual-U Rb_VO | 1+1 / 0–1 | 1–3 / 0.5–2 days |
| 8 | Re-relax four doped cells to 0.001 Ry/Bohr | 4 | 2–6 days |
| 9 | hp.x linear-response U (HPC) | 1+1 | HPC |
| 10 | 96-atom cells (cost note only) | – | – |

Default queue (P1) = jobs 1, 2, 0, 3, 4, 5 (27 runs, ≈5–11 days); `RUN_P2=1` adds 6, 7, 7b, 8; `RUN_P3=1` adds 9; `JOBS="0"` runs a chosen subset. Key variables at the top of `launch_revision_queue.sh`: `PRISTINE_VO_OUT` (defaults to the guessed name `Pristine_VO.out`, used silently if such a file exists; otherwise job 2 is skipped with a hint; set it to the real pristine V_O relaxation output), `DUALU_RBVO_OUT`, `DUALU_RBP_OUT`, `QE_HOME` (default `~/tio2_vo`), `DEGAUSS` (0.005; the launcher stops if production outputs show a different width unless `ALLOW_DEGAUSS_MISMATCH=1`). Launch: `bash launch_revision_queue.sh --dry-run` then `nohup bash launch_revision_queue.sh > revision.log 2>&1 & disown`. Analysis: `python3 analyze_revision_runs.py runs | tee revision_analysis.txt` — prints E_f at each cut-off, the corrected pristine E_f after job 0, −TS and internal energies, D3-corrected E_f, nosym comparisons and dual-U E_f. Full instructions: `revision_calculations/README.md`.

---

## 11. Data inventory

**In the repo:** energy ledger (48 rows), PDOS CSVs and Löwdin CSVs for Pr_VO and Rb_VO, `nscf_Rb_VO.out` (relaxed Rb_VO coordinates), all figure scripts.

**Uploaded to the previous session (`/root/.claude/uploads/<session id>/`, not available to a new session unless re-uploaded):** original FINAL and BACKUP docx, FINAL SI docx, both audits, `QE_simulations_master.csv/.xlsx` (run spreadsheet; the 36.6 KB CSV and the .xlsx sheet QE_master_v8 have sections 1–23 and are the main data source; a second, older 9.3 KB CSV has sections 1–9 only and the uncorrected Pr_VO_brokensym eV total −61703.1378, so do not use it), `QE_DFT_progress_report.docx`, `results_log.md`, PDOS `.dat/.csv` files, `proj_Pr_VO.out`, `proj_Rb_VO.out`, `nscf_Rb_VO.out`, a few `pdos_atm` files, input templates (`scf_template.in`, `nscf_template.in`, `projwfc_template.in`, `template_Pr_VO.in`, `template_Pristine_perfect.in`), the user's PDOS/U-sweep launch scripts and plotting scripts, and his own earlier audit notes, and the separate device-paper manuscript `Manuscript_Ghadimimehr.docx.docx` (uploaded three times, identical; source for §15).

**Never provided:** production `.in` files; any production pw.x `.out` (relaxations of Pr_perfect, Pr_VO, Rb_perfect, Rb_VO, Pristine_VO; the Pristine_perfect single point); `nscf_Pr_VO.out`; Bader `ACF.dat`; dual-U outputs; HSE06 input/output; vc-relax output; any of the job 0–8 outputs.

**Reference PDFs:** in the user's Google Drive (numbered files such as `9.pdf`, `14.pdf`, `58.pdf`, `65.pdf`; mapping in the uploaded `02_ref_to_pdf_mapping.csv`), reachable through the Google Drive connector.

---

## 12. Reference status

- 54 entries in `refs.py`, 50 cited. Unused: Yang2020, Ahmad2020 (removed: no compensation discussion), Deak2014 (U claim unverifiable, replaced by Orhan2020), Wang2020.
- Checked against the authors' PDFs (round 3): Yin2020, Vural2023, Bai2020, Polliotto2020, Chen2012, Torres2021, Mazierski2020, Orhan2020 (Table II values), Bahmanrokh2020, Chen2014; Arrigoni & Madsen and Boonchun used for protocol only.
- Read on alphaXiv, cited as preprints (check for published versions): McBride2024, Ahart2026, Chen2020, Falletta2022.
- `VERIFY` notes still open in `refs.py`: Bigi2020 and Tian2025 (American spelling of titles), PSlibrary, Shannon1976, Freysoldt2014 (added in v4; standard references), Boonchun2016 last page, Bahmanrokh2020 volume/pages.
- Pecunia2021 is cited only for "indoor PV can replace batteries"; the 200–1000 lx claim was dropped because the paper could not be read.

---

## 13. Rules and constraints for Claude

1. **Never change a computed number.** Values come from the user's QE outputs via the ledger; recompute derived values with `check_ledger.py`. Back up sources before bulk edits and diff the decimal numbers afterwards.
2. **Never invent or cite unread literature.** Verify a citation against the paper itself (Drive PDF, alphaXiv for arXiv). If a source cannot be read, reword so it is not needed.
3. When a fact is not in any file, say "not recorded" rather than asking the user to supply it, unless it blocks the work.
4. Abstract ≤ 250 words; highlights ≤ 85 characters each; package must show 0 markers in 01, 02, 03 and 06.
5. Git: branch `claude/exciting-shannon-z4bl69` only; author identity as in §3; commit footer as the system reminder prescribes; no new PR unless asked; push after every completed round.
6. The cover letter is final (13 Oct 2026); change it only if the user asks.
7. Environment lessons: parallel Bash calls share one working directory, so always use absolute paths; Wiley, Crossref and Semantic Scholar are blocked by the proxy; Scite needs a paid plan; Wiley Scholar Gateway and Consensus free quotas were exhausted until 1 Nov 2026; alphaXiv `answer_pdf_queries` works for arXiv papers; pandoc, matplotlib and Chromium are available; there is no Quantum ESPRESSO.
8. Elsevier generative-AI rules: AI may not create or alter images. All figures are plotted by Python scripts from the authors' data; the declaration in the manuscript says so. Elsevier's policy on AI-assisted plotting scripts is not explicit; the READ_ME tells the user that asking the editorial office is prudent but not required — keep that caveat when answering submission questions.

---

## 14. User communication notes

- Messages are very short ("done?", "now i go for submission?", "finish it now"). Answer the question in the first line (yes/no/what is missing), then give detail.
- The user wants Claude to fix things directly, not hand back lists of things to do; he was frustrated when asked for information that could be stated as "not recorded", and when asked to run calculations he says he already has.
- He makes decisions quickly when given one clear recommendation.
- He asked twice whether the paper could be submitted; be explicit about what still blocks and what does not.

---

## 15. The separate device paper

A second manuscript by the user (Pr³⁺-doped SnO₂ ETL with CsPbBr₃, indoor PV, MATLAB equivalent-circuit model) was audited in `device_paper_review/Device_Manuscript_Audit.md` (with `verify_numbers.py`). Verdict: do not submit as is — titles promise ML and DFT it lacks; claimed drift-diffusion results reproduce from a single-diode equation; Pr³⁺ on Sn⁴⁺ is an acceptor, not a donor (contradicts the DFT companion); EIS values inconsistent by ~11 orders of magnitude. It is **not** part of this submission.

---

## 16. Quick start for the next session (first 15 minutes)

1. `cd /home/user/TensorTonic-Solutions && git fetch origin claude/exciting-shannon-z4bl69 && git checkout claude/exciting-shannon-z4bl69 && git pull`
2. Edit `S=` (scratch path) at the top of `DFT_paper_revision/tools_rebuild.sh` and `tools_package.sh` to the new session's scratchpad and, if those files do not exist, `CH=` (Chromium, both scripts) and `V=` (docx validator, `tools_rebuild.sh` only); check with `ls $CH $V`.
3. Run §6 once to confirm the build works: expect 50 references, 0 placeholders, abstract 250, 29 OK, 0 markers.
4. Ask the user: (a) has the paper been submitted? (b) upload the outputs listed in §9.1.
5. When outputs arrive, follow the §9.1 table and procedure.

---

## 17. Glossary

| Label | Meaning |
|---|---|
| Pristine_perfect / Pristine_VO | undoped 48-atom cell / with one O removed (47 atoms) |
| Pr_perfect, Pr_VO, Rb_perfect, Rb_VO | one Ti replaced by Pr or Rb, without / with V_O |
| single-U / dual-U | U on Ti-3d only (3.5 eV) / plus U(O-2p) = 5.5 eV |
| m, m_abs | total and absolute magnetisation (μB); the sign of m is arbitrary |
| Run numbers 1–46, 20a, 20b | rows of `energy_ledger.csv` = SI Table S9 (1–7 production; 8–11 2×2×2; 12–14 alternative sites; 15–18 charged; 19–20b dual-U; 21 HSE06; 22–23 D3; 24–25 Pr_VO magnetic trial; 26–37 k-mesh series; 38–46 U sweep) |
| site 1 / 7 / 17 | alternative Pr V_O sites, numbered by the user's orchestration input (not pw.x atom numbers) |
| O8, O6, O17, Ti2, Ti26 | pw.x atom numbers in Rb_VO (O8 carries the hole; O6/O17 mirror pair; Ti2/Ti26 bonded to the vacancy); atom 3 is Rb |
| job0…job10, tags `job1_<cell>_ec55`, `job5_Rb_VO_nosym_Oh8` … | calculations in `revision_calculations/` |
| R01–R18, E1–E13 | findings of the two original audits |
| ED-, CM-, DC-, LS-, CT-, SI- | round-1/2 editorial panel findings |
| R3-xx, R4-xx, R5-xx | round 3–5 log entries |
| W1–W10, Q1–Q12 | weaknesses and questions of the paperreview.ai review |
| FINAL | the user's June 2026 manuscript that the audits rejected |
