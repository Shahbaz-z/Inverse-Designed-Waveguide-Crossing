"""Directional coupler parametric cell."""

from __future__ import annotations

import math

import gdsfactory as gf


def cross_power_fraction(
    coupling_length: float,
    gap: float,
    *,
    kappa_scale: float = 3.0,
    gap_decay_um: float = 0.1,
) -> float:
    """Qualitative coupled-mode estimate of cross-port (also known as coupled port) power fraction.

    Uses |sin(κ L)|² with κ ∝ exp(−gap / decay). This is **not** a substitute
    for EM simulation; it shows the trend that smaller gap and longer
    interaction length increase power transfer. 

    Parameters
    ----------
    coupling_length
        Interaction length L in µm.
    gap
        Edge-to-edge gap between waveguides in µm.
    kappa_scale, gap_decay_um
        Phenomenological parameters for the demo sweep plot only.
    """
    kappa = kappa_scale * math.exp(-gap / gap_decay_um) "simple mathematical expression for the coupling coefficient"
    return math.sin(kappa * coupling_length) ** 2 "mathematical expression for the power fraction"


@gf.cell
def my_directional_coupler(
    gap: float = 0.2,
    coupling_length: float = 10.0,
    width: float = 0.5,
    dx: float = 10.0,
    dy: float = 4.0,
) -> gf.Component:
    """Two-waveguide directional coupler (parametric layout cell).

    Parameters
    ----------
    gap
        Separation between the inner edges of the two strip cores in µm.
        Smaller gap increases evanescent overlap (evanescent overlap is the amount of power that leaks out of the waveguide) → stronger coupling
        coefficient κ.
    coupling_length
        Length of the parallel straight section where the guides run
        side-by-side (µm). Longer length allows more power to transfer
        between the "bar" and "cross" arms.
    width
        Strip width of both waveguides in µm.
    dx
        Horizontal distance from the coupling region to the S-bend start
        on each arm (µm). Controls how far apart the bus ports are in x.
    dy
        Vertical separation between the two waveguide centerlines outside
        the coupling region (µm). Must be large enough for the S-bends.

    Returns
    -------
    gf.Component
        Four-port cell with ports ``o1``–``o4`` (GDSFactory coupler convention). pretty self explanatory

    Notes
    -----
    **Directional coupler physics (layout view).** Two identical waveguides
    run parallel with center-to-center spacing set by ``gap`` and ``width``.
    When they are close, the fundamental mode of one guide has an
    evanescent tail overlapping the other. In **coupled-mode theory (CMT)**,
    the amplitudes in the two guides exchange energy with a coupling
    coefficient κ. The power cross-over scales as |sin(κ L)|² for a
    symmetric coupler over length L. - i will simulate this with maxwell equations in project 2

    The **coupling length** for 50:50 splitting is L_c = π / (2κ) (this equation comes from coupled mode theory i have seen in oscialations second year physics with pendulums and coupled pendulums).
     You do
    not need to compute κ in this repo; layout controls are ``gap`` (sets κ
    via overlap) and ``coupling_length`` (sets how much power transfers).

    This cell wraps ``gf.components.coupler`` with an explicit strip
    cross-section so gap, length, and width are the primary design knobs.
    """
    component = gf.Component()
    coupler = component << gf.components.coupler(
        gap=gap,
        length=coupling_length,
        dx=dx,
        dy=dy,
        cross_section=gf.cross_section.strip(width=width),
    )
    component.add_ports(coupler.ports)
    return component
