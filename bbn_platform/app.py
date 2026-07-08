"""
BBN Disease Risk Explorer
A Shiny (Python) decision support tool for policymakers.
Hosts four pre-computed Bayesian Belief Network models:
  - Mosquito-borne disease (hump pattern)
  - Rodent-borne disease (monotonic decline)
  - Tick-borne disease (small hump, very delayed stabilisation)
  - Direct-contact zoonoses (steady but shallow decline)
"""

from shiny import App, ui, render, reactive
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from data.model_summaries import ALL_MODELS, SCENARIOS
from data.funding_scenarios import (
    risk_at_transition,
    BASELINE_RISK,
    BASELINE_CI,
    MODEL_META,
    SYSTEMS,
)
from modules.plots import (
    disease_risk_plot,
    regulation_plot,
    stability_trajectory_plot,
    comparison_plot,
)
from modules.funding_plots import (
    transition_curve_plot,
    multi_system_transition_plot,
)
from modules.network_diagram import network_diagram_html
from modules.ui_helpers import scenario_card, model_header, insight_box

# ============================================================
# SCENARIO LABELS (plain language for policymakers)
# ============================================================
SCENARIO_LABELS = {
    "none":     "No restoration",
    "low":      "Low intensity",
    "moderate": "Moderate intensity",
    "high":     "High intensity",
}

# ============================================================
# CSS
# ============================================================
CSS = """
/* ── Base ──────────────────────────────────────────── */
:root {
  --restoreid-teal: #005252;
  --restoreid-green: #46bb86;
  --restoreid-orange: #f4ae6f;
  --restoreid-cream: #f4ebe4;
  --restoreid-black: #0c0c0c;
  --restoreid-border: rgba(0, 82, 82, 0.16);
  --restoreid-muted: rgba(12, 12, 12, 0.62);
}
body {
  font-family: 'Lato', 'Segoe UI', sans-serif;
  background: var(--restoreid-cream);
  color: var(--restoreid-black);
}
h1, h2, h3, h4, h5, .sidebar-title {
  font-family: 'Sentient', Georgia, serif;
  font-weight: 600;
  letter-spacing: 0;
}

/* ── Sidebar ────────────────────────────────────────── */
.sidebar-panel {
  background: #fffaf6;
  border-right: 1px solid var(--restoreid-border);
  padding: 1.2rem;
  min-height: 100vh;
}
.brand-lockup {
  display: flex;
  align-items: center;
  margin-bottom: 1.1rem;
}
.brand-logo {
  display: block;
  width: 74px;
  height: 74px;
  object-fit: contain;
  border-radius: 8px;
}
.sidebar-title {
  font-size: 1.1rem;
  font-weight: 700;
  color: var(--restoreid-black);
  margin-bottom: 0.25rem;
}
.sidebar-subtitle {
  font-size: 0.8rem;
  color: var(--restoreid-muted);
  margin-bottom: 1.5rem;
  line-height: 1.4;
}

/* ── Nav tabs ───────────────────────────────────────── */
.nav-tabs .nav-link {
  font-size: 0.9rem;
  color: var(--restoreid-muted);
  border-radius: 6px 6px 0 0;
}
.nav-tabs .nav-link.active {
  font-weight: 600;
  color: var(--restoreid-teal);
  border-color: var(--restoreid-border) var(--restoreid-border) #fffaf6;
}

/* ── Model selector ─────────────────────────────────── */
.model-btn {
  display: block; width: 100%;
  text-align: left; padding: 0.7rem 0.9rem;
  margin-bottom: 0.4rem;
  border: 1.5px solid var(--restoreid-border);
  border-radius: 8px;
  background: white; cursor: pointer;
  color: var(--restoreid-black);
  font-size: 0.88rem; font-weight: 700;
  transition: all 0.15s ease;
}
.model-btn:hover { border-color: var(--restoreid-green); background: #f8f2ed; }
.model-btn.active { color: white; border-color: transparent; }
.model-btn.mosquito.active { background: #005252; }
.model-btn.rodent.active   { background: #f4ae6f; color: #0c0c0c; }
.model-btn.tick.active     { background: #46bb86; color: #0c0c0c; }
.model-btn.zoonotic.active { background: #0c0c0c; }

/* ── Scenario selector ──────────────────────────────── */
.scenario-btn {
  display: inline-block; padding: 0.45rem 1rem;
  margin: 0.2rem;
  border: 1.5px solid var(--restoreid-border);
  border-radius: 20px; background: white;
  cursor: pointer; font-size: 0.85rem;
  font-weight: 700; color: var(--restoreid-black);
  transition: all 0.15s ease;
}
.scenario-btn:hover { border-color: var(--restoreid-green); }
.scenario-btn.active {
  color: white; border-color: transparent;
  background: var(--restoreid-teal);
}

/* ── Metric cards ───────────────────────────────────── */
.metric-card {
  background: white;
  border: 1px solid var(--restoreid-border);
  border-radius: 8px;
  padding: 1rem 1.2rem;
  margin-bottom: 0.8rem;
}
.metric-label {
  font-size: 0.78rem; color: var(--restoreid-muted);
  text-transform: uppercase; letter-spacing: 0.05em;
  margin-bottom: 0.3rem;
}
.metric-value {
  font-size: 1.9rem; font-weight: 700;
  line-height: 1.1;
}
.metric-range {
  font-size: 0.78rem; color: var(--restoreid-muted);
  margin-top: 0.2rem;
}
.metric-badge {
  display: inline-block;
  font-size: 0.72rem; font-weight: 600;
  padding: 0.15rem 0.5rem; border-radius: 12px;
  margin-top: 0.4rem;
}

/* ── Insight box ────────────────────────────────────── */
.insight-box {
  border-left: 4px solid;
  background: #fffaf6;
  border-radius: 0 8px 8px 0;
  padding: 0.9rem 1.1rem;
  margin: 1rem 0;
  font-size: 0.88rem; line-height: 1.6;
  color: var(--restoreid-black);
}

/* ── Interpretation card ────────────────────────────── */
.interp-card {
  border-radius: 8px; padding: 1rem 1.2rem;
  margin: 0.8rem 0; font-size: 0.88rem;
  line-height: 1.65; color: var(--restoreid-black);
}

/* ── Network diagram ────────────────────────────────── */
.network-container {
  background: white; border: 1px solid var(--restoreid-border);
  border-radius: 8px; padding: 1rem;
  overflow-x: auto; margin: 1rem 0;
}

/* ── Plot wrapper ───────────────────────────────────── */
.plot-wrap {
  background: white; border: 1px solid var(--restoreid-border);
  border-radius: 8px; padding: 1rem;
  margin-bottom: 1rem;
}

/* ── Section header ─────────────────────────────────── */
.section-head {
  font-size: 0.75rem; font-weight: 700;
  text-transform: uppercase; letter-spacing: 0.08em;
  color: var(--restoreid-teal); margin: 1.2rem 0 0.5rem;
}

/* ── Footer ─────────────────────────────────────────── */
.app-footer {
  align-items: center;
  border-top: 1px solid var(--restoreid-border);
  color: var(--restoreid-muted);
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  justify-content: center;
  font-size: 0.78rem;
  line-height: 1.5;
  margin: 1.5rem 1.5rem 0;
  padding: 1rem 0 1.5rem;
  text-align: left;
}
.eu-funded-logo {
  display: block;
  width: min(360px, 100%);
  height: auto;
}
.eu-disclaimer {
  max-width: 560px;
}
.form-control { border-color: var(--restoreid-border); }
.shiny-input-container:has(#active_model),
.shiny-input-container:has(#active_scenario) {
  display: none;
}
"""

# ============================================================
# UI
# ============================================================
app_ui = ui.page_fluid(
    ui.tags.head(
        ui.tags.link(
            rel="stylesheet",
            href="https://fonts.googleapis.com/css2?family=Lato:wght@400;700&family=Sentient:wght@500;600;700&display=swap"
        ),
        ui.tags.style(CSS),
    ),
    ui.layout_sidebar(
        # ── SIDEBAR ──────────────────────────────────────────
        ui.sidebar(
            ui.div(
                ui.div(
                    ui.tags.img(src="www/restoreid-logo.png", alt="Restoreid", class_="brand-logo"),
                    class_="brand-lockup",
                ),
                ui.div("BBN Disease Risk Explorer", class_="sidebar-title"),
                ui.div(
                    "Bayesian Network decision support tool for landscape restoration policy.",
                    class_="sidebar-subtitle"
                ),
            ),
            ui.div("Select model", class_="section-head"),
            ui.HTML("""
            <button class="model-btn mosquito active" id="btn_mosquito"
              onclick="selectModel('mosquito')">
              🦟 Mosquito-borne disease
            </button>
            <button class="model-btn rodent" id="btn_rodent"
              onclick="selectModel('rodent')">
              🐭 Rodent-borne disease
            </button>
            <button class="model-btn tick" id="btn_tick"
              onclick="selectModel('tick')">
              🕷️ Tick-borne disease
            </button>
            <button class="model-btn zoonotic" id="btn_zoonotic"
              onclick="selectModel('zoonotic')">
              🦠 Direct-contact zoonoses
            </button>
            """),
            ui.div("Select scenario", class_="section-head"),
            ui.HTML("""
            <div id="scenario-buttons">
              <button class="scenario-btn active" id="sbtn_none"
                onclick="selectScenario('none')">No restoration</button>
              <button class="scenario-btn" id="sbtn_low"
                onclick="selectScenario('low')">Low intensity</button>
              <button class="scenario-btn" id="sbtn_moderate"
                onclick="selectScenario('moderate')">Moderate intensity</button>
              <button class="scenario-btn" id="sbtn_high"
                onclick="selectScenario('high')">High intensity</button>
            </div>
            """),
            # Hidden inputs updated by JS
            ui.input_text("active_model",    "", value="mosquito"),
            ui.input_text("active_scenario", "", value="none"),
            ui.hr(),
            ui.div(
                "Results are pre-computed from Monte Carlo simulations (n=1,000) of "
                "Bayesian Belief Networks. Shaded areas show 95% credible intervals.",
                style="font-size:0.75rem; color:rgba(12,12,12,0.62); line-height:1.5;"
            ),
            width=260,
        ),

        # ── MAIN PANEL ────────────────────────────────────────
        ui.div(
            ui.navset_tab(
                # ── TAB 1: OVERVIEW ──────────────────────────
                ui.nav_panel(
                    "Overview",
                    ui.output_ui("overview_panel"),
                ),
                # ── TAB 2: DISEASE RISK ──────────────────────
                ui.nav_panel(
                    "Disease risk",
                    ui.output_ui("risk_panel"),
                ),
                # ── TAB 3: ECOLOGICAL RECOVERY ───────────────
                ui.nav_panel(
                    "Ecological recovery",
                    ui.output_ui("ecology_panel"),
                ),
                # ── TAB 4: NETWORK DIAGRAM ───────────────────
                ui.nav_panel(
                    "Causal model",
                    ui.output_ui("network_panel"),
                ),
                # ── TAB 5: COMPARE MODELS ────────────────────
                ui.nav_panel(
                    "Compare models",
                    ui.output_ui("compare_panel"),
                ),
                # ── TAB 6: FUNDING SCENARIOS ──────────────────
                ui.nav_panel(
                    "Funding scenarios",
                    ui.output_ui("funding_panel"),
                ),
            ),
            style="padding: 1rem 1.5rem;"
        ),
    ),
    ui.div(
        ui.tags.img(
            src="www/eu-funded-logo.png",
            alt="Funded by the European Union",
            class_="eu-funded-logo",
        ),
        ui.span(
            "Co-funded by the European Union. Views and opinions expressed are those of the authors only "
            "and do not necessarily reflect those of the European Union.",
            class_="eu-disclaimer",
        ),
        class_="app-footer",
    ),

    # ── JS: model + scenario selection ───────────────────────
    ui.tags.script("""
    const MODEL_COLORS = {
      mosquito: '#005252',
      rodent:   '#f4ae6f',
      tick:     '#46bb86',
      zoonotic: '#0c0c0c',
    };

    function selectModel(m) {
      ['mosquito','rodent','tick','zoonotic'].forEach(x => {
        var b = document.getElementById('btn_' + x);
        if (b) b.classList.toggle('active', x === m);
      });
      Shiny.setInputValue('active_model', m, {priority: 'event'});
      // update scenario button colors
      var c = MODEL_COLORS[m];
      document.querySelectorAll('.scenario-btn.active').forEach(function(el) {
        el.style.background = c;
      });
    }

    function selectScenario(s) {
      ['none','low','moderate','high'].forEach(x => {
        var b = document.getElementById('sbtn_' + x);
        if (b) {
          b.classList.toggle('active', x === s);
          if (x === s) {
            var m = document.getElementById('active_model') &&
                    document.getElementById('active_model').value || 'mosquito';
            // get active model from hidden input via Shiny
            b.style.background = '';
          } else {
            b.style.background = '';
          }
        }
      });
      Shiny.setInputValue('active_scenario', s, {priority: 'event'});
    }

    // Color active scenario button based on current model
    $(document).on('shiny:value', function(event) {
      if (event.name === 'active_model' || event.name === 'active_scenario') {
        setTimeout(function() {
          var m = document.querySelector('.model-btn.active');
          if (!m) return;
          var cls = ['mosquito','rodent','tick','zoonotic'].find(x => m.classList.contains(x));
          var c = MODEL_COLORS[cls] || '#005252';
          document.querySelectorAll('.scenario-btn.active').forEach(function(el) {
            el.style.background = c;
          });
        }, 50);
      }
    });
    """),
)

# ============================================================
# SERVER
# ============================================================
def server(input, output, session):

    # Reactive model / scenario getters
    @reactive.calc
    def model_data():
        m = input.active_model() or "mosquito"
        return ALL_MODELS.get(m, ALL_MODELS["mosquito"])

    @reactive.calc
    def scenario_data():
        m = model_data()
        s = input.active_scenario() or "none"
        return m["scenarios"].get(s, m["scenarios"]["none"])

    # ── OVERVIEW TAB ─────────────────────────────────────────
    @output
    @render.ui
    def overview_panel():
        m   = model_data()
        s   = input.active_scenario() or "none"
        sd  = scenario_data()
        col = m["color"]
        scen_label = SCENARIO_LABELS.get(s, s)

        risk_pct  = f"{sd['mean_disease']*100:.0f}%"
        risk_lo   = f"{sd['lower_disease']*100:.0f}%"
        risk_hi   = f"{sd['upper_disease']*100:.0f}%"
        reg_pct   = f"{sd['mean_regulation']*100:.0f}%"
        stab_pct  = f"{sd['mean_stability']*100:.0f}%"

        # badge colour
        risk_val = sd["mean_disease"]
        if risk_val < 0.25:
            badge_col, badge_bg, badge_txt = "#276749", "#c6f6d5", "Low risk"
        elif risk_val < 0.50:
            badge_col, badge_bg, badge_txt = "#92400e", "#fef3c7", "Moderate risk"
        else:
            badge_col, badge_bg, badge_txt = "#9b2c2c", "#fed7d7", "High risk"

        baseline = m["scenarios"]["none"]["mean_disease"]
        vs_base  = ((risk_val - baseline) / baseline) * 100
        delta_str = (
            f"↓ {abs(vs_base):.0f}% vs. baseline" if vs_base < 0
            else f"↑ {abs(vs_base):.0f}% vs. baseline" if vs_base > 0
            else "Same as baseline"
        )
        delta_col = "#005252" if vs_base < 0 else ("#0c0c0c" if vs_base > 0 else "#46bb86")

        interp = m["interpretation"][s]

        return ui.div(
            # Header
            ui.div(
                ui.h3(f"{m['icon']} {m['label']}", style=f"color:{col}; margin:0 0 0.25rem;"),
                ui.div(
                    f"Scenario: {scen_label}",
                    style="font-size:0.82rem; color:rgba(12,12,12,0.62);"
                ),
                style="margin-bottom:1.2rem;"
            ),

            # Metric row
            ui.layout_columns(
                ui.div(
                    ui.div("Disease risk probability", class_="metric-label"),
                    ui.div(risk_pct, class_="metric-value", style=f"color:{col};"),
                    ui.div(f"95% CI: {risk_lo} – {risk_hi}", class_="metric-range"),
                    ui.div(
                        ui.span(badge_txt, style=f"background:{badge_bg}; color:{badge_col};",
                                class_="metric-badge"),
                        ui.span(f"  {delta_str}",
                                style=f"font-size:0.78rem; color:{delta_col}; margin-left:0.4rem;"),
                    ),
                    class_="metric-card",
                ),
                ui.div(
                    ui.div("Ecological regulation (strong)", class_="metric-label"),
                    ui.div(reg_pct, class_="metric-value", style=f"color:{col};"),
                    ui.div("Probability of strong natural regulation", class_="metric-range"),
                    class_="metric-card",
                ),
                ui.div(
                    ui.div("Long-term stabilisation (8–15 yr)", class_="metric-label"),
                    ui.div(stab_pct, class_="metric-value", style=f"color:{col};"),
                    ui.div("Probability ecosystem stable by year 15", class_="metric-range"),
                    class_="metric-card",
                ),
                col_widths=[4, 4, 4],
            ),

            # Interpretation
            ui.div(
                ui.div("Scenario interpretation", class_="section-head"),
                ui.div(interp, class_="interp-card",
                       style=f"background:{m['color_bg']}; border-left:4px solid {col};"),
            ),

            # Mechanism
            ui.div(
                ui.div("How this model works", class_="section-head"),
                ui.div(
                    ui.div("Causal mechanism", style="font-weight:600; font-size:0.82rem; margin-bottom:0.4rem;"),
                    ui.div(m["mechanism"], style="font-size:0.86rem; line-height:1.65;"),
                    class_="insight-box",
                    style=f"border-left-color:{col};"
                ),
            ),

            # Key policy insight
            ui.div(
                ui.div("Key policy insight", class_="section-head"),
                ui.div(
                    ui.div("🔑 What policymakers need to know",
                           style="font-weight:600; font-size:0.82rem; margin-bottom:0.4rem;"),
                    ui.div(m["key_insight"], style="font-size:0.86rem; line-height:1.65;"),
                    class_="insight-box",
                    style=f"border-left-color:{col}; background:#fffaf6;"
                ),
            ),
        )

    # ── DISEASE RISK TAB ─────────────────────────────────────
    @output
    @render.ui
    def risk_panel():
        m = model_data()
        plot_html = disease_risk_plot(m)
        return ui.div(
            ui.div(
                ui.h4("Disease risk across restoration intensities",
                      style=f"color:{m['color']}; margin-bottom:0.3rem;"),
                ui.div(
                    "Each point shows the mean disease risk probability for the selected disease system. "
                    "Shaded band shows 95% credible interval across 1,000 Monte Carlo iterations.",
                    style="font-size:0.82rem; color:rgba(12,12,12,0.62); margin-bottom:1rem;"
                ),
                ui.HTML(plot_html),
                class_="plot-wrap",
            ),
            ui.div(
                ui.div("Reading this chart", class_="section-head"),
                ui.div(
                    "The horizontal dashed line marks the no-restoration baseline — the disease "
                    "risk expected without any intervention. Points above this line indicate "
                    "that a restoration intensity temporarily worsens outcomes; points below "
                    "indicate net benefit. Wider shaded bands signal greater uncertainty.",
                    class_="insight-box",
                    style=f"border-left-color:{m['color']};"
                ),
            ),
        )

    # ── ECOLOGY TAB ──────────────────────────────────────────
    @output
    @render.ui
    def ecology_panel():
        m = model_data()
        reg_html  = regulation_plot(m)
        traj_html = stability_trajectory_plot(m)
        return ui.div(
            ui.layout_columns(
                ui.div(
                    ui.h5("Ecological regulation recovery",
                          style=f"color:{m['color']};"),
                    ui.div(
                        "Probability of strong natural regulation (predators, competitors) "
                        "as a function of restoration intensity.",
                        style="font-size:0.8rem; color:rgba(12,12,12,0.62); margin-bottom:0.5rem;"
                    ),
                    ui.HTML(reg_html),
                    class_="plot-wrap",
                ),
                ui.div(
                    ui.h5("Stabilisation trajectories over time",
                          style=f"color:{m['color']};"),
                    ui.div(
                        "Probability distribution of time-to-stable-state by restoration "
                        "intensity. Later peaks indicate longer but ultimately more stable outcomes.",
                        style="font-size:0.8rem; color:rgba(12,12,12,0.62); margin-bottom:0.5rem;"
                    ),
                    ui.HTML(traj_html),
                    class_="plot-wrap",
                ),
                col_widths=[6, 6],
            ),
        )

    # ── NETWORK TAB ──────────────────────────────────────────
    @output
    @render.ui
    def network_panel():
        m   = model_data()
        key = input.active_model() or "mosquito"
        diagram_html = network_diagram_html(key, m["color"])
        return ui.div(
            ui.h4("Causal network structure",
                  style=f"color:{m['color']}; margin-bottom:0.3rem;"),
            ui.div(
                "The diagram below shows the Bayesian Belief Network structure — each arrow "
                "represents a direct probabilistic influence. Nodes are the key variables; "
                "intervention enters at Restoration Intensity.",
                style="font-size:0.82rem; color:rgba(12,12,12,0.62); margin-bottom:1rem;"
            ),
            ui.HTML(f'<div class="network-container">{diagram_html}</div>'),
            ui.div(
                ui.div("How to read this diagram", class_="section-head"),
                ui.div(
                    "Arrows show the direction of causal influence. The model computes "
                    "posterior probability distributions for all downstream nodes given "
                    "evidence set on restoration intensity and other upstream ecological drivers. "
                    "Conditional probability tables were specified by expert elicitation and "
                    "sampled 1,000 times via Monte Carlo to quantify uncertainty.",
                    class_="insight-box",
                    style=f"border-left-color:{m['color']};"
                ),
            ),
        )

    # ── FUNDING SCENARIOS TAB ────────────────────────────────
    @output
    @render.ui
    def funding_panel():
        return ui.div(
            ui.h4("Funding scenario explorer", style="color:#005252; margin-bottom:0.3rem;"),
            ui.div(
                "Drag the slider to explore what happens if a restoration project changes "
                "intensity at a different point in its 15-year lifecycle. Results reflect the "
                "ecosystem's accumulated ecological legacy at the transition point — projects "
                "that have already stabilised are harder to redirect.",
                style="font-size:0.82rem; color:rgba(12,12,12,0.62); margin-bottom:1.2rem;"
            ),

            ui.layout_columns(
                ui.div(
                    ui.div("Scenario direction", class_="section-head"),
                    ui.input_radio_buttons(
                        "funding_direction",
                        None,
                        choices={
                            "rampup_low":  "📈 Ramp-up: Low → High",
                            "rampup_mod":  "📈 Ramp-up: Moderate → High",
                            "collapse":    "📉 Funding collapse: High → Low",
                        },
                        selected="rampup_low",
                    ),
                    ui.div("Disease system", class_="section-head"),
                    ui.input_radio_buttons(
                        "funding_system",
                        None,
                        choices={
                            "mosquito": "🦟 Mosquito-borne",
                            "tick":     "🕷️ Tick-borne",
                            "rodent":   "🐭 Rodent-borne",
                            "zoonotic": "🦠 Direct-contact zoonoses",
                            "all":      "📊 Compare all 4 systems",
                        },
                        selected="mosquito",
                    ),
                    col_widths=12,
                ),
                col_widths=[12],
            ),

            ui.div("Transition year", class_="section-head"),
            ui.input_slider(
                "transition_year",
                None,
                min=0, max=15, value=5, step=0.5,
                post=" yr",
            ),
            ui.div(
                "Year 0 = transition happens immediately (no time spent at the starting intensity). "
                "Year 15 = no transition occurs (stays at starting intensity for the full project).",
                style="font-size:0.78rem; color:rgba(12,12,12,0.62); margin:-0.4rem 0 1rem;"
            ),

            ui.output_ui("funding_result_cards"),
            ui.output_ui("funding_curve_plot"),

            ui.div("Reading this chart", class_="section-head"),
            ui.div(
                "The curve shows the eventual (year-15) disease risk depending on when the "
                "restoration intensity change happens. The further right your transition point, "
                "the more years were spent at the starting intensity — and the more of that "
                "ecological trajectory carries forward, even after the change. This is why a "
                "late ramp-up only partially recovers the benefit of high-intensity restoration, "
                "and why a late funding collapse only partially erodes the benefit already gained.",
                class_="insight-box",
                style="border-left-color:#005252;"
            ),
        )

    @reactive.calc
    def funding_phases():
        direction = input.funding_direction()
        if direction == "rampup_low":
            return "low", "high", "Ramp-up (Low → High)"
        elif direction == "rampup_mod":
            return "moderate", "high", "Ramp-up (Moderate → High)"
        else:
            return "high", "low", "Funding collapse (High → Low)"

    @output
    @render.ui
    def funding_result_cards():
        p1, p2, label = funding_phases()
        t = input.transition_year()
        sysname = input.funding_system()

        if sysname == "all":
            cards = []
            for sk in SYSTEMS:
                meta = MODEL_META[sk]
                risk = risk_at_transition(sk, p1, p2, t)
                baseline_p1 = BASELINE_RISK[sk][p1]
                delta = risk - baseline_p1
                cards.append(
                    ui.div(
                        ui.div(f"{meta['icon']} {meta['label']}", class_="metric-label",
                               style="text-transform:none; font-size:0.82rem; font-weight:600;"),
                        ui.div(f"{risk*100:.0f}%", class_="metric-value",
                               style=f"color:{meta['color']};"),
                        ui.div(
                            f"{'↑' if delta > 0 else '↓' if delta < 0 else '='} "
                            f"{abs(delta)*100:.0f}pp vs. pure {p1}",
                            class_="metric-range",
                        ),
                        class_="metric-card",
                    )
                )
            return ui.layout_columns(*cards, col_widths=[3, 3, 3, 3])
        else:
            meta = MODEL_META[sysname]
            risk = risk_at_transition(sysname, p1, p2, t)
            risk_p1 = BASELINE_RISK[sysname][p1]
            risk_p2 = BASELINE_RISK[sysname][p2]
            return ui.layout_columns(
                ui.div(
                    ui.div(f"Year-15 risk at t={t:g} yr", class_="metric-label"),
                    ui.div(f"{risk*100:.0f}%", class_="metric-value",
                           style=f"color:{meta['color']};"),
                    ui.div("Resulting disease risk probability", class_="metric-range"),
                    class_="metric-card",
                ),
                ui.div(
                    ui.div(f"Pure {p1} (no transition)", class_="metric-label"),
                    ui.div(f"{risk_p1*100:.0f}%", class_="metric-value", style="color:rgba(12,12,12,0.62);"),
                    ui.div("Reference: stays at starting intensity", class_="metric-range"),
                    class_="metric-card",
                ),
                ui.div(
                    ui.div(f"Pure {p2} (immediate transition)", class_="metric-label"),
                    ui.div(f"{risk_p2*100:.0f}%", class_="metric-value", style="color:rgba(12,12,12,0.62);"),
                    ui.div("Reference: starts at new intensity from year 0", class_="metric-range"),
                    class_="metric-card",
                ),
                col_widths=[4, 4, 4],
            )

    @output
    @render.ui
    def funding_curve_plot():
        p1, p2, label = funding_phases()
        t = input.transition_year()
        sysname = input.funding_system()

        if sysname == "all":
            html = multi_system_transition_plot(p1, p2, t)
        else:
            html = transition_curve_plot(sysname, p1, p2, t, label)

        return ui.div(ui.HTML(html), class_="plot-wrap")


    @output
    @render.ui
    def compare_panel():
        comp_html = comparison_plot(ALL_MODELS)
        return ui.div(
            ui.h4("Disease risk comparison across models",
                  style="color:#005252; margin-bottom:0.3rem;"),
            ui.div(
                "Mean disease risk probability for each restoration scenario, across all four "
                "disease systems. Dashed lines connect scenarios within each model.",
                style="font-size:0.82rem; color:rgba(12,12,12,0.62); margin-bottom:1rem;"
            ),
            ui.HTML(f'<div class="plot-wrap">{comp_html}</div>'),

            ui.div("Key contrasts", class_="section-head"),
            ui.layout_columns(
                ui.div(
                    ui.div("🦟 Mosquito", style="font-weight:700; color:#005252;"),
                    ui.div("Hump pattern. Risk peaks at low restoration before falling "
                           "below baseline. Manage early-phase risk carefully.",
                           style="font-size:0.83rem; margin-top:0.3rem; color:#0c0c0c;"),
                    class_="metric-card",
                ),
                ui.div(
                    ui.div("🐭 Rodent", style="font-weight:700; color:#f4ae6f;"),
                    ui.div("Monotonic decline. Every increment of restoration reduces risk. "
                           "Clearest policy signal. No transitional risk peak.",
                           style="font-size:0.83rem; margin-top:0.3rem; color:#0c0c0c;"),
                    class_="metric-card",
                ),
                ui.div(
                    ui.div("🕷️ Tick", style="font-weight:700; color:#46bb86;"),
                    ui.div("Hump + very delayed recovery. Trophic cascades take 10–15 years. "
                           "Highest planning horizon of the four systems.",
                           style="font-size:0.83rem; margin-top:0.3rem; color:#0c0c0c;"),
                    class_="metric-card",
                ),
                ui.div(
                    ui.div("🦠 Zoonoses", style="font-weight:700; color:#0c0c0c;"),
                    ui.div("Steady but shallow decline. Highest residual risk even at full "
                           "restoration (~50%). Needs complementary contact-reduction measures.",
                           style="font-size:0.83rem; margin-top:0.3rem; color:#0c0c0c;"),
                    class_="metric-card",
                ),
                col_widths=[3, 3, 3, 3],
            ),
        )


app = App(app_ui, server)
