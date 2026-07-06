"""Ring resonator parametric cell."""


"traps and filters specific wavelengths, field builds up over many round trips, on resonance, transmission shows
# notch filter"
from __future__ import annotations

import math

import gdsfactory as gf


def ring_fsr(
    radius: float,
    *,
    n_g: float = 4.2,
    wavelength: float = 1.55,
) -> float:
    """Analytical free spectral range for a ring of given radius.

    FSR ≈ λ² / (n_g · L) with L = 2πr (round-trip length).

    Parameters
    ----------
    radius
        Bend radius in µm.
    n_g, wavelength
        Group index and wavelength in µm (phenomenological defaults for Si at 1550 nm).
    """
    length = 2 * math.pi * radius #trivial
    return wavelength**2 / (n_g * length)  # light going around the ring checking if in phase with itself


@gf.cell
def my_ring(
    radius: float = 10.0,
    gap: float = 0.2,
    width: float = 0.5,
) -> gf.Component:
    """Single-bus ring resonator (parametric layout cell).

    Parameters
    ----------
    radius
        Bend radius of the ring in µm.
    gap
        Edge-to-edge gap between bus waveguide and ring in µm.
        Smaller gap increases evanescent coupling (κ) to the ring.
    width
        Strip width of bus and ring waveguides in µm.

    Returns
    -------
    gf.Component
        Cell with bus ports (GDSFactory ``ring_single`` convention).

    Notes
    -----
    **Ring resonator physics (layout view).** Light couples from a straight
    bus into a closed ring via evanescent overlap. Resonances occur when the
    round-trip phase satisfies 2πr·n_eff = mλ. The **free spectral range**
    (spacing between adjacent resonances) is FSR ≈ λ²/(n_g·L) with
    L = 2πr. This cell wraps ``gf.components.ring_single``; coupling strength
    and Q are set by ``gap`` and ``radius`` in layout, not computed here.
    """
    component = gf.Component()
    ring = component << gf.components.ring_single(
        radius=radius,
        gap=gap,
        cross_section=gf.cross_section.strip(width=width),
    )
    component.add_ports(ring.ports)
    return component
