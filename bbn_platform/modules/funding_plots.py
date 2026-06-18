"""
Funding scenario plots: continuous transition-year curves.
"""
import io, base64
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from data.funding_scenarios import (
    risk_curve_over_transition_year,
    BASELINE_RISK,
    BASELINE_CI,
    MODEL_META,
)


def _fig_to_html(fig):
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=130, bbox_inches="tight", facecolor="white")
    buf.seek(0)
    b64 = base64.b64encode(buf.read()).decode()
    plt.close(fig)
    return f'<img src="data:image/png;base64,{b64}" style="width:100%;max-width:680px;display:block;margin:auto;" />'


def transition_curve_plot(system, phase1, phase2, current_t, scenario_label):
    """
    Plots the Year-15 disease risk as a continuous function of the
    transition year t, with a marker at the currently selected t
    (from the slider).
    """
    meta = MODEL_META[system]
    color = meta["color"]

    t_vals, risks = risk_curve_over_transition_year(system, phase1, phase2)

    fig, ax = plt.subplots(figsize=(7, 3.8))

    # Reference lines: pure phase1 / pure phase2 endpoints
    risk_p1 = BASELINE_RISK[system][phase1]
    risk_p2 = BASELINE_RISK[system][phase2]
    ax.axhline(risk_p1, color="#a0aec0", linestyle=":", linewidth=1.0)
    ax.axhline(risk_p2, color="#a0aec0", linestyle=":", linewidth=1.0)
    ax.text(14.7, risk_p1, f"Pure {phase1}", fontsize=7.5, color="#718096",
            ha="right", va="bottom")
    ax.text(14.7, risk_p2, f"Pure {phase2}", fontsize=7.5, color="#718096",
            ha="right", va="top")

    # Main curve
    ax.plot(t_vals, risks, color=color, linewidth=2.2, zorder=3)

    # Current selection marker
    current_risk = np.interp(current_t, t_vals, risks)
    ax.scatter([current_t], [current_risk], s=140, color=color, zorder=5,
               edgecolors="white", linewidths=2)
    ax.annotate(
        f"{current_risk:.2f}",
        xy=(current_t, current_risk),
        xytext=(current_t, current_risk + 0.045 if current_risk < 0.85 else current_risk - 0.06),
        ha="center", fontsize=10, fontweight="bold", color=color,
    )

    # Vertical guide line
    ax.axvline(current_t, color=color, linestyle="--", linewidth=1.0, alpha=0.4)

    ax.set_xlim(0, 15)
    ax.set_ylim(0, 1)
    ax.set_xlabel("Transition year", fontsize=9.5)
    ax.set_ylabel("Year-15 disease risk probability", fontsize=9.5)
    ax.set_title(f"{meta['label']} — {scenario_label}",
                 fontsize=10.5, color="#2d3748", pad=10)

    ax.set_facecolor("white")
    ax.spines[["top", "right"]].set_visible(False)
    ax.spines[["left", "bottom"]].set_color("#e2e8f0")
    ax.tick_params(colors="#718096", labelsize=9)

    fig.tight_layout()
    return _fig_to_html(fig)


def multi_system_transition_plot(phase1, phase2, current_t):
    """
    Overlay all 4 systems' transition curves for the same phase1->phase2
    scenario, so users can compare how sensitive each disease system is
    to the timing of the funding transition.
    """
    fig, ax = plt.subplots(figsize=(7.5, 4.2))

    for system, meta in MODEL_META.items():
        t_vals, risks = risk_curve_over_transition_year(system, phase1, phase2)
        ax.plot(t_vals, risks, color=meta["color"], linewidth=2.0,
                label=meta['label'], zorder=3)
        current_risk = np.interp(current_t, t_vals, risks)
        ax.scatter([current_t], [current_risk], s=90, color=meta["color"],
                   zorder=5, edgecolors="white", linewidths=1.5)

    ax.axvline(current_t, color="#a0aec0", linestyle="--", linewidth=1.0, alpha=0.6)

    ax.set_xlim(0, 15)
    ax.set_ylim(0, 1)
    ax.set_xlabel("Transition year", fontsize=9.5)
    ax.set_ylabel("Year-15 disease risk probability", fontsize=9.5)
    ax.set_title(f"All systems: {phase1} → {phase2} transition",
                 fontsize=10.5, color="#2d3748", pad=10)
    ax.legend(fontsize=8, loc="upper left" if phase1 < phase2 else "upper right",
              framealpha=0.85, edgecolor="#e2e8f0")

    ax.set_facecolor("white")
    ax.spines[["top", "right"]].set_visible(False)
    ax.spines[["left", "bottom"]].set_color("#e2e8f0")
    ax.tick_params(colors="#718096", labelsize=9)

    fig.tight_layout()
    return _fig_to_html(fig)
