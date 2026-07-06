"""Mach–Zehnder interferometer parametric cell. """
"mach zender interfermoter used to determine the phase shift between two waves, done by splitting light from single source"
from __future__ import annotations

import math

import gdsfactory as gf


def mzi_transmission(
    delta_length: float,
    *,
    n_g: float = 4.2, #group index, c/v_g how fast envelope of pulse moves, for silicon strips usually 4-4.5"
    wavelength: float = 1.55, "main telecom wavelength, C band"
) -> float:
    """Analytical MZI through-port transmission (qualitative).

    T = cos²(π ΔL · n_g / λ) for a symmetric 50:50 MZI with path difference ΔL.

    Parameters
    ----------
    delta_length
        Path length difference between arms in µm.
    n_g, wavelength
        Group index and wavelength in µm (phenomenological defaults for Si at 1550 nm).
    """
    phase = math.pi * delta_length * n_g / wavelength
    return math.cos(phase) ** 2


@gf.cell
def my_mzi(
    delta_length: float = 10.0,
    bend_radius: float = 10.0, #tighter bends usually mean more bend loss from radiation + fab /EM study wold pick R from allowed loss and area
) -> gf.Component:
    """Mach–Zehnder interferometer (parametric layout cell).

    Parameters
    ----------
    delta_length
        Path length difference between the two arms in µm. One arm is longer
        by this amount, creating a phase shift Δφ = 2π ΔL · n_g / λ.
    bend_radius
        Bend radius used in the MZI arms in µm.

    Returns
    -------
    gf.Component
        Two-port cell (GDSFactory ``mzi`` convention: ``o1``, ``o2``).

    Notes
    -----
    **MZI physics (layout view).** Two 50:50 directional couplers form a
    splitter and combiner; the two arms between them accumulate different
    optical path lengths giving them different phases. The through-port transmission is
    T = cos²(π ΔL · n_g / λ). Changing ``delta_length`` shifts the fringe
    pattern. This cell wraps ``gf.components.mzi``; use
    ``mzi_transmission()`` for a qualitative ΔL sweep plot.
    """
    component = gf.Component()
    mzi = component << gf.components.mzi(
        delta_length=delta_length,
        bend=gf.partial(gf.components.bend_euler, radius=bend_radius),
    )
    component.add_ports(mzi.ports)
    return component
