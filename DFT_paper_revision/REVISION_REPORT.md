# Pre-submission revision report — Pr/Rb-doped anatase TiO~2~ DFT+U manuscript

**Prepared 2 October 2026 from the five files supplied** (FINAL manuscript, BACKUP manuscript, FINAL Supporting Information, Full Reviewer/Editor Audit of 15 September 2026, Error Audit of 10 June 2026) **and the archive screenshot.**

## 1. Bottom line

The FINAL manuscript is not submittable as it stands, and the two audits you already have say why. The good news is that the underlying numbers hold up: I re-derived every formation energy, difference and electron count from the Rydberg totals in your own SI and they reproduce exactly (Section 3 below). What does not hold up is the interpretation built on them. Version 4, delivered here, keeps every number and rebuilds the paper around what the calculations can support. It is ready for you to complete; it is not ready to submit, because about a dozen items need data or short calculations that only you can supply (Section 5). With roughly one week of compute on the hardware stated in the SI, those can be closed.

## 2. The most important findings

**2.1 Your FINAL file does not contain the Error Audit's corrections.** The Error Audit (10 June 2026) states that thirteen findings "are applied in DFT_Manuscript_TiO2_PrRb_v3p51.docx". The FINAL file still carries the uncorrected text for E1, E2, E4, E5, E7, E9, E10, E11 and E12 (for example "5.35 eV" throughout, "ΔΔE = −40 meV", "static dielectric constant ε~∞~", "direct experimental support for the −4.06 eV value", and the four-cell Bader claim in the Conclusions). Worse, FINAL contains a different harmonisation from the audit's: §3.7 was changed from "+5.36 eV / −38 meV" to "+5.35 eV / −40 meV", i.e. the rounded value was propagated instead of the exact one and the sign error was kept. The screenshot shows the Error Audit sitting in `DFT_paper\_archive`, next to `old_manuscripts`; the likely explanation is that v3p51 was archived and FINAL was continued from v3p50. **Action: look in `_archive\old_manuscripts` for `DFT_Manuscript_TiO2_PrRb_v3p51.docx` and confirm; v4 re-applies all thirteen fixes regardless.** FINAL differs from BACKUP only by the added in-house pristine value (4.74 eV) and the relabelling of two Table 2 cells; everything else, including the stale figures, is identical.

**2.2 The Pr pseudopotential freezes the 4f electrons in the core, so the "Pr-4f hybridisation" mechanism was never computed.** The PSlibrary documentation states that the "spdn" lanthanide datasets "have 4f electrons in the core" and are generated for the trivalent ion; Pr.pbe-spdn has 11 valence electrons (5s^2^5p^6^5d^1^6s^2^). Your own SI proves this independently: the Bader electron totals of Pr_VO and Rb_VO (376.998 e and 374.998 e) equal the counts obtained with Z~val~(Pr) = 11 and Z~val~(Rb) = 9. The SI sentence "Z~val~ = 11 … and the 4f^2^ subshell are all explicit in the valence" is self-contradictory (11 electrons leave no room for 4f^2^) and the "Pr 4f" curve in Figure S1 is an empty channel. This confirms audit finding R02 and forces removal of the Pr^3+^/Pr^4+^ redox and 4f-hybridisation language. It does not invalidate the energetics.

**2.3 Every doped cell has an odd number of electrons, so the "closed-shell singlet" description of the Pr cells is wrong by construction.** Pr_perfect (383 e), Pr_VO (377 e), Rb_perfect (381 e) and Rb_VO (375 e) cannot be closed-shell. A collinear m = 0 result for an odd-electron cell is a smeared solution with fractional occupations. This resolves R04 and R05 in one stroke and is now stated in Section 3.3 of v4 with Table 1 (electron ledger).

**2.4 The formal carrier count explains the energetic ordering, which is the paper's real result.** Pristine 4.74 → Pr 1.29 → Rb −4.06 eV follows the hole count 0 → 1 → 3. One vacancy over-compensates Pr (net one excess electron) and under-compensates Rb (one residual hole). The dual-U calculation (3 μ~B~ for Rb_perfect, 1 μ~B~ for Pr_perfect) and the charged-cell spin series (1.21 → 1.99 → 2.99 μ~B~) both confirm the ledger. That is a clean, defensible story; "aliovalency over ionic radius" was not, because two dopants that differ in everything cannot isolate one variable (R03).

**2.5 Pr does not suppress V~O~ relative to pristine.** It lowers the cost by 3.45 eV. The "trap-free Pr ETL" framing (R01, R17) is withdrawn in v4.

**2.6 All five main-text figures and SI Figure S1 are stale or mislabelled**, exactly as the audit says (verified by inspecting the embedded PNGs): Figure 3 still plots a Janotti literature baseline of "~4.5 eV" with a note that the in-house pristine calculation "was deferred", contradicting Table 1; Figure 4 carries "NEW finding" and "Rb_VO carries Ti^3+^ trap"; Figures 1 and 5 label the Rb defect a "Ti^3+^ trap" while the text says O-hole polaron; Figure 2 cites an unsourced "0.01 Ry/Bohr literature standard"; Figure S1 shows a non-existent Pr-4f channel. I rebuilt the two figures that depend only on reported numbers (formation energies; magnetisation). The other four need your raw data; exact relabel instructions are in the v4 captions.

**2.7 Smaller provenance problems you should fix from the records.** (a) The pristine V~O~ relaxation ended at 0.0056 Ry/Bohr, above your 0.005 threshold (SI S1); v4 discloses it. (b) The main text quotes 2×2×1 and 3×3×2 energies that appear nowhere in the SI; Table S2 has only Γ and 2×2×2 for the four doped cells, and no pristine 2×2×2. (c) SI Table S6 says the 2×2×2 stage completed "Pr_perfect, Rb_perfect, Pr_VO", but Table S2 reports an Rb_VO value. (d) The D3 terms quoted (−10.29/−10.09 eV) differ by 0.04/0.01 eV from E(D3) − E(production). (e) The dual-U Rb_perfect and Rb_VO total energies are not in the SI. (f) The SI mentions a local path `JMCA_plan/` and "the v8 master spreadsheet"; the main text cites "Supporting Information spreadsheet, Section 15" that was not supplied.

## 3. Numbers I re-derived from your Ry totals (1 Ry = 13.605693 eV)

| Quantity | Re-derived | In FINAL | Note |
|---|---|---|---|
| E~f~(V~O~), pristine / Pr / Rb | +4.745 / +1.292 / −4.063 eV | 4.74 / 1.29 / −4.06 | reproduces |
| Pr − Rb contrast, Γ | 5.356 eV → **5.36** | 5.35 | FINAL double-rounded (E1) |
| Contrast at 2×2×2 | 5.394 eV | 5.39 | reproduces |
| ΔΔE (2×2×2 minus Γ) | **+0.038 eV** | −40 meV | FINAL sign and value wrong (E2) |
| Pr − pristine; Rb − pristine | −3.45; −8.81 eV | 3.45; 8.80 | reproduces |
| Alternative sites O1/O7/O17 | 2.07 / 2.72 / 2.07 eV; +0.78 / +1.43 | same | reproduces |
| Electron counts | 384 / 383 / 377 / 381 / 375 | not given | confirmed by Bader sums 376.998, 374.998 |
| Force threshold | 0.005 Ry/Bohr = 0.129 eV/Å | – | audit correct |
| Cell volume; V~O~ density | 570.25 Å^3^; 1.75×10^21^ cm^−3^ | – | audit correct |

## 4. What version 4 changes (summary; the response document lists every item)

- Title → "Oxygen-Vacancy Energetics and Hole Localization in Pr- and Rb-Substituted Anatase TiO~2~: A DFT+U Comparison". Abstract rewritten around the three formation energies, the electron ledger and the method dependence of Pr localisation.
- New Table 1 (pseudopotential valences, electron counts, formal carriers) and Table 2 (Ry totals to five decimals, E~f~ at Γ and 2×2×2, uncertainty statement). Old Table 2's interpretation rows replaced by observables (Table 3) and the dual-U results (Table 4).
- Methods consolidated (2.1–2.8), with the Pr-4f core treatment, smearing, spin-initialisation convention, force tolerance in eV/Å and the oxygen-reference definition made explicit.
- Results reorganised: structure; energetics; spin states and electron counts; oxygen-site U; charged-cell spin series (spin only); electronic-structure diagnostics (unaligned E~F~ caveat, PDOS, pristine-only HSE06); sensitivity tests (U, k-mesh corrected, D3 undetermined, "three selected sites", Bader qualified).
- Discussion (4.1–4.5) explains the ordering from the ledger, places the results against Carey–Nolan, Iwaszuk–Nolan, Tian and Vural correctly, states what the design does not isolate, and turns device statements into hypotheses.
- Limitations (fourteen items) placed before a short Conclusions; "eight orthogonal probes", slogans, "autonomous post-processing sequence", "submission window" and similar preparation language removed.
- All thirteen Error-Audit fixes applied; all reference-attribution errors fixed ([16]→[18]; [33]/[37] described correctly; [35]/[36] dropped; "OLED solar cells" fixed). References renumbered by first appearance from a keyed database (49 cited). Three references added and marked for verification: Shannon 1976 (ionic radii), Freysoldt et al. 2014 (defect formalism), Deák et al. 2014 (U ≈ 3.5 eV for anatase, retrieved via Wiley Scholar Gateway).
- Declarations added in Elsevier form: CRediT, competing interests, data availability (deposit at submission), generative-AI use.
- Length: ≈ 7,400 words of main text including tables and markers (FINAL: ≈ 11,500).

## 5. What only you can do (in priority order)

**Calculations (about one week on the i5 stated in the SI):**
1. Dual-U relaxation of Pr_VO and the dual-U formation-energy cycles for Pr and Rb (closes R06; the single most valuable addition).
2. D3 single points on Pr_perfect and Rb_perfect (closes R13), or delete the D3 paragraph.
3. Pristine 2×2×2 single points, and tabulation of the 2×2×1/2×2×2/3×3×2 energies already computed (closes R10 bookkeeping).
4. Tighter re-relaxation (0.001 Ry/Bohr) of at least Pr_VO and Rb_VO, with E~f~ re-evaluated (R09); one 55 Ry cut-off test.

**Bookkeeping from existing outputs (hours):** UPF hashes and header blocks (Table S7); smearing width; E~F~ of Pr_perfect and Rb_perfect; m and m~abs~ per charge state; dual-U Rb energies; D3 stage times; coordinates and distances of the four vacancy sites; first-shell dopant–O distances (Table S8); run manifest (Table S10); spin-density isosurface of Rb_VO (Figure S4); HSE06 input check (screening parameter, exx grid, +U off).

**Artwork:** regenerate Figures 1, 4, S1 and S3 as instructed in the captions; use the new Figures 2 and 3 (`figures/Fig2_formation_energies_v4.png`, `figures/Fig3_magnetisation_v4.png`; script `figures/make_figures.py`). Do not reuse the stale figures (copied to `figures/OLD_*_STALE_do_not_use.png` for reference only).

**Verification:** the values attributed to Mazierski 2020, Arrigoni & Madsen 2020, Boonchun 2016 and Raghav 2020 could not be opened from here; check them against the full texts. Decide whether to keep the Fermi-energy comparison (needs alignment) and the HSE06 paragraph (needs band gaps).

**Submission mechanics:** deposit the data package on Zenodo before submission; trim the abstract to the journal cap; write highlights; supply suggested reviewers; confirm which quartile list Universiti Malaya counts.

## 6. Journal strategy (details and sources in `submission/Journal_Shortlist.md`)

A bulk DFT+U two-dopant study with explicit limitations is a good paper for a solid Q1 materials journal and a weak one for an energy-flagship journal. Recommended: **Applied Surface Science** (IF 6.9, 2024; Scimago Q1 in all its categories; strong topical fit, modest scope risk) as the primary target after items 1–3 above are done; **Journal of Alloys and Compounds** (IF 6.5, Q1) as the transfer option; **Journal of Materials Chemistry A** (IF 9.5) only for a follow-up with a matched-valence dopant series; **Physical Review Materials** or **J. Phys. Chem. C** if readership matters more than impact factor. Note that JPCC is Q1 on Scimago but reported Q3 on JCR. All metrics are aggregator snapshots; confirm on Scimago/JCR before the cover letter goes out.

## 7. Files delivered (all under `DFT_paper_revision/`)

| Path | What it is |
|---|---|
| `REVISION_REPORT.md` / `.docx` | this report |
| `manuscript_v4/Ghadimimehr_DFT_TiO2_PrRb_v4_MANUSCRIPT.docx` (+ `.md`, `_PREVIEW.pdf`) | revised manuscript with [AUTHOR ACTION] markers; the PDF is a reading preview rendered from the Markdown source, not from the Word file |
| `manuscript_v4/part1…part3*.md`, `refs.py`, `build_refs.py` | editable sources; re-run `build_refs.py` after edits to renumber references |
| `supporting_information_v4/Ghadimimehr_DFT_TiO2_PrRb_v4_Supporting_Information.docx` (+ `.md`, `_PREVIEW.pdf`) | revised SI with new energy ledger (S9) and run manifest (S10) |
| `response_to_audit/Response_to_Audit_v4.docx` (+ `.md`) | point-by-point response to R01–R18, E1–E13, figure and reference audits; reusable as the reviewer response letter |
| `figures/` | rebuilt Figures 2 and 3 (PNG + PDF), generating script, staged originals with the names used in v4, stale figures quarantined |
| `submission/Journal_Shortlist.md` / `.docx` | nine candidates with tiers, metrics, sources and a pre-submission checklist |
| `submission/Cover_Letter_Applied_Surface_Science.docx` (+ `.md`) | cover letter for the recommended target |
| `source_text/` | plain-text extractions of the five supplied files, for diffing |

## 7a. Editorial pass after v4 (added 2 October 2026)

After v4 was built, an independent compliance check (19 applied / 13 partial / 9 not applied of 41 audit items reached) and an editorial reject-hunt (87 findings from a handling-editor lens and a computational-methods lens) were run; the usage limit interrupted the remaining lenses, so the findings were verified and applied by hand. The corrections that matter most for an editor or referee: the abstract is now 243 words and no longer contradicts Table 4; the double-rounded 8.80 eV is 8.81 eV; the production vacancy is no longer called the nearest-neighbour oxygen (the earlier draft said that site was not tested, so you must state the actual index and distance); the "zero starting magnetisation" statement is replaced by a request for the actual input values, because Quantum ESPRESSO requires a non-zero value; two nearly degenerate Rb_VO spin solutions (m~abs~ = 1.21 μB from the relaxation, 1.00 μB from every from-scratch single point) are disclosed and must be ranked; the HSE06 total energy differs from the PBE+U total by 348 Ry, which cannot come from the functional alone and must be explained (different pseudopotentials?); the Bader dopant charges fail the sum rule of Table S3 and must be re-extracted; the k-mesh series is non-monotonic between 2×2×2 and 3×3×2 and is now stated as such; all "withdrawn / used earlier" wording is gone from the manuscript (it belongs only in the response letter); placeholder notes no longer print in the reference list; a graphical abstract and five highlights now exist; the generative-AI, funding and CRediT statements are in Elsevier form. See response_to_audit/Editorial_Pass_Log.md for all 87 dispositions.

## 8. What I could not do

The six Word files pass the Office Open XML schema validator; LibreOffice is not functional in the preparation environment, so their page layout was checked on a Chromium render of the same Markdown source (the `_PREVIEW.pdf` files). Open each `.docx` in Word once before editing. I cannot run Quantum ESPRESSO here, open your archive, or read your output files, so nothing in v4 is a new result. I cannot submit on your behalf: submission must be made by the corresponding author through the journal's portal after all co-authors approve. Publisher, Scimago and DOI landing pages were blocked from this environment, so journal metrics and the four flagged references rest on secondary sources and need your confirmation.
