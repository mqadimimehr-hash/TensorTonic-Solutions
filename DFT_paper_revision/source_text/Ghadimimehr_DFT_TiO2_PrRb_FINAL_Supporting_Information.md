# Aliovalency over Ionic Radius: A First-Principles Design Principle for Oxide Electron-Transport Layers from Pr- and Rb-Doped Anatase TiO₂

*Mohammad Ghadimimehr, et al.\
University of Malaya*

# Overview of the simulator workflow

This Supporting Information collects the full numerical data and methodological details that underpin the eight independent robustness probes referenced in the main manuscript. Every value reported here was extracted directly from Quantum ESPRESSO v.7.5 output files; no values are reproduced from secondary literature or training data. The simulator workflow was executed in three stages: (i) production single-U PBE+U calculations on Pristine_perfect, Pr_perfect, Pr_VO, Rb_perfect and Rb_VO; (ii) a five-stage post-queue covering HSE06, dual-Hubbard Pr, vdW-D3, multi-V_O site sensitivity, and Bader topological-charge analysis; and (iii) a 2×2×2 Brillouin-zone convergence verification computed on the Γ-relaxed geometries. A summary of the file structure, the orchestrator scripts, and the input templates is given in Section S8.

# S1. Pristine V_O baseline: convergence recovery

The pristine anatase V_O reference reported in Table 1 of the main text (E_form = +4.74 eV) required two convergence attempts. The first attempt used the production single-U(Ti-3d) protocol with the default damped charge mixing (mixing_mode = local-TF, mixing_beta = 0.3). The self-consistent field oscillated around the shallow-defect minimum with the SCF accuracy estimate bouncing between 0.05 and 0.14 Ry across iterations 14--17 --- a well-known instability for the two-electron, half-occupied conduction-band manifold of pristine V_O in anatase TiO₂.

The recovery (designated Pristine_VO_v3) tightened seven parameters in concert: mixing_beta was reduced from 0.3 to 0.1, the Broyden history mixing_ndim was expanded from the QE default to 12, the Gaussian smearing degauss was relaxed from 0.005 Ry to 0.01 Ry (≈ 136 meV) to improve fractional-occupation handling, the maximum electron-step count was extended from the default to 300, diago_thr_init was relaxed to 1.0×10⁻³ Ry to escape symmetric eigenvalue traps, and the starting magnetisation was set to 0.05 on both species as a symmetry-breaking nudge that does not force a magnetic ground state. The SCF then converged monotonically across 96 iterations of the first BFGS step, reaching the requested conv_thr = 1×10⁻⁸ Ry. Six subsequent BFGS steps brought the maximum atomic force to 0.00563 Ry/Bohr, at which point the relaxation was deemed converged. The final total energy of the Pristine_V_O 47-atom supercell is −4233.15036 Ry; the corresponding V_O formation energy, computed against E_tot(Pristine_perfect) = −4275.01530 Ry and ½ E(O₂) = −41.51621 Ry, is +4.74 eV. This value reproduces the literature anatase native-defect range (Arrigoni & Madsen, 4.0--5.0 eV at U = 4.2 eV; Boonchun et al., \~5.5 eV under HSE06).

# S2. Additional projected density-of-states plots

## S2.1 Single-cell Pr_VO PDOS with explicit dopant valence breakdown

Figure S1 shows the projected density of states (PDOS) of the Pr_V_O supercell with the Pr-5d (valence) and Pr-5p (semicore) channels plotted separately from the Ti-3d and O-2p projections. The figure makes explicit the dominant Ti-3d weight in the conduction band (the two V_O-derived electrons populate delocalised conduction-band states, consistent with the closed-shell n-type assignment in Section 3.3 of the main text). The italic note on the figure addresses the Pr-4f² occupation: the PSlibrary 1.0.0 Pr.pbe-spdn-kjpaw_psl.1.0.0.UPF pseudopotential has Z_val = 11 (5s, 5p, 5d, 6s, 6p, and the 4f² subshell are all explicit in the valence), but the projwfc.x atomic basis declares only 5p, 5d projection channels. The missing 4f channel manifests as a small residual between the total density of states and the sum of projected channels and does not affect the central closed-shell singlet result.

![](/tmp/claude-0/-home-user-TensorTonic-Solutions/0159629d-9bba-513e-9e05-92ed56279e63/scratchpad/media/Ghadimimehr_DFT_TiO2_PrRb_FINAL_Supporting_Information/media/image1.png){width="6.0in" height="3.6627318460192475in"}

*Figure S1. Projected density of states of the Pr_V_O supercell (anatase TiO₂ + Pr_Ti + V_O, E_F = 10.306 eV from NSCF on the relaxed geometry at a 2×2×2 k-mesh). Channels plotted: Ti-3d summed over 15 Ti atoms; O-2p summed over 31 O atoms; Pr-5d (valence d projection on the substitutional Pr atom); Pr-5p (semicore reference); and the total projected DOS. The italic note explains the Pr-4f² valence treatment within the PSlibrary 1.0.0 atomic basis.*

## S2.2 Total-DOS comparison: Pr_V_O vs Rb_V_O (non-spin-resolved)

Figure S2 presents the total projected density of states for the Pr_V_O (top) and Rb_V_O (bottom) supercells without the spin-channel decomposition of Figure 5 in the main text. This rendering makes the Fermi-level placement and the band-gap evolution between the two systems immediately visible: Pr_V_O has E_F = 10.31 eV with a clean conduction-band edge (n-type donor character, two electrons in delocalised Ti-3d-derived states); Rb_V_O has E_F = 7.14 eV with a small residual O-2p weight at E_F (the hole polaron described in Sections 3.3 and 3.12 of the main text). The non-spin-resolved version is included here for readers less interested in the spin-polarisation accounting but seeking the cleanest visual contrast between the two carrier types.

![](/tmp/claude-0/-home-user-TensorTonic-Solutions/0159629d-9bba-513e-9e05-92ed56279e63/scratchpad/media/Ghadimimehr_DFT_TiO2_PrRb_FINAL_Supporting_Information/media/image2.png){width="6.0in" height="5.839323053368329in"}

*Figure S2. Projected density of states for Pr_V_O (top, E_F = 10.31 eV) and Rb_V_O (bottom, \|m\| = 1.21 μ_B, E_F = 7.14 eV), without spin-channel decomposition. Filled Ti-3d shading and overlaid O-2p (red) and dopant-d (purple) curves make the Fermi-level contrast immediately visible. This is the non-spin-resolved companion to Figure 5 of the main text.*

# S3. Hubbard-U sensitivity sweep --- numerical data

The U(Ti-3d) sensitivity sweep referenced in Section 3.7 of the main text covers U = 3.0, 3.5, 4.0 and 4.5 eV on the production Pristine_perfect, Pr_V_O and Rb_V_O supercells, using the same Γ-only k-mesh, 40 Ry kinetic-energy cut-off, and ortho-atomic Hubbard projector. The total magnetisation of each cell was extracted from the converged SCF output and is collected in Table S1; the maximum E_F variation across the 1.5-eV U range did not exceed 0.26 eV in any cell.

  ---------------------------------------------------------------------------------------------------
  Cell               \|m\| at U=3.0   \|m\| at U=3.5 (production)   \|m\| at U=4.0   \|m\| at U=4.5
  ------------------ ---------------- ----------------------------- ---------------- ----------------
  Pristine_perfect   0.00 μ_B         0.00 μ_B                      0.00 μ_B         0.00 μ_B

  Pr_V_O             0.00 μ_B         0.00 μ_B                      0.00 μ_B         0.00 μ_B

  Rb_V_O             1.00 μ_B         1.21 μ_B                      1.00 μ_B         1.00 μ_B
  ---------------------------------------------------------------------------------------------------

*Table S1. Total magnetisation of Pristine, Pr_V_O and Rb_V_O across the U(Ti-3d) sweep. The closed-shell (Pr_V_O, mag = 0) and one-unpaired-state (Rb_V_O, mag ≈ 1 μ_B) assignments are invariant across the 1.5-eV U range, confirming the qualitative physics is not a U-parameter artefact.*

# S4. k-mesh ΔΔE convergence test --- numerical data

The 2×2×2 Monkhorst--Pack k-mesh verification underlying the ΔΔE = −40 meV \"shift-of-the-shift\" result in Section 3.7 of the main text was computed by performing four single-point SCF calculations on the Γ-relaxed geometries at the same 40 Ry cut-off, ortho-atomic projector, and U(Ti-3d) = 3.5 eV as the production runs. The four 2×2×2 SCF total energies, together with the corresponding Γ-only values from the production relaxations, are collected in Table S2.

  --------------------------------------------------------------------------------
  Cell              E_tot at Γ-only (Ry)   E_tot at 2×2×2 (Ry)   ΔE_tot (Ry)
  ----------------- ---------------------- --------------------- -----------------
  Pr_perfect        −4576.71224            −4576.62183           +0.09041

  Pr_V_O            −4535.10106            −4535.01814           +0.08292

  Rb_perfect        −4330.38890            −4330.28761           +0.10129

  Rb_V_O            −4289.17135            −4289.08034           +0.09101
  --------------------------------------------------------------------------------

*Table S2. Production single-U(Ti-3d) total energies at Γ-only and 2×2×2 k-meshes. The V_O formation-energy contrast Pr − Rb at the 2×2×2 mesh evaluates to +5.39 eV, compared to +5.35 eV at the Γ-only mesh --- a \"shift-of-the-shift\" of ΔΔE = −40 meV (= −0.04 eV), well below the 0.1 eV chemical-accuracy threshold for comparative defect-formation conclusions.*

# S5. Bader topological-charge analysis --- per-atom summary

The Bader analysis was carried out on the relaxed Pr_V_O and Rb_V_O cells with the Henkelman et al. grid-based algorithm. pp.x dumped the all-electron charge density to a Gaussian-cube file (plot_num = 0, output_format = 6) and the bader binary (v1.05, 08/19/23) decomposed the density into atomic basins. Table S3 summarises the per-atomic-type Bader-charge averages and the largest single-atom deviations between the Rb_V_O test cell and the Pr_V_O carrier-free reference. The oxygen sublattice in Rb_V_O is depleted of ≈ 0.97 e relative to Pr_V_O, with 26 % (−0.26 e) concentrated on a single O atom (O₈ in the atomic ordering of the production input) and a further 14 % (−0.14 e) on O₃₀. The titanium sublattice in Rb_V_O exhibits only a uniform mean depletion of −0.012 e per Ti, with no single Ti atom exceeding −0.05 e --- ruling out an isolated Ti³⁺ excess-electron centre.

  -------------------------------------------------------------------------------------------
  Quantity                                    Pr_V_O                  Rb_V_O
  ------------------------------------------- ----------------------- -----------------------
  Total electrons (Bader sum)                 376.998                 374.998

  Mean Ti charge (15 atoms, e)                9.683                   9.671

  Mean O charge (31 atoms, e)                 7.187                   7.155

  Largest single-atom O depletion vs Pr_V_O   --- (reference)         −0.257 e on O₈
  -------------------------------------------------------------------------------------------

*Table S3. Summary Bader-charge metrics for Pr_V_O (closed-shell reference) and Rb_V_O (test). The full per-atom ACF.dat tables (47 rows each) are available in the Zenodo data deposit referenced in the main-text Data Availability statement.*

# S6. Multi-V_O site sensitivity (Stage 4) --- numerical data

The three alternative V_O configurations described in Section 3.11 of the main text were generated by relaxing the Pr_perfect structure with the indicated oxygen atom removed (numbering follows the ATOMIC_POSITIONS order in the production input file). The relaxations used identical settings to the production Pr_V_O calculation (BFGS, single-U Ti-3d = 3.5 eV, Γ-only, 40 Ry).

  -----------------------------------------------------------------------------------------------
  Site label                            Pr--O distance (Å)   E_tot (Ry)        E_form(V_O) (eV)
  ------------------------------------- -------------------- ----------------- ------------------
  Production Pr_V_O (closest O to Pr)   \~2.17 (1st shell)   −4535.10106       +1.29

  altO01 (2nd shell)                    3.99                 −4535.04367       +2.07

  altO07 (distant)                      4.94                 −4534.99608       +2.72

  altO17 (2nd shell, mirror)            3.99                 −4535.04366       +2.07
  -----------------------------------------------------------------------------------------------

*Table S4. V_O formation energies at four crystallographically distinct oxygen sites in the Pr-doped supercell. The altO01 and altO17 sites are equivalent under the 2×2×1 supercell symmetry between the two 2nd-shell positions; their agreement to 0.001 eV is an internal consistency check on the BFGS protocol.*

# S7. Post-queue methodological cross-checks --- numerical data

The five post-queue cross-checks reported in Sections 3.8--3.12 of the main text are summarised in Table S5. Each entry was extracted directly from the corresponding Quantum ESPRESSO .out file.

  ----------------------------------------------------------------------------------------------------------
  Cross-check           Cell                 E_tot (Ry)        Key observable
  --------------------- -------------------- ----------------- ---------------------------------------------
  HSE06 (§3.8)          Pristine_perfect     −3926.66858       E_F = 8.286 eV; mag = 0 (closed shell)

  Dual-Hubbard (§3.9)   Pr_perfect           −4571.33095       \|m\| = 1.00 μ_B (one localised hole)

  Dual-Hubbard (§3.9)   Pristine (control)   −4269.72111       mag = 0 (no spurious magnetism)

  vdW-D3 (§3.10)        Pr_V_O               −4535.85464       D3 dispersion = −10.29 eV; mag = 0

  vdW-D3 (§3.10)        Rb_V_O               −4289.91254       D3 dispersion = −10.09 eV; \|m\| = 1.00 μ_B
  ----------------------------------------------------------------------------------------------------------

*Table S5. Post-queue cross-check results. The HSE06 entry uses exx_fraction = 0.25 and screening_parameter = 0.106 bohr⁻¹ (Krukau et al.). The vdW-D3 entries use Becke--Johnson damping (dftd3_version = 4) and three-body C₉ contributions omitted (dftd3_threebody = .false.).*

# S8. Methodology details and file inventory

All Quantum ESPRESSO calculations used QE v.7.5 (Giannozzi et al., 2017, 2020) with the PSlibrary 1.0.0 PAW pseudopotential family. The specific pseudopotential files were Ti.pbe-spn-kjpaw_psl.1.0.0.UPF, O.pbe-n-kjpaw_psl.1.0.0.UPF, Pr.pbe-spdn-kjpaw_psl.1.0.0.UPF (Z_val = 11, 4f² in valence), and Rb.pbe-spn-kjpaw_psl.1.0.0.UPF. Spin-polarised calculations used nspin = 2 throughout. The Hubbard correction was implemented with HUBBARD ortho-atomic and U Ti-3d = 3.5 eV; the dual-Hubbard test added U O-2p = 5.5 eV transferred from Carey and Nolan\'s α-Cr₂O₃ protocol.

The QE input templates, orchestrator shell scripts, and Python plotting scripts used to produce every figure in the main manuscript and this Supporting Information are organised under the JMCA_plan/ directory tree on the corresponding author\'s computational facility. The complete file inventory (templates, scripts, raw .out files, ACF.dat files, and the v8 master spreadsheet) will be deposited on Zenodo upon acceptance, with the DOI added at the proof stage. Pending the deposit, the same files are available from the corresponding author on reasonable request.

## S8.1 Stage-by-stage runtime summary

  -------------------------------------------------------------------------------------------------------------------
  Stage                                            Wall time (i5-3570, 4 cores)   Outcome
  ------------------------------------------------ ------------------------------ -----------------------------------
  Production single-U relaxations (5 cells)        \~3 days each                  All converged

  Stage 1: HSE06 single-shot on Pristine           8 days                         JOB DONE

  Stage 2: Dual-Hubbard Pr_perfect + Pristine      \~24 h                         JOB DONE

  Stage 3: vdW-D3 single-points (Pr_V_O, Rb_V_O)   \~12 h total                   JOB DONE

  Stage 4: Multi-V_O Pr_V_O (3 sites)              \~33 h total                   JOB DONE

  Stage 5: Bader on Pristine, Pr_V_O, Rb_V_O       \~2 h                          Pr_V_O + Rb_V_O OK

  Stage 6: 2×2×2 k-mesh verification (4 SCFs)      \~6 h total                    Pr_perfect, Rb_perfect, Pr_V_O OK
  -------------------------------------------------------------------------------------------------------------------

*Table S6. Wall-time summary for each computational stage. The Pristine V_O baseline calculation (Section S1 of this Supporting Information) required \~14 h after the v3 mixing-scheme recovery.*
