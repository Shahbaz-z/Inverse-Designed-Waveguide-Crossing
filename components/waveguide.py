"""Strip waveguide parametric cell."""

import gdsfactory as gf


@gf.cell
def my_waveguide(length: float = 10.0, width: float = 0.5) -> gf.Component:
    
    """Straight strip waveguide (parametric layout cell).

    Parameters
    ----------
    length
        Propagation length along the waveguide axis, in micrometers (µm).
        GDSFactory uses µm as the layout unit; this is the distance between
        the input and output ports.

# longer, more phase accumulation and delay is also set by length        
    width
        Core (strip) width in µm. Typical SOI strip widths are ~0.4–0.6 µm
        at 1550 nm. The 220 nm silicon thickness is set by the fab layer
        stack (PDK), not by this 2D layout parameter.   - determines cross section of waveguide, affecting modes, (confinement, shape and effictive refractive index)
- wider more modes (multimode support)
    Returns
    -------
    gf.Component
        A flat cell with two edge ports: ``o1`` (input) and ``o2`` (output).

    Notes
    -----
    A **strip waveguide** is a raised silicon ridge on oxide. Light is guided
    by **total internal reflection** at the Si/SiO₂ interfaces and by
    confinement in the thin slab: the fundamental mode lives mostly in the
    core. Wider cores tend to be more multimode and shift effective index;
    narrower cores increase scattering and bend loss sensitivity.

    This cell wraps ``gf.components.straight`` with a strip cross-section so
    width and length are explicit, layout-only parameters.
    """
    component = gf.Component()
    waveguide = component << gf.components.straight(
        length=length,
        cross_section=gf.cross_section.strip(width=width),   ## simple function use in python to set length and width (defined at function)
    )
    component.add_ports(waveguide.ports) #### ensuring we can use the waveguide in the future for the input o1 and output o2
    return component
