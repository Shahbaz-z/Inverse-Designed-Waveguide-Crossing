import pytest

from components._pdk import ensure_generic_pdk


@pytest.fixture(scope="session", autouse=True)
def _activate_generic_pdk() -> None:
    ensure_generic_pdk()
