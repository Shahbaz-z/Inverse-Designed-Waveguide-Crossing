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
from components.mzi import mzi_transmission, my_mzi
from components.ring_resonator import my_ring, ring_fsr
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


def export_mzi_delta_length_sweep(
    delta_lengths: tuple[float, ...] = tuple(range(0, 41, 2)),
    *,
    n_g: float = 4.2,
    wavelength: float = 1.55,
) -> None:
    transmissions = [
        mzi_transmission(dl, n_g=n_g, wavelength=wavelength) for dl in delta_lengths
    ]

    fig, ax = plt.subplots(figsize=(6, 4))
    ax.plot(list(delta_lengths), transmissions, "o-", linewidth=2, markersize=4)
    ax.set_xlabel("ΔL (µm)")
    ax.set_ylabel("Through transmission T = cos²(π ΔL n_g / λ)")
    ax.set_title(f"MZI analytic sweep (n_g = {n_g}, λ = {wavelength} µm)")
    ax.grid(True, alpha=0.3)
    ax.set_ylim(0, 1.05)
    fig.tight_layout()
    sweep_png = ASSETS_DIR / "mzi_delta_length_sweep.png"
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

    mzi = my_mzi(delta_length=10.0, bend_radius=10.0)
    export_component("mzi", mzi, "mzi_example.gds")
    export_mzi_delta_length_sweep()

    ring = my_ring(radius=10.0, gap=0.2, width=0.5)
    export_component("ring_resonator", ring, "ring_resonator_example.gds")


if __name__ == "__main__":
    main()
