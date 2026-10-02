# Point-by-point response to the Reviewer/Editor Audit (15 September 2026) and the Error Audit (10 June 2026)

**Manuscript:** Oxygen-Vacancy Energetics and Hole Localization in Pr- and Rb-Substituted Anatase TiO~2~: A DFT+U Comparison (v4, formerly "Aliovalency over Ionic Radius…")

**Prepared:** 2 October 2026. Status codes: **Accepted** (changed as requested, by editing or re-analysis of existing outputs); **Claim withdrawn** (the statement is removed from the manuscript); **Requires new evidence** (the change needs a calculation or a record that the authors must supply; the manuscript carries an [AUTHOR ACTION] marker at the location). Locations refer to the v4 manuscript.

> **Note to the authors.** This document is written so that it can be reused as the response letter for a journal submission once the "Requires new evidence" items are closed. Replace the audit identifiers by the reviewers' numbering at that time. Nothing in it has been invented to close an item; where a number is missing it is marked.

## Part A — Reviewer/Editor Audit, findings R01–R18

**R01 — Pr does not suppress vacancies relative to the reported pristine baseline (Critical).**
*Status: Accepted; claim withdrawn.* Every statement that Pr "suppresses" V~O~ relative to pristine TiO~2~ has been removed. The Abstract, Section 3.2, Section 4.1 and the Conclusions now state that both substitutions lower the formation energy relative to pristine (by 3.45 eV for Pr and 8.80 eV for Rb), that the Pr cell remains uphill at the oxygen-rich reference and that the Rb cell is downhill. Figure 2 was rebuilt from the in-house values (4.74 / 1.29 / −4.06 eV) without the "stabilises/destabilises" and "better/worse ETL" labels. Table 4 (old Table 2) no longer carries interpretation rows. Title changed accordingly.

**R02 — The named Pr pseudopotential cannot establish the proposed 4f mechanism (Critical).**
*Status: Accepted; claim withdrawn; partly requires new evidence.* We confirmed from the PSlibrary documentation that the "spdn" lanthanide datasets are generated for the trivalent ion with 4f frozen in the core (Z~val~ = 11 = 5s^2^5p^6^5d^1^6s^2^). The Bader electron totals already in the SI (376.998 e for Pr_VO, 374.998 e for Rb_VO) reproduce the electron counts implied by Z~val~(Pr) = 11 and therefore confirm the frozen-4f dataset. All references to Pr-4f hybridisation, 4f occupation and Pr^3+^/Pr^4+^ redox accommodation have been removed (Sections 1, 2.1, 4.4, 5(vi)). The SI statement that "the 4f^2^ subshell is explicit in the valence" was wrong and has been corrected (S2.1); the empty "Pr 4f" curve in Figure S1 is flagged for removal. Table 1 (new) lists the valence configuration and electron count of every dataset and cell. *Requires new evidence:* UPF hashes and header blocks (Table S7). No explicit-4f calculation is planned for this submission; the mechanism is no longer claimed.

**R03 — The design confounds radius with valence and chemistry (Critical).**
*Status: Accepted; claim withdrawn.* The title, abstract and conclusions now describe a bounded two-dopant comparison. The sentence "far larger than any plausible strain-energy contribution" is withdrawn explicitly in Section 4.3, which states what the design does and does not isolate and specifies the controlled series (La/Y/Sc; K/Na; fixed-geometry single points) that would. The ionic radii are now sourced to Shannon (new reference). *Requires new evidence (optional):* relaxed dopant–O bond lengths (Table S8) for Section 3.1.

**R04 — Zero magnetisation over-interpreted as a physical singlet ground state (Critical).**
*Status: Accepted; claim withdrawn; partly requires new evidence.* Section 3.3 now states that every doped cell has an odd electron count (Table 1), that a collinear m = 0 solution of such a cell is a smeared solution with fractional occupations, and that the Pr cells are therefore "non-magnetic solutions", not closed-shell singlets. The magnetic trial is described as one trial (m = 1.00, m~abs~ = 1.13 μ~B~, +0.281 eV) and the non-magnetic solution as "the lowest among those tested". The "triplet" label in old Table 2 is removed. Section 2.5 explains the starting_magnetization convention. *Requires new evidence:* smearing width of the production runs (Section 2.4 marker); a broader spin search is listed as future work in Section 5(v).

**R05 — Charge bookkeeping and Pr carrier count inconsistent (Critical).**
*Status: Accepted.* Table 1 gives the formal ledger: Pr_perfect 1 hole; Pr_VO 1 net excess electron; Rb_perfect 3 holes; Rb_VO 1 residual hole; electron counts 383/377/381/375 derived from the UPF valences and confirmed by the Bader sums. All passages that attributed "two delocalised conduction electrons" to Pr_VO have been corrected to one net excess electron (Abstract, 3.3, 3.6, 4.1, 4.4). Section 4.1 explains the energetic ordering with this ledger.

**R06 — The oxygen Hubbard test changes the Pr interpretation (Critical).**
*Status: Accepted; partly requires new evidence.* Section 3.4 and Table 4 now present the dual-U results for all cells computed (pristine control, Pr_perfect, Rb_perfect, Rb_VO) and state explicitly that the Pr-parent localisation is method dependent. The assertion that formation energies are less sensitive than localisation descriptors is labelled an expectation, not a result. U(O-2p) = 5.5 eV is described as a transferred sensitivity parameter (2.2, 5(vii)). *Requires new evidence:* dual-U relaxation of Pr_VO and the dual-U formation-energy cycles for both dopants (marker in 3.4). We consider this the most valuable calculation to add before submission.

**R07 — Raw Fermi energies do not establish band alignment or clean transport (Critical).**
*Status: Accepted; claim withdrawn; partly requires new evidence.* Section 3.6 now states that the printed Fermi energies are unaligned, that their differences are diagnostic only, and that the HSE06 Fermi-energy shift is not a band-gap measurement. Claims of "trap pinning", quantitative transport and the Burstein–Moss estimate have been removed; a one-sentence order-of-magnitude remark about realistic carrier densities remains, without numbers. The 10.31 vs 9.99 eV discrepancy is explained (2×2×2 NSCF versus Γ SCF). *Requires new evidence (if the comparison is retained):* core-level or potential alignment and band edges per cell (marker in 3.6).

**R08 — Trap identity and recombination activity not proved by the current plots (Critical).**
*Status: Accepted; claim withdrawn; partly requires new evidence.* The "Ti^3+^ trap" labels in Figures 1, 4 (old 5) and old Figure 4 are flagged for removal, old Figure 4 has been rebuilt without them, and the text now says the in-gap feature of Rb_VO has mixed O-2p/Ti-3d weight whose character is indicated (not proved) by the Bader and dual-U results. The Pr-5d inconsistency ("negligible" vs "Pr-5d-derived conduction band") is resolved: the conduction band is Ti-3d, Pr-5d is small. Recombination-activity claims are removed; Section 4.5(iii) lists them as hypotheses requiring transition-level and capture calculations. *Requires new evidence:* regenerated Figure 4 and S1 with broadening and band count stated; spin-density isosurface (Figure S4).

**R09 — Force tolerance loose for the precision claimed (Major).**
*Status: Accepted; partly requires new evidence.* Section 2.6 now gives the threshold and all final forces in eV/Å, states that the tolerance is looser than the 0.01–0.03 eV/Å commonly used, discloses the manual stop of Pr_VO and the 0.0056 Ry/Bohr endpoint of the pristine V~O~ cell, and removes "numerically unnecessary". The unsourced "0.01 Ry/Bohr literature standard" is flagged for removal from Figure S3 (moved from the main text). *Requires new evidence:* tighter re-relaxations (listed in Section 5(iv) and Conclusions as a next step; not performed).

**R10 — Convergence must be tested for the full energetic cycle (Major).**
*Status: Accepted; partly requires new evidence.* Section 3.7 now reports the k-mesh results correctly: Γ-only energies are 22–25 meV/atom above 3×3×2 (not converged in absolute terms); the <1.5 meV/atom figure refers to 2×2×1 vs 3×3×2; formation energies rely on cancellation within each host; the 2×2×2 column of Table 2 quantifies the residual. The incorrect "equal-size, same-composition" wording is removed, and the "planned" k-mesh statement in Methods is replaced. Cut-off is listed as untested (5(iii)). *Requires new evidence:* the 2×2×1, 2×2×2 and 3×3×2 energies of the three cells, which are quoted but not tabulated (Table S2 marker); pristine 2×2×2 single points; a cut-off test.

**R11 — Formation energies require a defined thermodynamic scope (Major).**
*Status: Accepted; claim withdrawn.* Section 2.7 defines E~f~ with μ~O~ = ½E(O~2~) + Δμ~O~, Δμ~O~ = 0, labels it the oxygen-rich electronic-energy reference and cites the standard formalism. The "synthesisable Rb–V~O~ complex" and "lattice instability" statements are removed; Section 5(ix) states that no incorporation, phase-stability or concentration claims are made. The contradiction between "instability" and "not instability" no longer exists.

**R12 — The HSE check does not validate the dopant contrast (Major).**
*Status: Accepted; claim withdrawn; partly requires new evidence.* The abstract no longer lists HSE06 among validations of the dopant contrast; Section 3.6 restricts the result to the pristine cell and states that the doped/defective cells are unverified at the hybrid level. "Single-shot"/"single-point" wording is unified to "single point". *Requires new evidence:* confirmation of the input screening parameter, exx grid and absence of +U (marker in 2.8); band gaps if retained.

**R13 — The dispersion cancellation argument is incomplete (Major).**
*Status: Accepted; claim withdrawn; partly requires new evidence.* Section 3.7 now states that the dispersion correction to E~f~ and ΔE~f~ is undetermined, gives the four-term expression required, and removes the robustness claim. The small mismatch between the quoted D3 terms and the total-energy differences is disclosed. *Requires new evidence:* D3 single points on Pr_perfect and Rb_perfect, or deletion of the paragraph.

**R14 — Charged cells are a spin diagnostic, not corrected thermodynamics (Major).**
*Status: Accepted.* Section 3.5 is retitled "Charged-cell spin series", uses the spin state only, and no longer calls the series a formation-energy validation. "Invariant under image-charge offsets" is removed. m and m~abs~ are distinguished throughout (Section 2.5; Table 3); the 1.21 μ~B~ value is identified as m~abs~ and −0.97 μ~B~ as m. The dielectric constant is relabelled ion-clamped (ε~∞~), the q^2^ scaling is stated and the estimate is given as an upper bound that is not used (5(viii)). *Requires new evidence:* m and m~abs~ separately for each charge state (marker in 3.5).

**R15 — Bader comparison cannot isolate a single hole across different dopants (Major).**
*Status: Accepted; claim withdrawn.* Section 3.7 (Bader) now presents the differences as supporting evidence that the unpaired spin of Rb_VO resides mainly on oxygen, states that cross-composition differences include chemical polarisation, removes "unambiguous" and the "18 %" figure (replaced by the directly supported −0.012 e per Ti, −0.18 e total), and recommends a same-composition comparison. The Conclusions no longer claim a four-cell Bader analysis. *Requires new evidence:* grid, PAW-reconstruction statement (marker in 2.8); spin-density isosurface (Figure S4).

**R16 — Vacancy-site sampling asymmetric; no binding lower bound (Major).**
*Status: Accepted; claim withdrawn.* "Three crystallographically distinct" is replaced by "three selected sites, two symmetry-equivalent"; the production-site distance (2.17 Å) and all site energies are stated; "lower bound on the Pr…V~O~ cluster-preference energy" is removed; absence of Rb site sampling and of the nearest-neighbour test is stated. *Requires new evidence:* coordinates and minimum-image distances (Table S4 marker); Rb site sampling (optional).

**R17 — Bulk calculations do not demonstrate indoor-photovoltaic performance (Critical).**
*Status: Accepted; claim withdrawn.* Indoor photovoltaics are retained as motivation (Introduction, first paragraph) and as a proposed application (Section 4.5). All performance rankings ("trap-free", "worse than pristine", universal |Δq| rule, generalisation to SnO~2~/ZnO/ZrO~2~) are removed or re-stated as hypotheses with the evidence that would test them. Keywords and title changed.

**R18 — Result provenance must be reconciled (Major).**
*Status: Accepted; partly requires new evidence.* The manuscript now has one Methods section listing every calculation (2.8), a full-precision energy ledger (Table S9) from which all formation energies in the text are reproduced, and a run-manifest template (Table S10). Contradictions listed in the audit (k-mesh planned/completed; PDOS planned/plotted; Bader two/four cells; −0.97 vs 1.21 μ~B~; triplet vs 1 μ~B~; one vs two conduction electrons; instability wording) are each resolved in the text. The "eight orthogonal probes" count is removed. Figure 2 is rebuilt from Table 2; stale artwork is flagged. *Requires new evidence:* completion of Table S10 from the output files and deposit of the data package before submission (Data Availability now commits to deposit at submission rather than after acceptance).

## Part B — Figures, tables and consistency (audit Section 5)

| Item | Action in v4 |
|---|---|
| Figure 1 (structures) | Caption corrected (m, m~abs~, no trap labels). Artwork flagged for regeneration with vacancy index and distance. |
| Figure 2 (force trajectories) | Moved to SI as Figure S3; "literature standard" line flagged for removal; eV/Å labels requested. |
| Figure 3 (formation energies) | **Rebuilt** from the in-house 4.74 / 1.29 / −4.06 eV values with 2×2×2 markers; Janotti citation and "deferred" note removed; no ETL labels. Now Figure 2. |
| Figure 4 (magnetisation) | **Rebuilt** with |m| and m~abs~ as two labelled series; "NEW finding", "Ti^3+^ trap" and workflow identifiers removed. Now Figure 3. |
| Figure 5 (PDOS) | Caption rewritten; "Ti^3+^ trap" labels flagged for removal; broadening and band count requested. Now Figure 4. |
| Table 1 (formation energies) | Replaced by Table 2 with Ry totals to 5 decimals, E~f~ from unrounded values, 2×2×2 column and an uncertainty statement. |
| Table 2 (Pr vs Rb interpretation) | Replaced by Table 3 (observables only) and Table 4 (dual-U results). |
| Janotti et al. in Figure 3 | Removed (rutile/HSE study, not in bibliography, not the data plotted). |

## Part C — Error Audit, findings E1–E13

| ID | Finding | Status in v4 |
|---|---|---|
| E1 | 5.35 vs 5.36 eV contrast | Harmonised to 5.36 eV; rounding origin stated in 3.2. (The FINAL draft had harmonised the other way, to the rounded 5.35, and changed ΔΔE to −40 meV; both are corrected.) |
| E2 | Sign of ΔΔE | +0.04 eV (+38 meV), defined as 2×2×2 contrast minus Γ contrast (3.2, Table S2). |
| E3 | Dangling asterisk; uncited literature value; −4.07 rounding | Asterisk gone; Table 2 uses unrounded totals; literature comparison cited in 3.2 with verification marker. |
| E4 | Broken-symmetry cross-reference | Now Section 3.3 everywhere. |
| E5 | Non sequitur on dual-U Rb_VO | Rewritten (3.4). |
| E6 | Roadmap omits Bader | Roadmap rewritten (Introduction, last paragraph). |
| E7 | Four-cell Bader claim | Two cells (3.7, Conclusions). |
| E8 | "~12 %" / "~18 %" Ti share | Replaced by −0.012 e per Ti, −0.18 e total (3.7, Table S3). |
| E9 | |m| ambiguity | m and m~abs~ defined in 2.5 and used throughout. |
| E10 | "static" ε~∞~ | Relabelled ion-clamped; upper bound (5(viii)). |
| E11 | Tian "direct experimental support for −4.06 eV" | Softened to sign and mechanism (3.2, 4.2). |
| E12 | Delocalised vs localised Pr hole | Qualified as treatment dependent (3.4, 4.4). |
| E13 | μ~B~ / Makov–Payne typography | Normalised. |

The Error Audit's two recommendations are also implemented: an uncertainty statement accompanies Table 2, and the identifier-style notation is retained only for cell names (Pr_VO etc.) while physical quantities use subscripts.

## Part D — Reference audit (audit Section 9)

| Issue | Action |
|---|---|
| Arrigoni & Madsen cited as [16] in §3.2 | Corrected; references are now numbered by first appearance from a keyed database, which removes this class of error. |
| [37] and [33] described as K/Rb-doped TiO~2~ studies | Corrected: [Carey2017] is alkali-doped Cr~2~O~3~; [Iwaszuk2011] is trivalent-doped rutile (3.4, 3.5, 4.2). |
| [35], [36] used for the alkali consensus | Removed from that sentence and, being otherwise uncited, from the list. |
| Iwaszuk–Nolan recruited into a vacancy-free trivalent consensus | Corrected: now cited as evidence that V~O~ compensation competes for trivalent dopants (Introduction, 4.2). |
| "OLED solar cells" | Corrected to "electron-transport layers in organic light-emitting diodes". |
| Primary ionic-radius source | Shannon (1976) added. |
| PSlibrary website citation | Replaced by the PSlibrary paper plus repository URLs. |
| Added | Deák et al. (2014) for U(Ti-3d) ≈ 3.5 eV; Freysoldt et al. (2014) for the formation-energy formalism. All three new entries are marked for verification against the publisher record. |
| Unverified | Mazierski 2020, Arrigoni & Madsen 2020, Boonchun 2016 and Raghav 2020 could not be opened from this environment; the specific values attributed to them are marked [AUTHOR ACTION: verify]. |

## Part E — Items that require new calculations, in priority order

1. Dual-U (U~Ti~ = 3.5, U~O~ = 5.5 eV) relaxation of Pr_VO and the full dual-U formation-energy cycle for Pr and Rb (R06). ≈ 1–2 days on the stated hardware.
2. D3 single points on Pr_perfect and Rb_perfect (R13). ≈ 12 h.
3. Pristine 2×2×2 single points; tabulation of the already-computed 2×2×1 and 3×3×2 energies (R10). ≈ 6 h plus bookkeeping.
4. Spin-density isosurface of Rb_VO from existing pp.x output; m and m~abs~ per charge state from existing outputs (R08, R14). Bookkeeping only.
5. Tighter re-relaxation (0.001 Ry/Bohr) of Pr_VO and Rb_VO and re-evaluation of E~f~ (R09). ≈ 2–4 days.
6. One cut-off test (55 Ry) on Pr_VO/Pr_perfect (R10). ≈ 1 day.
7. Optional but strengthening: two Rb_VO sites (R16); a second alkali (K^+^) or a second trivalent (La^3+^) at the same protocol (R03).
