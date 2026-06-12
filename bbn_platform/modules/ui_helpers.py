"""UI helper components (kept minimal — most UI is inline in app.py)."""
from shiny import ui


def scenario_card(label, value, color, note=""):
    return ui.div(
        ui.div(label, class_="metric-label"),
        ui.div(value, class_="metric-value", style=f"color:{color};"),
        ui.div(note, class_="metric-range") if note else ui.div(),
        class_="metric-card",
    )


def model_header(icon, name, color, subtitle=""):
    return ui.div(
        ui.h3(f"{icon} {name}", style=f"color:{color}; margin:0 0 0.2rem;"),
        ui.div(subtitle, style="font-size:0.82rem; color:#718096;") if subtitle else ui.div(),
        style="margin-bottom:1rem;",
    )


def insight_box(content, color, bg="#f7fafc"):
    return ui.div(
        content,
        class_="insight-box",
        style=f"border-left-color:{color}; background:{bg};",
    )
