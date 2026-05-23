# PIC Component Library

Parametric **layout-only** silicon photonics cells in [GDSFactory](https://gdsfactory.github.io/gdsfactory/). No simulation in this repo—only geometry you could send to a fab flow later.

Components are added **one at a time**, with physics notes in this README so you know exactly what each pushed file represents.

## Repository layout

```text
├── README.md                 # What each component is and how to install
├── pyproject.toml            # Python 3.11 + gdsfactory (pip install -e .)
├── requirements.txt          # Pinned deps for reproducible CI
├── components/               # One Python file per cell (only finished cells in __init__)
├── scripts/
│   ├── verify_install.py     # Week 1: import gdsfactory, build a straight
│   └── export_gds.py         # Write gds_outputs/*.gds and assets/*.png
├── tests/                    # pytest: ports, GDS write, cell registration
├── notebooks/                # Demos (added with each component)
├── assets/                   # PNG previews embedded in README
└── gds_outputs/              # Example GDS committed for each implemented cell
```

## Install (GitHub / pip only)

Requires **Python 3.11** (GDSFactory supports 3.11–3.13).

```bash
git clone https://github.com/Shahbaz-z/PIC-component-Library.git
cd PIC-component-Library
python3.11 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
python scripts/verify_install.py

GDSFactory 9+ needs an active PDK. Importing `from components import my_waveguide` activates the generic PDK (`gf.gpdk`) automatically.
```

Optional local GDS viewer (not used in CI):

```bash
pip install -e ".[viewer]"   # installs klayout; then component.show() may open KLayout
```

## What gets pushed to GitHub

| Path | Purpose |
|------|---------|
| `components/*.py` | Source for each parametric cell (`@gf.cell` functions) |
| `gds_outputs/*.gds` | Binary layout exported from those cells (default parameters) |
| `assets/*.png` | 2D preview from `component.plot()` for the README |
| `.github/workflows/ci.yml` | Runs tests + re-exports on every push/PR |

When a new component is added, `scripts/export_gds.py` and `tests/test_components.py` are extended so CI proves the new cell builds and writes GDS.

---

## Component 1: Strip waveguide (`my_waveguide`)

**Status:** implemented — [`components/waveguide.py`](components/waveguide.py)

### What it is

A **strip waveguide** is a silicon ridge (core) on buried oxide. In the SOI platform, the wafer often uses ~220 nm thick Si; your layout draws the **in-plane** core width and length. The thickness is defined by the process design kit (PDK), not by this 2D cell.

### How light is guided

- Light is confined by **total internal reflection** at the high-index core vs. low-index cladding (SiO₂).
- The fundamental mode is mostly in the core; some field leaks into the cladding (evanescent tail).
- **Width** changes the effective index \(n_\mathrm{eff}\) and how many modes the guide supports: very narrow cores can be single-mode but bend-sensitive; wider cores can become multimode.

### Parameters (layout units: µm)

| Argument | Default | Meaning |
|----------|---------|---------|
| `length` | `10.0` | Distance along the guide between ports |
| `width` | `0.5` | Core width (typical strip range ~0.4–0.6 µm at 1550 nm) |

### Ports

- `o1` — input (one end of the straight)
- `o2` — output (other end)

These names match GDSFactory’s `straight` so you can connect this cell to couplers and rings later.

### Usage

```python
from components.waveguide import my_waveguide

wg = my_waveguide(length=20.0, width=0.45)
wg.plot()          # matplotlib preview
# wg.show()        # optional: KLayout if .[viewer] installed
print(wg.ports)
```

Regenerate committed artifacts:

```bash
python scripts/export_gds.py
```

### Preview

![Strip waveguide layout](assets/waveguide.png)

---

## Coming next (not in repo yet)

| Component | File | Topic |
|-----------|------|--------|
| 2 — Directional coupler | `components/directional_coupler.py` | Evanescent coupling, gap vs. coupling length |
| 3 — MZI | `components/mzi.py` | Phase arms, \(T = \cos^2(\pi \Delta L \cdot n_g / \lambda)\) |
| 4 — Ring resonator | `components/ring_resonator.py` | \(2\pi r n_\mathrm{eff} = m\lambda\), FSR |

Placeholder files exist so the folder structure is clear; they are not exported from `components/__init__.py` until implemented.

## License

MIT — see [LICENSE](LICENSE).
