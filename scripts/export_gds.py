#!/usr/bin/env python3
"""Write GDS and PNG previews for implemented components only."""

from __future__ import annotations

import os
from pathlib import Path

os.environ.setdefault("MPLBACKEND", "Agg")

import matplotlib.pyplot as plt
import numpy as np

from components._pdk import ensure_generic_pdk
from components.directional_coupler import cross_power_fraction, my_directional_coupler
from components.waveguide import my_waveguide

REPO_ROOT = Path(__file__).resolve().parents[1]
GDS_DIR = REPO_ROOT / "gds_outputs"
SWEEP_DIR = GDS_DIR / "sweeps"
ASSETS_DIR = REPO_ROOT / "assets"


def export_component(name: str, component, gds_name: str) -> None:
    GDS_DIR.mkdir(parents=True, exist_ok=True)
    ASSETS_DIR.mkdir(parents=True, exist_ok=True)

    gds_path = GDS_DIR / gds_name
    component.write_gds(gds_path)
    print(f"Wrote {gds_path}")

    png_path = ASSETS_DIR / f"{name}.png"
    component.plot()
    plt.savefig(png_path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"Wrote {png_path}")


def export_coupler_gap_sweep(
    gaps: tuple[float, ...] = (0.15, 0.2, 0.25, 0.3),
    coupling_length: float = 10.0,
    width: float = 0.5,
) -> None:
    SWEEP_DIR.mkdir(parents=True, exist_ok=True)
    cross_fractions: list[float] = []

    for gap in gaps:
        cell = my_directional_coupler(
            gap=gap,
            coupling_length=coupling_length,
            width=width,
        )
        gds_path = SWEEP_DIR / f"coupler_gap{gap:.2f}.gds"
        cell.write_gds(gds_path)
        print(f"Wrote {gds_path}")
        cross_fractions.append(cross_power_fraction(coupling_length, gap))

    fig, ax = plt.subplots(figsize=(6, 4))
    ax.plot(list(gaps), cross_fractions, "o-", linewidth=2)
    ax.set_xlabel("Gap (µm)")
    ax.set_ylabel("Qualitative cross power |sin(κL)|²")
    ax.set_title(f"Directional coupler (L = {coupling_length} µm, phenomenological κ(gap))")
    ax.grid(True, alpha=0.3)
    ax.set_ylim(0, 1.05)
    fig.tight_layout()
    sweep_png = ASSETS_DIR / "coupler_gap_sweep.png"
    ASSETS_DIR.mkdir(parents=True, exist_ok=True)
    fig.savefig(sweep_png, dpi=150)
    plt.close(fig)
    print(f"Wrote {sweep_png}")


def main() -> None:
    ensure_generic_pdk()

    wg = my_waveguide(length=20.0, width=0.45)
    export_component("waveguide", wg, "waveguide_example.gds")

    dc = my_directional_coupler(gap=0.2, coupling_length=10.0, width=0.5)
    export_component("directional_coupler", dc, "directional_coupler_example.gds")

    export_coupler_gap_sweep()


if __name__ == "__main__":
    main()
