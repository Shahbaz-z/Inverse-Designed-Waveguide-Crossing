"""Tests for implemented layout cells."""

import gdsfactory as gf

from components.waveguide import my_waveguide


def test_my_waveguide_ports_and_geometry() -> None:
    wg = my_waveguide(length=10.0, width=0.5)
    assert len(wg.ports) >= 2
    assert "o1" in wg.ports and "o2" in wg.ports


def test_my_waveguide_writes_gds(tmp_path) -> None:
    wg = my_waveguide(length=5.0, width=0.45)
    path = tmp_path / "wg.gds"
    wg.write_gds(path)
    assert path.stat().st_size > 0


def test_my_waveguide_is_gf_cell() -> None:
    assert callable(my_waveguide)
    assert hasattr(my_waveguide, "function") or hasattr(my_waveguide, "__wrapped__")

from components.directional_coupler import cross_power_fraction, my_directional_coupler


def test_my_directional_coupler_four_ports() -> None:
    dc = my_directional_coupler(gap=0.2, coupling_length=10.0, width=0.5)
    assert len(dc.ports) == 4
    for name in ("o1", "o2", "o3", "o4"):
        assert name in dc.ports


def test_my_directional_coupler_writes_gds(tmp_path) -> None:
    dc = my_directional_coupler(gap=0.25, coupling_length=8.0)
    path = tmp_path / "dc.gds"
    dc.write_gds(path)
    assert path.stat().st_size > 0


def test_cross_power_fraction_bounds() -> None:
    eta = cross_power_fraction(coupling_length=10.0, gap=0.2)
    assert 0.0 <= eta <= 1.0


from components.mzi import mzi_transmission, my_mzi
from components.ring_resonator import my_ring, ring_fsr


def test_my_mzi_ports() -> None:
    mzi = my_mzi(delta_length=10.0, bend_radius=10.0)
    assert len(mzi.ports) >= 2
    assert "o1" in mzi.ports and "o2" in mzi.ports


def test_my_mzi_writes_gds(tmp_path) -> None:
    mzi = my_mzi(delta_length=5.0, bend_radius=8.0)
    path = tmp_path / "mzi.gds"
    mzi.write_gds(path)
    assert path.stat().st_size > 0


def test_mzi_transmission_bounds() -> None:
    t = mzi_transmission(delta_length=10.0)
    assert 0.0 <= t <= 1.0


def test_my_ring_ports() -> None:
    ring = my_ring(radius=10.0, gap=0.2, width=0.5)
    assert len(ring.ports) >= 2
    assert "o1" in ring.ports


def test_my_ring_writes_gds(tmp_path) -> None:
    ring = my_ring(radius=8.0, gap=0.25)
    path = tmp_path / "ring.gds"
    ring.write_gds(path)
    assert path.stat().st_size > 0


def test_ring_fsr_positive() -> None:
    fsr = ring_fsr(radius=10.0)
    assert fsr > 0

