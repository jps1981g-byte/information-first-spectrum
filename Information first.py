import numpy as np
import pandas as pd
from scipy.special import gamma

print("===================================================================")
print(" INFORMATION-FIRST : COSMOLOGICAL SCALES + GLOBAL SPECTRUM ")
print("===================================================================\n")

# ------------------------------------------------------
# 1) FUNDAMENTAL CONSTANTS
# ------------------------------------------------------
pi = np.pi
V_univ = 1.0e78            # Universe volume (m^3)
l_Pl = 1.616255e-35        # Planck length (m)
Mpl4 = 2.22195e88          # Planck energy density (MeV^4)

# Equivalent radius of observable volume
R = (3.0 * V_univ / (4.0 * pi))**(1.0 / 3.0)

# Universal geometric normalization
alpha_geom = 0.31055152551549314

print("=== CONSTANTS ===")
print(f"V_univ     = {V_univ:.4e} m^3")
print(f"R          = {R:.4e} m")
print(f"l_Pl       = {l_Pl:.4e} m")
print(f"Mpl4       = {Mpl4:.4e} MeV^4")
print(f"alpha_geom = {alpha_geom:.12f}")
print()

# ------------------------------------------------------
# 2) CORRECTED HYPERSPHERICAL ENTROPY
# ------------------------------------------------------
def S_hypersphere(d):
    """
    Corrected geometric entropy:
    S(d) = alpha_geom * A_d(R) / l_Pl^(d-1)
    """
    A_d = (2.0 * pi**(d / 2.0) / gamma(d / 2.0)) * (R**(d - 1.0))
    return alpha_geom * A_d / (l_Pl**(d - 1.0))

# ------------------------------------------------------
# 3) MASS DERIVATION
# ------------------------------------------------------
def mass_from_entropy(S_ent):
    """
    Information-First chain:
    S_ent -> DeltaV -> I_eff^2 -> L* -> m
    Returns mass in eV.
    """
    DeltaV = Mpl4 / S_ent
    I_eff_sq = pi * DeltaV
    L_star = (2.0 / (3.0 * I_eff_sq))**0.25
    m_MeV = (4.0 / 3.0) / L_star
    return m_MeV * 1.0e6  # eV

# ------------------------------------------------------
# 4) INVERSION: ENERGY -> d_eff
# ------------------------------------------------------
def find_d_for_mass(target_MeV, d_min=1.0, d_max=3.5, steps=30000):
    d_vals = np.linspace(d_min, d_max, steps)

    masses_MeV = []
    for d in d_vals:
        S = S_hypersphere(d)
        m_eV = mass_from_entropy(S)
        masses_MeV.append(m_eV / 1.0e6)

    masses_MeV = np.array(masses_MeV)

    idx = np.argmin(np.abs(np.log10(masses_MeV) - np.log10(target_MeV)))
    return d_vals[idx], masses_MeV[idx]

# ------------------------------------------------------
# 5) COSMOLOGICAL SCALES
# ------------------------------------------------------
GeV_to_MeV = 1e3

cosmo_scales = {
    "Planck (Big Bang)": 1.22e19 * GeV_to_MeV,
    "GUT (hypothetical)": 1.0e16 * GeV_to_MeV,
    "Inflation": 1.0e13 * GeV_to_MeV,
    "Electroweak breaking": 246.0 * GeV_to_MeV,
    "QCD / confinement": 200.0,
    "Nucleosynthesis": 0.1,
    "Recombination": 0.0003
}

print("=== COSMOLOGICAL SCALES ===")
print("---------------------------------------------------------------")
print(" Phenomenon                    Energy (MeV)")
print("---------------------------------------------------------------")

for name, E in cosmo_scales.items():
    print(f"{name:<30} {E:12.6e}")

print("---------------------------------------------------------------\n")

print("=== COSMOLOGICAL CORRESPONDENCE IN MODEL ===")
print("-----------------------------------------------------------------------")
print(" Phenomenon                    d_eff      reconstructed mass (MeV)")
print("-----------------------------------------------------------------------")

for name, E in cosmo_scales.items():
    d_val, m_val = find_d_for_mass(E)
    print(f"{name:<30} {d_val:7.4f}    {m_val:14.6e}")

print("-----------------------------------------------------------------------\n")

# ------------------------------------------------------
# 6) TOPOLOGICAL SCAN
# ------------------------------------------------------
d_values = np.arange(2.0, 3.5, 0.0001)

results_d = []
results_m = []

print("=== SPECTRUM SCAN IN PROGRESS ===")
for d in d_values:
    S = S_hypersphere(d)
    m = mass_from_entropy(S)
    results_d.append(d)
    results_m.append(m)

results_d = np.array(results_d, dtype=float)
results_m = np.array(results_m, dtype=float)

print(f"Number of scanned points = {len(results_d)}")
print()

# ------------------------------------------------------
# 7) REFERENCE MASS SPECTRUM (eV)
# ------------------------------------------------------
particles = {
    "neutrino_scale": 0.009,

    # Leptons
    "electron": 5.1099895e5,
    "muon": 1.05658375e8,
    "tau": 1.77686e9,

    # Quarks
    "up_quark": 2.16e6,
    "down_quark": 4.67e6,
    "strange_quark": 9.3e7,
    "charm_quark": 1.27e9,
    "bottom_quark": 4.18e9,
    "top_quark": 1.7276e11,

    # Bosons
    "W_boson": 8.0379e10,
    "Z_boson": 9.11876e10,
    "Higgs": 1.251e11,

    # Light baryons
    "proton": 9.38272088e8,
    "neutron": 9.39565421e8,
    "Lambda_0": 1.115683e9,
    "Sigma_plus": 1.18937e9,
    "Sigma_minus": 1.197449e9,
    "Xi_0": 1.31486e9,
    "Xi_minus": 1.32171e9,
    "Delta_plusplus": 1.232e9,
    "Omega_minus": 1.67245e9,

    # Heavy baryons
    "Lambda_c_plus": 2.28646e9,
    "Lambda_b_0": 5.6196e9,

    # Light mesons
    "pion_0": 1.349768e8,
    "pion_charged": 1.39570e8,
    "kaon_charged": 4.93677e8,
    "kaon_0": 4.97611e8,
    "eta_meson": 5.4786e8,
    "rho_meson": 7.7526e8,
    "omega_meson": 7.8266e8,
    "phi_meson": 1.01946e9,

    # Heavy mesons
    "D_0_meson": 1.8648e9,
    "D_plus_meson": 1.8696e9,
    "D_s_plus": 1.9683e9,
    "B_0_meson": 5.2796e9,
    "B_plus_meson": 5.2793e9,

    # Quarkonia
    "J_psi_cc": 3.0969e9,
    "Upsilon_bb": 9.4603e9
}

# ------------------------------------------------------
# 8) MATCHING
# ------------------------------------------------------
best_matches = []

for name, target in particles.items():
    idx = np.argmin(np.abs(np.log10(results_m) - np.log10(target)))

    mass_calc = results_m[idx]
    dimension_eff = results_d[idx]
    error_percent = abs(mass_calc - target) / target * 100.0

    best_matches.append({
        "Particle": name,
        "d_eff (Geo)": dimension_eff,
        "M_calc (eV)": mass_calc,
        "M_ref (eV)": target,
        "Error %": error_percent
    })

# ------------------------------------------------------
# 9) FORMATTING AND DISPLAY
# ------------------------------------------------------
df = pd.DataFrame(best_matches).sort_values("d_eff (Geo)")

df["d_eff (Geo)"] = df["d_eff (Geo)"].apply(lambda x: f"{x:.4f} D")
df["M_calc (eV)"] = df["M_calc (eV)"].apply(lambda x: f"{x:.4e}")
df["M_ref (eV)"] = df["M_ref (eV)"].apply(lambda x: f"{x:.4e}")
df["Error %"] = df["Error %"].apply(lambda x: f"{x:.4f} %")

pd.set_option("display.max_rows", None)

print("=== BEST MATCHES IN THE SPECTRUM ===")
print(df.to_string(index=False, justify="left"))
print()

# ------------------------------------------------------
# 10) GLOBAL DIAGNOSTIC
# ------------------------------------------------------
print("===================================================================")
print(" PHYSICAL INTERPRETATION ")
print("===================================================================")
print("- alpha_geom acts as a universal geometric normalization.")
print("- d_eff organizes particles along a dimensional axis.")
print("- The same framework generates both:")
print("    1) cosmological energy scales")
print("    2) particle mass spectrum")
print("- The full structure is based on:")
print("      S(d) -> DeltaV -> I_eff^2 -> L* -> m")
print("===================================================================")
