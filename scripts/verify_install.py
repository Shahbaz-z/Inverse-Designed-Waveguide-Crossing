#!/usr/bin/env python3
"""Week 1 smoke test: GDSFactory imports and can build a straight waveguide."""

import gdsfactory as gf

from components._pdk import ensure_generic_pdk


def main() -> None:
    ensure_generic_pdk()
    straight = gf.components.straight(length=10)
    if len(straight.ports) < 2:
        raise RuntimeError("Expected at least two ports on gf.components.straight()")
    print("OK: gdsfactory", gf.__version__)
    print("OK: straight waveguide ports:", [p.name for p in straight.ports])


if __name__ == "__main__":
    main()
