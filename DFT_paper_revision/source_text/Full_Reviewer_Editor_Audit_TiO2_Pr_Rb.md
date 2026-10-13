Prepared for the authors \| 15 September 2026

Manuscript reviewed: Ghadimimehr_DFT_TiO2_PrRb_FINAL.docx. The submitted title begins "Aliovalency over Ionic Radius" and proposes design rules for trap-free electron-transport layers in indoor photovoltaics.

Overall recommendation: Do not submit this version. The reviewer recommends substantial scientific revision, including targeted recalculation. The independent editor recommends rejection in its present form, with consideration of a substantially rebuilt submission. These are advisory assessments, not an actual journal decision.

The potentially useful result is a same-host comparison of vacancy energetics in Pr- and Rb-substituted anatase. However, the interpretation relative to pristine TiO₂, the Pr electronic model, the spin-state assignments and the claimed validation are not sufficiently secure to support the title or device conclusions. Several figures preserve an earlier, incompatible interpretation.

# 1 Scope and evidence standard

This audit covers the complete supplied manuscript, its two tables, all five embedded figures, the abstract and conclusions, methods, numerical consistency, scientific interpretation, reproducibility, reference use and editorial presentation. A separate agent performed an independent editorial reading; its judgment and proposed restructuring are included in Section 7. The main reviewer inspected the embedded artwork and checked selected technical claims against primary documentation and research sources.

No Quantum ESPRESSO inputs, output logs, UPF files, density grids, plotting data or Supporting Information spreadsheet were supplied. The audit therefore evaluates reported results and their internal consistency; it does not reproduce the DFT calculations or certify their numerical validity. The spreadsheet mentioned as "Section 15" is unavailable for this audit, not demonstrated to be nonexistent. A full bibliographic metadata or plagiarism certification is outside the evidence available.

Locations use the manuscript's section numbers and figure or table numbers. Paragraph identifiers P1--P158 refer to one-based top-level Word paragraph order, including blank paragraphs, and are provided for precise retrieval. Reference numbers \[1\]--\[56\] are the manuscript's references; external audit sources use A1--A7 in Section 10.

  -----------------------------------------------------------------------------------------------------------------
  **Priority**   **Meaning**                                              **Required action**
  -------------- -------------------------------------------------------- -----------------------------------------
  Critical       Could change the main conclusion or the physical model   Resolve before submission

  Major          Prevents reliable interpretation or reproduction         Supply evidence or narrow the claim

  Minor          Presentation or traceability issue                       Correct after scientific reconciliation
  -----------------------------------------------------------------------------------------------------------------

# 2 Decision summary

  -------------------------------------------------------------------------------------------------------------------------
  **Area**                **Assessment**                    **Principal reason**
  ----------------------- --------------------------------- ---------------------------------------------------------------
  Research question       Potentially useful                Common-host Pr--Rb comparison may add a bounded benchmark

  Novelty claim           Overstated                        Two changing dopants do not isolate valence from radius

  Thermodynamics          Interpretation needs correction   Pr also lowers vacancy cost relative to pristine

  Electronic model        Critical verification needed      Frozen-core Pr 4f treatment conflicts with proposed mechanism

  Electronic states       Not established as claimed        Spin, occupations, O-site U and PDOS need reconciliation

  Numerical reliability   Incomplete                        Loose force criterion and incomplete convergence cycles

  Figures and reporting   Not submission ready              Stale baseline and incompatible carrier labels

  Device conclusions      Unsupported by this model         No interface, capture-rate or device calculations
  -------------------------------------------------------------------------------------------------------------------------

Strengths worth retaining are the explicit chemical reference, pristine comparison, same-host computational setup, attempts to explore localization and alternative vacancy sites, and disclosure of limitations and author roles. A large reported energy separation is worth investigating. None of these strengths removes the need to verify the calculation records.

# 3 Detailed scientific reviewer comments

## R01 Pr does not suppress vacancies relative to the reported pristine baseline

Critical \| Abstract; §§1, 3.2, 3.4, 3.5 and 4; Table 2; Figure 3

Finding. Table 1 reports 4.74 eV for pristine, 1.29 eV for Pr and −4.06 eV for Rb. Thus Pr lowers the stated neutral-vacancy cost by 3.45 eV; Rb lowers it by 8.80 eV. The text repeatedly turns the positive Pr value into a claim of vacancy suppression and improved ETL behavior.

Scientific consequence. A positive reaction energy at the selected oxygen reference means that this reaction is uphill. It does not mean that Pr raises the cost relative to pristine. With other factors equal, a lower formation free energy favors a higher equilibrium defect population. Actual populations additionally depend on charge state, chemical potentials, temperature, degeneracy and compensation \[A3\].

Required response. Replace every relative suppression claim. State that both substitutions lower the reported vacancy cost, with Pr remaining uphill at the chosen reference. If suppression relative to pristine is the intended scientific result, new, relevant evidence is required; copyediting cannot recover that conclusion from Table 1.

## R02 The named Pr pseudopotential cannot establish the proposed 4f mechanism

Critical \| §2 P19; §1 P13; §3.4 P51 and P55; conclusion P88

Finding. The named file is Pr.pbe-spdn-kjpaw_psl.1.0.0. PSlibrary documents its lanthanide spdn family as trivalent with 4f electrons frozen in the core \[A2\]. Yet the manuscript attributes compensation to Pr-4f hybridization and invokes accessible Pr³⁺/Pr⁴⁺ redox behavior.

Scientific consequence. Frozen-core 4f electrons are not variational valence states in that calculation. Their hybridization or changing occupation cannot be demonstrated by the reported model. A zero valence-spin result also does not establish that a real Pr³⁺ ion, normally associated with an f² configuration, is a fully closed-shell ion. The exact UPF bytes used remain uninspected.

Required response. Provide the UPF file, hash, valence configuration and core treatment. If the standard frozen-4f file was used, remove claims of computed 4f hybridization and Pr redox accommodation. To retain that mechanism, perform validated calculations with explicit Pr-4f valence states, appropriate correlation treatment and an assessment of spin--orbit effects. This is the highest-priority model check before expensive additional tests.

## R03 The design confounds radius with valence and chemistry

Critical \| Title; §1 P16--P17; §§3.2 and 3.4; §4

Finding. Pr and Rb differ in radius, formal valence, orbital structure, bonding and accessible charge states. Their quoted six-coordinate radii are 0.99 and 1.52 Å, versus 0.605 Å for Ti. Both being oversized does not hold the size variable constant.

Scientific consequence. The 5.35 eV contrast is not a decomposition into electronic and strain contributions. The statement that this difference is larger than any plausible strain contribution has no reported strain calculation behind it. The comparison can support an interpretation consistent with charge compensation, but cannot establish that size is unimportant or causally isolated.

Required response. Narrow the title and conclusion to a two-dopant comparison. Alternatively add a controlled series of dopants, matched-valence or approximately matched-radius controls, and clearly defined fixed-geometry versus relaxed energetic comparisons. Report local bond lengths, coordination changes and relaxation energies before attributing the effect quantitatively.

## R04 Zero magnetization is being overinterpreted as a physical singlet ground state

Critical \| §2 P21; §3.3 P41--P47; §3.6 P63; Table 2

Finding. The initial calculations use zero starting magnetization on every species. The reported nonmagnetic Pr-vacancy solution is compared with one magnetic trial 0.281 eV higher. Quantum ESPRESSO documentation warns that zero initialization can retain a nonmagnetic solution; values 0.3 and 0.5 in starting_magnetization are interpreted per valence electron, not as literal 0.3 and 0.5 μB site moments in this input range \[A1\].

Scientific consequence. One trial does not establish the global minimum across spin, orbital occupations and localized states. Zero net spin can also arise from fractional occupations or cancellation. Table 2 calls the excited state a triplet, whereas the prose reports approximately 1 μB, so the multiplicity is not established. The charge series remaining nonmagnetic at every Pr charge state requires an occupation audit.

Required response. Report total and absolute magnetization separately, electron counts, occupations, smearing type and width, spin constraints, symmetry settings and restart provenance. Try site-specific Ti and O seeds, opposing-spin configurations and local distortions with independent starts. Use "lowest-energy solution among those tested" and "nonmagnetic solution" until a stronger assignment is supported.

## R05 Charge bookkeeping and the Pr carrier count are inconsistent

Critical \| §§3.3, 3.4 and 3.9; P46--P55 and P74

Finding. The formal Pr³⁺ substitution introduces one hole relative to Ti⁴⁺; an oxygen vacancy can supply two electrons. The resulting Pr--vacancy complex therefore has one net excess electron under this bookkeeping, as §3.9 itself states. Earlier passages attribute two delocalized conduction electrons to the same complex. Rb substitution introduces three holes, leaving one after a single vacancy compensates two.

Scientific consequence. Hybridization does not remove the requirement to account for electron number. Electron localization on Ti³⁺ is not by itself positive compensation of an acceptor dopant. A neutral supercell and a formally doubly positive vacancy center plus its electrons are different descriptions; the manuscript mixes them. An odd-electron, integer-occupied collinear cell cannot simply be called a closed-shell singlet, although a smeared metallic calculation can have zero net spin.

Required response. Add an explicit electron and effective-charge ledger for each composition and charge state. Distinguish formal oxidation states, supercell charge q, electron and hole populations, and integrated spin. Use the actual UPF valence counts, not inferred donation alone. Explain any fractional occupancy rather than labeling it closed-shell chemistry. Correct the two-electron versus one-electron interpretation throughout.

## R06 The oxygen Hubbard test changes the Pr interpretation

Critical \| §3.3 P45; §3.9 P73--P74; §4.1

Finding. Pr_perfect changes from nonmagnetic in Ti-only +U to a localized one-hole state near 1 μB with U(O-2p) = 5.5 eV. The manuscript nevertheless treats this as confirmation of a generally closed-shell, trap-free Pr picture. A corresponding dual-U Pr_VO result is not actually reported in §3.9.

Scientific consequence. This is model sensitivity of a central observable. The assertion that defect energies are much less sensitive than localization is not demonstrated by the reported tests. U transferred from Cr₂O₃ is a sensitivity parameter, not automatically a calibrated anatase value.

Required response. Calculate both parent and vacancy cells consistently for both dopants with the selected O-site U treatment and compare full vacancy formation cycles. Test or justify the O-site U value. State explicitly that the Pr parent localization is method dependent. Do not use the parent-only result to certify the unreported dual-U Pr-vacancy state.

## R07 Raw Fermi energies do not establish band alignment or clean transport

Critical \| §3.3 P46--P49; §3.8 P71; §3.9 P74; §4 P87

Finding. The manuscript subtracts raw Fermi energies from chemically different periodic calculations and interprets 2.10 and 2.86 eV differences as physical carrier shifts. It also interprets a pristine HSE Fermi-energy change as evidence of gap widening. No common electrostatic or band-edge alignment is described.

Scientific consequence. Energy zeros and the reported Fermi position, especially in gapped or smeared systems, are not a substitute for aligned VBM and CBM values. A Fermi-energy difference alone is not a band-gap difference. The Pr value in Figure 5 is 10.31 eV, compared with 9.99 eV in the text; differing meshes may explain this, but must be identified.

Required response. Report band edges and occupations within each cell and establish a common alignment if comparing different cells. Give actual band gaps for the HSE comparison. Remove claims of quantitative transport, trap pinning and Burstein--Moss shifts based solely on unaligned output values. The numerical differences can remain as calculation diagnostics with their limitations stated.

## R08 Trap identity and recombination activity are not proved by the current plots

Critical \| §3.3; §3.5; Figure 5; Table 2

Finding. The text identifies an oxygen-hole polaron, while Figures 1, 4 and 5 retain Ti³⁺ trap labels. Figure 5's inset contains both Ti and O weight; assigning an electron or hole requires orbital occupations and spin-resolved localization, not a label placed on a peak. Pr-d weight is called negligible in one section and the conduction carrier is called Pr-5d-derived in another.

Scientific consequence. Net magnetic moment does not identify the atom or orbital carrying the spin. Lack of a resolved peak in a broadened projection does not establish absence of all traps. A spin-polarized defect state is not automatically a deep, efficient SRH recombination center.

Required response. Provide site-resolved O-2p and Ti-3d projections, Pr projections appropriate to the pseudopotential, integrated occupations, total DOS, and real-space spin or defect-state density. Report DOS broadening, band count and energy resolution. Reconcile the charge sign and carrier assignment before regenerating figures. Reserve recombination claims for suitable transition-level and capture evidence.

## R09 The force tolerance is loose for the precision claimed

Major \| §2 P22; §3.1; Figure 2

Finding. The stated threshold 0.005 Ry/Bohr equals approximately 0.129 eV/Å. The four listed final forces are approximately 0.067, 0.108, 0.095 and 0.103 eV/Å. Pr_VO was manually stopped. Figure 2 additionally labels 0.01 Ry/Bohr as a literature standard without an identified source.

Scientific consequence. Tight electronic self-consistency is not proof of a well-relaxed ionic geometry. Negligible energy change during stalled BFGS iterations does not demonstrate that further minimization is unnecessary. These residual forces can affect bond distortions, localization and small energy differences.

Required response. Perform tighter relaxations, for example initially targeting about 0.01--0.02 eV/Å and testing whether the relevant energy and localization results stabilize. This is a practical target, not a universal acceptance standard. Report final forces and energy changes against the production geometries. Remove unsupported "literature standard" and "numerically unnecessary" claims.

## R10 Convergence must be tested for the full energetic cycle

Major \| §2 P19--P20; §3.7; §4.1

Finding. Γ-to-3×3×2 differences are 1.05--1.16 eV per cell, or 22--25 meV/atom. The \<1.5 meV/atom result refers to 2×2×1 versus 3×3×2, but §4.1 assigns it to Γ-only. The text incorrectly describes vacancy energy terms as equal-size, same-composition cells. It later reports useful 2×2×2 formation energies of 1.19 and −4.20 eV.

Scientific consequence. Convergence of selected absolute energies per atom is not convergence of a defect reaction. The supplied 2×2×2 values suggest the Pr--Rb difference changes by only 0.04 eV, but the parent-cell energy records needed to verify them are absent. A 40 Ry cutoff is not validated merely by belonging to a PAW file family.

Required response. Publish all parent and defect terms at each tested mesh and cutoff, with the O₂ reference where needed. Resolve completed-versus-planned statements. Test representative tighter-cutoff and larger-cell cases. Use a stated tolerance on the target defect energy or energy difference rather than an unsupported "chemical accuracy" claim based on meV/atom.

## R11 Formation energies require a defined thermodynamic scope

Major \| §2 P23--P25; §3.2; §4 P91

Finding. The neutral reaction uses one half of an isolated O₂ total energy. No oxygen chemical-potential range, finite-temperature gas correction or competing-phase stability region is given. The negative Rb value is alternately called lattice instability and proof of an inseparable, synthesizable Rb--vacancy complex.

Scientific consequence. The result is a conditional oxygen-removal energy from an already substituted cell. It does not determine Rb incorporation, global phase stability, a kinetic rate or the equilibrium number of vacancies. Negative formation energy signals that the chosen vacancy-free reference favors oxygen removal under the modeled reservoir; it does not identify the final stable phase.

Required response. Label the reference precisely and distinguish the O₂ electronic-energy reference from finite-temperature oxygen thermodynamics. If making synthesis or stability claims, calculate dopant incorporation and competing compensation or phase channels. Provide sequential vacancy energies or a larger neutral complex such as two Rb substitutions with three vacancies to investigate full formal compensation. A full phase diagram is optional only if those claims are removed.

## R12 The HSE check does not validate the dopant contrast

Major \| Abstract; §3.8; §4 P90

Finding. HSE06 was applied only to pristine perfect anatase. Its nonmagnetic character survived, but no doped defect or vacancy formation cycle was computed with HSE. "Single-shot" and "single-point self-consistent" also need a consistent meaning in the methods.

Scientific consequence. The test does not challenge the oxygen-hole, Pr-carrier or neutral-vacancy conclusions. Agreement for an uncomplicated pristine cell cannot be advertised as hybrid-functional validation of chemically distinct defective cells.

Required response. Restrict the statement to a pristine-cell check, or calculate the relevant doped parents and defects using an appropriate hybrid protocol. Report exact-exchange, screening, exchange-grid and convergence settings and whether +U was retained. The printed 0.106 bohr⁻¹ and 0.11 bohr⁻¹ values are close but are not exactly equivalent by unit conversion; identify the actual input.

## R13 The dispersion cancellation argument is incomplete

Major \| §3.10 P76

Finding. D3 contributions of −10.29 and −10.09 eV are given only for Pr_VO and Rb_VO. The manuscript correctly admits that the parent and O₂ calculations are missing, then uses the 0.20 eV defect-only difference to argue robustness of the 5.35 eV vacancy-energy contrast.

Scientific consequence. For the Pr--Rb contrast the oxygen reference cancels, but the parent-cell D3 difference does not. Comparing defective-cell contributions alone cannot supply the correction to the vacancy formation contrast. At fixed geometry, D3 is primarily a geometry-dependent energy correction, so similar Fermi levels are not independent validation of the electronic structure.

Required response. Compute D3 contributions for both perfect substituted cells. For individual formation energies also include the consistent oxygen reference. Report the resulting complete correction, or state that the effect on vacancy energetics remains undetermined. Test structural relaxation under D3 only if claiming geometry robustness.

## R14 Charged cells are a spin diagnostic rather than corrected defect thermodynamics

Major \| §3.6 P61--P64; §4.1 P93

Finding. Raw total energies are reported for q = +1 and +2 without a charge-dependent formation-energy expression or corrected transition levels. The text appropriately avoids interpreting raw energy differences as ionization potentials, but elsewhere calls this a charged-defect formation-energy validation and says the moments are invariant to finite-size effects.

Scientific consequence. An additive image-charge correction does not alter an already computed moment; changing supercell size, background interactions or localization can. The 1.21 μB neutral Rb value is absolute magnetization, not the signed total −0.97 μB stated earlier. The dielectric constant is called static while labeled ε∞, which denotes electronic rather than full static screening.

Required response. Keep this as an explicitly limited charge-state spin test unless corrected thermodynamics are added. Separate total and absolute moments for every charge. For transition levels use a consistent reference, Fermi-level term, alignment and appropriate anisotropic dielectric treatment \[A3\]. Justify ε∞ versus static screening and the correction's q² scaling; do not assign the same generic 0.3--0.6 eV estimate to every charge.

## R15 Bader comparison cannot isolate a single hole across different dopants

Major \| §3.12 P80--P82; §4 P90

Finding. The charge comparison uses Pr_VO as a "carrier-free" reference, although the manuscript elsewhere calls that cell n-type. Pr and Rb differ in nuclear potential, pseudopotential valence and relaxed structure. A difference in Bader electron populations therefore includes chemical polarization as well as any carrier redistribution.

Scientific consequence. Bader charges are not orbital occupations or formal oxidation states. Absence of a full 1 e change on one Ti does not rule out Ti³⁺ character. An oxygen depletion summed across unlike systems cannot by itself prove a one-hole count or assign an 18% Ti-3d contribution. The conclusion also claims four-cell Bader analysis whereas §3.12 explicitly says pristine was not completed.

Required response. Provide full per-atom charges, charge sign convention, sum rules, grid convergence, PAW density reconstruction and spin-density analysis. Use same-composition charge-state or localized-state comparisons where possible, with clear atom mapping. Treat cross-dopant Bader differences as supporting evidence. Reconcile the calculation inventory and remove "unambiguous" orbital claims based only on basin charges.

## R16 Vacancy site sampling is asymmetric and does not establish a binding lower bound

Major \| §3.11 P78

Finding. Three alternative Pr vacancy sites are reported, but two are explicitly symmetry equivalent. The nearest neighbor is not tested, the production-site distance is not stated clearly, and comparable Rb site sampling is absent. Energies increase from 1.29 to 2.07 and 2.72 eV for the selected alternatives.

Scientific consequence. These are selected site-energy differences, not proof of the global minimum. A 0.78 eV difference is not a rigorous lower bound on nearest-neighbor binding when that configuration is absent. Finite periodic distances also complicate a near-versus-far interpretation.

Required response. Provide vacancy indices, coordinates, minimum-image dopant distances, degeneracies and energies for both dopants. Include the nearest-neighbor candidate and distinct far sites or restrict the conclusion to the sampled configurations. Define any binding energy relative to a consistent dissociated reference, and stop calling symmetry-equivalent sites crystallographically distinct.

## R17 Bulk calculations do not demonstrate indoor photovoltaic performance

Critical \| Title; §1; §3.5 P58--P59; Table 2; conclusion P89

Finding. No surface, absorber interface, band-offset calculation, carrier-capture coefficient, device model or photovoltaic measurement is reported. The manuscript nevertheless describes Pr as trap-free, Rb as worse than pristine, and generalizes to other dopants and oxide hosts using \|Δq\| thresholds.

Scientific consequence. Bulk electronic states alone do not establish interfacial recombination, voltage, fill factor or a universal valence threshold. Surface segregation, defect charge, concentration and coordination can change the outcome. Generalization to ZnO also changes the host valence and common coordination environment.

Required response. Keep indoor photovoltaics as motivation and a proposed follow-up application. Remove performance ranking and universal rules unless supported by appropriate interface and device evidence. Broader host and dopant predictions must be labeled hypotheses. A publishable bounded bulk-defect study need not undertake device experiments if its claims are narrowed accordingly.

## R18 Result provenance must be reconciled before the conclusions are trusted

Major \| Entire manuscript; especially P90, P93 and P99

Finding. The manuscript has conflicting accounts of completed k-mesh, PDOS and Bader work, and Figure 3 preserves a deferred pristine calculation despite Table 1 reporting it. Supporting data are promised after acceptance rather than supplied with this audit.

Scientific consequence. These inconsistencies prevent a reader from identifying which outputs generated each number and figure. They do not prove that calculations were fabricated, but they require an explicit record check. Counting related computations as eight orthogonal validations exaggerates the independence of the evidence.

Required response. Create a single calculation manifest and regenerate tables and plots from it. Identify each completed, partial or planned test and the actual claim it supports. Supply reviewer-accessible raw inputs and outputs, structures, density analyses and scripts at submission. Record corrections openly in the response to reviewers.

# 4 Numerical checks and corrected equations

These checks use numbers printed in the DOCX. They check arithmetic and bookkeeping, not the underlying DFT outputs.

  -------------------------------------------------------------------------------------------------------------------------------------
  **Quantity**                 **Recalculated result**               **Audit interpretation**
  ---------------------------- ------------------------------------- ------------------------------------------------------------------
  Pr minus pristine            1.29 − 4.74 = −3.45 eV                Pr lowers the stated vacancy cost

  Rb minus pristine            −4.06 − 4.74 = −8.80 eV               Larger reduction for Rb

  Pr minus Rb                  1.29 − (−4.06) = 5.35 eV              Reported contrast is arithmetically consistent

  Dense-mesh contrast          1.19 − (−4.20) = 5.39 eV              Change is +0.04 eV for new minus old

  Individual mesh shifts       Pr −0.10; Rb −0.14 eV                 Difference is more stable than either individual value

  Pristine energy conversion   −4233.150 Ry ≈ −57594.93984 eV        Consistent with Table 1 defective pristine entry

  Printed Table 1 cycle        Pristine 4.75; Pr 1.29; Rb −4.07 eV   0.01 eV differences may reflect rounding; provide full precision

  Supercell volume             570.247 Å³                            From the reported cell dimensions

  Dopant fraction              1/16 = 6.25% of Ti sites              Concentrated periodic substitution, not a dilute limit

  Vacancy fraction             1/32 = 3.125% of O sites              One vacancy per 570.247 Å³

  Force threshold              0.005 Ry/Bohr = 0.1286 eV/Å           Electronic convergence does not cure residual ionic forces
  -------------------------------------------------------------------------------------------------------------------------------------

## 4 1 Reaction energies

For the fixed neutral substituted parent used in the manuscript, write the oxygen-removal energy as:

Eᶠ_X(V_O⁰; μ_O) = E(X with vacancy, q = 0) − E(X without vacancy, q = 0) + μ_O

Here μ_O = ½E(O₂) + Δμ_O. The manuscript uses Δμ_O = 0 at the electronic-energy reference. Any finite-temperature or chemical-potential extension must be identified explicitly. For charged formation energies, define the reference convention before adding q(E_F + E_VBM + ΔV) and an electrostatic correction; avoid double-counting alignment if the correction scheme already includes it.

Define the comparative quantity as ΔEᶠ = Eᶠ_Pr − Eᶠ_Rb. The D3 change in this contrast requires four cell terms:

δ_D3(ΔEᶠ) = \[D3(Pr_VO) − D3(Pr_perfect)\] − \[D3(Rb_VO) − D3(Rb_perfect)\]

The O₂ term cancels in this comparative quantity only when the same oxygen reference is used. The two missing perfect-cell contributions prevent its reconstruction from the reported D3 results.

## 4 2 Formal carrier accounting

  --------------------------------------------------------------------------------------------------------
  **Composition**   **Substitutional deficit**   **Vacancy contribution**   **Net formal carrier count**
  ----------------- ---------------------------- -------------------------- ------------------------------
  Pr_perfect        1 hole                       None                       1 hole

  Pr_VO             1 hole                       2 electrons                1 excess electron

  Rb_perfect        3 holes                      None                       3 holes

  Rb_VO             3 holes                      2 electrons                1 residual hole
  --------------------------------------------------------------------------------------------------------

This ledger assumes Pr³⁺, Rb⁺, Ti⁴⁺ and O²⁻ bookkeeping. It does not determine where carriers localize or whether Pr changes oxidation state. Removing additional electrons from a charged supercell changes this balance again. Actual electron counts must be obtained from the UPF files and charge settings.

## 4 3 Dilute carrier estimate

Using the manuscript's cell volume gives about 1.75 × 10²¹ vacancies cm⁻³ for one vacancy per cell. At 10⁻³ vacancies per O site, the vacancy density is about 5.61 × 10¹⁹ cm⁻³. Under a zero-temperature, single spherical parabolic band with m\* = m_e, E_F − E_C = ħ²(3π²n)\^(2/3)/(2m\*) gives approximately 0.053 eV for one free electron per vacancy and 0.085 eV for two. These are illustrative reviewer calculations, not new material predictions. They do not reproduce the stated 10--50 meV range without further assumptions and do not validate the unaligned 2.1 eV shift. Compensation, effective mass, valley degeneracy and ionization must be specified.

# 5 Audit of figures tables and consistency

All five embedded figures were inspected directly. The following comments concern the actual artwork as well as the captions.

  ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  **Item**   **Observed problem**                                                                        **Required correction**
  ---------- ------------------------------------------------------------------------------------------- --------------------------------------------------------------------------------------------
  Figure 1   Rb panel says Ti³⁺ hole trap; caption says O-hole polaron                                   Resolve carrier identity and update artwork; include actual vacancy index and distance

  Figure 2   0.01 Ry/Bohr is labeled literature standard; only selected trajectory windows shown         Cite or remove standard; show units in eV/Å and identify selected steps; archive full logs

  Figure 3   Uses \~4.5 eV Janotti literature pristine baseline and says pristine calculation deferred   Rebuild using verified 4.74 eV in-house value; remove unsupported better/worse ETL labels

  Figure 4   Rb annotation says Ti³⁺ trap; title includes updated and workflow identifiers               Align with verified assignment; use total and absolute magnetization labels consistently

  Figure 5   Title and inset say Ti³⁺ trap; text claims O-hole; EF differs from production text          Regenerate with resolved orbital assignment, source run IDs, mesh and broadening

  Table 1    Rounded raw energies do not exactly recover two displayed formation values                  Provide higher-precision energy ledger and make caption agree with Figure 3

  Table 2    Triplet label disagrees with 1 μB trial; device and trap claims are excessive               Replace interpretation rows with reported computational observables and uncertainties
  ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Figure 3 has an additional reference problem: the embedded Janotti et al. citation is absent from the numbered bibliography. The cited Phys. Rev. B 81, 085212 paper studies rutile using HSE, whereas the artwork presents an anatase PBE+U reference. This mismatch is independently confirmed by the publisher abstract \[A5\].

  -------------------------------------------------------------------------------------------------------------------------------------------------------
  **Location pair**     **Contradiction**                                                     **Resolution**
  --------------------- --------------------------------------------------------------------- -----------------------------------------------------------
  §2 vs §3.7            k-mesh tests planned versus completed                                 Use actual output inventory

  §3.7 vs §4.1          Γ error 22--25 versus \<1.5 meV/atom                                  Correct which mesh comparison is described

  §3.4 vs Figure 5      PDOS follow-up planned versus plotted                                 Specify which projections are still missing

  §3.12 vs conclusion   Two-cell versus four-cell Bader analysis                              List only completed cases with files

  §3.3 vs §§3.6--3.7    Rb total −0.97 versus "total" 1.21 μB                                 Separate signed total and absolute integrals

  §3.3 vs Table 2       1 μB trial versus triplet label                                       Verify spin and occupation assignment

  §3.9 vs §3.3          Pr net one excess electron versus two conduction electrons            Use consistent charge ledger

  §3.2 vs §4 P91        Negative energy described as instability and then as no instability   Define reference-state instability versus phase stability
  -------------------------------------------------------------------------------------------------------------------------------------------------------

# 6 Section by section revision map

  ---------------------------------------------------------------------------------------------------------------------------------
  **Section**                   **Editorial action**                                                    **Scientific dependency**
  ----------------------------- ----------------------------------------------------------------------- ---------------------------
  Title and abstract            Replace universal and trap-free claims with a bounded comparison        R01--R08, R17

  Introduction                  Use four focused paragraphs; correct literature consensus and scope     R01--R03, reference audit

  Methods                       Consolidate all completed protocols and calculation IDs                 R02, R04, R09--R14

  3.1 Structure                 Add structural metrics and tighter relaxation evidence                  R03, R09

  3.2 Energetics                Correct pristine comparison and thermodynamic language                  R01, R10--R11

  3.3 Magnetism and PDOS        Reconcile spin, carriers, orbitals and plots                            R04--R08

  3.4 Mechanism                 Replace categorical rule with supported conditional explanation         R02--R06

  3.5 Device implications       Present motivation and testable hypotheses only                         R17

  3.6 Charged series            Label as limited spin diagnostic or add corrected thermodynamics        R14

  3.7 Convergence               Show full energy cycles and correct mesh comparisons                    R10

  3.8 HSE                       Limit to pristine check or calculate relevant defects                   R12

  3.9 Dual Hubbard              Make changed Pr localization a central result                           R06

  3.10 D3                       Supply missing parent terms or withdraw contrast validation             R13

  3.11 Site tests               Report distinct sites and compare both dopants                          R16

  3.12 Bader                    Use qualified interpretation and full numerical record                  R15

  Conclusions and limitations   Shorten; put limitations before final conclusion; reconcile inventory   All critical issues

  Data and references           Make supporting evidence accessible and correct claim attribution       R18; Section 9
  ---------------------------------------------------------------------------------------------------------------------------------

# 7 Independent editor assessment

The editor agent read the full manuscript independently of the main reviewer's scientific analysis. Its assessment was subsequently checked against the main reviewer's figure findings. The following is the consolidated editorial position; repeated technical details are cross-referenced rather than duplicated.

## 7 1 Editorial decision and rationale

Recommendation: Reject the present version and invite a substantially rebuilt submission if the computational record supports a narrower conclusion. The problems exceed language revision. The central comparator is misinterpreted, the experiment does not isolate radius from aliovalency, and contradictory validation claims obscure the evidence base. A specialist computational-materials manuscript could remain viable after model verification and scope reduction. Acceptance or minor revision is not justified by the supplied document.

The editor identifies three essential revisions: correct the scientific proposition, establish one traceable account of what was calculated, and rewrite the manuscript around evidence rather than the number of cross-checks. A journal-specific decision cannot be predicted because no target journal was supplied.

## 7 2 Recommended title and structure

Suggested title: Oxygen Vacancy Energetics and Hole Localization in Pr and Rb Substituted Anatase TiO₂

Suggested subtitle if useful: A DFT+U comparison

The title remains conditional on resolving the carrier assignment. If localization cannot be verified, retain only the energetics component.

Structure the introduction as motivation, relevant TiO₂ evidence, the unresolved common-host comparison, and the bounded study objective. Condense the extended historical defense of DFT+U. Place all completed methods in one section. Organize results as structural and numerical validation, vacancy energetics, method-dependent electronic structure, and selected sensitivity tests. Put limitations and application hypotheses before a short final conclusion. Move routine trajectories and detailed job logs to Supporting Information while retaining evidence essential to the main conclusions.

## 7 3 Proposed replacement passages

These passages use reported values and are suitable only after the authors verify the underlying calculations. They are proposed edits, not claims that this audit has rerun the study.

Numerical interpretation. Using a common oxygen reference, the calculated neutral oxygen-vacancy formation energies are 4.74 eV in pristine anatase, 1.29 eV in Pr-substituted anatase and −4.06 eV in Rb-substituted anatase. Both substitutions therefore lower the vacancy formation cost relative to pristine TiO₂, with a larger reduction for Rb.

Mechanistic scope. The contrast is consistent with different charge-compensation requirements, although the two-dopant comparison does not independently separate valence, local strain and dopant-specific bonding contributions.

Pr localization. Pr-substituted anatase without a vacancy is nonmagnetic in the Ti-only Hubbard treatment but develops a localized hole when an O-2p correction is added. Its predicted localization therefore depends on the treatment of oxygen correlation.

Spin comparison. The nonmagnetic Pr--vacancy solution was lower in energy than the tested magnetic initialization by 0.281 eV. This comparison establishes the ordering of the tested solutions; further spin and occupation searches are needed to identify the lowest-energy state reliably.

Hybrid check. An HSE06 calculation on pristine anatase preserved its nonmagnetic state. Hybrid-functional verification of the doped defects remains outstanding.

Dispersion check. D3 single-point energies were calculated for the two defective cells. Because the corresponding substituted parent-cell energies were not calculated, the effect of dispersion on the vacancy formation-energy contrast remains undetermined.

Application scope. These bulk calculations motivate further assessment of dopant-dependent defect states at TiO₂/absorber interfaces. They do not establish carrier recombination rates or photovoltaic performance.

## 7 4 Language and presentation corrections

Use "nonmagnetic solution" where only zero spin has been shown. Reserve "closed-shell singlet," "ground state," "trap-free," "unambiguous," "independent validation" and "thermodynamically required" for claims the evidence actually establishes. Use a consistent V_O notation and distinguish total from absolute magnetization at first use. In prose, replace raw job names with readable system descriptions; retain job identifiers in the data manifest.

Remove preparation language such as "autonomous post-processing sequence," "submission window," "defence," "shift-of-the-shift" and "NEW finding" in artwork. Remove the slogan at the end of the conclusions. Correct "OLED solar cells": OLEDs are light-emitting devices, not a solar-cell class. Avoid repeating the design-rule claim in the introduction, every results subsection and the conclusions. Replace "three crystallographically distinct" with "three selected" when two sites are symmetry equivalent.

# 8 Required evidence and practical revision sequence

## 8 1 Minimum calculation and data package

  ----------------------------------------------------------------------------------------------------------------------------------------------------------------
  **Record**               **Minimum contents**                                                              **Purpose**
  ------------------------ --------------------------------------------------------------------------------- -----------------------------------------------------
  Run manifest             System, geometry, charge, method, U, mesh, cutoff, spin seed, completion status   Defines exactly what was calculated

  Pseudopotentials         Actual UPF files, hashes, core and valence definitions                            Resolves Pr 4f and electron counts

  Energy ledger            Full precision total energies and all reaction terms                              Reconstructs Tables 1 and 2 and dense-mesh contrast

  Convergence record       Final forces, electronic and ionic exit status, mesh and cutoff changes           Tests quantitative reliability

  Spin and occupations     Total and absolute spin, electron counts, smearing, local projections             Resolves carrier and spin assignments

  Geometries               Parent and defect coordinates, site indices, local distances                      Makes site comparison reproducible

  Density analysis         DOS data, spin densities, Bader tables, grid and PAW settings                     Checks localization claims

  Figure provenance        Scripts and exact source run IDs for Figures 1--5                                 Prevents obsolete plots and labels

  Supporting Information   Accessible indexed package, including cited spreadsheet Section 15                Allows substantive external peer review
  ----------------------------------------------------------------------------------------------------------------------------------------------------------------

## 8 2 Revision order

First, freeze the current manuscript and reconcile the run inventory, UPF model and electron counts. Correct the pristine comparison immediately. These steps determine which scientific questions the existing calculations can answer.

Second, resolve the Pr model, spin initialization and occupation treatment. Then perform tighter representative relaxations and converge complete vacancy-energy cycles. Only after that should additional dual-U or hybrid calculations be interpreted as validation. Repeating expensive calculations with an unresolved electronic model would not address the main problem.

Third, compare site-dependent energetics and carrier localization consistently. Complete missing D3 parent terms if dispersion robustness remains part of the paper. Perform corrected charged-defect thermodynamics only if equilibrium charge-state or transition-level claims are retained.

Fourth, rebuild every table and figure from the verified ledger. Rewrite the abstract and conclusion last. Keep application language proportional to the bulk evidence. Independently cross-check all citations and make the supporting package accessible before external review.

## 8 3 What can be fixed by editing and what requires evidence

  ----------------------------------------------------------------------------------------------------------------------------------------------------
  **Editing now**                            **Reanalysis of existing outputs**       **New calculations if claims retained**
  ------------------------------------------ ---------------------------------------- ----------------------------------------------------------------
  Correct Pr versus pristine wording         Electron and occupation audit            Pr model with explicit 4f if asserting 4f mechanism

  Remove universal and device claims         Rebuild spin and energy tables           Tighter relaxations and complete convergence cycles

  Fix citation numbering and stale artwork   Identify completed Bader and PDOS runs   Consistent dual-U parent and vacancy calculations

  Restrict HSE and D3 descriptions           Trace all plotted points to run IDs      Hybrid doped-defect checks if claiming hybrid validation

  Define thermodynamic reference             Verify figure and table rounding         Interfaces and capture evidence if claiming device improvement
  ----------------------------------------------------------------------------------------------------------------------------------------------------

An issue is closed when the author response identifies the correction, its location and the supporting file or new result. For each R01--R18, record "accepted," "resolved by new evidence," or "claim withdrawn," followed by a concise justification. No result should be invented to complete a response table.

# 9 Reference and citation audit

All 56 numbered bibliography entries are cited at least once in the manuscript text. This numbering check does not establish relevance or accuracy. The audit below covers the complete reference list at the level of visible titles and citation use, with targeted external checks for decisive claims. Items without an external check are explicitly left unverified. The Janotti citation inside Figure 3 is an additional unnumbered item.

## 9 1 Confirmed or directly identifiable attribution problems

In §3.2, Arrigoni and Madsen are cited as \[16\], but their entry is \[18\]. In §3.6, \[37\] and \[33\] are described as experimental and theoretical K/Rb-doped TiO₂ studies even though their listed subjects are alkali-doped Cr₂O₃ and trivalent-doped rutile, respectively. In the introduction, \[35\] and \[36\] are used within an alkali-doping consensus but concern pulsed-discharge oxygen control and Mo doping. These are substantive claim-support mismatches.

The accessible publisher abstract of Tian et al. \[14\] supports a qualitative reduction of vacancy formation energy through Rb doping and strain in a photochromic system. It does not directly validate the exact −4.06 eV value or establish worse photovoltaic performance \[A4\]. The Iwaszuk--Nolan paper \[33\] reports vacancy compensation for trivalent dopants, so it should not be recruited into a blanket vacancy-free, closed-shell trivalent consensus \[A6\].

## 9 2 Full bibliography coverage ledger

  ---------------------------------------------------------------------------------------------------------------------------
  **Ref**   **Subject in supplied bibliography**   **Audit disposition**
  --------- -------------------------------------- --------------------------------------------------------------------------
  1         Indoor photovoltaics                   Relevant motivation; check specific low-flux loss assertions

  2         CsPbBr₃ film efficiency                Does not by itself establish superiority to Si under indoor spectra

  3         TiO₂ and SnO₂ dye cells                Supports that application; not every listed device class

  4         OLED electron transport                Distinguish OLEDs from photovoltaic cells

  5         Benzene photodegradation               Photocatalysis context; not direct ETL capture evidence

  6         CO₂ photoreduction review              Background source; not direct proof of universal trap behavior

  7         Anatase surface vacancies              Check exact U and projector transfer; surface is not bulk

  8         Photothermal water splitting           Contextual evidence; narrow the claim to studied system

  9         Anatase vacancy superstructures        Relevant defects; not alone a device-loss benchmark

  10        Anatase localized carriers             Relevant carrier context; distinguish surface and bulk

  11        Trapped-electron photocatalysis        Trap activity is application dependent

  12        N-doped TiO₂ dynamics                  Different dopant and observable; qualify extrapolation

  13        Excess-electron review                 Useful context; distinguish electrons and oxygen holes

  14        Rb and strain in TiO₂                  External abstract checked; qualitative trend only

  15        Gd-doped CeO₂                          Different host; not proof of universal closed-shell compensation

  16        TiO₂(B) magnesium storage              Wrong citation for Arrigoni in §3.2; should be \[18\]

  17        Native anatase defects                 Verify actual species, cutoffs and configuration before comparison

  18        Anatase defect methods                 Relevant benchmark; detailed method transfer not externally verified

  19        Rutile vacancy DFT+U                   Not an anatase-specific U validation

  20        Ce-doped zirconium titanate            Different host; qualify mechanism transfer

  21        Er-doped TiO₂                          Verify U value and projector context; not a direct Pr calibration

  22        Gd TiO₂ water splitting                Experimental context; not proof of trap-free Pr ETLs

  23        Ca₂SnO₄ luminescence                   Different host and property; weak support for TiO₂ consensus

  24        Lanthanides in anatase                 Potentially relevant; compare actual 4f model and defects

  25        Pr-doped anatase                       Relevant prior art; verify exact charge-state treatment

  26        Ce-doped anatase vacancies             Check against claim of vacancy-free rare-earth consensus

  27        Pr adsorption on anatase               Surface adsorption cannot directly prove bulk substitution binding

  28        Al in titanate conductors              Different composition; use only explicit mechanistic analogy

  29        Ce anatase defect equilibria           Relevant framework; describe the actual equilibrium channels

  30        Mg-doped rutile surface                Different dopant and geometry; no broad closed-shell conclusion

  31        Nonmetal TiO₂ doping                   Not direct evidence for rare-earth or alkali compensation

  32        Hydrogenated doped TiO₂                Additional chemistry; qualify analogy

  33        Trivalent rutile compensation          External source located; vacancy compensation challenges broad narrative

  34        Alkalis in α-Bi₂O₃                     Relevant analogy; host cation valence differs

  35        Pulsed-discharge Ti oxide              Not alkali-specific evidence as cited

  36        Mo-doped TiO₂                          Not alkali-specific evidence as cited

  37        Alkalis in Cr₂O₃                       Correct host must be stated; transferred U needs justification

  38        Kröger--Vink formalism                 Appropriate bookkeeping source; does not prove an energetic ranking

  39        Quantum ESPRESSO capabilities          Appropriate software citation; not validation of input choices

  40        Quantum ESPRESSO exascale              Appropriate software citation

  41        PBE functional                         Appropriate method citation

  42        PSlibrary website                      Add exact files and hashes; no blanket 40 Ry guarantee

  43        Original LDA+U                         Background; consolidate lengthy method history

  44        Linear-response U                      Appropriate if distinguishing derived and transferred U

  45        NiO methodology                        Background; not material-specific calibration

  46        Dudarev functional                     Appropriate formulation citation; give actual input

  47        Derivative discontinuity               Background; +U does not guarantee all errors are corrected

  48        Original screened hybrid               Method reference; pair with actual HSE06 parameters

  49        Hybrid screening parameter             Relevant HSE06 specification

  50        Hybrid anatase native defects          Relevant comparator; match charge and oxygen conditions

  51        D3 dispersion                          Appropriate method citation; full energy cycle still required

  52        D3 damping                             Appropriate BJ-damping reference

  53        D3 and spin in anatase                 Related precedent; no automatic validation of doped calculations

  54        Bader algorithm                        Algorithm citation; does not validate carrier interpretation

  55        Grid Bader algorithm                   Algorithm citation; grid convergence remains necessary

  56        Cu on TiO₂ CO₂ reduction               Different dopant; chemical analogy is not proof of Pr mechanism
  ---------------------------------------------------------------------------------------------------------------------------

For every retained citation, the authors should verify authors, title, year, journal, pages or article number and DOI against the publisher record, then inspect the specific passage supporting the manuscript claim. Unverified entries above are not alleged to be false. Recentness alone is not a reason to retain a weakly relevant source. Add a primary ionic-radius source specifying coordination and oxidation state if those numerical radii remain central.

# 10 External sources used for targeted checks

Checked on 15 September 2026. These sources support the specific audit checks identified above. The broader findings also rely on direct manuscript comparison, arithmetic and explicitly stated reviewer reasoning. Primary sources were preferred; full-text access was incomplete for several manuscript references.

[A1 Quantum ESPRESSO 7.5 pw.x input documentation](https://www.quantum-espresso.org/Doc/INPUT_PW.html)

Supports the initialization, charge, cutoff and input-parameter checks. It documents the starting_magnetization input convention and cautions about a zero-magnetization start. It also identifies dftd3_version = 4 as BJ damping.

[A2 Andrea Dal Corso PSlibrary source and lanthanide documentation](https://github.com/dalcorso/pslibrary)

Documents the frozen-core 4f treatment in the lanthanide spdn family and the need to inspect individual pseudopotential information. This identifies a conflict with the model described in the manuscript; the authors' actual UPF file still needs verification.

[A3 Kim and colleagues Quick start guide for first principles modelling of point defects in crystalline materials](https://arxiv.org/html/2005.01941v4)

Supports the scope of formation-energy, chemical-potential, charge-neutrality, supercell and charge-correction requirements. The audit does not infer quantitative equilibrium populations from the manuscript's neutral energies.

[A4 Tian and colleagues Rb doping and lattice strain in TiO₂ 2025](https://advanced.onlinelibrary.wiley.com/doi/full/10.1002/adfm.202423514)

Publisher abstract checked. DOI 10.1002/adfm.202423514. Supports a qualitative vacancy-energy trend in a photochromic material; not a validation of the present numerical value or photovoltaic ranking.

[A5 Janotti and colleagues Hybrid functional studies of the oxygen vacancy in TiO₂ 2010](https://journals.aps.org/prb/abstract/10.1103/PhysRevB.81.085212)

Publisher abstract checked. Phys. Rev. B 81, 085212. The studied polymorph is rutile and the method is HSE, contrary to the anatase PBE+U description embedded in Figure 3.

[A6 Iwaszuk and Nolan Charge compensation in trivalent cation doped bulk rutile TiO₂ 2011](https://doi.org/10.1088/0953-8984/23/33/334207)

Bibliographic record and indexed author-manuscript evidence were checked; full text was not available through all access routes. The reported vacancy-compensation result warrants correction of the manuscript's generalized consensus. Author-manuscript location:

[A6 Author manuscript in the University College Cork repository](https://cora.ucc.ie/bitstream/10468/5190/1/4427.pdf)

[A7 Carey and Nolan Alkali doping and oxygen vacancies in chromium oxide 2017](https://pubs.rsc.org/en/content/articlelanding/2017/ta/c7ta00315c/unauth)

Publisher identity and title checked. DOI 10.1039/C7TA00315C. The host is Cr₂O₃. Detailed numerical U transfer and all claimed precedents require author verification from the full paper.

# 11 Final author action statement

Retain the common-host comparison, but rebuild the paper around what the calculations can demonstrate. Resolve the Pr pseudopotential and spin model first, verify complete energetic cycles, correct the pristine comparison, and regenerate the figures. If the 5.35 eV ordering survives these checks, it can support a focused comparative study. Universal trap-free ETL design rules and improved indoor photovoltaic performance are not established by the supplied manuscript.
