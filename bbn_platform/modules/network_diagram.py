"""
Network diagram module.
Returns inline SVG strings showing the DAG structure for each BBN model.
"""


def network_diagram_html(model_key: str, color: str) -> str:
    diagrams = {
        "mosquito": _mosquito_dag(color),
        "rodent":   _rodent_dag(color),
        "tick":     _tick_dag(color),
    }
    return diagrams.get(model_key, "")


# ── shared arrow marker ───────────────────────────────────────
DEFS = """<defs>
  <marker id="arr" viewBox="0 0 10 10" refX="8" refY="5"
    markerWidth="6" markerHeight="6" orient="auto-start-reverse">
    <path d="M2 1L8 5L2 9" fill="none" stroke="#718096"
          stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
  </marker>
</defs>"""

NODE_STYLE  = "font-family:'Inter',sans-serif; font-size:11px; font-weight:600;"
LABEL_STYLE = "font-family:'Inter',sans-serif; font-size:9.5px; fill:#718096;"
LINE_STYLE  = 'stroke="#a0aec0" stroke-width="1.2" fill="none" marker-end="url(#arr)"'


def _node(x, y, w, h, label, sublabel, fill, text_col, rx=8):
    cx = x + w / 2
    ty = y + h / 2 - (6 if sublabel else 0)
    sy = y + h / 2 + 10
    sub = (
        f'<text x="{cx}" y="{sy}" text-anchor="middle" '
        f'style="{LABEL_STYLE}">{sublabel}</text>'
        if sublabel else ""
    )
    return (
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" '
        f'fill="{fill}" stroke="{fill}" stroke-width="1.5" opacity="0.92"/>'
        f'<text x="{cx}" y="{ty}" text-anchor="middle" dominant-baseline="central" '
        f'fill="{text_col}" style="{NODE_STYLE}">{label}</text>'
        + sub
    )


def _arrow(x1, y1, x2, y2):
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" {LINE_STYLE}/>'


def _bezier(x1, y1, x2, y2, cx1=None, cy1=None):
    if cx1 is None:
        cx1 = (x1 + x2) / 2
    if cy1 is None:
        cy1 = (y1 + y2) / 2
    return (
        f'<path d="M{x1},{y1} Q{cx1},{cy1} {x2},{y2}" '
        f'{LINE_STYLE}/>'
    )


# ── MOSQUITO DAG ─────────────────────────────────────────────
# Nodes:
#   Region Context        (top-left)
#   Restoration Intensity (top-right)
#   Hydrological Recovery (mid-left)
#   Standing Water        (mid-centre)
#   Ecological Regulation (mid-right)
#   Mosquito Disease Risk (lower-centre)
#   Time to Stable State  (bottom-right)
def _mosquito_dag(color: str) -> str:
    G = "#eaf3fb"   # node fill (light)
    A = "#2171b5"   # accent
    T = "#1a365d"   # text on light
    W = "#ffffff"   # text on accent

    nodes = (
        _node( 40,  20, 160, 44, "Region context",        "exogenous",            G, T) +
        _node(320,  20, 200, 44, "Restoration intensity", "policy lever",         A, W) +
        _node( 40, 110, 160, 44, "Hydrological recovery", "hydrology",            G, T) +
        _node(230, 110, 140, 44, "Standing water",        "mosquito habitat",     G, T) +
        _node(430, 110, 160, 44, "Ecological regulation", "natural control",      G, T) +
        _node(200, 210, 180, 48, "Mosquito disease risk", "outcome",              A, W) +
        _node(440, 210, 160, 44, "Time to stable state",  "stabilisation",        G, T)
    )

    arrows = (
        _arrow(120,  64, 100, 108)  +   # Region → Hydro
        _arrow(420,  64, 350, 108)  +   # Restoration → Hydro (bent)
        _bezier(420, 44, 510, 108, 520, 60) +   # Restoration → EcoReg
        _arrow(200, 154, 260, 208)  +   # Hydro → StandingWater
        _arrow(360,  64, 300, 108)  +   # Restoration → Hydro
        _arrow(300, 154, 290, 208)  +   # StandingWater → Disease
        _arrow(510, 154, 390, 208)  +   # EcoReg → Disease (bent)
        _arrow(510, 154, 520, 208)      # EcoReg → Time
    )

    # legend
    legend = (
        f'<rect x="40" y="280" width="12" height="12" rx="2" fill="{A}"/>'
        f'<text x="58" y="291" style="{LABEL_STYLE}">Policy lever / outcome</text>'
        f'<rect x="180" y="280" width="12" height="12" rx="2" fill="{G}" stroke="{A}" stroke-width="1"/>'
        f'<text x="198" y="291" style="{LABEL_STYLE}">Intermediate variable</text>'
    )

    return (
        f'<svg width="100%" viewBox="0 0 640 305" role="img">'
        f'<title>Mosquito-borne disease BBN structure</title>'
        f'<desc>Causal network: Region Context and Restoration Intensity drive '
        f'Hydrological Recovery and Ecological Regulation, which jointly determine '
        f'Mosquito Disease Risk and Time to Stable State.</desc>'
        + DEFS + arrows + nodes + legend +
        f'</svg>'
    )


# ── RODENT DAG ───────────────────────────────────────────────
# Region → Habitat Quality ← Restoration
# Habitat Quality → Rodent Abundance → Disease Risk
# Disease Risk → Ecological Regulation ← Restoration
# Ecological Regulation → Time to Stable State
def _rodent_dag(color: str) -> str:
    G = "#fff0ef"
    A = "#cb181d"
    T = "#4a0014"
    W = "#ffffff"

    nodes = (
        _node( 40,  20, 155, 44, "Region context",        "exogenous",            G, T) +
        _node(340,  20, 200, 44, "Restoration intensity", "policy lever",         A, W) +
        _node(180, 110, 150, 44, "Habitat quality",       "biodiversity",         G, T) +
        _node(180, 210, 150, 44, "Rodent abundance",      "reservoir host",       G, T) +
        _node(180, 310, 160, 48, "Rodent disease risk",   "outcome",              A, W) +
        _node(400, 210, 170, 44, "Ecological regulation", "natural control",      G, T) +
        _node(400, 310, 160, 44, "Time to stable state",  "stabilisation",        G, T)
    )

    arrows = (
        _arrow(118,  64, 220, 108)  +   # Region → Habitat
        _arrow(440,  64, 300, 108)  +   # Restoration → Habitat
        _arrow(255, 154, 255, 208)  +   # Habitat → Rodent
        _arrow(255, 254, 260, 308)  +   # Rodent → Disease
        _bezier(340, 44, 485, 208, 500, 120) +  # Restoration → EcoReg
        _bezier(260, 330, 398, 228, 340, 250) +  # Disease → EcoReg
        _arrow(485, 254, 485, 308)      # EcoReg → Time
    )

    legend = (
        f'<rect x="40" y="375" width="12" height="12" rx="2" fill="{A}"/>'
        f'<text x="58" y="386" style="{LABEL_STYLE}">Policy lever / outcome</text>'
        f'<rect x="200" y="375" width="12" height="12" rx="2" fill="{G}" stroke="{A}" stroke-width="1"/>'
        f'<text x="218" y="386" style="{LABEL_STYLE}">Intermediate variable</text>'
    )

    return (
        f'<svg width="100%" viewBox="0 0 620 400" role="img">'
        f'<title>Rodent-borne disease BBN structure</title>'
        f'<desc>Causal network: Restoration improves habitat quality, which suppresses '
        f'rodent abundance, directly reducing disease risk. Ecological regulation builds '
        f'over time with continued restoration.</desc>'
        + DEFS + arrows + nodes + legend +
        f'</svg>'
    )


# ── TICK DAG ─────────────────────────────────────────────────
# Restoration → Host Connectivity (hump)
# Restoration → Predator Recovery (lagged)
# Host Connectivity + Predator Recovery → Tick Disease Risk
# Predator Recovery + Disease → Ecological Regulation
# Ecological Regulation → Time to Stable State
def _tick_dag(color: str) -> str:
    G = "#edf7f0"
    A = "#238b45"
    T = "#1a3d26"
    W = "#ffffff"

    nodes = (
        _node(220,  20, 200, 44, "Restoration intensity", "policy lever",         A, W) +
        _node( 40, 120, 165, 44, "Host connectivity",     "hump shape",           G, T) +
        _node(410, 120, 165, 44, "Predator recovery",     "lagged response",      G, T) +
        _node(195, 230, 175, 48, "Tick disease risk",     "outcome",              A, W) +
        _node(395, 230, 175, 44, "Ecological regulation", "trophic cascade",      G, T) +
        _node(395, 330, 165, 44, "Time to stable state",  "stabilisation",        G, T)
    )

    arrows = (
        _arrow(320,  64, 150, 118)  +   # Restoration → HostConn
        _arrow(320,  64, 490, 118)  +   # Restoration → Predator
        _arrow(130, 164, 250, 228)  +   # HostConn → Disease
        _arrow(490, 164, 370, 228)  +   # Predator → Disease
        _bezier(490, 164, 480, 228, 520, 190) +  # Predator → EcoReg
        _bezier(282, 274, 393, 248, 350, 230) +  # Disease → EcoReg
        _arrow(482, 274, 482, 328)      # EcoReg → Time
    )

    # annotation: hump note
    hump_note = (
        f'<text x="123" y="178" text-anchor="middle" style="{LABEL_STYLE}" fill="#e07b00">'
        f'⚠ peaks at low</text>'
    )

    legend = (
        f'<rect x="40" y="390" width="12" height="12" rx="2" fill="{A}"/>'
        f'<text x="58" y="401" style="{LABEL_STYLE}">Policy lever / outcome</text>'
        f'<rect x="210" y="390" width="12" height="12" rx="2" fill="{G}" stroke="{A}" stroke-width="1"/>'
        f'<text x="228" y="401" style="{LABEL_STYLE}">Intermediate variable</text>'
    )

    return (
        f'<svg width="100%" viewBox="0 0 620 415" role="img">'
        f'<title>Tick-borne disease BBN structure</title>'
        f'<desc>Causal network: Restoration simultaneously increases host connectivity '
        f'(hump-shaped) and slowly drives predator recovery. The combination determines '
        f'tick disease risk; ecological stabilisation is very delayed via trophic cascades.</desc>'
        + DEFS + arrows + nodes + hump_note + legend +
        f'</svg>'
    )
