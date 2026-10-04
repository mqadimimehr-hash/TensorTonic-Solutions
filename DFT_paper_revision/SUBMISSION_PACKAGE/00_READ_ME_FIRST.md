# Submission package — Applied Surface Science (Elsevier)

**Manuscript:** Oxygen-Vacancy Energetics and Dopant-Induced Holes in Pr- and Rb-Substituted Anatase TiO₂: A DFT+U Comparison
**Built:** 4 October 2026, from branch `claude/exciting-shannon-z4bl69` (PR #5)

## Status: almost ready — do not upload until the items in sections A and B are done

The manuscript still contains **34 bold [AUTHOR ACTION] notes** and **1 [NEEDS CITATION]**, and the Supporting Information **21 notes**. Every note must be resolved or deleted before upload; the editor must not see them. They fall into three groups.

## Files in this folder (what to upload, in Elsevier's order)

| File | Upload as | Notes |
|---|---|---|
| `01_Cover_Letter.docx` | Cover letter | Addressed to the Editor of Applied Surface Science |
| `02_Manuscript.docx` | Manuscript (editable Word) | Title page, abstract (248 words), text, tables, figure captions, references (46). `02_Manuscript_preview.pdf` is for checking only |
| `03_Highlights.docx` | Highlights | 5 bullets, each ≤ 85 characters |
| `04_Graphical_Abstract.png` / `.pdf` | Graphical abstract | 1535 × 590 px (Elsevier minimum 1328 × 531 px) |
| `05_Figures/Figure_1–4.pdf` (+ `.png`) | Figures | Vector PDF preferred; PNG at 300 dpi as backup |
| `06_Supporting_Information.docx` | Supplementary material | Includes Figures S1–S3 and Tables S1–S10. Preview PDF for checking only |
| `07_Data_and_scripts_for_Zenodo/` | **Not uploaded to the journal** — deposit on Zenodo, then put the DOI in the Data availability statement | Energy ledger + check script (reproduces every formation energy), figure data and plotting scripts. Add your QE input/output files, pseudopotentials and Bader ACF.dat files to the same deposit |

## A. Administrative items (must be done; nobody else can do them)

1. **Funding statement** — insert grant numbers, or the standard sentence "This research did not receive any specific grant…".
2. **Zenodo deposit** — upload folder 07 plus your QE inputs/outputs, pseudopotentials and ACF.dat files; insert the DOI in the Data availability statement.
3. **Figure S3** (force convergence) is still interim artwork with patched labels; regenerate it from the BFGS force lines of the Pr_VO and Rb_VO relaxation outputs (or send me the two `.out` files and I will script it).
4. **Generative-AI declaration** — confirm with the journal that figures plotted from your data by AI-assisted plotting scripts are acceptable (Elsevier forbids AI-created or AI-altered images), or regenerate them with your own scripts; adjust the declaration accordingly.
5. **Indoor-illuminance citation** ([NEEDS CITATION], Introduction) — put the Pecunia et al. 2021 PDF in your Google Drive so it can be checked, or cite another source you have read.

## B. One-line facts from your input/output files (needed; about one hour with the files)

Send me the WSL bundle (`tio2_needed.tar.gz`) and I can fill all of these myself:

- degauss, starting_magnetization, etot_conv_thr / forc_conv_thr, nosym and any tot_magnetization in the production inputs (Methods 2.4–2.6; Table S10)
- whether the production **Pristine_perfect** energy is from a relaxed geometry (Methods 2.6) — if it is not, it must be relaxed and Table 2 updated
- k-mesh, cut-off and residual stress of the bulk variable-cell relaxation (Methods 2.3)
- Pr dataset MD5 checksum and the "Valence configuration" block of each UPF header; the suggested cut-offs in the UPF headers (Methods 2.1; Table S7)
- Pr_VO final coordinates (Figure 1 panel c, Pr–O distances, Table S8) and confirmation of the removed oxygen
- Pristine_VO Fermi energy (Table 3); m~abs~ of Rb_VO at q = +1 (Section 3.5)
- dual-U Rb_perfect / Rb_VO energies in Ry, m~abs~, and whether the Rb_VO relaxation finished (Section 3.4; Tables S5, S9)
- E~tot~, m, m~abs~ of the SCF run before the Rb_VO PDOS (Section 3.3)
- Bader: re-extract the four dopant/mean populations from ACF.dat, FFT grid, PAW reconstruction (Section 3.7; Table S3)
- HSE06 input details (screening parameter, q-grid, ecutfock, pseudopotentials) (Methods 2.8)
- smearing (−TS) lines; occupations near E~F~ of Pr_perfect and Pr_VO (Sections 2.4, 3.3)
- run 25 identity (the 0.281 eV reference) and output file names for the run manifest (Table S9/S10)

## C. Optional extra calculations (can instead be stated as limitations)

Each of these is already described as "not performed" in Section 5. If you do not run them, delete the corresponding note (or ask me to convert all of them to plain statements in one pass):

- dual-U Pr_VO relaxation and dual-U formation energies (the single most valuable addition)
- re-relaxation of the four doped cells to 0.001 Ry/Bohr
- D3 single points on Pr_perfect, Rb_perfect and O₂
- 55 Ry cut-off check; Pristine_VO at 2×2×2; NSCF rerun with `diago_full_acc = .true.`
- two extra Rb vacancy sites; core-level alignment of Fermi energies; HSE06 band gaps
- Rb_VO spin-density isosurface (optional Figure S4); reading literature V_O values from figures of Arrigoni & Madsen / Boonchun et al.

## Before you press "submit"

- Search both Word files for `AUTHOR ACTION` and `NEEDS CITATION` — the count must be zero.
- Check author names, affiliations and the corresponding-author e-mail on the title page.
- Suggested reviewers (optional in Editorial Manager): choose researchers you have cited but not co-authored with.
- The companion device-simulation paper (Pr³⁺:SnO₂ / CsPbBr₃) is **not** part of this submission; see `device_paper_review/Device_Manuscript_Audit.docx` before sending it anywhere.
