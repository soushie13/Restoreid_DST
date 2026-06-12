# BBN Disease Risk Explorer — Shiny (Python)

A decision support platform for policymakers evaluating wetland restoration
strategies and their effects on vector-borne disease risk.

---

## Project structure

```
bbn_platform/
├── app.py                   # Main Shiny application
├── requirements.txt
├── data/
│   └── model_summaries.py   # Pre-computed BBN outputs (edit this!)
└── modules/
    ├── plots.py             # Matplotlib chart generation
    ├── network_diagram.py   # SVG DAG diagrams
    └── ui_helpers.py        # Reusable UI components
```

---

## Running locally

```bash
pip install -r requirements.txt
shiny run app.py --reload
```

Open http://localhost:8000 in your browser.

---

## Updating the model data

All BBN outputs live in `data/model_summaries.py`.

After running your R Monte Carlo simulations, update the `scenarios` dict
for each model with the actual computed values:

```python
"scenarios": {
    "none": {
        "mean_disease":      0.38,   # mean of disease_risk
        "lower_disease":     0.28,   # quantile(disease_risk, 0.025)
        "upper_disease":     0.48,   # quantile(disease_risk, 0.975)
        "mean_regulation":   0.07,   # mean of regulation_strong
        "lower_regulation":  0.02,
        "upper_regulation":  0.14,
        "mean_stability":    0.22,   # mean of long_term_stability
        "lower_stability":   0.10,
        "upper_stability":   0.35,
        "years_1_3":         0.47,   # mean of years_1_3
        "years_4_7":         0.30,
        "years_8_12":        0.14,
        "years_13_15":       0.09,
    },
    ...
}
```

Each field maps directly to a column from `mosq_summary` / `rodent_summary` /
`tick_summary` in your R code.

---

## Adding a 4th model

1. Add a new dict to `data/model_summaries.py` following the same schema.
2. Add it to `ALL_MODELS` at the bottom of that file.
3. In `app.py`:
   - Add a model button in the sidebar HTML block.
   - Add it to `MODEL_COLORS` in the JS block.
4. In `modules/network_diagram.py`:
   - Add a new `_yourmodel_dag()` function and register it in `network_diagram_html()`.

---

## Deployment options

### Shiny Server / Posit Connect
Standard deployment — upload the whole folder, set `app.py` as the entrypoint.

### shinylive (WebAssembly / browser-only)
```bash
pip install shinylive
shinylive export . site/
```
Then serve `site/` from any static host (GitHub Pages, Netlify, etc.).

> ⚠️ shinylive uses Pyodide — `matplotlib` works but may be slow on first load.
> The pre-computed data approach (no R runtime needed) is specifically designed
> for this constraint.

---

## Next steps (roadmap)

- [ ] Wire up live inference via a FastAPI backend (for real-time evidence setting)
- [ ] Add free-text question interpreter (LLM → node evidence mapping)
- [ ] Export scenario comparison as PDF report
- [ ] Add a fourth model from your remaining R scripts
