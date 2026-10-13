Error Audit --- DFT_Manuscript_TiO2_PrRb v3p50

Audit date: 10 June 2026. Scope: dimensional/unit consistency, numerical arithmetic, significant figures, notation and symbol consistency, cross-references, citation integrity, and logical consistency of claims. Thirteen findings were verified and corrected; all corrections are applied in DFT_Manuscript_TiO2_PrRb_v3p51.docx. No errors were found in the underlying DFT results themselves --- all findings concern presentation, internal consistency, or strength of claims.

Findings corrected in v3p51

  -------- ------------------------------------------------- -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- -----------------------------------------------------------------------------------------------------------------------
  **ID**   **Location**                                      **Issue**                                                                                                                                                                                                **Fix applied in v3p51**

  E1       Abstract; §3.2; §3.4; §3.10; §4; Fig. 3 caption   Formation-energy contrast quoted as 5.35 eV in six places but +5.36 eV in §3.7 (the unrounded value is 5.36 eV; 5.35 arises from double rounding of +1.29 and −4.06).                                    Harmonised to 5.36 eV throughout; §3.2 now notes the rounding origin.

  E2       §3.7                                              ΔΔE = −38 meV has the wrong sign under the natural definition: the contrast grows from 5.36 eV (Γ) to 5.39 eV (2×2×2), so the shift is +38 meV. No sign convention was defined.                          Changed to ΔΔE = +38 meV with the definition stated explicitly (2×2×2 contrast minus Γ-only contrast).

  E3       Table 1                                           Dangling asterisk on "Pristine TiO_2 \*" with no footnote anywhere; the literature value ≈+4.5 eV was uncited. Rounded column arithmetic for Rb gives −4.07, not the stated −4.06.                       Footnote added citing \[13,18\] and explaining that formation energies use unrounded Ry energies.

  E4       §3.7                                              Broken-symmetry cross-check cited as "Section 3.2" in one place and "Section 3.3" in another; it is in §3.3.                                                                                             Corrected to Section 3.3.

  E5       §3.3                                              Non sequitur: the Rb_VO dual-Hubbard moment was claimed to be "verified by the dual-Hubbard Pr_perfect relaxation (§3.9)" --- a different cell cannot verify it.                                         Rephrased: the dual-Hubbard protocol is independently validated on Pr_perfect in §3.9.

  E6       §1 (roadmap)                                      Paper roadmap omits §3.12 (Bader analysis), which was added in v3p50.                                                                                                                                    §3.12 added to the roadmap.

  E7       §4                                                Conclusions claim Bader analysis was applied to four cells (Pristine_perfect, Pr_VO, Rb_VO, Rb_perfect); §3.12 and the computation record show only Pr_VO and Rb_VO produced ACF.dat results.            Corrected to "the Pr_VO and Rb_VO cells".

  E8       §3.12                                             Internal arithmetic: "\~12 % of the total hole density" on Ti is inconsistent with the stated mean depletion (−0.012 e × 15 Ti ≈ 0.18 e, i.e. \~16--19 %).                                               Replaced the percentage with the directly supported numbers (−0.012 e per Ti; ≈0.18 e summed).

  E9       Throughout                                        Symbol ambiguity: \|m\| used for two different quantities --- absolute magnetisation (1.21 μB) in most places, but \|net magnetisation\| (0.97 μB) in §3.10.                                             Notation defined once in §2 (m = net, m_abs = absolute); all occurrences disambiguated (13 × m_abs, net values as m).

  E10      §4.1 (vii)                                        Physics terminology: ε∞ ≈ 5.8 called the "static dielectric constant"; ε∞ is the ion-clamped (high-frequency) constant. The static ε₀ of anatase is ≥20, which would reduce the image-charge estimate.   Relabelled ion-clamped (high-frequency); estimate now stated as an upper bound.

  E11      §3.2                                              Overclaim: Tian et al. \[14\] said to provide "direct experimental support for the −4.06 eV value"; experiment supports the sign/mechanism, not a supercell-model number.                                Softened to support for sign and mechanism.

  E12      §3.4                                              Internal tension: hole described unconditionally as delocalised with "no localised trap", but §3.9 (dual-Hubbard) localises it on O-2p.                                                                  Qualified: delocalised in the single-U description, localised under dual-Hubbard (§3.9).

  E13      Typography                                        Mixed symbols: μ_B / µB vs μB; Makov-Payne (hyphen) vs Makov--Payne (en dash).                                                                                                                           Normalised to μB and Makov--Payne throughout.
  -------- ------------------------------------------------- -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- -----------------------------------------------------------------------------------------------------------------------

Checked and confirmed correct

-   All formation-energy arithmetic in Table 1 reproduces from the Ry totals (Pr: +1.29 eV; Rb: −4.06 eV; contrast 5.36 eV).

-   Ry→eV conversions in Tables 1--2 correct to the displayed precision.

-   Fermi-level differences: 9.99 − 7.89 = 2.10 eV; 9.99 − 7.13 = 2.86 eV --- both as stated.

-   Kröger--Vink bookkeeping: Δq = −3 per Rb; 1.5 V_O per Rb (each V_O contributing +2) --- consistent.

-   Charged-defect magnetisation trajectory 1.21 → 1.99 → 2.99 μB consistent with the 3-hole picture.

-   HSE06 ω conversion 0.106 bohr⁻¹ = 0.2 Å⁻¹ --- correct.

-   Supercell stoichiometry (48/47 atoms; 16 Ti + 32 O) and lattice parameters consistent with anatase.

-   Fig. 5 caption EF = 10.31 eV (NSCF, 2×2×2) vs 9.99 eV (Γ, SCF) --- consistent with the k-mesh dependence reported in §3.7, not an error.

-   O₂ triplet reference (m = 2.00 μB) --- correct internal sanity check.

-   All 56 references checked against in-text citations: every citation resolves; no orphaned or missing entries found.

Recommendations (not changed)

-   Identifier-style notation (V_O, Pr_VO, E_form with literal underscores, \~113 occurrences) is consistent but unconventional for JMCA; consider converting to true subscripts at submission. Not changed, as the labels also serve as computational cell identifiers.

-   Formation energies carry no explicit ± uncertainty; §3.7/§4.1 quantify convergence instead, which is acceptable, but a one-line summary uncertainty (e.g. ±0.05 eV from k-mesh + cutoff) in Table 1 would pre-empt reviewer comments.

-   The pasted "review" document (gpai PDF, 2026-06-10) contains no manuscript-specific findings --- it is a generic checklist of error types (gas constant, Lorentz factor, π truncation) none of which appear in this manuscript. The audit above is what that checklist demands when actually applied.
