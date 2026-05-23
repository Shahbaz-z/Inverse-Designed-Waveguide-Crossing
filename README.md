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
```

GDSFactory 9+ needs an active PDK. Importing from `components` activates the generic PDK (`gf.gpdk`) automatically.

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


---

## Component 2: Directional coupler (`my_directional_coupler`)

**Status:** implemented — [`components/directional_coupler.py`](components/directional_coupler.py)

### What it is

A **directional coupler** is two parallel strip waveguides placed close enough that their optical modes overlap. Power is exchanged between the guides by **evanescent coupling** in the straight section; S-bends separate the buses afterward so you get four accessible ports.

### How coupling works (CMT, no simulation here)

In **coupled-mode theory**, each guide carries a mode amplitude. The coupling coefficient κ (rad/µm in this layout-centric view) sets how fast energy sloshes between guides:

- **Smaller gap** → stronger evanescent overlap → larger κ.
- **Longer `coupling_length`** → more accumulated phase Δφ = κ L → more (or less) power transferred.

For a symmetric coupler, a common result is that the **cross-port power fraction** scales as |sin(κ L)|². A **50:50 splitter** occurs when κ L = π/2, i.e. at the **coupling length** L_c = π / (2κ). This repo does not compute κ from Maxwell’s equations; you sweep `gap` and `coupling_length` in layout and validate later in measurement or EM tools.

### Parameters (layout units: µm)

| Argument | Default | Meaning |
|----------|---------|---------|
| `gap` | `0.2` | Edge-to-edge spacing between the two strip cores in the coupling region |
| `coupling_length` | `10.0` | Length of the parallel coupling section |
| `width` | `0.5` | Strip width of both guides |
| `dx` | `10.0` | Horizontal offset from coupling region to bend (port spacing in x) |
| `dy` | `4.0` | Centerline separation of the two buses outside the coupler |

### Ports (GDSFactory convention)

| Port | Typical role |
|------|----------------|
| `o1` | Input on upper bus |
| `o2` | Through / bar port on upper bus |
| `o3` | Cross port on lower bus |
| `o4` | Input on lower bus |

Exact routing follows `gf.components.coupler`; use `print(dc.ports)` on an instance to inspect coordinates before connecting in a circuit.

### Usage

```python
from components import my_directional_coupler

dc = my_directional_coupler(gap=0.2, coupling_length=10.0, width=0.5)
dc.plot()
print(dc.ports)
```

### Gap sweep (layout + qualitative plot)

`scripts/export_gds.py` writes:

- `gds_outputs/directional_coupler_example.gds` — default parameters above
- `gds_outputs/sweeps/coupler_gap*.gds` — same `coupling_length`, gaps 0.15–0.30 µm (CI artifact; not committed)
- `assets/coupler_gap_sweep.png` — |sin(κ L)|² vs gap using `cross_power_fraction()` (phenomenological κ(gap), for trend only)

```python
from components.directional_coupler import cross_power_fraction

eta = cross_power_fraction(coupling_length=10.0, gap=0.2)
```

### Previews

![Directional coupler layout](assets/directional_coupler.png)

![Gap sweep (qualitative CMT)](assets/coupler_gap_sweep.png)


## Coming next (not in repo yet)

| Component | File | Topic |
|-----------|------|--------|
| 3 — MZI | `components/mzi.py` | Phase arms, \(T = \cos^2(\pi \Delta L \cdot n_g / \lambda)\) |
| 4 — Ring resonator | `components/ring_resonator.py` | \(2\pi r n_\mathrm{eff} = m\lambda\), FSR |

Placeholder files exist for MZI and ring; they are not exported from `components/__init__.py` until implemented.

## License

MIT — see [LICENSE](LICENSE).
