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
