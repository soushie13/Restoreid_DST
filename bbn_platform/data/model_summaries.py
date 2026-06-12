# ============================================================
# PRE-COMPUTED MODEL SUMMARIES
# Extracted from R Monte Carlo BBN simulations (n=1000 iterations)
# These represent the expected output of the three disease models.
# Replace with actual computed values after running your R code.
# ============================================================

SCENARIOS = ["none", "low", "moderate", "high"]

# ------------------------------------------------------------
# MOSQUITO-BORNE DISEASE MODEL
# Mechanism: Restoration → Hydrological Recovery → Standing Water
#            → Ecological Regulation → Mosquito Disease Risk
# Pattern:   Hump (peaks at low restoration, falls below baseline at high)
# ------------------------------------------------------------
MOSQUITO = {
    "label": "Mosquito-borne disease",
    "color": "#2171b5",
    "color_light": "#bdd7e7",
    "color_bg": "#EEF5FC",
    "icon": "🦟",
    "mechanism": (
        "Wetland restoration temporarily increases standing water during early phases, "
        "raising mosquito breeding habitat before mature vegetation and ecological "
        "regulation (predators, competitors) establish. High-intensity restoration "
        "ultimately suppresses disease risk below the no-restoration baseline."
    ),
    "key_insight": (
        "Watch out for the early-phase risk peak: low-intensity restoration temporarily "
        "worsens disease risk before ecological regulation catches up. "
        "Only high-intensity, long-term restoration achieves net disease suppression."
    ),
    "scenarios": {
        "none":     {"mean_disease": 0.38, "lower_disease": 0.28, "upper_disease": 0.48,
                     "mean_regulation": 0.07, "lower_regulation": 0.02, "upper_regulation": 0.14,
                     "mean_stability": 0.22, "lower_stability": 0.10, "upper_stability": 0.35,
                     "years_1_3": 0.47, "years_4_7": 0.30, "years_8_12": 0.14, "years_13_15": 0.09},
        "low":      {"mean_disease": 0.51, "lower_disease": 0.40, "upper_disease": 0.62,
                     "mean_regulation": 0.11, "lower_regulation": 0.04, "upper_regulation": 0.20,
                     "mean_stability": 0.28, "lower_stability": 0.14, "upper_stability": 0.43,
                     "years_1_3": 0.15, "years_4_7": 0.30, "years_8_12": 0.36, "years_13_15": 0.19},
        "moderate": {"mean_disease": 0.40, "lower_disease": 0.29, "upper_disease": 0.52,
                     "mean_regulation": 0.28, "lower_regulation": 0.15, "upper_regulation": 0.42,
                     "mean_stability": 0.52, "lower_stability": 0.35, "upper_stability": 0.68,
                     "years_1_3": 0.15, "years_4_7": 0.30, "years_8_12": 0.36, "years_13_15": 0.19},
        "high":     {"mean_disease": 0.22, "lower_disease": 0.13, "upper_disease": 0.33,
                     "mean_regulation": 0.72, "lower_regulation": 0.58, "upper_regulation": 0.84,
                     "mean_stability": 0.75, "lower_stability": 0.60, "upper_stability": 0.88,
                     "years_1_3": 0.07, "years_4_7": 0.17, "years_8_12": 0.38, "years_13_15": 0.38},
    },
    "interpretation": {
        "none":     "Without restoration, moderate endemic disease risk persists in high-risk regions. "
                    "Ecological regulation is weak; conditions are stable but unfavourable.",
        "low":      "⚠️ Early-phase risk peak. Partial re-wetting increases standing water "
                    "without yet establishing ecological controls. Risk rises above baseline. "
                    "This is a transitional phase — not a final outcome.",
        "moderate": "Risk returns near baseline as partial ecological regulation establishes. "
                    "Hydrological conditions are improving. Stabilisation begins shifting "
                    "toward the medium-term window (8–12 years).",
        "high":     "✅ Full restoration achieves strong ecological regulation — natural predators "
                    "and competitors suppress mosquito populations. Disease risk falls well below "
                    "the no-restoration baseline. Stabilisation requires 8–15 years.",
    },
}

# ------------------------------------------------------------
# RODENT-BORNE DISEASE MODEL
# Mechanism: Restoration → Habitat Quality → Rodent Abundance
#            → Disease Risk (direct, steep)
# Pattern:   Monotonic steady decline with restoration intensity
# ------------------------------------------------------------
RODENT = {
    "label": "Rodent-borne disease",
    "color": "#cb181d",
    "color_light": "#fcae91",
    "color_bg": "#FEF2F2",
    "icon": "🐭",
    "mechanism": (
        "Improved habitat quality from restoration supports diverse competitor communities "
        "(raptors, mustelids, diverse small mammals) that suppress rodent dominance. "
        "Lower rodent abundance directly reduces reservoir host density and transmission risk. "
        "This pathway is direct — no transitional risk peak occurs."
    ),
    "key_insight": (
        "Rodent-borne disease shows the clearest policy signal: every increment of "
        "restoration reduces risk monotonically. Even low-intensity restoration delivers "
        "measurable benefit. High-intensity restoration can halve endemic risk."
    ),
    "scenarios": {
        "none":     {"mean_disease": 0.72, "lower_disease": 0.60, "upper_disease": 0.82,
                     "mean_regulation": 0.06, "lower_regulation": 0.01, "upper_regulation": 0.13,
                     "mean_stability": 0.18, "lower_stability": 0.08, "upper_stability": 0.30,
                     "years_1_3": 0.55, "years_4_7": 0.28, "years_8_12": 0.11, "years_13_15": 0.06},
        "low":      {"mean_disease": 0.55, "lower_disease": 0.43, "upper_disease": 0.67,
                     "mean_regulation": 0.14, "lower_regulation": 0.06, "upper_regulation": 0.24,
                     "mean_stability": 0.35, "lower_stability": 0.20, "upper_stability": 0.50,
                     "years_1_3": 0.19, "years_4_7": 0.38, "years_8_12": 0.28, "years_13_15": 0.15},
        "moderate": {"mean_disease": 0.38, "lower_disease": 0.27, "upper_disease": 0.50,
                     "mean_regulation": 0.32, "lower_regulation": 0.18, "upper_regulation": 0.48,
                     "mean_stability": 0.55, "lower_stability": 0.38, "upper_stability": 0.70,
                     "years_1_3": 0.11, "years_4_7": 0.32, "years_8_12": 0.37, "years_13_15": 0.20},
        "high":     {"mean_disease": 0.18, "lower_disease": 0.10, "upper_disease": 0.28,
                     "mean_regulation": 0.73, "lower_regulation": 0.60, "upper_regulation": 0.85,
                     "mean_stability": 0.72, "lower_stability": 0.57, "upper_stability": 0.85,
                     "years_1_3": 0.06, "years_4_7": 0.15, "years_8_12": 0.49, "years_13_15": 0.30},
    },
    "interpretation": {
        "none":     "Degraded habitat strongly favours rodent irruptions. High endemic disease "
                    "risk. Weak ecological regulation means no natural population control.",
        "low":      "Marginal habitat recovery begins suppressing rodent abundance. Measurable "
                    "risk reduction even at low intensity. No early-phase risk increase.",
        "moderate": "Significant habitat improvement. Diverse competitor communities establishing. "
                    "Disease risk roughly halved compared to no-restoration baseline.",
        "high":     "✅ Mature, diverse habitat strongly suppresses rodent dominance through "
                    "trophic regulation. Disease risk reduced to low endemic levels. "
                    "Stabilisation concentrated in the 8–12 year window.",
    },
}

# ------------------------------------------------------------
# TICK-BORNE DISEASE MODEL
# Mechanism: Restoration → Host Connectivity (hump) AND Predator Recovery (lag)
#            → Tick Disease Risk → Ecological Regulation
# Pattern:   Small hump at low restoration; very delayed stabilisation (trophic cascades)
# ------------------------------------------------------------
TICK = {
    "label": "Tick-borne disease",
    "color": "#238b45",
    "color_light": "#bae4b3",
    "color_bg": "#F0FAF2",
    "icon": "🕷️",
    "mechanism": (
        "Early restoration increases host connectivity (deer, rodent habitat) before "
        "predator recovery and trophic regulation can establish. This creates a transient "
        "risk peak. At high restoration intensity, trophic cascades eventually suppress "
        "host density and tick exposure — but this process is very slow (10–15 years)."
    ),
    "key_insight": (
        "Tick-borne diseases demand the longest planning horizon of the three systems. "
        "Policymakers must anticipate a transient risk increase and communicate clearly "
        "that ecological stabilisation requires 10–15 years of sustained restoration."
    ),
    "scenarios": {
        "none":     {"mean_disease": 0.46, "lower_disease": 0.30, "upper_disease": 0.62,
                     "mean_regulation": 0.08, "lower_regulation": 0.02, "upper_regulation": 0.18,
                     "mean_stability": 0.20, "lower_stability": 0.08, "upper_stability": 0.34,
                     "years_1_3": 0.44, "years_4_7": 0.33, "years_8_12": 0.14, "years_13_15": 0.09},
        "low":      {"mean_disease": 0.58, "lower_disease": 0.44, "upper_disease": 0.71,
                     "mean_regulation": 0.10, "lower_regulation": 0.03, "upper_regulation": 0.20,
                     "mean_stability": 0.24, "lower_stability": 0.11, "upper_stability": 0.39,
                     "years_1_3": 0.21, "years_4_7": 0.27, "years_8_12": 0.29, "years_13_15": 0.23},
        "moderate": {"mean_disease": 0.44, "lower_disease": 0.30, "upper_disease": 0.58,
                     "mean_regulation": 0.22, "lower_regulation": 0.10, "upper_regulation": 0.36,
                     "mean_stability": 0.48, "lower_stability": 0.30, "upper_stability": 0.64,
                     "years_1_3": 0.22, "years_4_7": 0.27, "years_8_12": 0.29, "years_13_15": 0.26},
        "high":     {"mean_disease": 0.28, "lower_disease": 0.16, "upper_disease": 0.42,
                     "mean_regulation": 0.60, "lower_regulation": 0.44, "upper_regulation": 0.74,
                     "mean_stability": 0.72, "lower_stability": 0.55, "upper_stability": 0.86,
                     "years_1_3": 0.04, "years_4_7": 0.09, "years_8_12": 0.28, "years_13_15": 0.59},
    },
    "interpretation": {
        "none":     "Fragmented landscape with low host connectivity. Moderate baseline risk "
                    "with high uncertainty. Trophic regulation absent.",
        "low":      "⚠️ Risk peak. Vegetation regeneration expands host habitat and connectivity "
                    "before predator recovery. Tick exposure elevated. High uncertainty reflects "
                    "this transitional instability.",
        "moderate": "Risk returning toward baseline as predators begin establishing. Trophic "
                    "regulation still partial. Stabilisation signal beginning to shift later.",
        "high":     "✅ Trophic cascades eventually suppress host density and tick exposure. "
                    "Significant uncertainty remains (trophic dynamics are inherently variable). "
                    "Full stabilisation requires 13–15 years — the slowest of the three systems.",
    },
}

ALL_MODELS = {
    "mosquito": MOSQUITO,
    "rodent": RODENT,
    "tick": TICK,
}
