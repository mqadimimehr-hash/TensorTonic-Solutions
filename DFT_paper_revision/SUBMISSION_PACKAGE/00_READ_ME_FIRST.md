# Submission package — Applied Surface Science (Elsevier)

**Manuscript:** Oxygen-Vacancy Energetics and Dopant-Induced Holes in Pr- and Rb-Substituted Anatase TiO₂: A DFT+U Comparison
**Built:** 4 October 2026 (round 5), from branch `claude/exciting-shannon-z4bl69` (PR #5)

## Status: ready to upload

Every [AUTHOR ACTION] note has been resolved. The Funding section reads "This work was supported by the Universiti Malaya Research Grant [grant number RU004-2025H]." `tools_package.sh` reports 0 markers in both Word files. The internal "Revision note" boxes are removed automatically from the copies in this folder.

Facts that could not be recovered from the files at hand are now stated as such in the text ("not recorded", "not extracted", "not re-inspected for this revision"), which is acceptable to a reviewer; they are listed in group B below in case you want to replace them with real values.

**One substantive finding from the run log (round 5):** the production pristine perfect cell is an unrelaxed single point (residual force 0.0225 Ry/Bohr). The manuscript now says so, and the pristine formation energy (+4.74 eV) and the two reductions measured from it are labelled lower bounds in the Abstract, Table 2, Sections 2.6, 3.2, 4.1, 4.2, 5 and the Conclusions, the Highlights, the cover letter and the graphical abstract. Job 0 of `revision_calculations/` relaxes that cell (about 1–3 days) and the analysis script prints the corrected values.

## Files in this folder (what to upload, in Elsevier's order)

| File | Upload as | Notes |
|---|---|---|
| `01_Cover_Letter.docx` | Cover letter | Addressed to the Editor of Applied Surface Science |
| `02_Manuscript.docx` | Manuscript (editable Word) | Title page, abstract (248 words), text, tables, figure captions, references (50). `02_Manuscript_preview.pdf` is for checking only |
| `03_Highlights.docx` | Highlights | 5 bullets, each ≤ 85 characters |
| `04_Graphical_Abstract.png` / `.pdf` | Graphical abstract | 1535 × 590 px (Elsevier minimum 1328 × 531 px) |
| `05_Figures/Figure_1–4.pdf` (+ `.png`) | Figures | Vector PDF preferred; PNG at 300 dpi as backup |
| `06_Supporting_Information.docx` | Supplementary material | Includes Figures S1–S2 and Tables S1–S10. Preview PDF for checking only |
| `07_Data_and_scripts_for_Zenodo/` | **Not uploaded to the journal** — deposit on Zenodo, then put the DOI in the Data availability statement | Energy ledger + check script (reproduces every formation energy), figure data and plotting scripts. Add your QE input/output files, pseudopotentials and Bader ACF.dat files to the same deposit |

## A. Optional before upload

- **Zenodo deposit.** The Data availability statement now says the files are available on request and will be deposited with a DOI on acceptance. If you deposit folder 07 (plus your QE inputs/outputs, pseudopotentials and ACF.dat files) before submission, replace that sentence with the DOI.
- **AI declaration.** It now states the facts (text editing, consistency checks, Python plotting scripts; no image generated or altered). Elsevier's policy on AI-assisted figure scripts is not explicit; asking the editorial office is prudent but not required.
- **Author details.** Check names, affiliations and the corresponding-author e-mail on the title page.

## B. "Not recorded" entries you can fill later (none blocks submission)

If you send the WSL bundle (`tio2_needed.tar.gz`) I can replace these statements with values: degauss and etot_conv_thr of the production inputs (Section 2.4, 2.6, Table S10); the "smearing contrib. (−TS)" lines (Section 2.4, S1); the Pr dataset MD5 (Table S7); the k-mesh, cut-off and residual stress of the bulk vc-relax (Section 2.3); the relaxed Pr_VO coordinates (Figure 1 panel c, Table S8); E~F~ and m~abs~ of Pristine_VO (Table 3); m~abs~ of the dual-U and q = +1 runs; the per-atom Bader table (Table S3; the dopant charges are currently derived from the recorded totals); the HSE06 q-grid/ecutfock (Section 2.8); wall times (Table S6).

## C. Optional extra calculations (all stated as "not performed" in the text)

Inputs are ready in `revision_calculations/` (job numbers in brackets); run `launch_revision_queue.sh` as its README describes and send back the `.out` files and the analysis output:

- **recommended, desktop:** relaxation of the pristine perfect cell [0]; cut-off 55/70 Ry [1]; Pristine_VO at 2×2×2 [2]; smearing test with −TS [3]; D3 on Pr_perfect, Rb_perfect and O₂ [4]; symmetry-free, O-seeded spin search on the Rb cells [5, then 6 if lower]
- **longer, desktop:** dual-U Pr_VO relaxation [7] (a dual-U formation energy also needs a dual-U O₂ reference and the completed dual-U Rb_VO relaxation); re-relaxation of the four doped cells to 0.001 Ry/Bohr [8]
- **HPC only:** linear-response U with hp.x [9]; 96-atom supercells [10, cost estimate only]
- NSCF rerun with `diago_full_acc = .true.`; Rb_VO spin-density isosurface (optional Figure S4)

## Before you press "submit"

- `tools_package.sh` reports 0 `AUTHOR ACTION` markers in both Word files; if you edit the sources again, re-run it and check that line.
- Check author names, affiliations and the corresponding-author e-mail on the title page.
- Suggested reviewers (optional in Editorial Manager): choose researchers you have cited but not co-authored with.
- The companion device-simulation paper (Pr³⁺:SnO₂ / CsPbBr₃) is **not** part of this submission; see `device_paper_review/Device_Manuscript_Audit.docx` before sending it anywhere.
