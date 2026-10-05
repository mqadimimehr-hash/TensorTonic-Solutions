#!/usr/bin/env python3
"""
verify_numbers.py -- independent re-computation of every derived number that
can be checked in the device manuscript

  "Machine Learning-Accelerated Discovery of Praseodymium-Doped Electron
   Transport Layers ..." (Ghadimimehr, Omar, Sheikh Raihan), Word file
   77d4b4a6-Manuscript_Ghadimimehr.docx.docx

Only inputs printed in the manuscript (tables / text / rendered equations) are
used, plus three external, verifiable data sets:
  * ASTM G173-03 AM1.5G spectrum (bundled with pvlib)
  * CIE 1924 photopic V(lambda) and CIE 015:2018 illuminants (bundled with
    colour-science): LED-B1..B5, FL*, HP*, illuminant A
  * Planck's law

Run:  python3 verify_numbers.py      (needs numpy, scipy, pvlib, colour-science)
"""
import numpy as np
from scipy import integrate, optimize

# --------------------------------------------------------------------------
# constants (CODATA 2018)
q = 1.602176634e-19      # C
kB = 1.380649e-23        # J/K
h = 6.62607015e-34       # J s
c = 2.99792458e8         # m/s
eps0 = 8.8541878128e-14  # F/cm
T = 300.0
VT = kB * T / q          # 0.025852 V
n_id = 1.5               # ideality factor used in the manuscript
a = n_id * VT


def hdr(s):
    print("\n" + "=" * 78 + "\n" + s + "\n" + "=" * 78)


def pct(x, ref):
    return 100.0 * (x - ref) / ref


# ==========================================================================
hdr("A. Simple ratios quoted in abstract / text")
print(f"kT/q at 300 K                       = {VT*1e3:.3f} mV  (MS: 25.85 mV)")
print(f"R_sh ratio 6.05e5/6.05e3            = {6.05e5/6.05e3:.1f}x  (MS: 100x)")
r_J0 = 7.939e-16 / 1.430e-17
print(f"J0 ratio 7.939e-16/1.430e-17        = {r_J0:.3f}x (MS: 55.5x)")
print(f"J0 ratio 7.941e-16/1.431e-17 (eqs)  = {7.941e-16/1.431e-17:.3f}x  [eq. images use 7.941/1.431, Table 2 uses 7.939/1.430]")
print(f"Voc gain LED 1.115-0.232            = {1.115-0.232:.3f} V (MS: 883 mV)")
print(f"PCE fold LED 13.62/0.713            = {13.62/0.713:.2f}x (MS: 19.1x)")
print(f"AM1.5G PCE gain 8.16/5.69           = {8.16/5.69:.3f}x (MS: 1.43x)")
print(f"lambda_g = 1239.84/2.30             = {1239.84193/2.30:.2f} nm (MS: 539 / 539.06 nm)")
print(f"Indoor/outdoor contrast 100/0.3119  = {100/0.3119:.0f}-fold (MS: >300-fold)")
print(f"Useful photon-flux range 5.59e16/3.40e14 = {5.59e16/3.40e14:.0f}x = {np.log10(5.59e16/3.40e14):.2f} decades (MS: 'two orders')")
print(f"S_n = sigma*v_th*N_it : {1e-15*1e7*1e13:.1e} (control), {1e-15*1e7*1e11:.1e} cm/s (doped) (MS: 1e5 -> 1e3)")
print(f"IoT growth 21.1/18.5                = {100*(21.1/18.5-1):.1f} % (MS: 14 %)")

# ==========================================================================
hdr("B. Ideal-diode Voc gain from J0 suppression (Eq. 19) and the '5.5 %' claim")
dV_th = a * np.log(r_J0)
print(f"dVoc_theory = n VT ln(55.52)        = {dV_th*1e3:.2f} mV (MS: 155.7 mV)")
for lab, dv in [("text sec 3.2.1 '145 mV'", 0.145), ("Table 4 1.315-1.150", 0.165),
                ("Fig 8 text 1.316-1.150 = '166 mV'", 0.166), ("sec 2.6 'full model 164.1 mV'", 0.1641)]:
    print(f"  {lab:38s}: {dv*1e3:6.1f} mV, deviation from theory = {pct(dv, dV_th):+.1f} %")
print(f"  NOTE: 1.315 - 1.150 = {1.315-1.150:.3f} V, not 145 mV.")
print(f"Voc roll-off n VT ln10              = {a*np.log(10)*1e3:.1f} mV/dec (MS: 89.3; sec 3.2.1 says '~60 mV/dec')")
print(f"  60 mV/dec corresponds to n = {0.060/(VT*np.log(10)):.2f}")
dec = np.log10(7.610 / 0.0463)
print(f"  Jsc AM1.5G->LED: {dec:.3f} decades -> predicted dVoc = {a*np.log(10)*dec*1e3:.0f} mV; "
      f"MS: 1.320-1.115 = 205 mV; table 1.315-1.115 = 200 mV")

# ==========================================================================
hdr("C. Single-diode model (Eq. 14) -- does it reproduce Table 4 exactly?")


def J_of_V(V, Jsc, J0, Rs, Rsh):
    f = lambda J: Jsc - J0 * np.expm1((V + J * Rs) / a) - (V + J * Rs) / Rsh - J
    lo = -(abs(V) / Rs) - 1.0
    return optimize.brentq(f, lo, Jsc + 1e-12, xtol=1e-18, rtol=1e-14, maxiter=500)


def solve_device(Jsc, J0, Rsh, Rs=10.0):
    Voc = optimize.brentq(lambda V: Jsc - J0 * np.expm1(V / a) - V / Rsh, 0.0, 3.0, xtol=1e-12)
    res = optimize.minimize_scalar(lambda V: -V * J_of_V(V, Jsc, J0, Rs, Rsh),
                                   bounds=(0.0, Voc), method="bounded", options={"xatol": 1e-9})
    Pmax = -res.fun
    return Voc, Pmax / (Voc * Jsc), Pmax, res.x


# Table 3 (J_sc,max in A/cm2, P_in in W/cm2)
T3 = {  # source: (LER, Pin mW/cm2, f_use %, Jsc_max uA/cm2, <E> eV, Phi cm-2 s-1)
    "AM1.5G": (109.45, 100.0, 24.52, 8953.0, 2.739, 5.59e16),
    "LED": (320.57, 0.3119, 45.89, 54.46, 2.628, 3.40e14),
    "CFL": (183.20, 0.5458, 48.83, 97.09, 2.745, 6.06e14),
    "MH": (304.66, 0.3282, 29.32, 36.93, 2.605, 2.31e14),
    "Halogen": (121.11, 0.8257, 10.73, 34.24, 2.588, 2.14e14),
    "INC": (5.94, 16.846, 4.05, 255.97, 2.668, 1.60e15),
}
# Table 4 (Jsc mA/cm2, Voc V, FF, PCE %)
T4 = {
    ("ctrl", "AM1.5G"): (6.293, 1.150, 0.787, 5.69), ("ctrl", "CFL"): (0.06835, 0.414, 0.250, 1.295),
    ("ctrl", "LED"): (0.03834, 0.232, 0.250, 0.713), ("ctrl", "MH"): (0.02600, 0.157, 0.250, 0.312),
    ("ctrl", "Halogen"): (0.02410, 0.146, 0.250, 0.106), ("ctrl", "INC"): (0.1802, 0.938, 0.291, 0.292),
    ("dop", "AM1.5G"): (7.610, 1.315, 0.816, 8.16), ("dop", "CFL"): (0.0825, 1.139, 0.838, 14.42),
    ("dop", "LED"): (0.0463, 1.115, 0.823, 13.62), ("dop", "MH"): (0.0314, 1.100, 0.808, 8.49),
    ("dop", "Halogen"): (0.0291, 1.097, 0.804, 3.11), ("dop", "INC"): (0.2176, 1.177, 0.852, 1.29),
}
PAR = {"ctrl": dict(EQE=0.704, J0=7.939e-16, Rsh=6.05e3), "dop": dict(EQE=0.85, J0=1.430e-17, Rsh=6.05e5)}

print(f"{'dev':5s}{'src':8s} | {'EQE=Jsc/Jmax':>12s} | {'Voc calc':>8s} {'Voc MS':>7s} | {'FF calc':>7s} {'FF MS':>6s} | "
      f"{'PCE calc':>8s} {'PCE MS':>7s} | {'JscVocFF/Pin':>12s}")
for (dev, src), (Jsc_ms, Voc_ms, FF_ms, PCE_ms) in T4.items():
    Jmax = T3[src][3] * 1e-6
    Pin = T3[src][1] * 1e-3
    Jsc = PAR[dev]["EQE"] * Jmax
    Voc, FF, Pmax, Vmp = solve_device(Jsc, PAR[dev]["J0"], PAR[dev]["Rsh"])
    pce_tab = Jsc_ms * 1e-3 * Voc_ms * FF_ms / Pin * 100
    print(f"{dev:5s}{src:8s} | {Jsc_ms*1e-3/Jmax:12.4f} | {Voc:8.3f} {Voc_ms:7.3f} | {FF:7.3f} {FF_ms:6.3f} | "
          f"{Pmax/Pin*100:8.3f} {PCE_ms:7.3f} | {pce_tab:12.3f}")
print("=> Every Table 4 entry is reproduced (to rounding) by the lumped single-diode Eq. 14 with")
print("   Jsc = EQE x Jsc,max (EQE fixed at 0.85 / 0.704), J0 and R_sh taken from Table 2, n = 1.5, Rs = 10.")
print("   No Poisson / drift-diffusion / Fermi-Dirac / Einstein-relation output enters these numbers.")
print(f"   Control indoor Voc = Jsc*Rsh check: LED {0.03834e-3*6050:.3f} V, CFL {0.06835e-3*6050:.3f} V, "
      f"MH {0.026e-3*6050:.3f} V, Halogen {0.0241e-3*6050:.3f} V (pure resistor, FF = 0.25)")

hdr("C2. Decomposition of the AM1.5G Voc gain (full Eq. 14)")
Jmax = 8.953e-3
base = solve_device(0.704 * Jmax, 7.939e-16, 6.05e3)[0]
full = solve_device(0.85 * Jmax, 1.430e-17, 6.05e5)[0]
onlyJ0 = solve_device(0.704 * Jmax, 1.430e-17, 6.05e3)[0]
onlyJ0Rsh = solve_device(0.704 * Jmax, 1.430e-17, 6.05e5)[0]
print(f"control Voc = {base:.4f} V, doped Voc = {full:.4f} V, total dVoc = {(full-base)*1e3:.1f} mV")
print(f"  J0 only                 : +{(onlyJ0-base)*1e3:.1f} mV")
print(f"  + Rsh (6.05e3 -> 6.05e5): +{(onlyJ0Rsh-onlyJ0)*1e3:.2f} mV")
print(f"  + EQE 0.704 -> 0.85     : +{(full-onlyJ0Rsh)*1e3:.2f} mV  (analytic n VT ln(0.85/0.704) = {a*np.log(0.85/0.704)*1e3:.2f} mV)")
print("=> The ~8 mV beyond the J0 term comes from the ASSUMED EQE change, not from R_sh (MS: '~8.6 mV from improved R_sh').")

hdr("C3. Sensitivity of the headline LED result to the assumed R_sh(N_it) mapping (Eq. 1)")
JmL = 54.46e-6
PinL = 0.3119e-3
for lab, EQE, J0, Rsh in [("control (all control params)", 0.704, 7.939e-16, 6.05e3),
                          ("J0 doped only", 0.704, 1.430e-17, 6.05e3),
                          ("EQE doped only", 0.85, 7.939e-16, 6.05e3),
                          ("Rsh doped only", 0.704, 7.939e-16, 6.05e5),
                          ("J0+EQE doped, Rsh control", 0.85, 1.430e-17, 6.05e3),
                          ("all doped", 0.85, 1.430e-17, 6.05e5)]:
    Voc, FF, Pm, _ = solve_device(EQE * JmL, J0, Rsh)
    print(f"  {lab:30s}: Voc={Voc:.3f} V FF={FF:.3f} PCE={Pm/PinL*100:6.2f} %")
print("  Full 2^3 factorial (c = control value, d = doped value) under 1000-lx LED:")
import itertools
for e, j, r in itertools.product([0, 1], repeat=3):
    EQE = [0.704, 0.85][e]; J0 = [7.939e-16, 1.430e-17][j]; Rsh = [6.05e3, 6.05e5][r]
    Voc, FF, Pm, _ = solve_device(EQE * JmL, J0, Rsh)
    print(f"    EQE={'cd'[e]} J0={'cd'[j]} Rsh={'cd'[r]} : Voc={Voc:.3f} V FF={FF:.3f} PCE={Pm/PinL*100:6.2f} %")
print("  R_sh proportional to N_it^-beta (beta = assumed exponent), all other doped params fixed:")
for beta in [0.0, 0.25, 0.5, 0.75, 1.0]:
    Rsh = 6.05e3 * (100.0 ** beta)
    Voc, FF, Pm, _ = solve_device(0.85 * JmL, 1.430e-17, Rsh)
    print(f"    beta={beta:4.2f}  Rsh={Rsh:9.3e}  LED PCE={Pm/PinL*100:6.2f} %  (gain vs control {Pm/PinL*100/0.713:5.1f}x)")

hdr("C4. Shunt-current statements")
for src in ["LED", "CFL", "MH", "Halogen", "INC"]:
    Jc = T4[("ctrl", src)][0] * 1e3
    Jd = T4[("dop", src)][0] * 1e3
    print(f"  {src:8s}: ctrl Jsc={Jc:7.2f} uA  vs  J_sh(0.5V)={0.5/6.05e3*1e6:.1f} uA -> exceeds Jsc: {0.5/6.05e3*1e6 > Jc};"
          f"  doped J_sh(0.5V)/Jsc = {0.5/6.05e5*1e6/Jd*100:.2f} %")
print(f"  (MS lists LED, MH, halogen only; CFL also satisfies J_sh > Jsc. The '<=3.4 %' equals 0.83/24.10 = "
      f"{0.8264/24.10*100:.2f} %, i.e. doped J_sh divided by the CONTROL halogen Jsc.)")
print(f"  AM1.5G V/Rsh at Voc: control {1.150/6050/6.293e-3*100:.2f} % of Jsc, doped {1.315/6.05e5/7.610e-3*100:.3f} % (MS: <= 2.6 %)")

# ==========================================================================
hdr("D. Fermi-Dirac integrals, eta = 3.03, 78.3 meV, 2.44 and 1.56")
from scipy.special import gamma


def F_unnorm(j, eta):
    # int_0^inf xi^j/(1+exp(xi-eta)) dxi, via xi = t^2 to remove the j=-1/2 singularity
    from scipy.special import expit
    g = lambda t: 2.0 * t ** (2 * j + 1) * expit(eta - t * t)   # = 1/(1+exp(t^2-eta)), overflow-safe
    return integrate.quad(g, 0, np.inf, limit=200)[0]


def F_norm(j, eta):  # Blakemore normalisation 1/Gamma(j+1)
    return F_unnorm(j, eta) / gamma(j + 1)


ratio_n = 1e19 / 2.2e18
eta_sol = optimize.brentq(lambda e: F_norm(0.5, e) - ratio_n, -10, 20)
print(f"n/Nc = 1e19/2.2e18                  = {ratio_n:.4f}")
print(f"solve F_1/2(eta)[2/sqrt(pi) norm] = n/Nc -> eta = {eta_sol:.4f}  (MS: 3.03)")
print(f"F_1/2(3.03) normalised              = {F_norm(0.5,3.03):.4f}  (MS: 4.543)")
print(f"F_-1/2(3.03) normalised (1/sqrt(pi))= {F_norm(-0.5,3.03):.4f}  (MS: 1.864)")
print(f"ratio F_1/2/F_-1/2 (both normalised)= {F_norm(0.5,3.03)/F_norm(-0.5,3.03):.4f}  (MS: 2.44)")
print(f"unnormalised F_1/2(3.03)            = {F_unnorm(0.5,3.03):.4f}; F_-1/2 = {F_unnorm(-0.5,3.03):.4f};"
      f" ratio = {F_unnorm(0.5,3.03)/F_unnorm(-0.5,3.03):.4f}")
print("  -> the 2.44 ratio is only correct if BOTH integrals use the 1/Gamma(j+1) normalisation;")
print("     the printed Eq. 7 defines F_1/2 with 2/sqrt(pi) but F_-1/2 is never defined.")
print(f"sqrt(2.44)                          = {np.sqrt(2.44):.4f}  (MS Eq. 9: 1.56; text sec 2.3 says L enhanced by '2.44')")
print(f"eta*kT = 3.03 x {VT*1e3:.3f} meV        = {3.03*VT*1e3:.2f} meV  (MS: 78.3 meV)")
print(f"Boltzmann estimate ln(n/Nc)         = {np.log(ratio_n):.3f} -> E_F-E_C = {np.log(ratio_n)*VT*1e3:.1f} meV")
eta_inv = optimize.brentq(lambda e: F_norm(0.5, e) - 1 / ratio_n, -10, 20)
print(f"AS PRINTED Eq. 7, F_1/2 = Nc/n = {1/ratio_n:.3f} -> eta = {eta_inv:.3f} (non-degenerate!)  => Eq. 7 is inverted")
print(f"Is Fermi level 'within ~3 kT of band edge'? It is 3.03 kT INSIDE the band (degenerate).")

hdr("E. Work functions in Table 1")
phi_etl = 4.50 + (-3.03 * VT)
print(f"ETL: phi = chi + (Ec-Ef) = 4.50 - {3.03*VT:.4f} = {phi_etl:.4f} eV  (MS 4.422) OK")
EfEv = VT * np.log(8.47e18 / 1e16)
print(f"CsPbBr3: phi = chi+Eg-(Ef-Ev) = 3.35+2.30-{EfEv:.4f} = {3.35+2.30-EfEv:.3f} eV (MS 5.357)")
need = 3.35 + 2.30 - 5.357
print(f"   MS value needs Ef-Ev = {need:.3f} eV -> N_A = Nv*exp(-{need:.3f}/kT) = {8.47e18*np.exp(-need/VT):.2e} cm-3 (Table: 1e16)")
EfEv2 = VT * np.log(1e20 / 1e18)
print(f"Co3O4: phi = 3.45+2.10-{EfEv2:.4f} = {3.45+2.10-EfEv2:.3f} eV (MS 5.05)")
print(f"CBO SnO2/CsPbBr3 = 4.50-3.35 = {4.50-3.35:.2f} eV; ETL CBM is BELOW absorber CBM -> 'cliff', not 'spike'")

hdr("F. EIS (Table 5, Eqs. 20-21)")
for lab, J0, Rrec, Cmu, Rct, Rsh in [("control", 7.939e-16, 308.0, 177e-9, 95.0, 6.05e3),
                                     ("doped", 1.430e-17, 17109.0, 23.5e-9, 25.0, 6.05e5)]:
    Rrec_eq = a / J0
    C1 = eps0 * 9.86 / 50e-7
    tau = Rrec * Cmu
    f2 = 1 / (2 * np.pi * tau)
    f1 = 1 / (2 * np.pi * Rct * C1)
    print(f"{lab:8s}: Eq.21 at V=0: R_rec = nVT/J0 = {Rrec_eq:.3e} Ohm cm2  vs Table 5 {Rrec:.0f}  (factor {Rrec_eq/Rrec:.1e})")
    print(f"          parallel with R_sh -> R_LF(dark,0V) = {1/(1/Rrec_eq+1/Rsh):.3e} Ohm cm2 (= R_sh)")
    print(f"          tau = {tau*1e6:.1f} us, f2 = {f2:.0f} Hz, f1 = {f1:.0f} Hz, f1/f2 = {f1/f2:.1f}")
    w = 2 * np.pi * np.logspace(-1, 6, 20001)
    Z = 10.0 + Rct / (1 + 1j * w * Rct * C1) + Rrec / (1 + 1j * w * Rrec * Cmu)
    ph = -np.degrees(np.angle(Z))
    imz = -Z.imag
    from scipy.signal import find_peaks
    pk, _ = find_peaks(ph)
    pki, _ = find_peaks(imz)
    print(f"          Bode-phase maxima at f = {[f'{w[i]/2/np.pi:.3g}' for i in pk]} Hz (phase {[f'{ph[i]:.1f}' for i in pk]} deg);"
          f" -Z'' maxima at {[f'{w[i]/2/np.pi:.3g}' for i in pki]} Hz")
print(f"R_rec ratio 17109/308 = {17109/308:.2f}; C_mu ratio 177/23.5 = {177/23.5:.2f} (vs 100x N_it); tau ratio = {17109*23.5/(308*177):.2f}")
print(f"C1 = eps0*9.86/50nm (ETL)        = {eps0*9.86/50e-7*1e9:.1f} nF/cm2 (MS 175)")
print(f"C_geo = eps0*6.5/500nm (absorber)= {eps0*6.5/500e-7*1e9:.1f} nF/cm2 (a degenerate ETL is a conductor, not a dielectric)")

hdr("G. J0 bulk/interface partition ('irreducible ~1.8 %')")
J0c, J0d = 7.939e-16, 1.430e-17
J0i = (J0c - J0d) / (1 - 0.01)
J0b = J0c - J0i
print(f"Assume J0 = J0b + J0i*(N_it/1e13): J0i = {J0i:.3e}, J0b = {J0b:.3e} A/cm2")
print(f"  J0b/J0(control) = {J0b/J0c*100:.2f} %, J0b/J0(doped) = {J0b/J0d*100:.1f} %; 1/55.5 = {100/r_J0:.2f} %")
print("  -> the '1.8 %' is simply J0(doped)/J0(control); under the paper's own linear picture ~55 % of the doped J0 is still interfacial.")

# ==========================================================================
hdr("H. Table 3 internal consistency  (f_use = Jsc,max*<E>/Pin ; Phi = Jsc,max/q ; Pin = 1000 lx/LER)")
for s, (LER, Pin, fu, Jm, E, Phi) in T3.items():
    Pin_calc = (1000.0 / LER) / 10.0 if s != "AM1.5G" else 100.0   # W/m2 -> mW/cm2
    print(f"  {s:8s}: Pin calc {Pin_calc:8.4f} (MS {Pin:8.4f}) | f_use calc {Jm*1e-6*E/(Pin*1e-3)*100:6.2f} % (MS {fu}) | "
          f"Phi calc {Jm*1e-6/q:.3e} (MS {Phi:.2e})")
print("  Text sec 3.2.1 quotes f_useful(AM1.5G) = 20.6 % and INC = 4.06 %; Table 3 gives 24.52 % and 4.05 %.")
print(f"  Intro: 200-1000 lx 'approx 10-100 uW/cm2' vs MS LED LER: 200 lx = {200/320.57/10*1e3:.0f} uW/cm2, 1000 lx = {1000/320.57/10*1e3:.0f} uW/cm2")
print(f"         '200 lux ~ 1 uW/cm2' -> actual (LED) {200/320.57/10*1e3:.0f} uW/cm2, i.e. ~{200/320.57/10*1e3:.0f}x larger")

hdr("I. External reference spectra: AM1.5G (ASTM G173 via pvlib) and CIE illuminants (colour-science)")
lam_g = 1239.84193 / 2.30
import colour
V = colour.SDS_LEFS["CIE 1924 Photopic Standard Observer"]
Vint = lambda l: np.interp(l, V.wavelengths, V.values, left=0, right=0)
try:
    from pvlib.spectrum import get_reference_spectra
    spec = get_reference_spectra()
    lam = spec.index.values.astype(float)     # nm
    Eg_ = spec["global"].values                # W m-2 nm-1
    Ptot = np.trapezoid(Eg_, lam)
    m = lam <= lam_g
    phot = Eg_ * lam * 1e-9 / (h * c)          # photons m-2 s-1 nm-1
    Jmax_am = q * np.trapezoid(phot[m], lam[m]) / 1e4   # A/cm2
    Puse = np.trapezoid(Eg_[m], lam[m])
    LER_am = 683 * np.trapezoid(Eg_ * Vint(lam), lam) / Ptot
    print(f"AM1.5G: integral = {Ptot:.1f} W/m2; Jsc,max(lambda<={lam_g:.2f} nm) = {Jmax_am*1e3:.3f} mA/cm2 (MS 8.953)")
    print(f"        f_use (power fraction) = {Puse/Ptot*100:.2f} % (MS 24.52; text 20.6), "
          f"<E_ph> = {Puse/(np.trapezoid(phot[m], lam[m]))/q:.3f} eV (MS 2.739), LER = {LER_am:.1f} lm/W (MS 109.45)")

    # detailed-balance (SQ) limit for Eg = 2.30 eV
    def J0_rad(Eg_eV, Tc=300.0):
        f = lambda E: E ** 2 / np.expm1(E / (kB * Tc))
        I = integrate.quad(f, Eg_eV * q, (Eg_eV + 3.0) * q)[0]   # integrand negligible beyond Eg+3 eV
        return q * 2 * np.pi / (h ** 3 * c ** 2) * I / 1e4   # A/cm2

    J0r = J0_rad(2.30)

    def sq(Jsc, Pin):
        Voc = VT * np.log(Jsc / J0r + 1)
        V = np.linspace(0, Voc, 200001)
        P = V * (Jsc - J0r * np.expm1(V / VT))
        return Voc, P.max() / Pin

    Voc_sq, eff_sq = sq(Jmax_am, Ptot / 1e4)
    print("NOTE: CIE LED-B1..B5 span f_use 19.5-46.8 %; the MS LED (45.89 %) matches only a cool-white (~6500 K) LED.")
    print(f"Detailed balance Eg=2.30 eV: J0,rad = {J0r:.2e} A/cm2; AM1.5G: Voc_SQ = {Voc_sq:.3f} V, PCE_SQ = {eff_sq*100:.1f} %")
    print(f"   -> MS J0(doped)=1.43e-17 with n=1.5 is {1.43e-17/J0r:.1e} x J0,rad (fitted, not derived)")

    print("CIE 015:2018 sources scaled to 1000 lx (spectral range of the CIE tables, 380-780 nm unless noted):")
    for key in ["LED-B1", "LED-B2", "LED-B3", "LED-B4", "LED-B5", "LED-BH1", "FL3.15", "FL11", "FL2", "HP1", "HP3", "HP5", "A"]:
        sd = colour.SDS_ILLUMINANTS[key]
        l = np.asarray(sd.wavelengths, float)
        S = np.asarray(sd.values, float)
        Ev = 683 * np.trapezoid(S * Vint(l), l)
        k = 1000.0 / Ev
        Pin = k * np.trapezoid(S, l)           # W/m2
        mm = l <= lam_g
        ph = k * S * l * 1e-9 / (h * c)
        Jm = q * np.trapezoid(ph[mm], l[mm]) / 1e4
        fuse = k * np.trapezoid(S[mm], l[mm]) / Pin
        Vq, eff = sq(Jm, Pin / 1e4)
        print(f"  {key:8s} ({l.min():.0f}-{l.max():.0f} nm): LER={1000/Pin:6.1f} lm/W  Pin={Pin/10*1e3:6.1f} uW/cm2  "
              f"Jsc,max={Jm*1e6:6.2f} uA/cm2  f_use={fuse*100:5.1f} %  PCE_SQ(2.30 eV)={eff*100:5.1f} %")
except Exception as e:  # pragma: no cover
    print("pvlib/colour not available:", e)

hdr("J. Thermal (Planck) sources: LER, usable fraction, IR fraction vs integration window")


def planck(lnm, Tk):
    l = lnm * 1e-9
    return 1.0 / (l ** 5 * np.expm1(h * c / (l * kB * Tk)))


try:
    for Tk in [2400, 2700, 2856, 3000, 3200]:
        out = []
        for lo, hi in [(380, 780), (350, 800), (300, 1100), (300, 2500), (200, 30000)]:
            l = np.linspace(lo, hi, 200000)
            B = planck(l, Tk)
            P = np.trapezoid(B, l)
            LER = 683 * np.trapezoid(B * Vint(l), l) / P
            fu = np.trapezoid(B[l <= lam_g], l[l <= lam_g]) / P
            ir = np.trapezoid(B[l > 800], l[l > 800]) / P if hi > 800 else 0.0
            out.append(f"[{lo}-{hi}] LER={LER:6.1f} f_use={fu*100:5.2f}% IR>800={ir*100:4.1f}%")
        print(f"T={Tk} K: " + " | ".join(out))
    print("  MS: Halogen LER 121.11 lm/W, f_use 10.73 %; INC LER 5.94 lm/W, f_use 4.05 %; '>85 % of energy at >800 nm'.")
except Exception as e:
    print("Planck section failed:", e)

# ==========================================================================
hdr("K. Tauc absorption (Eq. 11) with A_Tauc = 6.7e11 cm-1 eV^1/2")
E470 = 1239.84193 / 470
for A in [6.7e11, 6.7e5]:
    alpha = A * np.sqrt(E470 - 2.30) / E470
    print(f"  A={A:.1e}: alpha(470 nm) = {alpha:.3e} cm-1   (MS Table 1: 1.8e5 cm-1)")
print(f"  A needed for 1.8e5 at 470 nm = {1.8e5*E470/np.sqrt(E470-2.30):.3e} cm-1 eV^1/2")

hdr("L. Literature rows of the comparison table (Jsc*Voc*FF vs PCE) and Jsc,max bound")
for lab, J, V_, FF_, P in [("[34] Tong", 10.83, 1.44, 0.70, 10.91), ("[35] Li", 8.28, 1.52, 0.83, 10.45),
                           ("[36] Teng", 8.20, 1.71, 0.81, 11.23), ("[37] Patel", 7.98, 1.10, 0.56, 4.97)]:
    print(f"  {lab:10s}: Jsc*Voc*FF = {J*V_*FF_:6.2f} % (listed {P}); Jsc/Jsc,max(2.30 eV, 8.953) = {J/8.953:.2f}")

hdr("M. Figure 8 / Table 4 / text mismatches (AM1.5G)")
print(f"  control: Table 6.293*1.150*0.787 = {6.293*1.150*0.787:.3f} %, Fig 8 6.283*1.150*0.7855 = {6.283*1.150*0.7855:.3f} %")
print(f"  doped  : Table 7.610*1.315*0.816 = {7.610*1.315*0.816:.3f} %, Fig 8 7.610*1.316*0.815 = {7.610*1.316*0.815:.3f} %")
print(f"  Jsc gain 7.610/6.283 = {7.610/6.283:.3f} ('21 %'); 7.201->8.695 quoted in sec 2.6 = {8.695/7.201:.3f} (appears nowhere else)")
print(f"  PCE fold ranges: CFL {14.42/1.295:.1f}x, LED {13.62/0.713:.1f}x, MH {8.49/0.312:.1f}x, Halogen {3.11/0.106:.1f}x, INC {1.29/0.292:.2f}x")
print(f"  Voc recovery: Halogen {1.097-0.146:.3f} V, MH {1.100-0.157:.3f} V, LED {1.115-0.232:.3f} V, CFL {1.139-0.414:.3f} V")

hdr("N. Bulk SRH lifetime / diffusion length from Table 1 and the applicability of Eq. 12 (Jsc = qG(Ln+Lp))")
tau = 1.0 / (1e-15 * 1e7 * 1e15)          # sigma * v_th * N_t (CsPbBr3)
Dn, Dp = 50 * VT, 10 * VT
Ln, Lp = np.sqrt(Dn * tau), np.sqrt(Dp * tau)
d = 500e-7
print(f"CsPbBr3: tau_SRH = {tau*1e9:.0f} ns, Ln = {Ln*1e4:.2f} um, Lp = {Lp*1e4:.2f} um, thickness = {d*1e4:.2f} um")
print(f"  If G is uniform with q*G*d = Jsc,max(AM1.5G) = 8.953 mA/cm2, Eq. 12 gives "
      f"qG(Ln+Lp) = {8.953*(Ln+Lp)/d:.0f} mA/cm2 > Jsc,max -> Eq. 12 is not applicable to a 500-nm absorber with L >> d.")
print(f"  Doped-ETL electron L enhancement sqrt(2.44) = 1.56 refers to the ETL (majority carriers), not the absorber Ln of Eq. 12.")

hdr("O. Can J0 be derived from Table 1? (intrinsic density and order-of-magnitude J0 estimates)")
ni = np.sqrt(4.94e17 * 8.47e18) * np.exp(-2.30 / (2 * VT))
print(f"CsPbBr3 n_i = sqrt(Nc Nv) exp(-Eg/2kT) = {ni:.3e} cm-3")
print(f"  n=2 depletion SRH estimate J0 ~ q n_i d /(2 tau) = {q*ni*d/(2*tau):.2e} A/cm2 (tau = {tau*1e9:.0f} ns, d = 500 nm)")
for S in [1e5, 1e3]:
    print(f"  n=1 interface estimate J0 ~ q S n_i^2 / N_A (S = {S:.0e} cm/s) = {q*S*ni**2/1e16:.2e} A/cm2")
print("  -> the n = 1.5 values 7.939e-16 / 1.430e-17 A/cm2 are phenomenological; their 55.5 ratio cannot be")
print("     obtained from N_it or S_n with the stated parameters (the paper gives no derivation; Fig. 6 caption: 'J0 fixed from AM1.5G fit').")
print(f"  Non-degeneracy margins: CsPbBr3 (E_F-E_V)/kT = ln(Nv/NA) = {np.log(8.47e18/1e16):.2f}; Co3O4 = {np.log(1e20/1e18):.2f} (so eta_p=(E_V-E_F)/kT is NEGATIVE)")
print(f"  Rs = 10 Ohm cm2 drop at AM1.5G MPP: Rs*Jmp ~ {10*7.3e-3*1e3:.0f} mV (~{10*7.3e-3/1.12*100:.1f} % of Vmp)")
