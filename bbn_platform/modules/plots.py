"""
Plot generation module.
All plots return self-contained HTML strings (inline SVG via matplotlib).
No file I/O — safe for shinylive deployment.
"""

import io, base64
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

SCENARIOS = ["none", "low", "moderate", "high"]
SCENARIO_LABELS = ["No restoration", "Low", "Moderate", "High"]

# ── shared style ─────────────────────────────────────────────
def _apply_style(ax, color, ymax=1.0):
    ax.set_facecolor("white")
    ax.spines[["top", "right"]].set_visible(False)
    ax.spines[["left", "bottom"]].set_color("#e2e8f0")
    ax.tick_params(colors="#718096", labelsize=9)
    ax.set_ylim(0, ymax)
    ax.yaxis.label.set_color("#4a5568")
    ax.xaxis.label.set_color("#4a5568")

def _fig_to_html(fig):
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=130, bbox_inches="tight",
                facecolor="white")
    buf.seek(0)
    b64 = base64.b64encode(buf.read()).decode()
    plt.close(fig)
    return f'<img src="data:image/png;base64,{b64}" style="width:100%;max-width:680px;display:block;margin:auto;" />'


# ============================================================
# DISEASE RISK PLOT
# ============================================================
def disease_risk_plot(model_data: dict) -> str:
    col   = model_data["color"]
    col_l = model_data["color_light"]
    scens = model_data["scenarios"]

    means  = [scens[s]["mean_disease"]  for s in SCENARIOS]
    lowers = [scens[s]["lower_disease"] for s in SCENARIOS]
    uppers = [scens[s]["upper_disease"] for s in SCENARIOS]
    baseline = means[0]

    fig, ax = plt.subplots(figsize=(7, 3.6))
    x = np.arange(len(SCENARIOS))

    # Ribbon
    ax.fill_between(x, lowers, uppers, color=col, alpha=0.12, zorder=1)

    # Baseline
    ax.axhline(baseline, color="#a0aec0", linestyle="--", linewidth=1.0, zorder=2)
    ax.text(0, baseline + 0.015, "No-restoration baseline",
            fontsize=8, color="#a0aec0", va="bottom")

    # Main line
    ax.plot(x, means, color=col, linewidth=2.2, zorder=3)

    # Points
    point_colors = [model_data["color_light"]] * len(SCENARIOS)
    for i, (xi, y, c) in enumerate(zip(x, means, point_colors)):
        ax.scatter(xi, y, s=80, color=col, zorder=5, edgecolors="white", linewidths=1.5)

    # Annotations: peak + endpoint
    peak_idx = means.index(max(means))
    end_idx  = SCENARIOS.index("high")
    for idx, direction, label in [
        (peak_idx, +1, f"Peak\n{means[peak_idx]:.2f}"),
        (end_idx,  -1, f"Endpoint\n{means[end_idx]:.2f}"),
    ]:
        y_anchor = uppers[idx] if direction > 0 else lowers[idx]
        offset   = 0.06 * direction
        ax.annotate(
            label,
            xy=(x[idx], y_anchor),
            xytext=(x[idx], y_anchor + offset),
            ha="center", va="bottom" if direction > 0 else "top",
            fontsize=8, color=col, fontweight="bold",
            arrowprops=dict(arrowstyle="-", color=col, lw=0.8),
        )

    ax.set_xticks(x)
    ax.set_xticklabels(SCENARIO_LABELS, fontsize=9)
    ax.set_ylabel("Disease risk probability", fontsize=9)
    ax.set_title(f"Disease risk — {model_data['label']}", fontsize=10,
                 color="#2d3748", pad=10)
    _apply_style(ax, col, ymax=max(uppers) + 0.15)
    fig.tight_layout()
    return _fig_to_html(fig)


# ============================================================
# REGULATION PLOT
# ============================================================
def regulation_plot(model_data: dict) -> str:
    col   = model_data["color"]
    scens = model_data["scenarios"]

    means  = [scens[s]["mean_regulation"]  for s in SCENARIOS]
    lowers = [scens[s]["lower_regulation"] for s in SCENARIOS]
    uppers = [scens[s]["upper_regulation"] for s in SCENARIOS]

    fig, ax = plt.subplots(figsize=(5.5, 3.2))
    x = np.arange(len(SCENARIOS))

    ax.fill_between(x, lowers, uppers, color=col, alpha=0.12, zorder=1)
    ax.plot(x, means, color=col, linewidth=2.0, zorder=3)
    for xi, y in zip(x, means):
        ax.scatter(xi, y, s=70, color=col, zorder=5, edgecolors="white", linewidths=1.5)

    ax.set_xticks(x)
    ax.set_xticklabels(SCENARIO_LABELS, fontsize=9)
    ax.set_ylabel("P(strong regulation)", fontsize=9)
    ax.set_title("Ecological regulation recovery", fontsize=10, color="#2d3748", pad=8)
    _apply_style(ax, col)
    fig.tight_layout()
    return _fig_to_html(fig)


# ============================================================
# STABILITY TRAJECTORY PLOT
# ============================================================
def stability_trajectory_plot(model_data: dict) -> str:
    col   = model_data["color"]
    scens = model_data["scenarios"]

    TIME_KEYS   = ["years_1_3", "years_4_7", "years_8_12", "years_13_15"]
    TIME_LABELS = ["1–3 yr", "4–7 yr", "8–12 yr", "13–15 yr"]

    # Color ramp: lightest to darkest for none → high
    alphas = [0.4, 0.6, 0.8, 1.0]
    labels = SCENARIO_LABELS

    fig, ax = plt.subplots(figsize=(5.5, 3.2))
    x = np.arange(len(TIME_KEYS))

    for i, s in enumerate(SCENARIOS):
        vals = [scens[s][k] for k in TIME_KEYS]
        rgba = matplotlib.colors.to_rgba(col, alpha=alphas[i])
        ax.plot(x, vals, color=rgba, linewidth=1.8, marker="o",
                markersize=5, label=labels[i])

    ax.set_xticks(x)
    ax.set_xticklabels(TIME_LABELS, fontsize=9)
    ax.set_ylabel("Probability", fontsize=9)
    ax.set_title("Time to stabilisation by scenario", fontsize=10, color="#2d3748", pad=8)
    ax.legend(fontsize=8, loc="upper right", framealpha=0.7,
              edgecolor="#e2e8f0")
    _apply_style(ax, col)
    fig.tight_layout()
    return _fig_to_html(fig)


# ============================================================
# COMPARISON PLOT (all 3 models)
# ============================================================
def comparison_plot(all_models: dict) -> str:
    model_keys = ["mosquito", "rodent", "tick"]
    labels     = ["No restoration", "Low", "Moderate", "High"]
    x = np.arange(len(SCENARIOS))

    fig, ax = plt.subplots(figsize=(7, 3.8))

    for mk in model_keys:
        m     = all_models[mk]
        means = [m["scenarios"][s]["mean_disease"] for s in SCENARIOS]
        lowers= [m["scenarios"][s]["lower_disease"] for s in SCENARIOS]
        uppers= [m["scenarios"][s]["upper_disease"] for s in SCENARIOS]

        ax.fill_between(x, lowers, uppers, color=m["color"], alpha=0.08, zorder=1)
        ax.plot(x, means, color=m["color"], linewidth=2.0,
                linestyle="--", zorder=3, alpha=0.9)
        ax.scatter(x, means, s=60, color=m["color"], zorder=5,
                   edgecolors="white", linewidths=1.5,
                   label=m['label'])

    ax.set_xticks(x)
    ax.set_xticklabels(labels, fontsize=9)
    ax.set_ylabel("Disease risk probability", fontsize=9)
    ax.set_title("Disease risk by model & restoration scenario",
                 fontsize=10, color="#2d3748", pad=10)
    ax.legend(fontsize=8.5, loc="upper right", framealpha=0.8,
              edgecolor="#e2e8f0")
    _apply_style(ax, "#2d3748")
    fig.tight_layout()
    return _fig_to_html(fig)
