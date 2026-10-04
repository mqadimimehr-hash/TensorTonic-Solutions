# Response to the AI pre-submission review (paperreview.ai, 4 October 2026)

**Manuscript:** Oxygen-Vacancy Energetics and Dopant-Induced Holes in Pr- and Rb-Substituted Anatase TiO₂: A DFT+U Comparison
**Target journal:** Applied Surface Science
**Manuscript version answered:** v4 after round 4 of the editorial pass (branch `claude/exciting-shannon-z4bl69`)

This is an internal document for the authors. It records how each point of the automated review was handled. It is not a journal response letter, because no journal reviewer has seen the paper yet. Its purpose is to remove, before submission, the objections a real reviewer is most likely to raise.

## How to read the status labels

| Label | Meaning |
|---|---|
| **TEXT** | The manuscript or SI was changed in this round; the new wording is quoted or located |
| **CALC** | A Quantum ESPRESSO input is ready in `revision_calculations/` (job number given); the result still has to be run and added |
| **LIMIT** | Not computed; now stated explicitly as a limitation, so a reviewer cannot say it was hidden |
| **CLARIFY** | The review reads the manuscript differently from what it says, or the request does not change the main result; the reason is given |

## 1. Summary of what changed

**Text changes (all rebuilt; abstract unchanged at 248 words; the 26 ledger checks still pass):**

1. **§2.2 Hubbard U.** Adds that U can be fixed by enforcing piecewise linearity on polaronic defect states (Falletta and Pasquarello 2022), and states that no such calibration was attempted. The first-principles anatase values of Orhan and O'Regan (U_eff 3.28 eV on Ti-3d, 7.66 eV on O-2p) were already quoted, so the reader can see how far the transferred 5.5 eV lies from a calibrated value.
2. **§3.3 Spin states.** The non-magnetic pristine V_O cell is now set against embedded coupled-cluster results (Chen et al. 2020). Those results put the triplet of the neutral anatase vacancy 1.4 eV above a closed-shell colour-centre singlet.
3. **§3.6 Electronic structure.** The Rb_VO O-2p hole is now compared with Koopmans-compliant hybrid calculations (McBride et al. 2024; Ahart et al. 2026), which find that holes in bulk anatase self-trap on a single oxygen.
4. **§3.6 Hybrid check.** The HSE06 total-energy and Fermi-energy comparison with PBE+U has been **removed**. The datasets and exact-exchange settings of the hybrid run cannot be confirmed. The paragraph now keeps only the qualitative point that the pristine cell stays non-magnetic. Methods §2.8(iii) says to delete the hybrid item altogether if the input cannot be recovered.
5. **§3.7 Alternative vacancy sites.** Reports the in-cell Pr–V_O association energy: 1.43 eV from the most distant sampled site and 0.78 eV from the second shell. It is labelled as not a dilute-limit binding energy, because in a 2×2×1 cell the "distant" site is still within one lattice parameter of a periodic image of the dopant.
6. **§3.7 New paragraph, "Uncertainty of the main results".** States which numerical settings were varied (only the k-mesh) and which were not (cut-off, smearing entropy, residual forces, supercell size, O₂ reference). It explains why the untested terms would have to reach several eV to change the sign of the Rb value or remove the Pr–Rb contrast. It also notes that the sign of the Pr value and the reductions relative to pristine are more sensitive.
7. **§4.2 Relation to previous work.** Gives E_f(V_O; Pr) = 1.29 eV + Δμ_O. Oxygen removal near Pr turns exothermic once μ_O is more than 1.29 eV below ½E(O₂). For Rb, E_f is negative at every μ_O where TiO₂ exists. The paragraph now says explicitly that substitution of Rb on the Ti site, as opposed to interstitial or surface sites or a secondary phase, was not evaluated.
8. **Limitations (ix) and (x).** (ix) now names competing Pr and Rb oxides and the uncorrected PBE O₂ overbinding. (x) now names Rb interstitials and surface sites.
9. **Methods §2.8(iii).** The hybrid run's recorded settings (input_dft, exx_fraction, screening parameter, same PAW datasets) are stated, with the reason its total is not comparable with the PBE+U total. Limitation (ix) had a comma splice, now fixed.
10. **Pristine reference (found while clearing the author notes).** The run log shows that the production pristine perfect cell is an unrelaxed single point (F_max 0.0225 Ry/Bohr). The manuscript now states this and labels the pristine E_f (+4.74 eV) and the two reductions measured from it as lower bounds; job 0 relaxes the cell. The doped-cell values and the Pr–Rb contrast do not involve this cell.

**Calculations prepared (inputs, launcher and analysis script in `revision_calculations/`; see its README):**

| Job | What it answers | Review item |
|---|---|---|
| 0 | Relaxation of the pristine perfect cell, whose production energy is an unrelaxed single point | W1 (forces); item 10 above |
| 1 | Cut-off 55 and 70 Ry for the four doped cells and the O₂ molecule; E_f and ΔE_f at each cut-off | Q1, W1 |
| 2 | Pristine V_O at 2×2×2 on its Γ geometry (completes Table 2) | Q3, W6 |
| 3 | Smearing test on the odd-electron Pr cells (degauss 0.002 Ry Gaussian; Marzari–Vanderbilt cold smearing); prints −TS and internal energy | Q7, W8 |
| 4 | D3(BJ) on Pr_perfect, Rb_perfect and O₂ (completes the dispersion correction to E_f) | Limitation (xii) |
| 5 | Symmetry-free (nosym, noinv) SCF of Rb_VO and Rb_perfect with the spin seeded on one oxygen (Rb_VO: O8 and the off-mirror O6) | Q2, W2 |
| 6 | Re-relaxation without symmetry, run only if job 5 finds a lower energy | Q2 |
| 7 | Dual-U (U Ti-3d 3.5 eV, U O-2p 5.5 eV) relaxation of Pr_VO from a spin-polarised start; optional dual-U O₂ reference; 7b completes the dual-U Rb_VO relaxation | Q4, W6 |
| 8 | Re-relaxation of the four doped cells to 0.001 Ry/Bohr (0.026 eV/Å) | W1, detailed comments |
| 9 | Linear-response U(Ti-3d) and U(O-2p) with hp.x on the 12-atom anatase cell (for an HPC allocation) | Q4, W3 |
| 10 | Cost estimate only: 96-atom 2×2×2 supercells of Pr_VO and Rb_VO | Q5, W4 |

Run order and estimated wall times on the authors' i5-3570 are in Section 5.

## 2. Weaknesses

**W1. Cut-offs (40 Ry), Γ-only relaxations, the 2×2×1 cell and loose forces (~0.07–0.11 eV/Å) are under-converged or untested.**
*TEXT + CALC + LIMIT.* All four points were already disclosed: Methods §2.1 for the cut-off, §2.6 for the force threshold, and Limitations (i)–(iv). The new §3.7 paragraph "Uncertainty of the main results" now pulls them together and says which conclusions they could affect.
- **k-mesh** is the one setting that was tested (Table S2a). Γ-only energies lie 22–25 meV/atom below 3×3×2, and the 2×2×2 single points shift the individual E_f by 0.10–0.14 eV and the contrast by 0.04 eV.
- **Cut-off:** job 1.
- **Forces:** job 8.
- **Supercell:** job 10 gives only a cost estimate. 96-atom DFT+U relaxations are not practical on a 4-core desktop (Limitation (i)).

*CLARIFY.* The 0.07–0.11 eV/Å values quoted by the review are the final forces reached. The threshold was 0.005 Ry/Bohr (0.129 eV/Å).

**W2. Symmetry was not disabled, which may block symmetry-broken polaron localisation.**
*TEXT + CALC.* §2.4 states that the Rb_VO cell kept a mirror plane (two symmetry operations in the pw.x output). It also says that hole configurations breaking that plane were therefore excluded by construction. §3.6 and Limitation (xiii) repeat this. Job 5 tests the point directly with nosym and the spin seeded on one oxygen, including O6, which lies off the mirror plane. Job 6 re-relaxes the structure if job 5 finds a lower energy.

**W3. U(O-2p) is transferred from Cr₂O₃ and not calibrated; there is no PWL or linear-response U/J; the HSE06 check is incomplete.**
*TEXT + CALC + LIMIT.* §2.2 says outright that 5.5 eV is a transferred value, used only as a sensitivity parameter. It quotes the first-principles anatase value (U_eff(O-2p) = 7.66 eV, Orhan and O'Regan 2020) and now also cites the PWL route (Falletta and Pasquarello 2022). Job 9 provides the hp.x linear-response inputs. Running them needs more memory and cores than the desktop has. The dual-U results are presented only as a spin-state diagnostic (§3.4). No dual-U formation energy is reported, and Limitation (vii) says so. The HSE06 comparison was removed (item 4 in Section 1).

**W4. No finite-size correction for charged defects; no finite-size or elastic assessment for the neutral defects.**
*CLARIFY + LIMIT.* The charged cells are used only to count unpaired spins, never for energies or transition levels (§2.8(i), Limitation (viii)). Limitation (viii) also gives a first-order monopole estimate and says why it is not applied. For the neutral cells, Limitation (i) states the concentrations and that image interactions and band filling are not corrected. It also says these terms need not cancel in ΔE_f, because the Pr cell carries an electron and the Rb cell a hole. The new in-cell association energy (W10) shows how strongly the vacancy–dopant separation matters inside this cell.

**W5. No chemical-potential window or O₂ overbinding correction; negative E_f not set against thermodynamic bounds or competing phases.**
*TEXT + CLARIFY.* §4.2 now gives the dependence on μ_O for both dopants (item 7 in Section 1). Limitation (ix) names the competing oxides and the O₂ error. Two points limit how much the requested analysis could change the conclusions:
- **The Pr–Rb contrast does not depend on μ_O or on any O₂ correction.** Both doped hosts lose the same oxygen to the same reservoir, so ΔE_f = E_f(Pr) − E_f(Rb) contains neither term. A constant O₂ correction shifts all three E_f by the same amount and leaves the reductions relative to pristine unchanged.
- **The dopant chemical potentials cancel in E_f(V_O).** The dopant count is the same in the parent and vacancy cells. Competing Pr and Rb oxides bound μ_Pr and μ_Rb. They therefore decide whether Pr_Ti and Rb_Ti form at all (solubility), not the vacancy formation energy once they have. The manuscript now says the Rb_Ti assumption is untested (§4.2).

Only the O-poor end of the TiO₂ window would add information. It needs a bulk Ti₂O₃ (or Ti metal) calculation with the same datasets and U. This is listed as optional in Section 5.

**W6. Missing controls: pristine V_O at 2×2×2, converged dual-U E_f, cut-off convergence, larger supercells, nosym.**
*CALC.* Jobs 2, 7, 1, 10 and 5 respectively. One more point matters for any dual-U formation energy. The O₂ reference must be computed with the same U on O-2p. Otherwise the oxygen-site term does not cancel between the solid and the reservoir. The logged dual-U Rb_VO relaxation must also be completed (Section 5).

**W7. AUTHOR ACTION placeholders, a revision note and missing table values; the HSE06 setup is unclear.**
*CLARIFY.* The markers and the revision note are internal and are not meant to reach the journal. The submission copies in `SUBMISSION_PACKAGE/` are now built with both revision notes removed (the manuscript's and the SI's). `00_READ_ME_FIRST` lists every remaining marker by group, and none may be left when the files are uploaded. The HSE06 point is covered under W3.

**W8. Conclusions rely on smearing free energies without −TS or internal energies.**
*TEXT + CALC.* §2.4 already asks for the "smearing contrib. (−TS)" line of every production output. It also says to report internal energies wherever −TS exceeds 0.01 Ry. Job 3 adds two independent smearing tests on the odd-electron Pr cells. The analysis script extracts −TS and E = F + TS from every output.

For orientation only, and not as a substitute for the printed values: with Gaussian smearing, one level exactly at E_F contributes σ/(2√π) per spin channel to −TS. That is about 0.02 eV at degauss 0.005 Ry and 0.04 eV at 0.01 Ry. If several levels lie within σ of E_F, the term grows in proportion. Even so, one or two such levels stay an order of magnitude below the 0.281 eV and 0.394 eV separations between the magnetic and non-magnetic Pr_VO solutions (§3.3).

**W9. O-2p U/J and projector dependence under-contextualised relative to DFT+U(+J), ACBN0 and Koopmans-compliant practice.**
*TEXT.* The new citations cover first-principles U+J (Orhan and O'Regan 2020), PWL-derived U (Falletta and Pasquarello 2022) and Koopmans-compliant hybrids (McBride et al. 2024; Ahart et al. 2026). ACBN0 is not cited: no ACBN0 study of anatase has been read and checked for this paper, and an unchecked citation is worse than none. §2.8(vii) and Limitation (xiii) already say that Löwdin populations depend on the projector basis and are used only to locate the spin density.

**W10. Little discussion of dopant–vacancy binding, far-separated configurations, or alternative Rb configurations.**
*TEXT + LIMIT.* §3.7 now reports the in-cell association energy for Pr (1.43 and 0.78 eV), with its caveat. §4.2 and Limitation (x) now name Rb interstitials and surface sites as untested alternatives for a large monovalent ion. Two further Rb vacancy sites remain an optional extra (Section 5). An Rb-interstitial study would need its own defect reaction and the Rb chemical potential, and is outside the scope of this paper.

## 3. Detailed comments not covered above

- **Tighter forces (≤0.03 eV/Å):** job 8 uses 0.001 Ry/Bohr = 0.026 eV/Å.
- **O-rich and O-poor limits; O₂ correction or benchmark:** see W5. A hybrid, GW or experimental benchmark of the absolute pristine value is not attempted. §3.2 explains that the literature values are given only in figures and under different protocols, so no numerical comparison is made.
- **Error bars and their propagation to ΔE_f and the sign of the Rb value:** new §3.7 paragraph, which will be completed with jobs 1, 3 and 4.
- **Rb interstitials and surface sites:** see W10.
- **Pristine V_O non-magnetic and the colour-centre singlet:** added (item 2 in Section 1). The review also notes that in-gap features could be hidden by the small cell. That remains true and is covered by Limitations (i) and (xi).
- **Ti-3d-only U and the "expected multiplicity" of O-centred holes:** *CLARIFY.* The manuscript does not claim that Ti-3d-only U "fails". It reports that this treatment gives one unpaired spin in Rb_perfect against three formal holes (§3.3), and that the oxygen-site term raises it to three (§3.4). Orhan and O'Regan are cited for their U values only. Their paper is about the band gap, not hole multiplicity.

## 4. Questions for the authors

**Q1. Cut-off tests at 55 and 70 Ry, and their effect on ΔE_f.**
*CALC (job 1).* Eight SCF runs (four doped cells at two cut-offs) plus O₂ at each cut-off, so the reference is consistent. The analysis script prints E_f(Pr), E_f(Rb) and ΔE_f for 40, 55 and 70 Ry. Until then, Methods §2.1 and Limitation (iii) state that no test was made and that comparable anatase work uses 55 Ry.

**Q2. nosym re-relaxation of Rb_VO and Rb_perfect with O-centred starting magnetisation.**
*CALC (jobs 5 and 6).* SCF first: Rb_VO seeded on O8 (the Löwdin maximum) and on O6 (off the mirror plane), and Rb_perfect seeded on the oxygen nearest Rb. A relaxation follows only if an SCF lies below the production energy. Single-U is used so that the results compare directly with the production cells.

**Q3. Pristine V_O at 2×2×2.**
*CALC (job 2).* One SCF on the relaxed pristine V_O geometry. It completes footnote a of Table 2 and the k-mesh line of Limitation (ii). The launcher needs the file name of the pristine V_O relaxation output (variable `PRISTINE_VO_OUT`).

**Q4. Calibrated U(O-2p) and dual-U formation energies for both dopants.**
*CALC (jobs 7 and 9) + LIMIT.* A complete answer has three parts:
- linear-response U (job 9; HPC);
- the dual-U Pr_VO relaxation (job 7) and completion of the dual-U Rb_VO relaxation;
- a dual-U pristine V_O cell and a dual-U O₂ reference.

On the desktop this is several weeks of computing. For this submission the manuscript states the transferred value, quotes the first-principles value (7.66 eV), and uses the dual-U runs only as a spin-state diagnostic.

The literature suggests the value matters. McBride et al. found that a hole in rutile stays delocalised at U(O-2p) = 6 eV and localises at 8 eV (their SI Table S1, rutile only; U values depend on the code and the projectors). If hp.x gives a U(O-2p) well away from 5.5 eV, the dual-U tests should be repeated at that value.

**Q5. Dopant–vacancy binding (far versus first-shell V_O) and larger supercells.**
*TEXT + LIMIT.* The in-cell association energy is now reported (§3.7): 1.43 eV relative to the most distant sampled site and 0.78 eV relative to the second shell. A dilute-limit binding energy needs a supercell in which the far site is not close to an image of the dopant. That is the same 96-atom calculation as job 10, which is not feasible on the desktop.

**Q6. Alternative Rb configurations and stability against Rb oxides; effect on the claim that Rb_Ti drives spontaneous V_O formation.**
*TEXT + CLARIFY.* §4.2 now says that whether Rb substitutes on the Ti site at all was not evaluated. The paper's statement is conditional: *if* Rb occupies a Ti site, oxygen removal next to it is exothermic at the O-rich reference. Competing Rb oxides bound μ_Rb and therefore the Rb_Ti concentration, not E_f(V_O) next to an Rb_Ti that exists (W5). The 1.27 Å off-centring of Rb in Rb_VO is reported as a structural result (§3.1). §4.3 notes that it shows an elastic channel exists, but its energy has not been separated.

**Q7. −TS and internal energies for the odd-electron m = 0 cells; lower degauss or cold smearing.**
*TEXT + CALC (job 3).* See W8. The −TS lines of the existing production outputs can be read without any new calculation. They are requested in §2.4 and Table S10 (READ_ME group B).

**Q8. Alignment of DOS and Fermi levels via core levels or the electrostatic potential.**
*CLARIFY + optional.* The manuscript makes no band-offset or carrier-density claim from Fermi energies:
- Table 3's caption and the §3.6 paragraph "Fermi energies" state that the printed values are not aligned to a common reference and are qualitative only.
- Where an E_F difference is interpreted (dual-U Pr_perfect against dual-U pristine in §3.4; Pr_VO and Rb_VO against pristine in §3.6), the same caveat is attached.

If alignment is wanted, the Ti-3s semicore level, which is in valence in the Ti dataset, can serve as the marker. It costs one projwfc.x run per cell with the energy window extended to about −70 eV, on the existing NSCF data, plus the same run on a pristine cell. The present PDOS files stop at −15 eV, so this cannot be done from the data already in hand.

**Q9. HSE06 details, or remove the comparison.**
*TEXT.* The comparison is removed (§3.6). §2.8(iii) asks for the input details and says to delete the hybrid item if they cannot be recovered. The 348 Ry gap between the HSE06 and PBE+U totals of the same cell points to different datasets in the hybrid run. That is why its totals are not compared (Table S5, Table S9 note).

**Q10. Spin-density isosurfaces and site-projected moments for the dual-U cases.**
*LIMIT + needs files.* Limitation (xiii) states that no site-resolved analysis exists for the dual-U cells. Once the dual-U output folders are available, two steps produce it:
- projwfc.x (Löwdin moments, same settings as §2.8(vii));
- pp.x with plot_num = 6 (spin density).

For single-U Rb_VO, the Löwdin site moments are already in Figure S1. A spin-density isosurface would be the optional Figure S4.

**Q11. Chemical-potential stability analysis including Pr and Rb secondary phases.**
*TEXT + CLARIFY.* See W5. The μ_O dependence and its consequence for each dopant are now in §4.2. The dopant secondary phases bound solubility, not E_f(V_O). The O-poor bound needs a Ti₂O₃ calculation (optional, Section 5).

**Q12. 4f-in-valence Pr dataset.**
*LIMIT.* Methods §2.1 and Limitation (vi) state that the 4f electrons are frozen. They also state that the trivalent state, and with it the carrier counts of Table 1, is imposed by this choice. A 4f-in-valence test would also need a Hubbard U on Pr-4f and a search over 4f occupations and spin states. It was not attempted, and no 4f-related mechanism is claimed.

## 5. What the authors need to do

**Before submission (no new physics, about one hour with the files):** groups A and B of `SUBMISSION_PACKAGE/00_READ_ME_FIRST`. These cover the funding statement, Zenodo DOI, Figure S3, AI declaration, the −TS lines, the production settings and the remaining one-line facts.

**Recommended calculations (in this order):** see the table below. Jobs 1–5 (the default queue) can all run in the background on the desktop. Their results drop into the existing "Uncertainty of the main results" paragraph, Table 2 footnote a, Table S2a and Limitations (ii)–(v) and (xii). If the authors decide not to run a job, the corresponding AUTHOR ACTION note becomes a plain "not performed" statement. The limitation text is already written for that case.

Estimates are scaled from the authors' measured times on the i5-3570 (SI Table S6): a Γ SCF from scratch takes 3–6 h at 40 Ry and a production relaxation about 3 days. Higher cut-offs are scaled by (E_cut/40 Ry)^1.5. They are the figures in `revision_calculations/README.md`, which runs the jobs in its own order (1 to 5, then P2). All six P1 jobs run unattended in one queue; a restarted queue skips finished runs.

| Job | Runs | Estimated wall time | Feeds into |
|---|---|---|---|
| 1: cut-off 55/70 Ry, with 40 Ry reference single points on the same geometries and O₂ at 40/55/70 Ry | 8 + 4 + 3 SCF | 2.5–5 days | §2.1; Limitation (iii); uncertainty paragraph |
| 2: Pristine V_O, 2×2×2 | 1 SCF | 3–8 h | Table 2 footnote a; Limitation (ii) |
| 0: relax the pristine perfect cell | 1 relax | 1–3 days | Table 2; §2.6; §3.2; §4.1; Limitation (iv) |
| 3: smearing tests, Pr cells | 4 SCF | 12–24 h | §2.4; §3.3; uncertainty paragraph |
| 4: D3 on Pr_perfect, Rb_perfect, O₂ | 3 SCF | 7–14 h | D3-corrected E_f; Limitation (xii) |
| 5: nosym, O-seeded Rb cells | 3 SCF | 12–24 h | §3.6; Limitations (v), (xiii) |
| **P1 total (default queue)** | **27** | **5–11 days** | |
| 6: nosym re-relaxation (only if job 5 is lower by > 10⁻⁴ Ry) | 0–2 relax | 1–3 days each | §3.3, §3.6 |
| 7: dual-U Pr_VO relaxation + dual-U O₂ | 1 + 1 | 1–3 days | §3.4; Limitation (vii) |
| 7b: finish dual-U Rb_VO (needs its output file name) | 0–1 | 0.5–2 days | §3.4; Table S5 |
| 8: re-relax the four doped cells to 0.001 Ry/Bohr | 4 relax | 2–6 days | Limitation (iv) |
| 9: hp.x linear-response U | 1 + 1 | HPC: 1–3 h per node (desktop 0.5–1.5 days, memory-limited) | §2.2 |

The 40 Ry reference runs in job 1 are fresh single points on the production geometries. The production energies are relaxation endpoints and differ from fresh single points by 0.5 mRy (Rb_VO) and 2.8 mRy (Pr_VO; Table S2a). With the references, every cut-off comparison is like for like.

**Optional, beyond this paper:** dual-U formation-energy cycles (jobs 7 and 9 plus a dual-U pristine V_O and O₂), 96-atom supercells (job 10), a Ti₂O₃ bulk calculation for the O-poor limit, Rb interstitials, and a 4f-in-valence Pr test.

## 6. References added in this round

All four were read in full on alphaXiv on 4 October 2026, and each sentence that cites them was checked against the paper. They are cited as preprints. Check for published versions before submission.

- Falletta, S.; Pasquarello, A. Hubbard U through polaronic defect states. arXiv:2209.11341 (2022). §2.2.
- Chen, J.; Bogdanov, N. A.; Usvyat, D.; Fang, W.; Michaelides, A.; Alavi, A. The color center singlet state of oxygen vacancies in TiO₂. arXiv:2011.03269 (2020). §3.3.
- McBride, S.; Chen, W.; Ćuk, T.; Hautier, G. Do small hole polarons form in bulk rutile TiO₂? arXiv:2410.21452 (2024). §3.6. The paper is about rutile, but it uses anatase as its benchmark. With a Koopmans-compliant PBE0 (α = 0.15) it finds a stable bulk hole polaron in anatase (binding −0.32 eV, transition level 1.4 eV). That anatase result is the only part cited.
- Ahart, C. S.; Li, D.; Blumberger, J.; Liu, S. Polaron transport in TiO₂ from machine learning molecular dynamics. arXiv:2606.01763 (2026). §3.6. With HSE (19% exact exchange, satisfying the generalised Koopmans condition), the anatase hole polaron places 78% of its spin density on a single O atom.

The review's fifth reference (arXiv:2003.00922, Orhan and O'Regan) was already cited in its published form, Phys. Rev. B 101, 245137 (2020). Its values were checked against the authors' PDF.
