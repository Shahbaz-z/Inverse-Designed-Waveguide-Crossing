#!/usr/bin/env python3
"""Write GDS and PNG previews for implemented components only."""

from __future__ import annotations

import os
from pathlib import Path

# Headless matplotlib for CI and servers without a display
os.environ.setdefault("MPLBACKEND", "Agg")

import matplotlib.pyplot as plt

from components._pdk import ensure_generic_pdk
from components.waveguide import my_waveguide

REPO_ROOT = Path(__file__).resolve().parents[1]
GDS_DIR = REPO_ROOT / "gds_outputs"
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


def main() -> None:
    ensure_generic_pdk()
    wg = my_waveguide(length=20.0, width=0.45)
    export_component("waveguide", wg, "waveguide_example.gds")


if __name__ == "__main__":
    main()
