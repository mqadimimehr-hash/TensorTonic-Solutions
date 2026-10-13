---
title: "Pre-submission audit: Pr³⁺:SnO₂ / CsPbBr₃ indoor–outdoor device-simulation manuscript (Ghadimimehr, Omar, Sheikh Raihan)"
subtitle: "Handling-editor report with two referee perspectives (device physics / perovskite PV, and numerical modelling)"
date: "3 October 2026"
---

**What was audited.** The Word file `77d4b4a6-Manuscript_Ghadimimehr.docx.docx` (about 8,700 words, 41 references, 9 figures, 5 tables, 21 numbered equations). Line numbers ("L123") point to the pandoc extraction `ms.md`. All 94 embedded WMF/MathType equations were rendered with libwmf and read. All raster figures were inspected. Figure captions held in floating text boxes, which pandoc drops, were read from `word/document.xml`.

**How numbers were checked.** Every derived number that could be recomputed is in `verify_numbers.py`, with its output saved in `verify_numbers_output.txt`, both in this folder. The script uses only values printed in the manuscript plus three verifiable external sources:

- the ASTM G173 AM1.5G spectrum, as bundled in pvlib;
- the CIE 1924 V(λ) curve and the CIE 015:2018 LED-B, FL and HP illuminants, as bundled in colour-science;
- Planck's law.

No citations or numbers were invented. Where a source is needed but could not be verified here, the text says **[NEEDS CITATION]**. Note that Crossref and publisher sites were blocked by the network proxy, so DOIs could not be resolved automatically.

---

# 0. Verdict

| Item | Assessment |
|---|---|
| Desk-reject risk at Solar RRL / SOLMAT / Progress in PV / Nano Energy / ACS AEM, as written | **Very high.** Three things on their own would justify editorial rejection: the title promises "Machine Learning" and "Density Functional Theory" that the paper does not contain; the methods claim a self-consistent Poisson/drift-diffusion solution that the results do not use; and the central chemistry (Pr³⁺ on Sn⁴⁺ as an electron donor that removes O-vacancies) is the opposite of standard defect chemistry and of the authors' own DFT companion. |
| Scientific soundness | **Not sound in its current form.** All 12 device results in Table 4 come out of a lumped single-diode equation (Eq. 14), reproduced here to rounding. The inputs J₀, R_sh and EQE are assumed. The headline 100× R_sh and 19.1× indoor PCE gain are **imposed** by the assumed scaling R_sh ∝ 1/N_it (Eq. 1). The impedance (EIS) section is described as "experimental", yet its R_rec values disagree with its own Eq. 21 by about 11 orders of magnitude. |
| Novelty | Moderate, if reframed honestly. A multi-spectrum (LSPDD) analysis that quantifies **how much shunt resistance a wide-gap CsPbBr₃ cell needs indoors** is useful. "Discovery" of a Pr-doped ETL is not supported. |
| Overall recommendation | **Do not submit yet.** This is equivalent to "reject and resubmit". Either (A) reframe as a transparent equivalent-circuit and sensitivity study, which can be done mostly in text plus small new calculations, or (B) add a real drift-diffusion validation (e.g., SCAPS-1D), a sensitivity analysis on the N_it→R_sh mapping, and corrected defect chemistry before targeting a Q1 venue. Route B is needed for Solar RRL or SOLMAT. Route A is realistic for *Solar Energy*. |

---

# 1. Fatal and major issues

Each item gives the location, a quote, the problem, the evidence, and the fix.

## F1. Title, abstract and claims do not match the content (fatal for editorial screening)

- **Location:** L1–8 (two alternative titles), L36–41 (abstract), L60–61 (keywords).
- **Quotes:**
  - Title 1: "Machine Learning‑Accelerated Discovery of Praseodymium‑Doped Electron Transport Layers to Overcome Shunt Leakage in **Rigid** Solar Cells …".
  - Title 2: "Machine Learning‑Enhanced **Density Functional Theory** for Praseodymium‑Doped Electron Transport Layers …".
- **Problems:**
  1. **No machine learning anywhere.** "Machine Learning" occurs only in the two titles; there is no model, dataset, training, regression or surrogate.
  2. **No DFT in this paper.** "DFT" appears only inside the title of ref. [27], and "density functional theory" only when citing others ([9], [11]). The DFT companion (anatase TiO₂) is never cited.
  3. **Rigid vs flexible.** Title 1 says "Rigid", but the body says "flexible" 16 times (ITO-PET, Figure 1b bending).
  4. **No mechanical analysis.** "Flexible" is nominal: there is no bending-radius, strain or cycling analysis.
  5. **"Discovery" is not shown.** One assumed parameter set is evaluated; nothing is screened or discovered.
  6. **Two titles.** Two alternative titles in the submitted file signals an unfinished manuscript.
- **Fix:** Pick one title that describes what is actually done. Suggested titles, chosen so they do not claim Pr chemistry:
  - For the current content: *"Shunt Resistance Governs the Indoor Efficiency of Wide-Gap CsPbBr₃ Solar Cells: A Multi-Spectrum Equivalent-Circuit Analysis of Interface-Passivated SnO₂ Electron-Transport Layers"*
  - If a drift-diffusion validation is added (route B): *"Interface-Trap and Shunt Engineering of SnO₂/CsPbBr₃ Solar Cells for Indoor Light Harvesting: Drift–Diffusion and Equivalent-Circuit Analysis under LED, CFL, Metal-Halide and Thermal Sources"*
- Remove "Machine Learning", "DFT" and "Discovery" unless the corresponding work is actually added. Delete "Rigid".
- Replace the abstract sentence at L36–41 with: *"Using a single-diode equivalent-circuit model parameterised from literature values, we quantify how the interface-trap density (N_it) at the SnO₂/CsPbBr₃ interface, represented through the dark saturation current density J₀ and an assumed shunt-resistance scaling R_sh ∝ N_it^−β, controls performance under AM1.5G and five 1000-lx indoor spectra taken from the LSPDD database."* Then move the Fermi–Dirac and generalised-Einstein material to the SI, or delete it (see F2).

## F2. "Self-consistent Poisson/drift-diffusion" is claimed, but every result comes from a lumped single-diode model (fatal for the modelling referee)

- **Location:** L36–41, L156–157, L366–400, L595 ("In the self-consistent device model …"), L1060.
- **Quotes:**
  - "We model the device physics using a self-consistent framework of coupled Poisson and drift-diffusion equations" (L366–367).
  - "The relations (1) to (5) … establish the governing system solved self-consistently in this work" (L398–400).
- **Evidence from the script, section C:** With J_sc = EQE × J_sc,max (EQE fixed at 0.85 or 0.704), J₀ and R_sh from Table 2, n = 1.5 and R_s = 10 Ω cm², the single-diode Eq. 14 reproduces **all 12 rows of Table 4** (V_oc, FF, PCE) to within rounding:

  | | V_oc calc. | V_oc paper | FF calc. | FF paper | PCE calc. | PCE paper |
  |---|---|---|---|---|---|---|
  | Doped, LED | 1.115 V | 1.115 V | 0.822 | 0.823 | 13.61 % | 13.62 % |
  | Control, LED | 0.232 V | 0.232 V | 0.250 | 0.250 | 0.712 % | 0.713 % |

  The control indoor V_oc values are exactly J_sc × R_sh (0.232, 0.414, 0.157, 0.146 V), i.e. a pure resistor, which is why FF = 0.250.
- **Nothing beyond the circuit enters the results:**
  - No band diagram, carrier profile or Poisson solution is shown.
  - The quantities η = 3.03, D_n = 2.44 μ_n k_BT/q, L_n × 1.56, S_n and the Tauc α(λ) have **no effect** on any reported number.
  - Eq. 12, J_sc = qG(L_n+L_p), is not applicable. With the paper's own τ_SRH = 1/(σ v_th N_t) = 100 ns, L_n = 3.6 µm and L_p = 1.6 µm, both much larger than the 500-nm thickness. Eq. 12 would then give 93 mA cm⁻², about 10× the absorbable limit (script section N).
  - The hole continuity equation (Eq. 6) has the wrong sign (see F6), which suggests the drift-diffusion system was never implemented.
  - "Relations (1) to (5)" includes Eq. 1, the R_sh scaling, which is not a transport equation.
  - No mesh, boundary conditions, interface model, discretisation (e.g., Scharfetter–Gummel), convergence criterion or code is described. The only implementation detail is "MATLAB software (Fermi-Dirac distribution)" (L156–157).
- **Fix, choosing one of:**
  - **(a) Honest reframing.** State that the device is described by Eq. 14 with literature-based parameters. Delete or move §2.2–2.5 (Poisson/DD, Fermi–Dirac, generalised Einstein, Eq. 12) to the SI as context. Rename "self-consistent numerical investigation" to "equivalent-circuit analysis".
  - **(b) Do it properly.** Run SCAPS-1D, Setfos, IonMonger or a documented MATLAB Scharfetter–Gummel solver with Table 1, including an explicit interface defect layer with N_it, its energy distribution and capture cross-sections. Report the J–V output, then **fit** Eq. 14 to the drift-diffusion J–V to extract J₀, n and R_sh. Only then is the single-diode analysis "derived".
  - In both cases add a "Model implementation and reproducibility" subsection and release the code and data.

## F3. The headline result is circular: R_sh ∝ 1/N_it is assumed, so the 100× R_sh and the indoor gain are inputs, not findings (fatal)

- **Location:** Eq. 1 (L186–190); Abstract L44–50; L158–160; L681–695; Conclusion L1071–1074 and L1099–1100.
- **Quote:** "The shunt resistance scales inversely with N_it: R_sh^(doped) = R_sh^(control) × N_it^(control)/N_it^(doped)" (Eq. 1, as rendered).
- **Problem 1 — the result is an input.** Choosing N_it = 10¹³ → 10¹¹ cm⁻² sets R_sh = 6.05×10³ → 6.05×10⁵ Ω cm² by construction. Neither 6.05×10³ Ω cm² nor the linear scaling is derived or cited. The abstract and conclusion ("a two-order-of-magnitude recovery of both shunt and recombination resistances … quantitatively confirm") present an assumption as a result.
- **Problem 2 — the physics does not support it.**
  - Interface traps produce a **non-ohmic** recombination current. That current enters J₀ and n (the exponential diode term).
  - An ohmic shunt in perovskite cells is normally attributed to pinholes, incomplete coverage, direct ETL/HTL contact, edge leakage or ion-related paths **[NEEDS CITATION]**.
  - A linear R_sh ∝ 1/N_it law has no stated physical basis.
- **Problem 3 — J₀ and EQE are not derived either.**
  - J₀ = 7.939×10⁻¹⁶ and 1.430×10⁻¹⁷ A cm⁻² come with no derivation. The Figure 6 caption (text box) admits "J₀ fixed from AM1.5G fit", yet there are no experimental data to fit.
  - With Table 1 values, n_i(CsPbBr₃) ≈ 0.1 cm⁻³. Order-of-magnitude estimates are J₀(n = 2, SRH) ≈ 4×10⁻¹⁸ A cm⁻² and J₀(n = 1, interface, S = 10⁵ cm s⁻¹) ≈ 10⁻³² A cm⁻² (script section O). So the 55.5× J₀ ratio cannot be obtained from N_it or S_n.
  - EQE = 0.85 vs 0.704 is also an input. It alone supplies the "21 % J_sc increase" and about 2.5 PCE points of the LED result.
- **Evidence from the script, section C3 (1000-lx LED, full factorial; c = control value, d = doped value):**

  | EQE | J₀ | R_sh | V_oc (V) | FF | PCE (%) |
  |---|---|---|---|---|---|
  | c | c | c | 0.232 | 0.250 | 0.71 |
  | c | d | c | 0.232 | 0.250 | **0.71** (J₀ alone does nothing while shunted) |
  | c | c | d | 0.952 | 0.804 | **9.42** (R_sh alone) |
  | c | d | d | 1.108 | 0.816 | 11.11 |
  | d | d | d | 1.115 | 0.822 | 13.61 |

- **Sensitivity to the assumed exponent.** If R_sh ∝ N_it^−β with the other doped values fixed, the LED PCE is:

  | β | LED PCE | Gain over control |
  |---|---|---|
  | 0 | 1.04 % | 1.5× |
  | 0.25 | 3.28 % | 4.6× |
  | 0.5 | 9.12 % | 12.8× |
  | 0.75 | 12.51 % | 17.5× |
  | 1 | 13.61 % | 19.1× |

  The "19.1-fold" headline is therefore a direct readout of β = 1.
- **Fix:**
  - Treat R_sh as an **independent design variable**.
  - Present PCE(R_sh, J₀) maps for each spectrum.
  - State the minimum R_sh needed to reach, say, 90 % of the R_sh→∞ PCE under each source. This is a defensible design rule that does not depend on Pr chemistry.
  - If a link to N_it is kept, present it as a scenario (β = 0, 0.5, 1) and cite any evidence for it **[NEEDS CITATION]**.
  - Suggested replacement for L158–160: *"Within the equivalent-circuit model, the indoor PCE is controlled primarily by R_sh: with R_sh = 6.05×10³ Ω cm² the cell behaves as a resistor (FF = 0.25) regardless of J₀, whereas raising R_sh to ≥ 6×10⁴ Ω cm² recovers most of the attainable PCE. Whether interface-trap passivation raises R_sh, and by how much, is an open experimental question; we therefore report results for R_sh ∝ N_it^−β with β = 0–1."*

## F4. Defect chemistry is reversed: Pr³⁺ on Sn⁴⁺ is an acceptor, not an electron donor and vacancy passivator (fatal)

- **Location:** L153–155; L178–186; L355–358; L404–410; Figure 2 caption (text box); Conclusion L1066–1069.
- **Quotes:**
  - "Substituting Pr³⁺ at Sn⁴⁺ sites supply an **excess electron** that compensates oxygen vacancy V(O) deep traps" (L355–357).
  - "Heavy Pr³⁺ doping of the SnO₂ ETL sets sets the **donor** concentration to N_D = 1.0 × 10¹⁹ cm⁻³" (L404–405).
- **Problem 1 — wrong sign of doping.** A trivalent cation on a tetravalent site is a negatively charged substitutional defect (Pr′_Sn in Kröger–Vink notation). It **removes** an electron, i.e. it is an acceptor. Charge balance is achieved by holes or by oxygen vacancies (2 Pr′_Sn + V_O••). So Pr³⁺ substitution, by itself:
  - cannot supply donors, so it cannot justify N_D = 10¹⁹ cm⁻³ and a degenerate Fermi level 78 meV inside the conduction band;
  - tends to **increase**, not decrease, the oxygen-vacancy concentration.
- **Problem 2 — the manuscript contradicts itself.** L146–148 states: "trivalent ions induce oxygen vacancies to maintain charge neutrality; however, pentavalent codoping (Nb⁵⁺, V⁵⁺) suppresses these defects".
- **Problem 3 — size mismatch.** The ionic radii differ strongly (Pr³⁺ much larger than Sn⁴⁺ in six-fold coordination; see R. D. Shannon, *Acta Crystallogr. A* **32**, 751 (1976)). This makes lattice substitution at 10¹⁹ cm⁻³ questionable; surface or grain-boundary segregation is more likely.
- **Problem 4 — the DFT companion says the opposite.** It reports (v4 abstract):
  - neutral V_O formation energy falls from **+4.74 eV** (pristine anatase) to **+1.29 eV** with Pr, so Pr makes vacancies *easier* to form;
  - "one hole per Pr³⁺";
  - "one vacancy over-compensates Pr".
- **Fix:**
  - Attribute the n-type doping (N_D = 10¹⁹ cm⁻³) to native donors (V_O, Sn_i) or to a deliberate donor, with citation, and **not** to Pr³⁺.
  - Present any Pr benefit as a *hypothesis*, e.g. surface or grain-boundary passivation of under-coordinated sites, or Pr–O–Sn bonding that lowers the electrically active D_it. Cite experimental evidence for rare-earth-modified SnO₂ ETLs if it exists **[NEEDS CITATION]**.
  - Run N_D as a sensitivity parameter (10¹⁷–10¹⁹ cm⁻³).
  - Suggested replacement for L355–360: *"Substitutional Pr³⁺ on Sn⁴⁺ sites is formally an acceptor (Pr′_Sn) and, by charge neutrality, tends to be compensated by oxygen vacancies. Any reduction of the electrically active interface-trap density by Pr incorporation must therefore arise from surface or grain-boundary passivation rather than from lattice electron donation. In this work we do not model the microscopic mechanism; we treat the interface-trap density N_it (10¹³ vs 10¹¹ cm⁻²) as an input and examine its device-level consequences."*

## F5. The EIS section presents simulated parameters as experimental, contradicts its own Eq. 21, and its "independent confirmation" is circular (fatal)

- **Location:** L39–40 ("EIS-derived interface parameters"); L750 ("TRPL and EIS measurements validate"); L880 and Fig. 6 caption ("experimental shunt-resistance values"); L893–896; L950–1053; Table 5; L1065; L1097 ("experimentally informed").
- **Quotes:**
  - "The **experimental spectra** were modeled using a two-arc equivalent circuit" (L950–951).
  - "This mutual consistency across **independent characterization techniques** confirms …" (L1012–1013).
- **Problem 1 — no experiments.** The manuscript contains no measured devices, films or impedance data. Every EIS number is generated from assumed values.
- **Problem 2 — Table 5 disagrees with Eq. 21 by about 10¹¹.** Eq. 21 at V_dc = 0 in the dark gives R_rec = nV_T/J₀ = **4.88×10¹³** (control) and **2.71×10¹⁵ Ω cm²** (doped). Table 5 lists 308 and 17,109 Ω cm².
- **Problem 3 — the low-frequency arc is wrong.** In the dark at 0 V, R_sh is in parallel with R_rec, so the low-frequency resistance equals R_sh. That gives 6.05×10³ and 6.05×10⁵ Ω cm², a ratio of **100**, not 55.5.
- **Problem 4 — the "55.5× match" is a tautology.** R_rec is *defined* through 1/J₀, so it must reproduce the J₀ ratio exactly.
- **Problem 5 — wrong layer for C₁.** C₁ = ε₀ε_r/d is assigned to the 50-nm ETL (174.6 nF cm⁻²). A degenerately doped ETL (N_D = 10¹⁹) is a conductor, not a dielectric. The geometric capacitance should come from the absorber: ε₀ × 6.5 / 500 nm = 11.5 nF cm⁻².
- **Problem 6 — the trap/capacitance link fails.** C_μ falls 7.5× while N_it falls 100×, yet the text calls this "consistent with the N_it reduction" (L1045–1046).
- **Problem 7 — the Bode claim cannot be read from the plot.** Recomputed from Eq. 20 with Table 5 values:
  - −Z″ peaks are at 3.4 kHz (control) and 396 Hz (doped);
  - Bode-*phase* maxima are at 33.5 kHz and 9.6 kHz;
  - so f₁/f₂ = 92 cannot be read from the phase plot, contrary to L1049–1050.
- **Problem 8 — figure vs text.** The doped Nyquist plot (Fig. 9a) shows **one** arc, contradicting "clearly resolved semicircles" (L1027–1028).
- **Problem 9 — misused references.** Refs. [31]–[33], cited as TRPL/EIS "validation" of "this Pr³⁺-based passivation strategy" (L747–750), concern Pd-doped and Pr-doped Cs₂AgBiBr₆ *absorbers* and a SCAPS study. None concerns Pr:SnO₂ ETLs.
- **Fix:**
  - Delete the EIS section, **or** retitle it "Simulated impedance response of the equivalent circuit (predictions for future experiments)".
  - Compute R_rec from Eq. 21 under illumination at the operating bias (e.g., at V_oc), including R_sh in parallel and stating the bias.
  - Use the absorber geometric capacitance.
  - Remove "experimental", "measured", "extracted", "independent" and "validate".
  - Remove the claims attributed to [31]–[33].
  - Suggested replacement for L950–952: *"To provide testable predictions, we computed the small-signal impedance of a two-RC equivalent circuit whose low-frequency branch is linked to the diode parameters through Eq. (21), evaluated at V_oc under 1000-lx LED illumination."*

## F6. Equation errors (major; fixable in text)

All equations were read from the rendered WMF images.

| Eq. | As printed | Problem | Correct form / fix |
|---|---|---|---|
| (6) | (1/q) ∂J_p/∂x = U_p − G_p | Sign error for holes | −(1/q) ∂J_p/∂x = U_p − G_p (or (1/q) ∂J_p/∂x = G_p − U_p) |
| (7) | N_D = N_C·F_1/2(η) ⇒ **F_1/2(η) = N_C/n** → η = 3.03 | Ratio inverted. As printed, F_1/2 = 0.22 gives η = −1.44 (non-degenerate). η = 3.03 only follows from F_1/2 = n/N_C = 4.545. | n = N_D = N_C F_1/2(η) ⇒ F_1/2(η) = N_D/N_C = 4.545 ⇒ η = 3.03, E_F − E_C = ηk_BT = +78.3 meV |
| (7)/(8) | F_1/2 defined with 2/√π; F_−1/2 never defined | 4.543/1.864 = 2.44 is correct **only** if both use the 1/Γ(j+1) normalisation. With unnormalised integrals the ratio is 1.22. | State F_j(η) = [1/Γ(j+1)] ∫₀^∞ ξ^j/(1+e^(ξ−η)) dξ for both j = 1/2 and j = −1/2 |
| Text after (8) | "diffusion length … exceeds the Boltzmann prediction by a factor of 2.44" (L424–425) | Contradicts Eq. 9, which gives √2.44 = 1.56 | "the diffusion coefficient exceeds … by 2.44, and the diffusion length by √2.44 = 1.56" |
| (9) | L_n/L_non-deg = √(F_1/2/F_−1/2) = 1.56 | Arithmetic correct. Placed inside a heading (L428). Applies to ETL electrons (majority carriers), so "minority-carrier diffusion length" (L1032) is wrong. | Put in body text; refer to the ETL majority-carrier diffusivity |
| Inline after (9) | η_p = (E_V − E_F)/k_BT **> 0** = "non-degenerate" (L433) | Sign wrong: with this definition a non-degenerate p-type layer has η_p ≪ 0. Here (E_F − E_V)/k_BT = 6.74 (CsPbBr₃) and 4.61 (Co₃O₄). | "(E_F − E_V)/k_BT ≥ 3, i.e. η_p = (E_V − E_F)/k_BT ≤ −3" |
| (11) | α = A_Tauc (hν − E_g)^1/2/hν with **A_Tauc = 6.7×10¹¹ cm⁻¹ eV^1/2** | Gives α(470 nm) = 1.48×10¹¹ cm⁻¹, against 1.8×10⁵ cm⁻¹ in Table 1 and L458. Matching 1.8×10⁵ needs A ≈ 8.2×10⁵. Also derived from [21], an MAPbI₃ paper. | Correct A_Tauc and cite a CsPbBr₃ absorption source **[NEEDS CITATION]** |
| (12) | J_sc = qG(L_n + L_p) | Long-base p–n approximation. Not valid for a 500-nm p-i-n absorber with L ≫ d (gives 93 mA cm⁻²). Not used anyway, since J_sc = EQE·J_sc,max. | Delete, or replace with J_sc = q∫₀^d G(x) η_c(x) dx |
| (13) | Plain text with zero-width characters (L516) | Not an equation object | Typeset |
| Cross-refs | "relations (1) to (5)" (L398); "Eq. (6)" for the Fermi integral (L415); "Equation (13) reveals" (L547); "full Eq. (11)" (L553); "Equation (19)" for J_sc,max (L614) | Wrong numbers | (2)–(6); (7); (15); (14); (18) |
| (21) | R_rec = (∂J/∂V)⁻¹ ≈ nV_T/[J₀ exp(V_dc/nV_T)] | Form fine but ignores R_sh in parallel; Table 5 inconsistent with it (F5) | Add R_sh in parallel; recompute Table 5 |

## M7. Band alignment and carrier-collection physics is wrong in the text and schematic (major)

- **Location:** L352–355; Figure 2; abstract L37–38.
- **Quote:** "CBM (≈ −4.5 eV) gives a **+1.15 eV spike-type offset** with CsPbBr₃ (CBM ≈ −3.3 eV) … and **collected at the graphene paper back contact**".
- **Problem 1 — cliff, not spike.** The ETL conduction-band minimum (−4.50 eV) lies **below** the absorber's (−3.35 eV). For electrons this is a 1.15 eV **cliff** (downhill), not a spike. A cliff this large is normally associated with enhanced interface recombination and V_oc loss **[NEEDS CITATION]**, which the single-diode model cannot capture. The χ(CsPbBr₃) = 3.35 eV value also needs a source.
- **Problem 2 — wrong contact.** In the stated n-i-p stack (ITO-PET/ETL/absorber/HTL/graphene), electrons are collected at **ITO** and holes at graphene paper.
- **Problem 3 — inconsistent stack order across the paper.**
  - Figure 2 places "ITO−PET" next to Co₃O₄ and "Graphene Paper" next to the ETL, contradicting §2.1 and Figure 1.
  - The abstract gives "ITO/PET/CsPbBr₃/Pr³⁺:SnO₂/graphene paper", which puts PET between ITO and the absorber, omits Co₃O₄ and places the ETL after the absorber.
- **Fix:**
  - Replace with: *"The SnO₂ CBM (−4.50 eV) lies 1.15 eV below that of CsPbBr₃ (−3.35 eV), forming a cliff-type offset that favours electron extraction but may enhance interface recombination; electrons are collected at the ITO front contact and holes, through Co₃O₄, at the graphene-paper back contact."*
  - Redraw Figure 2.
  - Use one stack string everywhere: ITO-PET/SnO₂(:Pr)/CsPbBr₃/Co₃O₄/graphene paper.

## M8. Internal numerical inconsistencies (major; text-fixable once the true values are confirmed)

Script sections A–M. The main items:

1. **"V_oc improvement of 145 mV (1.315 V vs. 1.150 V)"** (L724–725). 1.315 − 1.150 = **165 mV**.
2. **"within 5.5 % of our theoretical expectation (155.7 mV)"** (L53, L726). Against 145 mV the deviation is −6.9 %; against 165 mV it is +5.9 %; against 164.1 mV it is +5.4 %. Also the abstract's "observed V_oc gain" is a simulation compared with an analytic formula fed the *same* J₀, so it confirms nothing.
3. **"~8.6 mV addition from improved R_sh"** (L727–728). Full-model decomposition (C2): J₀ +155.6 mV, R_sh **+1.3 mV**, EQE change **+7.3 mV**. The residual comes from the assumed EQE, not R_sh.
4. **Stale J_sc values.** "concurrent J_sc enhancement from 7.201 to 8.695 mA/cm²" (L562) appears nowhere else; Table 4 has 6.293 → 7.610.
5. **AM1.5G doped V_oc is quoted three ways:** 1.320 V (L558), 1.315 V (Table 4, Conclusion), 1.316 V (Fig. 8).
6. **Control AM1.5G values differ between Table 4 and Figure 8:**

   | Quantity | Table 4 | Figure 8 |
   |---|---|---|
   | PCE | 5.69 % | 5.67 % |
   | J_sc | 6.293 mA cm⁻² | 6.283 mA cm⁻² |
   | FF | 0.787 | 78.55 % |

   Doped FF is 0.816 in Table 4 and 81.5 % in Figure 8.
7. **f_useful.** "AM1.5G (20.6 %)" and "incandescent (4.06 %)" (L716–717) vs Table 3: 24.52 % and 4.05 %. The ASTM G173 recomputation confirms 24.52 %.
8. **"~60 mV per decade"** (L721) contradicts the paper's own 89.3 mV/dec for n = 1.5 (L558). 60 mV/dec implies n ≈ 1.0.
9. **J₀ digits.** The equation images use 7.941×10⁻¹⁶ and 1.431×10⁻¹⁷; Table 2 uses 7.939×10⁻¹⁶ and 1.430×10⁻¹⁷.
10. **"irreducible ~1.8 % Lower Bound"** (L691) is simply 1/55.5. Under the paper's own linear partition J₀ = J₀,bulk + J₀,int·(N_it/10¹³), the bulk part is 0.81 % of the control J₀ and 45 % of the doped J₀. So the doped device is **not** "bulk-limited" (L538).
11. **"two-order-of-magnitude recovery of both shunt and recombination resistances"** (L1073). R_rec rises 55.5× (1.74 decades).
12. **Shunt dominance list.** The shunt current at 0.5 V (82.6 µA cm⁻²) exceeds J_sc for LED, MH, halogen **and CFL** (68.35 µA cm⁻²). CFL is omitted at L736.
13. **"≤3.4 % of J_sc".** 0.83 µA cm⁻² divided by the **control** halogen J_sc gives 3.43 %. Against doped J_sc the maximum is 2.84 %.
14. **Introduction irradiance.** "200 to 1000 lux, corresponding to approximately 10 to 100 µW/cm²" (L76–78) and "200 lux … ≈ 1 µW/cm²" (L99–100) contradict the paper's own LED LER: 200 lx = 62 µW cm⁻² and 1000 lx = 312 µW cm⁻².
15. **Work functions.** CsPbBr₃ φ = 5.357 eV and Co₃O₄ φ = 5.05 eV (Table 1) cannot be reproduced from Table 1. The calculated values are 5.476 and 5.431 eV. 5.357 eV would need N_A ≈ 1×10¹⁴ cm⁻³.
16. **Figure 7 vs Table 4.** The undoped dashed J–V curves reach J = 0 at about 0.175 V (LED), 0.34 V (CFL), 0.10 V (MH and halogen) and 0.87 V (INC). Table 4 gives 0.232, 0.414, 0.157, 0.146 and 0.938 V. The figure was generated with different parameters.

## M9. Illumination spectra and the P_in denominator are not on a common basis (major)

- **Location:** §2.7 (L566–600); Table 3; Figure 3b; L652–658.
- **Evidence from the script, sections I–J:**
  - **AM1.5G row is correct.** J_sc,max = 8.954 mA cm⁻², f_use = 24.52 %, ⟨E_ph⟩ = 2.740 eV and LER = 109.5 lm/W all match Table 3.
  - **INC LER = 5.94 lm/W is implausible.** It is below the full-spectrum (0.2–30 µm) LER of a 2400 K blackbody (6.2 lm/W) and about ⅓ of a 2856 K blackbody (16.4 lm/W).
  - **Halogen implies a truncated window.** LER = 121 lm/W with f_use = 10.73 % matches a ~2700 K blackbody integrated only over **350–800 nm** (132 lm/W, 10.9 %). So halogen and INC use different integration windows or normalisations.
  - **The INC curve in Figure 3b is not a thermal spectrum.** It is near zero from 550 to 700 nm, with a bump near 470 nm and a rise only above 700 nm.
  - **">85 % of their energy radiates as near-infrared (λ > 800 nm)"** (L654–656) is true only for full-range integration (85.7 % at 2856 K over 300–2500 nm). That is not the window the halogen numbers imply.
  - **The LED is a cool-white type.** The paper's f_use = 45.89 % matches only CIE LED-B5 (6598 K, 46.8 %); LED-B1 to B4 give 19.5–39 %. With a warm-white LED, J_sc,max and the indoor PCE would be substantially lower.
  - **"LED and CFL concentrate the bulk of their emission below 539 nm"** (L484) is contradicted by f_use < 50 % for both.
- **Fix:**
  - Give LSPDD lamp IDs, CCT and the spectral range for every source.
  - Integrate every spectrum over the same window, preferably its full measured range. State whether P_in includes IR.
  - Recompute the halogen and INC rows, and replace the INC spectrum with a verified one.
  - Add a warm-white (2700–3000 K) LED case.

## M10. Plausibility, limits and benchmarking (major)

- **No physical limit is exceeded.** The detailed-balance limit at E_g = 2.30 eV is **16.5 %** under AM1.5G and **13.0–30.8 %** under CIE LED-B1 to B5 at 1000 lx. The simulated 8.16 % (AM1.5G) and 13.62 % (cool-white LED) are below these, roughly 45–50 % of the limit.
- **But those numbers are set by the assumed EQE (0.85), J₀, n and R_s, not predicted.**
- **J₀ is phenomenological.** It is about 3×10¹⁸ times the radiative J₀ and comes with n = 1.5. R_s = 10 Ω cm² costs about 73 mV (~6.5 %) at the AM1.5G maximum-power point. Neither value is justified or cited.
- **Benchmark claims are overstated.**
  - "Within the competitive range of the best-reported CsPbBr₃ solar cells" (L1084): 8.16 % (simulated) is below the experimental 10.45–11.23 % in the paper's own Table 4.
  - "Slight improvement … beyond their simulated limit" (Patel) compares two different simulations with different assumptions.
  - "First systematic indoor performance metrics for CsPbBr₃ solar cells" (L842–845) needs a literature search. Simulated indoor CsPbBr₃ studies exist in the SCAPS literature, so the claim should be removed or softened **[NEEDS CITATION]**.
- **Literature row check.** Tong et al. [34] is listed with J_sc = 10.83 mA cm⁻². That is **21 % above** the absorbable limit for E_g = 2.30 eV (8.95 mA cm⁻², the paper's own Table 3). Verify against the source; it may be a transcription error. Teng et al. [36]: 8.20 × 1.71 × 0.81 = 11.36 %, against the listed 11.23 %.
- **Fix:** Add a short "limits" paragraph (SQ under each spectrum), justify or vary n, R_s and EQE, and soften the benchmarking language.

## M11. Citation integrity (major)

Details are in Section 5. In summary:

- refs. [31]–[33] are cited for validation they do not provide;
- [21] (MAPbI₃) is used for a CsPbBr₃ Tauc constant;
- [12] cites only the Supporting Information;
- [36] is attributed to "Zhang et al." but the first author is Teng;
- [8] has a stray "[1]" and concerns GeSnO₂/GeO₂ on GeSn, not SnO₂ ETLs;
- [11] (K-salt interface engineering) is cited for the RbCl/CsPbBr₃ result, which belongs to Xie et al.;
- **Table 1 has no citations** despite "Material properties from literature";
- CIE 015:2018 is cited in the text but not in the reference list;
- the opening IoT paragraph on "security frameworks to mitigate escalating cyber risks" (L68–71) is off-topic.

## M12. "Flexible" device claims are not supported by any analysis (major)

The ITO-PET substrate, graphene paper (20 µm in Figure 1) and Figure 1b bending mechanics play no role in the calculation:

- no strain, radius, cycling or mechanical model;
- no optical model for ITO/PET transmission or parasitic absorption (EQE is fixed);
- no temperature or humidity effects.

**Fix:** Either remove "flexible" from title, abstract and conclusions (keep it as an application note), or add at least a bending-strain estimate and an optical transfer-matrix calculation for the ITO-PET stack.

## M13. Reproducibility and statements required by journals (major for submission)

Missing items:

- model and code description and code availability;
- data availability statement;
- CRediT author contributions;
- funding statement (the grant is only in the acknowledgements);
- Highlights and graphical abstract (Elsevier journals);
- ORCID iDs;
- disclosure of the related DFT manuscript.

There are two generative-AI headings (L1112, empty, and L1121). "Deep seek" should be "DeepSeek".

---

# 2. Minor issues

**Language and typos**

- "sets sets" (L404).
- "billion in 2024.This" (L68).
- "the logarithmic regime where. In the logarithmic regime" (L720).
- "Given an illuminance of E_v = 1000 lux is the illuminance" (L577).
- "The LER values range from LER varies widely" (L579).
- "For the theoretical maximum short-circuit current density is then:" (L587).
- "In contrast of outdoor situation" (L732).
- "shows and that" (L887).
- Duplicated sentence "where the standard Einstein relation applies. meaning …" (L434–435).
- "Upon the simulation conditions" (L611).
- "Our SiO2-based ETL" (L821), which is unclear and probably wrong.
- "c-TiO₂ evaporation" (L820) vs "c-SnO₂ evaporation" in Table 4 for the same ref. [35].
- "DPPP" (text) vs "DPP" (table).
- "remains" should be "remain" (L433).

**Superscripts and units**

- "CsPbBr^3^" (L38) should be CsPbBr₃.
- "6.05×103 … 6.05×105" (L46, L533) need superscripts.
- "1.8 × 105 cm⁻¹" (L458) needs a superscript.
- "Ω.cm²" should be "Ω cm²" or "Ω·cm²" throughout.
- "cm²/V.s" should be "cm² V⁻¹ s⁻¹".
- "(E_g = 2.30)" is missing "eV" (L593).
- "~10¹¹" has no units (L120); see Section 5 on [7].
- "~10¹³ cm⁻² eV⁻¹" (an energy density, D_it) vs N_it in cm⁻²: unit conflation.
- "I_shunt" is used for a current density; use J_sh.
- "J0" vs "J₀" vs "J~0~"; "Pr^3^⁺" vs "Pr³⁺".
- "V(O)" should be "V_O" (Kröger–Vink V_O••).
- "Pr³⁺: SnO₂" has a stray space; use Pr³⁺:SnO₂.

**Symbol clash.** η is the reduced Fermi level (§2.3) and also PCE (L912, L934, Figs. 7–8). Use PCE or η_PCE.

**Significant figures.** Mixed precision, e.g. "0.06835" vs "0.0825" mA cm⁻², and 0.713 vs 1.29 vs 5.69 %. Use 3 significant figures consistently.

**Tone.** "rigorously", "profound", "transformative", "catastrophic", "massive", "perfectly bracket", "exceptional". Delete; editors read these as overclaiming.

**Section numbering**

- "1. Results and Discussion" (L607; Word auto-list) should be "3".
- "Interfacial Passivation Physics …" is unnumbered (should be 3.2).
- "4.3.1" (L814) should be 3.3.1.
- The EIS section is unnumbered (3.4).
- Heading levels are inconsistent (§2.1 and §2.4 at level 1, §2.2 at level 2, §2.3 bold text).

**Abbreviations**

- "HID" (L201) is never used again; the sources are "MH".
- Define LER, LSPDD, CFL, MH and INC at first use in the abstract or introduction.

**Wrong figure reference.** "mirrors the spectral overlap … shown in Figure 7" (L917–918): the spectral overlap is Figure 3.

**Leftover text.** "Two table :" at the end of the document (L1328).

**Equation objects.** These are MathType OLE/WMF objects. Make sure the journal accepts them, or convert to native Word equations; pandoc and some production systems lose them.

**Keywords.** Add "shunt resistance", "equivalent-circuit modelling" and "LSPDD"; remove "Pr³⁺ doping" if the chemistry is reframed.

---

# 3. Numerical re-check table

"Recomputed" values come from `verify_numbers.py`; the section letter is in brackets.

| # | Claim (location) | Recomputed | Status |
|---|---|---|---|
| 1 | R_sh 6.05e3 → 6.05e5, 100× (Abstract L46) | 100.0× [A] | Arithmetic OK; **by construction** (Eq. 1) |
| 2 | J₀ ratio 55.5 (L45) | 7.939e-16/1.430e-17 = 55.52; 7.941e-16/1.431e-17 = 55.49 [A] | OK; digits inconsistent between table and equations |
| 3 | V_oc gain 883 mV LED (L49) | 0.883 V [A] | OK |
| 4 | 19.1-fold PCE LED (L49–50) | 13.62/0.713 = 19.10 [A] | OK (but set by β = 1, see F3) |
| 5 | 1.43-fold AM1.5G (L1082) | 1.434 [A] | OK |
| 6 | ΔV_oc,theory = n kT/q ln(55.5) = 155.7 mV (L726) | 155.76 mV [B] | OK |
| 7 | "145 mV (1.315 vs 1.150 V)" (L724–725) | 165 mV [B] | **Error** |
| 8 | "within 5.5 %" (L53, L726) | 145: −6.9 %; 164.1: +5.4 %; 165: +5.9 % [B] | **Inconsistent / tautological** |
| 9 | "~8.6 mV from improved R_sh" (L727–728) | R_sh +1.3 mV; EQE +7.3 mV [C2] | **Misattributed** |
| 10 | Full-model ΔV_oc 164.1 mV (L560) | 164.2 mV [C2] | OK |
| 11 | n V_T ln10 = 89.3 mV/dec (L557–558) | 89.3 mV/dec [B] | OK |
| 12 | "~60 mV per decade" (L721) | 89.3 for n = 1.5 (60 implies n = 1.01) [B] | **Error** |
| 13 | AM1.5G→LED drop 1.320→1.115 V (L558–559) | Predicted 198 mV; table 200 mV [B] | OK; 1.320 vs 1.315 inconsistent |
| 14 | J_sc 7.201→8.695 mA cm⁻² (L562) | Not in any table (6.293→7.610) | **Error (stale)** |
| 15 | η = 3.03 from n = 10¹⁹, N_C = 2.2×10¹⁸ (L415) | 3.031 with F_1/2 = n/N_C [D] | OK; Eq. 7 as printed (N_C/n) gives −1.44 |
| 16 | 78.3 meV above CBM (L179, Table 2) | 3.03 × 25.852 = 78.33 meV [D] | OK |
| 17 | F_1/2(3.03)/F_−1/2(3.03) = 4.543/1.864 = 2.44 (L422–423) | 4.5433/1.8642 = 2.437 (Γ-normalised); 4.026/3.304 = 1.22 unnormalised [D] | OK only with normalisation stated |
| 18 | Diffusion length ×2.44 (L424–425) | √2.44 = 1.562 [D] | **Error** (Eq. 9 and L506 correct) |
| 19 | "Fermi level lies within ~3 k_BT of the band edge" (L180) | It lies 3.03 k_BT inside the band [D] | Wording |
| 20 | φ_ETL = 4.422 eV (Table 1) | 4.4217 eV [E] | OK |
| 21 | φ_CsPbBr₃ = 5.357 eV (Table 1) | 5.476 eV (N_A = 10¹⁶); 5.357 needs N_A ≈ 1×10¹⁴ [E] | **Not reproducible** |
| 22 | φ_Co₃O₄ = 5.05 eV (Table 1) | 5.431 eV [E] | **Not reproducible** |
| 23 | λ_g = 539 / 539.06 nm | 539.06 nm [A] | OK |
| 24 | S_n = 10⁵ → 10³ cm s⁻¹ (L196) | σv_thN_it = 1e5 / 1e3 [A] | OK (reuses bulk σ) |
| 25 | P_in = 1000 lx/LER (Table 3) | All match; INC 16.835 vs 16.846 [H] | OK |
| 26 | f_use and Φ_useful (Table 3) | All internally consistent [H] | OK |
| 27 | f_useful AM1.5G = 20.6 % (L716) | 24.52 % (Table 3 and ASTM G173) [H, I] | **Error (text)** |
| 28 | J_sc,max AM1.5G = 8.953 mA cm⁻² | 8.954 mA cm⁻² (ASTM G173) [I] | OK |
| 29 | LER AM1.5G = 109.45 lm/W; ⟨E⟩ = 2.739 eV | 109.5 lm/W; 2.740 eV [I] | OK |
| 30 | INC LER = 5.94 lm/W | BB 2856 K: 16.4 (full), 156 (380–780 nm); BB 2400 K full: 6.2 [J] | **Implausible / inconsistent basis** |
| 31 | Halogen LER 121.11, f_use 10.73 % | ≈ 2700 K BB truncated at 350–800 nm (132, 10.9 %) [J] | Implies truncated window |
| 32 | ">85 % energy at λ > 800 nm" (L654–656) | 85.7 % (2856 K, 300–2500 nm); 0 % within a 350–800 nm window [J] | Conditional |
| 33 | LED f_use = 45.89 % | CIE LED-B1…B5: 19.5–46.8 % [I] | Cool-white only; **state lamp** |
| 34 | 200–1000 lx ≈ 10–100 µW cm⁻² (L76–78) | 62–312 µW cm⁻² (paper's own LED LER) [H] | **Error** |
| 35 | 200 lx ≈ 1 µW cm⁻² (L99–100) | ≈ 62 µW cm⁻² [H] | **Error (~60×)** |
| 36 | Table 4 PCE = J_scV_ocFF/P_in | All 12 rows consistent [C] | OK |
| 37 | Table 4 from "self-consistent" model | All 12 rows reproduced by Eq. 14 alone [C] | **Lumped model** |
| 38 | Control indoor V_oc | = J_sc·R_sh: 0.232/0.414/0.157/0.146 V [C] | Pure resistor |
| 39 | J_sh(0.5 V) = 82.6 µA cm⁻² exceeds J_sc for LED, MH, halogen (L735–736) | 82.6; also exceeds CFL (68.35) [C4] | Incomplete |
| 40 | Doped J_sh 0.83 µA cm⁻² (≤ 3.4 % of J_sc) (L744) | 0.826; max 2.84 % of doped J_sc; 3.43 % only vs control J_sc [C4] | Minor error |
| 41 | "V/R_sh ≤ 2.6 % of J_sc" (L550) | At V_oc: control 3.02 %, doped 0.029 % [C4] | Unclear basis |
| 42 | PCE gain 11.1–29.2× (L864) | 11.1 (CFL) … 29.3 (halogen) [M] | OK (rounding) |
| 43 | V_oc recovery up to 951 mV (halogen) (L863) | 0.951 V [M] | OK |
| 44 | INC 0.29 → 1.29 %, +4.4× (L867–868) | 4.42× [M] | OK |
| 45 | Figure 8: control 5.67 % / 6.283 / 78.55 %; doped 1.316 V / 81.5 % | Table 4: 5.69 / 6.293 / 0.787; 1.315 / 0.816 [M] | **Inconsistent** |
| 46 | "21 % J_sc increase" (L937) | 21.1 % [M] | OK, but entirely from assumed EQE |
| 47 | R_rec = nV_T/J₀ at V_dc = 0 (Eq. 21) vs Table 5 | 4.88e13 / 2.71e15 vs 308 / 17,109 Ω cm² [F] | **Error (~10¹¹)** |
| 48 | R_rec ratio 55.5× "independent confirmation" | 55.55 [F] | Tautological |
| 49 | τ_EIS = 54.6 / 402 µs; f₂ = 2917 / 396 Hz | 54.5 / 402.1 µs; 2919 / 396 Hz [F] | OK |
| 50 | f₁/f₂ = 3.3 → 92 "in the Bode phase plot" | 3.3 / 92.1 from −Z″ peaks; phase maxima at 33.5 kHz / 9.6 kHz [F] | Misleading |
| 51 | C₁ = ε₀ε_r/d (ETL) = 175 nF cm⁻² | 174.6 nF cm⁻²; absorber C_g = 11.5 nF cm⁻² [F] | Arithmetic OK; **physically wrong layer** |
| 52 | C_μ 7.5-fold reduction "consistent with" 100× N_it | 7.53× [F] | Inconsistent physics |
| 53 | "irreducible ~1.8 %" bulk floor (L691) | 1/55.5; bulk share of doped J₀ = 45 % [G] | **Misinterpreted** |
| 54 | "two-order-of-magnitude recovery of … recombination resistance" (L1073) | 55.5× = 1.74 decades | Overstated |
| 55 | α(470 nm) = 1.8×10⁵ cm⁻¹ with A_Tauc = 6.7×10¹¹ | 1.48×10¹¹ cm⁻¹ [K] | **Error** |
| 56 | Eq. 12 J_sc = qG(L_n+L_p) | 93 mA cm⁻² (L_n = 3.6 µm, L_p = 1.6 µm ≫ 500 nm) [N] | **Not applicable** |
| 57 | J₀ derivable from N_it, S_n | n = 2 SRH ≈ 4e-18; n = 1 interface ≈ 1e-32 A cm⁻² [O] | Not derivable; assumed |
| 58 | Tong [34] J_sc = 10.83 mA cm⁻² | 1.21 × J_sc,max(2.30 eV) [L] | **Check source** |
| 59 | Teng [36] 8.20 × 1.71 × 0.81 → 11.23 % | 11.36 % [L] | Minor |
| 60 | SQ limits | AM1.5G 16.5 %; CIE LED-B 13.0–30.8 % [I] | No limit exceeded (if cool LED) |
| 61 | IoT +14 % (L66–68) | 21.1/18.5 = +14.1 % [A] | OK (off-topic paragraph) |
| 62 | > 300-fold contrast (L674) | 100/0.3119 = 321 [A] | OK |
| 63 | EQE control = 0.704 | AM1.5G 6.293/8.953 = 0.7029; indoor 0.7040 [C] | Minor |

---

# 4. Figure, table and equation checklist

## Figures

| Fig. | Status | Issues | Fix |
|---|---|---|---|
| 1 | Caption present | Caption says "(a) 3D device structure, (b) layer structure and bending mechanics", but panel (a) is the 2D layer stack and (b) is bending plus 3D. "ETO" label should be ITO. "C(20 µm)" for graphene paper is unexplained. Bending is drawn but never analysed. | Fix caption order and labels; drop the bending panel or add analysis |
| 2 | Caption in floating text box (dropped by pandoc and many production systems) | Stack order contradicts §2.1/Fig. 1 (ITO-PET next to HTL, graphene next to ETL). LUMO/HOMO used for inorganic semiconductors (use CBM/VBM). "Pr³⁺:SnO" typo. CBM −3.3 vs χ = 3.35 eV. Decorative orbitals. Caption repeats the Pr passivation chemistry (F4). | Redraw as a clean band diagram with correct contacts; inline caption |
| 3 | Caption present | (b) normalisation basis not stated. INC curve not thermal-like (F/M9). Window 350–800 nm differs from the integration range. Lamp IDs/CCT missing. Coloured background lowers contrast. | Add lamp IDs/CCT and range; verify INC; white background |
| 4 | Number is a Word field that renders as "Figure ." in exports | Mixed sig figs; control CFL shown as "1.29" (1.295) identical to doped INC "1.29"; no sensitivity bars | Convert fields to text before submission; 3 s.f.; add β-sensitivity bars |
| 5 | Caption present | (b) "experimental shunt-resistance values" is false. Undoped marker at ≈1.16 V sits on the J ≈ 7 mA cm⁻² contour of a map computed with **doped** J₀/J_sc (that map gives V_oc ≈ 1.31 V at R_sh = 6.05×10³). | Remove "experimental"; compute a separate map per device or mark only the doped device |
| 6 | Caption in text box | "experimental device values"; "J₀ fixed from AM1.5G fit" (fit to what?); control V_oc markers placed on doped-parameter maps; "V_oc drop to floor" unclear | As above |
| 7 | Caption in text box | Undoped dashed curves do not reach the Table 4 V_oc (M8 item 16); non-round y-ticks (43, 86, 128 …); inset halogen V_oc 1.096 vs 1.097; "η" used for PCE; floating "MPP (Undoped)" labels | Regenerate from the Table 4 parameter set; round ticks |
| 8 | Caption "Figure8" | Inset values differ from Table 4 (5.67 vs 5.69 %, 6.283 vs 6.293, 78.55 vs 78.7 %, 1.316 vs 1.315 V, 81.5 vs 81.6 %); panel (a) missing x-axis label | Regenerate; one set of numbers |
| 9 | Caption in text box | "low forward bias" (caption) vs "V_dc = 0 V" (Table 5); legend "N_t = 10¹³" has no units and uses the bulk symbol (should be N_it, cm⁻²); inset "55.5× smaller scale" (axes differ ~40×); doped Nyquist shows one arc, not "clearly resolved semicircles"; phase plot cannot show f₁/f₂ = 92 | Re-plot −Z″ vs f; fix legend, units and bias; or delete with the EIS section |

## Tables

| Table | Issues | Fix |
|---|---|---|
| 1 | "Material properties from literature" but **no citations**. N_D = 10¹⁹ attributed to Pr (F4). φ for CsPbBr₃ and Co₃O₄ not reproducible. α(470) vs Tauc constant inconsistent. Bulk N_t in ETL/HTL not used by the single-diode model. Formatting ("Brad", "cm²/V.s"). | Add a "Ref." column; fix φ; state which parameters actually enter the calculation |
| 2 | N_it without energy distribution or σ; S_n uses bulk σ; EQE, J₀ and R_sh are inputs but not labelled as such; "Surf-recomb-velocity" | Add a "Source / assumption" column |
| 3 | INC row questionable (M9); lamp IDs/CCT missing | Add lamp ID, CCT, integration range |
| 4 | In the Word file the caption is correctly placed; the misplacement in the extraction ("Table 4" caption under Table 1, L288) is a pandoc artefact. Problems: experimental literature rows and simulated "this work" rows mixed without a "Simulated" label; Tong J_sc > J_sc,max; Li row "c-SnO₂" vs text "c-TiO₂"; Patel "4.97, 8.08" (experimental and simulated in one cell); DPP vs DPPP; mixed sig figs | Split into Table 4a (literature, experimental) and 4b (this work, simulated); verify every literature row against the source |
| 5 | R_rec inconsistent with Eq. 21; "extracted" values are assumed; C₁ assigned to a conducting ETL; unit formatting inconsistent ("10 Ω.cm²" vs "10 (Ω.cm²)") | Recompute or delete (F5) |

## Equations

- Eq. 1: an assumption that needs justification or a citation (F3).
- Eqs. 2–5, 8, 10, 14–21: form acceptable.
- Eq. 6: sign error.
- Eq. 7: inverted.
- F_−1/2: undefined.
- η_p: wrong sign.
- Eq. 11: constant wrong.
- Eq. 12: not applicable.
- Eq. 13: plain text.
- Eq. 9: sits inside a heading.
- Cross-references to Eqs. (1)–(5), (6), (11), (13) and (19) are wrong (table in F6).

---

# 5. Reference checklist

- **Count and order.** 41 references, all cited, in order of first appearance ([1]–[37], then [34]–[37] re-cited, then [38]–[41]). Numbering is self-consistent.
- **Style.** Mostly IEEE, but with inconsistencies:
  - full journal names vs abbreviations ("Journal of Physical Chemistry C" vs "J. Phys. Chem. C");
  - some entries lack volume, issue or pages ([21], [22], [31], [33], [41]);
  - two use a Zotero web-style format ([22] "Oct. 15, 2015, *American Chemical Society*"; [41] "May 28, 2011. doi: …" with no journal);
  - [8] begins with a stray "[1]";
  - [35] has "CsPbBr ~3~".
- **Verification limits.** Crossref was blocked in this environment. Items marked "web-verified" were confirmed by search-engine metadata; all others need a DOI check by the author before submission.

| Ref. | Used for | Problem | Action |
|---|---|---|---|
| [1] IoT Analytics 2025 (web) | IoT growth; 39 billion by 2030 | Grey literature; surrounding paragraph on "security frameworks" is off-topic | Keep one sentence on device counts; delete the security text; verify the "39 billion by 2030" figure is in [1] |
| [2] Pecunia et al., Adv. Energy Mater. 2021 | Indoor irradiance | Issue number "no. 20" not verified | Verify issue and article number |
| [3] Zhang et al., iScience 2021 | Indoor irradiance | Authors and article number not verified | Verify |
| [4] Righini & Enrichi (book chapter) | c-Si indoor | Fine | — |
| [5] Reich et al., SOLMAT 2009; [6] Reynaud et al., SOLMAT 2019 | Low-light c-Si | Fine | — |
| [7] Tan et al., ACS AMI 2024 (CsPbBr₃ single-crystal films) | "trap densities as low as ~10¹¹" | Single-crystal trap densities are usually *volumetric* (cm⁻³); the text compares them with *areal* interface densities (cm⁻²) | Check units; do not mix cm⁻³ and cm⁻² |
| [8] Gupta et al., ACS AMI 2016 | "interface trap densities up to 10¹³ … at tin-oxide interfaces" | Stray "[1]"; concerns GeSnO₂/GeO₂ on GeSn (MOS), not SnO₂/perovskite | Replace with a perovskite/SnO₂ interface source **[NEEDS CITATION]** |
| [9] Trani et al., PRB 2008 | V_O formation energy 3.42 eV; surface states | Value not verified here | Check the 3.42 eV value and conditions (O-rich/poor) in [9] |
| [10] Wang et al., Small 2024 | SnO₂ defects increase recombination | Fine | — |
| [11] Adam et al., ACS AMI 2025 (K-salt) | RbCl/SnO₂ CsPbBr₃ 7.88 → 10.04 % | Mismatch: these numbers are Xie et al. | Cite [11] only for K-salt passivation |
| [12] Xie et al., "Supporting Information …", 2021 | Same | Cites the SI only, without journal or DOI | **Web-verified replacement:** G. Xie *et al.*, "Alkali chloride doped SnO₂ electron-transporting layer for boosting charge transfer and passivating defects in all-inorganic CsPbBr₃ perovskite solar cells," *J. Mater. Chem. A*, vol. 9, pp. 15003–15011, 2021, doi: 10.1039/D1TA02672K (author to confirm DOI on the RSC page) |
| [13] Thorat et al., JPCC 2014; [14] Kiisk et al., Mater. Chem. Phys. 2018 | Eu-doped oxides; Nb codoping | Relevant, but support the *opposite* of the Pr premise (trivalent → more V_O) | Keep and discuss honestly (F4) |
| [15] Ullah et al., Mater. Adv. 2021 (CsPbBr₃ review) | Cited at the end of the Eu/Nb sentence | Mismatch | Move to the CsPbBr₃ introduction sentence |
| [16] Sze, Li & Ng, 4th ed. 2021; [24] Sze & Ng, 3rd ed. 2006 | Poisson; Newton–Raphson | Two editions of the same book | Keep the 4th edition only; cite a numerical-methods source for Newton–Raphson if needed |
| [17] Basore, IEEE TED 1990 (PC-1D) | DD system | Acceptable historical citation; a perovskite DD reference would be better **[NEEDS CITATION]** | — |
| [18] Sze & Lee, 2012; [19] Marshak & Assaf, Solid-State Electron. 1973 | Generalised Einstein relation [18]; standard relation [19] | Apparently swapped: [19] is titled "A generalized Einstein relation for semiconductors" | Cite [19] for the generalised relation |
| [20] Karmokov et al., "Appl. Phys." 2025 (Prikladnaya Fizika) | G(x) integral | Weak source for a textbook equation | Replace with [16] or a textbook |
| [21] Shahivandi, Results Phys. 2025 (MAPbI₃) | CsPbBr₃ Tauc constant | **Wrong material** | Use a CsPbBr₃ absorption source **[NEEDS CITATION]** |
| [22] Hodes & Kamat, JPCL 2015 | Diffusion length | Incomplete format | Add vol. 6, pages (verify) |
| [23] Sherkar et al., ACS Energy Lett. 2017 | "J_sc determined by weighted spectral photon flux" | Mismatch: the paper is about recombination at grain boundaries and interfaces | Cite for interface recombination instead |
| [25] Ghani et al., Renew. Energy 2014 | Numerical single-diode solution | Fine | — |
| [26] LSPDD website | Lamp spectra | Fine; give lamp IDs | — |
| [27] Aktary et al., RSC Adv. 2022 (DFT of CsPbX₃) | J_sc,max equation | Mismatch | Replace with a detailed-balance or indoor-PV methods source **[NEEDS CITATION]** |
| [28] Borah et al., Solar Energy 2023 | Methodology extended | Fine | — |
| [29] Zhang et al., Commun. Chem. 2024 | E_g of CsPbBr₃ | "Art. no. 1265" equals the DOI suffix (…01265-5); probably not the article number. Pressure study, a weak source for ambient E_g. | Verify article number; use an ambient-pressure E_g source |
| [30] Caicedo-Dávila et al., JPCC 2020 | Hot-carrier thermalisation | Weak match | Replace or remove |
| [31] Lei et al., Small 2024 (Pd-doped Cs₂AgBiBr₆); [32] Otmani et al., J. Ovonic Res. 2025; [33] Ullah et al., Chem. Eng. Sci. 2026 (Pr-doped Cs₂AgBiBr₆) | "TRPL and EIS measurements validate that this Pr³⁺-based passivation strategy" | **Misused:** none concerns Pr:SnO₂ ETLs; [31] is Pd, not Pr | Remove the validation claim; cite [33] only as absorber-side Pr doping |
| [34] Tong et al., Nano Energy 2019 (web-verified: title, journal, vol. 65, 104015) | 10.91 % benchmark | Table J_sc = 10.83 mA cm⁻² exceeds the E_g = 2.30 eV limit | Re-extract J_sc, V_oc, FF from the paper |
| [35] Li et al., ACS AMI 2019 (web-verified: title, journal, year) | 10.45 % | Text says "c-TiO₂", table says "c-SnO₂"; "8.16 % (Our SiO2-based ETL) for their reference device" is garbled | Re-read the source and correct |
| [36] Teng et al., J. Mater. Chem. A 2025, 13, 21493–21500 (web-verified) | 11.23 %, V_oc 1.707 V | Text attributes it to "**Zhang** et al."; additive family is diphenylphosphines (DPP), optimal 1,3-bis(diphenylphosphino)propane (DPPP) | Change to "Teng et al."; harmonise DPP/DPPP |
| [37] Patel et al., ACS AEM 2026 | Experimental 4.97 % / simulated 8.08 % | Not verified | Verify |
| [38] Sun et al., J. Solid State Chem. 2022 | Pr in triple-cation absorber | Fine | — |
| [39] Guerrero et al., JPCC 2016; [40] Bisquert, PCCP 2003; [41] Fabregat-Santiago et al., PCCP 2011 | EIS models | [39] month ("May") likely wrong; [41] missing journal, volume, pages | Complete the metadata |
| — | CIE 015:2018 (K_m = 683 lm/W) | Cited in text, absent from the list | Add as a reference |
| — | Table 1 parameters (ε_r, χ, N_C, N_V, μ, B_rad, Auger, σ, Co₃O₄ set) | **Uncited** | Cite each, e.g. a SCAPS parameter source for SnO₂ and CsPbBr₃ **[NEEDS CITATION]** |
| — | Companion DFT manuscript | Not cited although the title invokes DFT | Cite as "submitted" or a preprint and disclose to the editor |

---

# 6. Cross-paper consistency with the DFT companion

The companion is *"Oxygen-Vacancy Energetics and Dopant-Induced Holes in Pr- and Rb-Substituted Anatase TiO₂: A DFT+U Comparison"* (manuscript v4, this repository).

| Point | Device paper | DFT companion | Consequence and fix |
|---|---|---|---|
| Host oxide | SnO₂ ETL (rutile-type) | Anatase TiO₂ | DFT numbers cannot parameterise a SnO₂ device. Either (a) present the TiO₂ results only as a qualitative analogue, or (b) switch the device ETL to compact TiO₂ (common in CsPbBr₃ cells) so both papers share a host, or (c) compute Pr/Rb in SnO₂. |
| Effect of Pr on V_O | "Pr³⁺ passivates oxygen vacancies", N_it 10¹³ → 10¹¹ cm⁻² | V_O formation energy **falls** from +4.74 eV (pristine) to **+1.29 eV** (Pr): Pr makes V_O *easier* to form | **Direct contradiction.** Pr can at most "passivate" in the sense of forming electronically benign Pr–V_O complexes, which the device paper must argue explicitly and which implies *more* vacancies, not fewer. |
| Electron count | "Pr³⁺ at Sn⁴⁺ sites supply an excess electron" (L355–356); N_D = 10¹⁹ from Pr | "one hole per Pr³⁺"; "one vacancy over-compensates Pr" | Contradiction. The only route to net donors in the companion is Pr–V_O pairing, which needs [V_O] ≥ [Pr]. Rewrite per F4. |
| Rb | Introduction praises RbCl-doped SnO₂ for V_O passivation (Xie et al.) | Rb substitution gives E_form(V_O) = **−4.06 eV** (spontaneous V_O) with residual holes | Not strictly contradictory (RbCl in Xie et al. acts mainly at the surface, with Cl⁻ filling V_O), but the device paper must distinguish surface passivation from lattice substitution. |
| "DFT" in device title | Title 2 claims ML-enhanced DFT | DFT is in the companion only; no ML in either | Remove "DFT" and "ML" from the device title, or add a genuine DFT section on SnO₂ |
| Machine learning | Both titles | None | Remove from both papers unless ML is actually performed |
| Terminology | "V(O)", "oxygen vacancy induced trap states" | V_O, Kröger–Vink | Harmonise notation (V_O, Pr′_Sn / Pr′_Ti) |
| Duplicate-publication risk | — | — | Disclose the companion in both cover letters; cite each other as "submitted". Make sure no figure or text is reused without attribution. |
| Logical link | Device N_it (10¹³ → 10¹¹) chosen ad hoc | DFT gives formation energies, not N_it | If linked, state explicitly that formation energies do not determine N_it without a defect-concentration model (chemical potentials, temperature, Fermi-level self-consistency). Do not claim that the device N_it values "come from DFT". |

---

# 7. Journal recommendations

Quartiles change yearly and by category; confirm in JCR/Scopus at submission.

| Journal | Scope fit | Realistic? |
|---|---|---|
| **Solar Energy** (Elsevier) | Publishes device-simulation and indoor-PV modelling papers, including multi-spectrum and SCAPS-type studies. Borah et al. [28], which this work extends, appeared here. | **Most realistic** after route A plus the minimum sensitivity analysis, ideally with SCAPS-1D cross-validation. |
| **Solar Energy Materials & Solar Cells** | Device physics and materials for PV; accepts modelling with clear physical insight. | Realistic only after route B (DD validation, corrected chemistry, sensitivity analysis). Simulation-only papers with assumed parameters are frequently desk-rejected. |
| **Solar RRL** (Wiley) | Rapid research letters and full papers on emerging PV, including indoor PV; strong preference for experiments or high-insight modelling. | Possible only with route B plus some experimental anchoring (e.g., measured R_sh/J₀ of SnO₂-based CsPbBr₃ cells from the authors' lab or open data). |
| **ACS Applied Energy Materials** | Materials-centric; expects synthesis and characterisation. | Not suitable unless Pr:SnO₂ films/devices are fabricated and characterised (XPS, PL/TRPL, EIS, J–V). |
| Progress in Photovoltaics; Nano Energy | High bar on novelty and experimental validation | **Not realistic** for this work in any simulation-only form. |

**Candid assessment.** In its current form the manuscript would very likely be **desk-rejected** at all of the above. The editor would see: title claims not delivered; methods claims contradicted by the results; circular central result; chemistry error; "experimental" EIS with no experiment.

**Minimum additions to be competitive:**

1. Remove ML/DFT/"discovery" from the title, or actually perform them. Fix the Pr chemistry (F4).
2. Validate with a drift-diffusion solver (SCAPS-1D or equivalent), using an explicit interface-defect layer. Extract J₀, n and R_sh from the drift-diffusion J–V instead of assuming them (F2).
3. Make R_sh an independent variable. Give PCE(R_sh, J₀) maps and the minimum-R_sh design rule per spectrum. Run the β-sensitivity analysis for any N_it→R_sh link (F3).
4. Put all spectra on a common P_in basis with lamp IDs. Add a warm-white LED (M9).
5. Correct the EIS section or delete it (F5). Correct all equations (F6) and numbers (M8).
6. Add an SQ/detailed-balance limit paragraph per spectrum and soften the benchmarking (M10).
7. Release code and data. Add data availability, CRediT, Highlights and graphical abstract (M13).
8. Ideally, add experimental anchoring: even literature J–V data of SnO₂/CsPbBr₃ cells fitted with the model, or measured R_sh distributions, would greatly strengthen the paper.

---

# 8. Prioritised action plan for the author

Legend:

- **T** = text-only fix that Claude can draft now.
- **S** = new or redone simulation the author must run.
- **E** = experiment or data the author must supply.
- **A** = author decision.

| Priority | Action | Type | Notes |
|---|---|---|---|
| 1 | Choose route A (equivalent-circuit sensitivity paper) or route B (DD-validated paper) | A | Determines everything below |
| 2 | One title; remove ML/DFT/"Discovery"/"Rigid"; rewrite the abstract to match the content (F1) | T | Suggested titles and abstract text in F1/F3 |
| 3 | Rewrite the Pr defect chemistry (acceptor; V_O compensation); detach N_D = 10¹⁹ from Pr; reconcile with the DFT companion (F4, §6) | T (+A) | Replacement paragraph in F4 |
| 4 | Remove "self-consistent Poisson/DD" claims (route A), or implement and report the DD solution with implementation details (route B) (F2) | T / **S** | Route B: SCAPS-1D with Table 1, interface defect layer, mesh/BC/convergence statement |
| 5 | R_sh as an independent variable: PCE(R_sh, J₀) maps per spectrum; β = 0–1 sensitivity; minimum-R_sh design rule (F3) | **S** (light) | Can be produced with the existing MATLAB single-diode code; the script here already gives the LED numbers |
| 6 | EIS: delete, or recompute R_rec from Eq. 21 at a stated bias with R_sh in parallel; absorber C_g; remove "experimental/independent/validate"; drop [31]–[33] validation claim (F5) | T + **S** | |
| 7 | Fix equations: Eq. 6 sign, Eq. 7 ratio, F_j normalisation, 2.44 → 1.56 for L, η_p sign, A_Tauc, delete Eq. 12, Eq. 13 typesetting, all cross-refs (F6) | T | Exact corrected forms in F6 |
| 8 | Fix band-offset wording (cliff), collection contact, stack order; redraw Figure 2 (M7) | T + figure | |
| 9 | Fix every inconsistent number (M8; Section 3 rows 7–14, 18, 21–22, 27, 34–35, 39–41, 45, 47, 53–55) | T (+ **S** for φ and Fig. 7) | Fig. 7 and Fig. 8 must be regenerated from the Table 4 parameter set |
| 10 | Spectra: lamp IDs, CCT, common integration window; recompute halogen/INC; verify the INC SPD; add a warm-white LED (M9) | **S** | |
| 11 | Justify or vary n = 1.5, R_s = 10 Ω cm², EQE 0.85/0.704; add an SQ limit paragraph; soften benchmarks; re-extract literature rows (Tong J_sc) (M10) | **S** + T | |
| 12 | References: replace [12] with the main Xie et al. article; "Teng et al." for [36]; remove or retarget [8], [15], [20], [21], [23], [27], [29], [30], [31]–[33]; cite Table 1 sources; add CIE 015:2018; harmonise IEEE format (M11, §5) | T (+A for new sources) | Do not add sources without reading them |
| 13 | Delete the IoT security text; tone down hype words; fix typos, superscripts, units, section numbering, symbol clash (§2) | T | |
| 14 | Inline all figure captions (no text boxes); fix figure-specific issues (§4) | T + figures | |
| 15 | Add code/data availability, CRediT, funding statement, Highlights, graphical abstract; merge the duplicate AI declarations; disclose the companion paper (M13) | T (+A) | |
| 16 | (Route B, strongly recommended) Experimental anchoring: J–V/EIS of SnO₂ vs rare-earth-modified SnO₂ CsPbBr₃ cells, or fit of published J–V data | **E** | Needed for Solar RRL/SOLMAT competitiveness |

**What Claude can deliver immediately on request:** items 2, 3, 7, 8 (text), 9 (text parts), 12 (formatting and flagged removals), 13, 14 (captions), 15 (templates), plus the β-sensitivity tables from `verify_numbers.py` (item 5) ready to insert.

**What needs the author:** the route decision, any drift-diffusion run, lamp IDs and spectra, verification of literature values against PDFs, new references, and any experiment.

---

*Files in this folder:*

- `Device_Manuscript_Audit.md` / `.docx` — this report.
- `verify_numbers.py` — all recomputations.
- `verify_numbers_output.txt` — script output used for every number quoted above.
