"""
Network diagram module.
Returns inline SVG strings showing the DAG structure for each BBN model.
"""


def network_diagram_html(model_key: str, color: str) -> str:
    diagrams = {
        "mosquito": _mosquito_dag(color),
        "rodent":   _rodent_dag(color),
        "tick":     _tick_dag(color),
        "zoonotic": _zoonotic_dag(color),
    }
    return diagrams.get(model_key, "")


# ── ZOONOTIC DAG ─────────────────────────────────────────────
# Restoration Intensity (driver)
# → Habitat Disturbance
#     → Host Diversity
#     → Human Wildlife Contact (also direct from Restoration)
# Host Diversity + Human Wildlife Contact → MultiHost Amplification
# MultiHost Amplification → Direct Transmission Risk
# Restoration + Host Diversity → Resilient Ecological Regulation
# Restoration + Direct Transmission Risk + Resilient Ecological Regulation
#   → Time to Stable State
def _zoonotic_dag(color: str) -> str:
    G = "#f4ebe4"
    A = "#0c0c0c"
    T = "#005252"
    W = "#ffffff"

    nodes = (
        _node(300,  20, 190, 42, "Restoration intensity",  "policy lever",     A, W) +
        _node(140, 100, 170, 42, "Habitat disturbance",    "land condition",   G, T) +
        _node( 20, 180, 150, 42, "Host diversity",         "biodiversity",     G, T) +
        _node(230, 180, 190, 42, "Human-wildlife contact", "interface",        G, T) +
        _node(120, 260, 190, 42, "Multi-host amplification","spillover",       G, T) +
        _node(120, 340, 200, 46, "Direct transmission risk","outcome",         A, W) +
        _node(380, 180, 200, 42, "Resilient ecol. regulation","natural control", G, T) +
        _node(380, 340, 190, 42, "Time to stable state",   "stabilisation",    G, T)
    )

    arrows = (
        _arrow(370,  62, 270, 98)   +   # Restoration → Disturbance
        _arrow(190, 142, 110, 178)  +   # Disturbance → HostDiv
        _arrow(240, 142, 310, 178)  +   # Disturbance → Contact
        _bezier(460, 62, 480, 178, 520, 110) +  # Restoration → Contact (direct, bent)
        _arrow(110, 222, 195, 258)  +   # HostDiv → Amplification
        _arrow(320, 222, 245, 258)  +   # Contact → Amplification
        _arrow(215, 302, 215, 338)  +   # Amplification → Disease
        _bezier(95, 222, 420, 220, 250, 200) +  # HostDiv → EcoReg (bent, long)
        _bezier(420, 62, 460, 178, 520, 100) +  # Restoration → EcoReg
        _bezier(310, 363, 420, 340, 360, 350) +  # Disease → Time
        _bezier(460, 222, 470, 338, 480, 280)    # EcoReg → Time
    )

    legend = (
        f'<rect x="20" y="405" width="12" height="12" rx="2" fill="{A}"/>'
        f'<text x="38" y="416" style="{LABEL_STYLE}">Policy lever / outcome</text>'
        f'<rect x="200" y="405" width="12" height="12" rx="2" fill="{G}" stroke="{A}" stroke-width="1"/>'
        f'<text x="218" y="416" style="{LABEL_STYLE}">Intermediate variable</text>'
    )

    return (
        f'<svg width="100%" viewBox="0 0 600 430" role="img">'
        f'<title>Direct-contact zoonoses BBN structure</title>'
        f'<desc>Causal network: Restoration reduces Habitat Disturbance, which increases '
        f'Host Diversity and reduces Human-Wildlife Contact. These combine to determine '
        f'Multi-Host Amplification and Direct Transmission Risk. Restoration also directly '
        f'builds Resilient Ecological Regulation.</desc>'
        + DEFS + arrows + nodes + legend +
        f'</svg>'
    )
DEFS = """<defs>
  <marker id="arr" viewBox="0 0 10 10" refX="8" refY="5"
    markerWidth="6" markerHeight="6" orient="auto-start-reverse">
    <path d="M2 1L8 5L2 9" fill="none" stroke="#6f6862"
          stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
  </marker>
</defs>"""

NODE_STYLE  = "font-family:'Lato',sans-serif; font-size:11px; font-weight:700;"
LABEL_STYLE = "font-family:'Lato',sans-serif; font-size:9.5px; fill:#6f6862;"
LINE_STYLE  = 'stroke="#6f6862" stroke-width="1.2" fill="none" marker-end="url(#arr)"'


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
#   Restoration Intensity (top-right)
#   Hydrological Recovery (mid-left)
#   Standing Water        (mid-centre)
#   Ecological Regulation (mid-right)
#   Mosquito Disease Risk (lower-centre)
#   Time to Stable State  (bottom-right)
def _mosquito_dag(color: str) -> str:
    G = "#f4ebe4"   # node fill (light)
    A = "#005252"   # accent
    T = "#005252"   # text on light
    W = "#ffffff"   # text on accent

    nodes = (
        _node(320,  20, 200, 44, "Restoration intensity", "policy lever",         A, W) +
        _node( 40, 110, 160, 44, "Hydrological recovery", "hydrology",            G, T) +
        _node(230, 110, 140, 44, "Standing water",        "mosquito habitat",     G, T) +
        _node(430, 110, 160, 44, "Ecological regulation", "natural control",      G, T) +
        _node(200, 210, 180, 48, "Mosquito disease risk", "outcome",              A, W) +
        _node(440, 210, 160, 44, "Time to stable state",  "stabilisation",        G, T)
    )

    arrows = (
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
        f'<desc>Causal network: Restoration Intensity drives Hydrological Recovery '
        f'and Ecological Regulation, which jointly determine '
        f'Mosquito Disease Risk and Time to Stable State.</desc>'
        + DEFS + arrows + nodes + legend +
        f'</svg>'
    )


# ── RODENT DAG ───────────────────────────────────────────────
# Restoration → Habitat Quality
# Habitat Quality → Rodent Abundance → Disease Risk
# Disease Risk → Ecological Regulation ← Restoration
# Ecological Regulation → Time to Stable State
def _rodent_dag(color: str) -> str:
    G = "#fff6ef"
    A = "#f4ae6f"
    T = "#0c0c0c"
    W = "#0c0c0c"

    nodes = (
        _node(340,  20, 200, 44, "Restoration intensity", "policy lever",         A, W) +
        _node(180, 110, 150, 44, "Habitat quality",       "biodiversity",         G, T) +
        _node(180, 210, 150, 44, "Rodent abundance",      "reservoir host",       G, T) +
        _node(180, 310, 160, 48, "Rodent disease risk",   "outcome",              A, W) +
        _node(400, 210, 170, 44, "Ecological regulation", "natural control",      G, T) +
        _node(400, 310, 160, 44, "Time to stable state",  "stabilisation",        G, T)
    )

    arrows = (
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
    G = "#f4ebe4"
    A = "#46bb86"
    T = "#005252"
    W = "#0c0c0c"

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
